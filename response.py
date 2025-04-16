import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import smtplib
from email.mime.text import MIMEText
import os
import subprocess
import time
import data_collection
import DataPreprocessing_CNN_LSTM

class MonitoringThread(QThread):
    """
    实时监控线程类
    继承自QThread，用于在后台运行实时监控功能
    """
    # 定义信号用于在主线程中显示弹窗
    alert_signal = pyqtSignal(str, str, int, bool)  # 参数: 标题, 内容, 消息类型, 是否需要响应
    action_signal = pyqtSignal(str, str, dict)  # 用于传递需要执行的操作(响应方式, 邮件地址, 包信息)


    def __init__(self, model, response_method, email_address=None):
        super().__init__()
        self.model = model
        self.response_method = response_method
        self.email_address = email_address
        self.running = False
        self.current_alert_info = None

    def run(self):
        """
        线程主运行方法
        """
        self.running = True
        try:
            # 加载特征选择
            try:
                with open("selected_features.txt", "r") as f:
                    self.selected_feature_names = f.read().splitlines()
            except FileNotFoundError:
                self.alert_signal.emit("系统提示", "未找到特征选择文件", QMessageBox.Critical, False)
                return

            # 启动抓包
            Start_Log = data_collection.Start_MAR()
            self.alert_signal.emit("系统提示", Start_Log, QMessageBox.Information, False)

            self.i = 1
            while self.running:
                # 获取每10个包的批次数据
                batch = data_collection.get_next_batch()
                self.Test(batch)
                self.i += 1

        except Exception as e:
            self.alert_signal.emit("系统错误", f"监控线程发生异常: {str(e)}", QMessageBox.Critical, False)
        finally:
            self.cleanup()

    def stop(self):
        """安全停止线程的方法"""
        self.running = False  # 先标记停止

        # 非阻塞停止抓包
        if hasattr(data_collection, 'sniffer') and data_collection.sniffer:
            data_collection.sniffer.stop(join=False)

        # 清空队列
        while not data_collection.packet_queue.empty():
            try:
                data_collection.packet_queue.get_nowait()
            except:
                break

        # 等待线程正常结束（最多1秒）
        self.wait(1000)
        if self.isRunning():
            self.terminate()  # 强制终止
    def handle_user_response(self, response):
        """
        处理用户对警报的响应
        """
        if response == QMessageBox.Ok and self.current_alert_info:
            # 通过信号触发操作，确保在主线程执行
            self.action_signal.emit(
                self.response_method,
                self.email_address,
                self.current_alert_info
            )

    def send_alert_email(self, to_addr, subject, content):
        """发送警报邮件"""
        try:
            msg = MIMEText(content)
            msg['Subject'] = subject
            msg['From'] = "m17854629961@163.com"
            msg['To'] = to_addr

            with smtplib.SMTP('smtp.163.com', 587) as server:
                server.starttls()
                username = os.getenv('SMTP_USER')
                password = os.getenv('SMTP_PASS')
                server.login(username, password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False

    def block_ip(self, ip):
        """使用PowerShell封禁IP"""
        if not ip:
            return False

        try:
            ps_script = f"""
            New-NetFirewallRule `
                -DisplayName "BlockIP_{ip}" `
                -Direction Inbound `
                -RemoteAddress {ip} `
                -Action Block `
                -Enabled True
            """

            subprocess.run(
                ["powershell", "-Command", ps_script],
                check=True,
                shell=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"封禁失败（错误 {e.returncode}）：{e.stderr}")
        except Exception as e:
            print(f"意外错误: {e}")
        return False
    def Test(self, batch):
        if not self.running:  # 如果线程已停止，不再处理
            return

        if batch is not None:
            # 检测异常
            self.alert_signal.emit("系统提示", "开始检测异常", QMessageBox.Information, False)
            Data_Preprocessed = DataPreprocessing_CNN_LSTM.preprocess_data(batch, self.selected_feature_names, 10)
            self.alert_signal.emit("系统提示", "数据预处理完成", QMessageBox.Information, False)
            predictions = np.array(self.model.predict(Data_Preprocessed))
            results = np.where(predictions > 0.5, 1, 0)

            # 处理检测结果
            self.alert_signal.emit("系统提示", "开始处理检测结果", QMessageBox.Information, False)
            has_anomaly = False
            for idx, (is_anomaly, packet_info) in enumerate(zip(results[:, 0], batch.to_dict('records'))):
                if is_anomaly:
                    has_anomaly = True
                    self.alert_signal.emit("系统警告", "有异常数据", QMessageBox.Warning, False)
                    alert_msg = f"检测到异常流量!\n\n" \
                                f"协议: {packet_info.get('proto', '未知')}\n" \
                                f"源IP: {packet_info.get('src_ip', '未知')}\n" \
                                f"目标IP: {packet_info.get('dst_ip', '未知')}\n" \
                                f"包大小: {packet_info.get('length', 0)}字节"

                    # 保存当前警报信息用于后续处理
                    self.current_alert_info = packet_info

                    # 发送警报信号(需要用户响应)
                    self.alert_signal.emit(
                        "安全警报",
                        alert_msg,
                        QMessageBox.Warning,
                        True
                    )

            if not has_anomaly:
                self.alert_signal.emit("系统提示", f"第{self.i}批网络数据无异常", QMessageBox.Information, False)
        time.sleep(0.1)

    def cleanup(self):
        """确保资源释放"""
        if hasattr(data_collection, 'running'):
            data_collection.running = False
        self.alert_signal.emit("系统提示", "监控已停止", QMessageBox.Information, False)