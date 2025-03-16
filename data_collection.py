from scapy.all import AsyncSniffer
import pandas as pd
import time
import os

# 定义表头（与Excel表一致）
columns = [
    "id", "dur", "proto", "service", "state", "spkts", "dpkts", "sbytes", "dbytes", "rate", "sttl", "dttl",
    "sload", "dload", "sloss", "dloss", "sinpkt", "dinpkt", "sjit", "djit", "swin", "stcpb", "dtcpb", "dwin",
    "tcprtt", "synack", "ackdat", "smean", "dmean", "trans_depth", "response_body_len", "ct_srv_src", "ct_state_ttl",
    "ct_dst_ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm", "ct_dst_src_ltm", "is_ftp_login", "ct_ftp_cmd", "ct_flw_http_mthd",
    "ct_src_ltm", "ct_srv_dst", "is_sm_ips_ports", "attack_cat", "label"
]

# 初始化一个空的DataFrame
data = []

# 定义全局变量存储AsyncSniffer对象
sniffer = None
output_file = None
textEdit_Log = None

# 定义回调函数，处理每个捕获的数据包
def packet_callback(packet, output_file):
    # 提取数据包中的关键信息
    packet_info = {
        "id": len(data) + 1,  # 自增ID
        "dur": time.time(),  # 时间戳作为持续时间
        "proto": packet.getlayer("IP").proto if packet.haslayer("IP") else None,  # 协议类型
        "service": None,  # 服务类型（需要根据具体协议解析）
        "state": None,  # 连接状态（需要根据具体协议解析）
        "spkts": 1,  # 源包数量（假设每个数据包为1）
        "dpkts": 1,  # 目的包数量（假设每个数据包为1）
        "sbytes": len(packet.getlayer("IP")) if packet.haslayer("IP") else 0,  # 源字节数
        "dbytes": len(packet.getlayer("IP")) if packet.haslayer("IP") else 0,  # 目的字节数
        "rate": 1.0,  # 速率（假设为1.0）
        "sttl": packet.getlayer("IP").ttl if packet.haslayer("IP") else None,  # 源TTL
        "dttl": None,  # 目的TTL（需要根据具体协议解析）
        "sload": None,  # 源负载（需要根据具体协议解析）
        "dload": None,  # 目的负载（需要根据具体协议解析）
        "sloss": 0,  # 源丢包数（假设为0）
        "dloss": 0,  # 目的丢包数（假设为0）
        "sinpkt": None,  # 源包间隔时间（需要根据具体协议解析）
        "dinpkt": None,  # 目的包间隔时间（需要根据具体协议解析）
        "sjit": None,  # 源抖动（需要根据具体协议解析）
        "djit": None,  # 目的抖动（需要根据具体协议解析）
        "swin": None,  # 源窗口大小（需要根据具体协议解析）
        "stcpb": None,  # 源TCP基础序列号（需要根据具体协议解析）
        "dtcpb": None,  # 目的TCP基础序列号（需要根据具体协议解析）
        "dwin": None,  # 目的窗口大小（需要根据具体协议解析）
        "tcprtt": None,  # TCP往返时间（需要根据具体协议解析）
        "synack": None,  # SYN-ACK时间（需要根据具体协议解析）
        "ackdat": None,  # ACK数据时间（需要根据具体协议解析）
        "smean": None,  # 源平均包大小（需要根据具体协议解析）
        "dmean": None,  # 目的平均包大小（需要根据具体协议解析）
        "trans_depth": None,  # 传输深度（需要根据具体协议解析）
        "response_body_len": None,  # 响应体长度（需要根据具体协议解析）
        "ct_srv_src": None,  # 服务源连接数（需要根据具体协议解析）
        "ct_state_ttl": None,  # 连接状态TTL（需要根据具体协议解析）
        "ct_dst_ltm": None,  # 目的连接时间（需要根据具体协议解析）
        "ct_src_dport_ltm": None,  # 源目的端口连接时间（需要根据具体协议解析）
        "ct_dst_sport_ltm": None,  # 目的源端口连接时间（需要根据具体协议解析）
        "ct_dst_src_ltm": None,  # 目的源连接时间（需要根据具体协议解析）
        "is_ftp_login": 0,  # 是否为FTP登录（假设为0）
        "ct_ftp_cmd": 0,  # FTP命令数（假设为0）
        "ct_flw_http_mthd": 0,  # HTTP方法数（假设为0）
        "ct_src_ltm": None,  # 源连接时间（需要根据具体协议解析）
        "ct_srv_dst": None,  # 服务目的连接数（需要根据具体协议解析）
        "is_sm_ips_ports": 0,  # 是否为相同IP和端口（假设为0）
        "attack_cat": "Normal",  # 攻击类别（假设为Normal）
        "label": 0  # 标签（假设为0）
    }

    # 将提取的信息添加到数据列表
    data.append(packet_info)

    # 每捕获10个数据包保存一次
    if len(data) % 10 == 0:
        save_to_csv(output_file)

# 将数据保存为CSV文件
def save_to_csv(output_file):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_file, index=False)
    textEdit_Log.append(f"Saved {len(data)} packets to {output_file}")
    return True

# 开始捕获数据包
def Start(Output_Dir,textEdit):
    global sniffer, textEdit_Log
    # 定义CSV文件保存路径
    os.makedirs(Output_Dir, exist_ok=True)  # 创建目录（如果不存在）
    output_file = os.path.join(Output_Dir, f"TrafficData_{time.time()}.csv")
    textEdit_Log = textEdit
    textEdit_Log.append("Starting packet capture...")

    # 创建异步抓包对象
    sniffer = AsyncSniffer(prn=lambda packet: packet_callback(packet, output_file))

    # 启动抓包
    sniffer.start()
    textEdit_Log.append("Packet capture is running...")

# 停止抓包并保存数据
def End():
    global sniffer
    if sniffer:
        # 停止抓包
        packets = sniffer.stop()
        textEdit_Log.append(f"Stopped capture. Captured {len(packets)} packets.")

        # 保存剩余的数据
        save_to_csv(output_file)
        textEdit_Log.append("Packet capture completed.")
    else:
        textEdit_Log.append("No capture is running.")
