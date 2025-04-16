from collections import defaultdict
from ftplib import FTP
from io import StringIO
from threading import Lock
import re

import numpy as np
from scapy.all import AsyncSniffer
import pandas as pd
import time
import os
from queue import Queue
import threading
from itertools import count


from scapy.layers.dns import DNS
from scapy.layers.http import HTTP
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.inet6 import IPv6
from scapy.packet import Raw

# 定义表头（与Excel表一致）
columns = [
    "id", "dur", "proto", "service", "state", "spkts", "dpkts", "sbytes", "dbytes", "rate", "sttl", "dttl",
    "sload", "dload", "sloss", "dloss", "sinpkt", "dinpkt", "sjit", "djit", "swin", "stcpb", "dtcpb", "dwin",
    "tcprtt", "synack", "ackdat", "smean", "dmean", "trans_depth", "response_body_len", "ct_srv_src", "ct_state_ttl",
    "ct_dst_ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm", "ct_dst_src_ltm", "is_ftp_login", "ct_ftp_cmd", "ct_flw_http_mthd",
    "ct_src_ltm", "ct_srv_dst", "is_sm_ips_ports","attack_cat"
]

# 全局变量
packet_queue = Queue()
batch_size = 50
output_file = None
textEdit_Log = None
sniffer = None
save_timer = None
running = False
# 全局会话状态存储
session_stats = defaultdict(lambda: {
    "start_time": None,
    "last_src_time": None,
    "last_dst_time": None,
    "src_intervals": [],  # 用于计算sjit
    "dst_intervals": [],  # 用于计算djit
    "src_ttl": None,
    "dst_ttl": None,
    "syn_time": None,
    "synack_time": None,
    "ack_time": None,
    "src_window": None,
    "dst_window": None,
    "src_base_seq": None,
    "dst_base_ack": None,
    "spkts": 0,
    "dpkts": 0,
    "sbytes": 0,
    "dbytes": 0,
    "trans_depth": 0,
    "response_body_len": 0,
    "ct_srv_src": set(),
    "ct_state_ttl": {},
    "ct_dst_ltm": defaultdict(int),
    "ct_src_dport_ltm": defaultdict(int),
    "ct_dst_sport_ltm": defaultdict(int),
    "ct_dst_src_ltm": defaultdict(int),
    "ftp_commands": 0,
    "http_methods": set(),
})
global_id_counter = 0
id_counter_lock = Lock()


def packet_callback(packet):
    global global_id_counter

    # 初始化packet_info
    packet_info = {
        "id": None,
        "srcip": None,
        "sport": None,
        "dstip": None,
        "dport": None,
        "proto": "-",
        "dur": 0.0,
        "service": None,
        "state": "-",
        "spkts": 0,
        "dpkts": 0,
        "sbytes": 0,
        "dbytes": 0,
        "rate": 0.0,
        "sttl": None,
        "dttl": None,
        "sload": 0,
        "dload": 0,
        "sloss": 0,
        "dloss": 0,
        "sinpkt": 0,
        "dinpkt": 0,
        "sjit": 0,
        "djit": 0,
        "swin": 0,
        "stcpb": 0,
        "dtcpb": 0,
        "dwin": 0,
        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0,
        "smean": 0,
        "dmean": 0,
        "trans_depth": 0,
        "response_body_len": 0,
        "ct_srv_src": 0,
        "ct_state_ttl": 0,
        "ct_dst_ltm": 0,
        "ct_src_dport_ltm": 0,
        "ct_dst_sport_ltm": 0,
        "ct_dst_src_ltm": 0,
        "is_ftp_login": 0,
        "ct_ftp_cmd": 0,
        "ct_flw_http_mthd": 0,
        "ct_src_ltm": 0,
        "ct_srv_dst": 0,
        "is_sm_ips_ports": 0,
        "attack_cat": "Normal",
    }

    try:
        # 基础协议解析
        if not packet.haslayer(IP):
            return

        ip_layer = packet[IP]
        packet_info.update({
            "srcip": ip_layer.src,
            "dstip": ip_layer.dst,
            "sttl": ip_layer.ttl,
            "proto": {6: "tcp", 17: "udp", 1: "icmp"}.get(ip_layer.proto, "-")
        })

        # 传输层解析
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            packet_info.update({
                "sport": tcp_layer.sport,
                "dport": tcp_layer.dport,
                "swin": tcp_layer.window
            })

            # TCP状态解析
            try:
                # 使用位掩码检查标志位
                flags = tcp_layer.flags

                # 检查FIN标志 (0x01)
                if flags & 0x01:
                    packet_info["state"] = "FIN"

                # 检查SYN标志 (0x02)
                elif flags & 0x02:
                    # 区分SYN和SYN-ACK
                    if flags & 0x10:  # 检查ACK标志 (0x10)
                        packet_info["state"] = "SYN-ACK"
                    else:
                        packet_info["state"] = "SYN"

                # 检查RST标志 (0x04)
                elif flags & 0x04:
                    packet_info["state"] = "RST"

                # 其他状态处理
                else:
                    packet_info["state"] = "OTHER"

            except Exception as e:
                print(f"TCP flag parsing error: {e}")

        elif packet.haslayer("UDP"):
            udp_layer = packet["UDP"]
            packet_info.update({
                "sport": udp_layer.sport,
                "dport": udp_layer.dport
            })

        # 过滤无效会话
        if None in (packet_info["srcip"], packet_info["sport"],
                    packet_info["dstip"], packet_info["dport"]):
            return

        # 会话跟踪
        session_key = (packet_info["srcip"], packet_info["sport"],
                       packet_info["dstip"], packet_info["dport"],
                       packet_info["proto"])
        stats = session_stats[session_key]

        # 初始化会话
        if stats["start_time"] is None:
            stats["start_time"] = time.time()
            if packet.haslayer(TCP):
                stats["src_base_seq"] = packet[TCP].seq

        # 更新会话统计
        is_src_to_dst = (packet[IP].src == packet_info["srcip"])
        pkt_len = len(packet)
        current_time = time.time()

        if is_src_to_dst:
            stats["spkts"] += 1
            stats["sbytes"] += pkt_len
            if stats["last_src_time"]:
                interval = (current_time - stats["last_src_time"]) * 1000
                stats["src_intervals"].append(interval)
                packet_info["sinpkt"] = interval
            stats["last_src_time"] = current_time
            stats["src_window"] = packet_info["swin"]
        else:
            stats["dpkts"] += 1
            stats["dbytes"] += pkt_len
            if stats["last_dst_time"]:
                interval = (current_time - stats["last_dst_time"]) * 1000
                stats["dst_intervals"].append(interval)
                packet_info["dinpkt"] = interval
            stats["last_dst_time"] = current_time
            stats["dst_window"] = packet[TCP].window if packet.haslayer(TCP) else 0
            packet_info["dwin"] = stats["dst_window"]
            packet_info["dttl"] = packet_info["sttl"]  # 假设反向TTL相同

        # 特殊协议处理
        if packet.haslayer(Raw):
            raw = packet[Raw].load.decode(errors="ignore")

            # HTTP处理
            if packet_info["dport"] == 80 or packet_info["sport"] == 80:
                if "HTTP" in raw[:20]:
                    stats["trans_depth"] += 1
                    packet_info["trans_depth"] = stats["trans_depth"]

                    if "Content-Length:" in raw:
                        try:
                            length = int(re.search(r"Content-Length: (\d+)", raw).group(1))
                            stats["response_body_len"] += length
                            packet_info["response_body_len"] = length
                        except:
                            pass

                    if packet_info["trans_depth"] == 1:  # 请求方法
                        method = raw.split()[0]
                        stats["http_methods"].add(method)
                        packet_info["ct_flw_http_mthd"] = len(stats["http_methods"])

            # FTP处理
            elif packet_info["dport"] == 21:
                stats["ftp_commands"] += 1
                packet_info["ct_ftp_cmd"] = stats["ftp_commands"]
                if any(cmd in raw for cmd in ["USER", "PASS"]):
                    packet_info["is_ftp_login"] = 1

        # 连接统计特征
        service_key = (packet_info["dport"], packet_info["proto"])
        stats["ct_srv_src"].add((packet_info["srcip"], service_key))
        packet_info["ct_srv_src"] = len(stats["ct_srv_src"])

        state_ttl_key = (packet_info["state"], packet_info["sttl"])
        stats["ct_state_ttl"][state_ttl_key] = stats["ct_state_ttl"].get(state_ttl_key, 0) + 1
        packet_info["ct_state_ttl"] = stats["ct_state_ttl"][state_ttl_key]

        current_minute = int(time.time() / 60)
        stats["ct_dst_ltm"][packet_info["dstip"]] = current_minute
        packet_info["ct_dst_ltm"] = sum(1 for t in stats["ct_dst_ltm"].values() if t == current_minute)

        # 相同IP端口检查
        if (packet_info["srcip"] == packet_info["dstip"] and
                packet_info["sport"] == packet_info["dport"]):
            packet_info["is_sm_ips_ports"] = 1

        # 会话结束处理
        is_session_end = False
        if packet.haslayer(TCP):
            flags = packet[TCP].flags
            # 使用位掩码检查 FIN (0x01) 和 RST (0x04) 标志
            if flags & 0x01 or flags & 0x04:
                is_session_end = True

        if is_session_end:
            with id_counter_lock:
                global_id_counter += 1
                packet_info["id"] = global_id_counter

            # 计算会话统计值
            duration = time.time() - stats["start_time"]
            packet_info.update({
                "dur": duration,
                "spkts": stats["spkts"],
                "dpkts": stats["dpkts"],
                "sbytes": stats["sbytes"],
                "dbytes": stats["dbytes"],
                "rate": (stats["spkts"] + stats["dpkts"]) / duration if duration > 0 else 0,
                "swin": stats["src_window"],
                "stcpb": stats["src_base_seq"],
                "dtcpb": stats.get("dst_base_ack", 0),
                "dwin": stats["dst_window"],
                "smean": stats["sbytes"] / stats["spkts"] if stats["spkts"] > 0 else 0,
                "dmean": stats["dbytes"] / stats["dpkts"] if stats["dpkts"] > 0 else 0,
                "sload": (stats["sbytes"] * 8) / duration if duration > 0 else 0,
                "dload": (stats["dbytes"] * 8) / duration if duration > 0 else 0,
                "sjit": np.std(stats["src_intervals"]) if len(stats["src_intervals"]) > 1 else 0,
                "djit": np.std(stats["dst_intervals"]) if len(stats["dst_intervals"]) > 1 else 0,
                "ct_src_ltm": len(stats["ct_src_dport_ltm"]),
                "ct_srv_dst": len(stats["ct_dst_sport_ltm"]),
                "ct_dst_src_ltm": len(stats["ct_dst_src_ltm"]),
            })

            # 三次握手时间计算
            if stats["syn_time"] and stats["synack_time"]:
                packet_info.update({
                    "synack": (stats["synack_time"] - stats["syn_time"]) * 1000,
                    "tcprtt": (stats["synack_time"] - stats["syn_time"]) * 1000,
                    "ackdat": (stats["ack_time"] - stats["synack_time"]) * 1000 if stats["ack_time"] else 0,
                })

            # 清理会话状态
            del session_stats[session_key]
            packet_queue.put(packet_info)

    except Exception as e:
        print(f"Packet processing error: {e}")

def auto_save_worker():
    """后台自动保存线程"""
    global running
    while running:
        time.sleep(5)  # 每5秒检查一次
        if output_file and not packet_queue.empty():
            save_to_csv()

# 将数据保存为CSV文件
def save_to_csv():
    global output_file
    """增强版的保存函数，保证ID连续性"""
    # 获取当前队列数据
    temp_data = []
    while not packet_queue.empty():
        temp_data.append(packet_queue.get())

    if not temp_data:
        return

    # 处理ID连续性
    if os.path.exists(output_file):
        try:
            last_id = pd.read_csv(output_file)['id'].max()
            next_id = int(last_id) + 1
        except:
            next_id = 1
    else:
        next_id = 1

    df = pd.DataFrame(temp_data)
    df['id'] = range(next_id, next_id + len(df))

    # 保存数据
    df.to_csv(
        output_file,
        mode='a',
        header=not os.path.exists(output_file),
        index=False,
        columns=columns  # 确保列顺序一致
    )
    if textEdit_Log:
        textEdit_Log.append(f"Saved {len(temp_data)} packets to {output_file}")

# 开始捕获数据包
def Start(Output_Dir, textEdit):
    """启动数据包捕获（文件模式）"""
    global sniffer, output_file, textEdit_Log, running, save_timer

    os.makedirs(Output_Dir, exist_ok=True)
    output_file = os.path.join(Output_Dir, f"TrafficData_{int(time.time())}.csv")
    textEdit_Log = textEdit

    # 清空队列
    while not packet_queue.empty():
        packet_queue.get()

    # 启动自动保存线程
    running = True
    save_timer = threading.Thread(target=auto_save_worker)
    save_timer.daemon = True
    save_timer.start()

    sniffer = AsyncSniffer(prn=packet_callback)
    sniffer.start()
    textEdit_Log.append(f"Capture started. Saving to {output_file}")


def End():
    """停止捕获并保存剩余数据"""
    global sniffer, running, save_timer

    if not sniffer:
        textEdit_Log.append("No active capture to stop.")
        return

    # 1. 停止抓包（获取Scapy捕获的原始包数量）
    scapy_packets = sniffer.stop()
    sniffer = None

    # 2. 停止自动保存线程
    running = False
    if save_timer:
        save_timer.join()

    # 3. 获取队列中剩余的包
    remaining_packets = []
    while not packet_queue.empty():
        remaining_packets.append(packet_queue.get())

    # 4. 计算总捕获量（原始包 + 队列剩余包）
    total_captured = len(scapy_packets) + len(remaining_packets)

    # 5. 保存剩余数据（如果有）
    if remaining_packets and output_file:
        df = pd.DataFrame(remaining_packets, columns=columns)
        df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)

    # 6. 输出统计信息
    log_msg = [
        f"Capture stopped.",
        f"Total captured: {total_captured}"
    ]
    textEdit_Log.append("\n".join(log_msg))

def Start_MAR():
    """启动数据包捕获（实时监测模式）"""
    global sniffer
    # 清空队列
    while not packet_queue.empty():
        packet_queue.get()

    sniffer = AsyncSniffer(prn=packet_callback)
    sniffer.start()
    return "开始抓取网络流量数据包..."


def get_next_batch():
    """获取下一批数据（50个数据包），返回dataframe格式"""
    batch = []
    while len(batch) < batch_size:
        batch.append(packet_queue.get())

    if not batch:
        return None

    # 将数据转换为DataFrame
    df = pd.DataFrame(batch, columns=columns)

    return df
def End_MAR():
    """停止实时监测模式的抓包并返回剩余数据"""
    global sniffer

    if not sniffer:
        return "No active capture to stop.", None
    try:
        # 停止抓包
        packets = sniffer.stop()
        sniffer = None

        # 获取队列中剩余的数据包
        remaining_packets = []
        while not packet_queue.empty():
            remaining_packets.append(packet_queue.get())

        # 计算总共捕获的数据包数
        total_captured = len(packets) + len(remaining_packets)

        message = f"Real-time monitoring stopped. Total packets captured: {total_captured}"

        # 如果还有剩余数据包，一并返回
        if remaining_packets:
            return message, remaining_packets
        return message, None
    except Exception as e:
        print(e)

