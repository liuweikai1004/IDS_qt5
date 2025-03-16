import sys
import numpy as np
import tensorflow as tf
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5 import QtCore, QtGui
from tensorflow.keras.models import load_model
import Login
import Home
import data_collection
import DataPreprocessing_CNN_LSTM
import user_management


class UI_main_1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Login.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_Login.clicked.connect(self.login)
        self.ui.pushButton_Register.clicked.connect(self.register)
        self.ui.pushButton_mininum.clicked.connect(self.mini)
        self.ui.pushButton_maximum.clicked.connect(self.max)
        self.ui.pushButton_close.clicked.connect(self.exit)

        self.show()
        self.m_flag = False
        self.main_window_2 = None

    def get_username_password(self):
        """获取用户名和密码"""
        username = self.ui.lineEdit_ID.text().strip()
        password = self.ui.lineEdit_Psd.text().strip()
        return username, password

    def login(self):
        username, password = self.get_username_password()
        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空")
            return
        if user_management.login_user(username, password):
            QMessageBox.information(self, "提示", "登录成功")
            self.close()
            self.main_window_2 = UI_main_2()
            self.main_window_2.show()
        else:
            QMessageBox.warning(self, "警告", "登录失败，请检查用户名和密码")

    def register(self):
        QMessageBox.information(self, "提示", "准备注册")
        username, password = self.get_username_password()
        QMessageBox.information(self, "提示",
                                "获取到的用户名和密码信息如下：\n用户名: {}\n密码: {}".format(username, password))
        if not username or not password:
            QMessageBox.warning(self, "警告", "用户名和密码不能为空")
            return
        if user_management.register_user(username, password):
            QMessageBox.information(self, "提示", "注册成功")
        else:
            QMessageBox.warning(self, "警告", "注册失败，用户名可能已存在")

    def exit(self):
        self.close()

    def mini(self):
        self.showMinimized()

    def max(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and not self.isMaximized():
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


class UI_main_2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Home.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show_home_page()


        self.ui.pushButton_mininum.clicked.connect(self.mini)
        self.ui.pushButton_maximum.clicked.connect(self.max)
        self.ui.pushButton_close.clicked.connect(self.exit)

        # 绑定功能按键
        self.ui.pushButton_Start.clicked.connect(self.TrafficDataCap_Start)
        self.ui.pushButton_End.clicked.connect(self.TrafficDataCap_End)
        self.ui.pushButton_InputData.clicked.connect(self.import_csv)
        self.ui.pushButton_loadModel.clicked.connect(self.Load_Model)
        self.ui.pushButton_StartPredict.clicked.connect(self.Run_Detection)

        self.show()
        self.m_flag = False

    def show_home_page(self):
        self.ui.label_Welcome.show()
        self.ui.textEdit_Tips.show()
        self.ui.pushButton_Start.hide()
        self.ui.pushButton_End.hide()
        self.ui.pushButton_InputData.hide()
        self.ui.textEdit_Result.hide()
        self.ui.pushButton_loadModel.hide()
        self.ui.pushButton_StartPredict.hide()
        self.ui.textEdit_Log.hide()

    def exit(self):
        self.close()

    def mini(self):
        self.showMinimized()

    def max(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and not self.isMaximized():
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    #收集网络流量数据包
    # 开始
    def TrafficDataCap_Start(self):
        path = QFileDialog.getExistingDirectory(self, '选择目录')
        data_collection.Start(path, self.ui.textEdit_Log)

    # 结束
    def TrafficDataCap_End(self):
        data_collection.End()

    # 导入csv数据
    def import_csv(self):
        # 打开文件选择对话框
        self.csv_path, _ = QFileDialog.getOpenFileName(self, '选择 CSV 文件', '', 'CSV 文件 (*.csv)')

        if self.csv_path:
            # 加载训练时选择的特征名称
            with open("selected_features.txt", "r") as f:
                selected_feature_names = f.read().splitlines()
            self.ui.textEdit_Result.append(f"已选择文件: {self.csv_path}")
            self.X_test_res = DataPreprocessing_CNN_LSTM.preprocess_data(self.csv_path, selected_feature_names, 10)
            self.ui.textEdit_Result.append(f"数据已处理完毕！")
        else:
            self.ui.textEdit_Result.append("未选择文件")

    # 计算类别权重
    def calculate_class_weight(X_test_res):
        class_counts = np.bincount(X_test_res.astype(int))
        total_samples = np.sum(class_counts)
        num_classes = len(class_counts)
        class_weights = total_samples / (num_classes * class_counts)
        return class_weights


    # 定义加权损失函数
    def weighted_binary_crossentropy(self,y_true, y_pred):
        # 计算训练数据的类别权重
        class_weights = self.calculate_class_weights(self.X_test_res)
        weight_positive = class_weights[1]  # 正类权重
        weight_negative = class_weights[0]  # 负类权重
        weights = tf.where(y_true == 1, weight_positive, weight_negative)
        weights = tf.cast(weights, tf.float32)  # 将 weights 转换为 float32
        return tf.reduce_mean(weights * tf.keras.losses.binary_crossentropy(y_true, y_pred))

    # 加载模型
    def Load_Model(self):
        # 打开文件选择对话框
        model_path, _ = QFileDialog.getOpenFileName(self, '选择模型文件', '', 'Keras 模型文件 (*.h5)')

        if model_path:
            try:
                # 定义 custom_objects
                custom_objects = {
                    'weighted_binary_crossentropy': self.weighted_binary_crossentropy
                }
                # 加载模型
                self.model = load_model(model_path, custom_objects = custom_objects)
                self.ui.textEdit_Result.append(f"模型已从 {model_path} 加载")
            except Exception as e:
                self.ui.textEdit_Result.append(f"加载模型失败: {str(e)}")
        else:
            self.ui.textEdit_Result.append("未选择模型文件")

    # 入侵检测
    def Run_Detection(self):
        print("1111")
        if not self.model:
            self.ui.textEdit_Result.append("请先加载模型")
            return

        if self.X_test_res is None:
            self.ui.textEdit_Result.append("请先加载测试数据")
            return

        try:
            self.ui.textEdit_Result.append("开始检测...")

            # 分批处理测试数据
            batch_size = 1000  # 每次处理 1000 个样本
            predictions = []

            for i in range(0, len(self.X_test_res), batch_size):
                batch = self.X_test_res[i:i + batch_size]
                self.ui.textEdit_Result.append(f"处理批次: {i} 到 {i + batch_size}")
                batch_predictions = self.model.predict(batch)
                predictions.extend(batch_predictions)

            predictions = np.array(predictions)
            # 将预测概率转换为类别标签（二分类问题）
            pred_labels = np.where(predictions > 0.5, 1, 0)
            self.ui.textEdit_Result.append("检测完成")
            self.ui.textEdit_Result.append(f"检测结果: {pred_labels}")

            # 保存检测结果
            output_path = "predictions.npy"
            np.save(output_path, pred_labels)
            self.ui.textEdit_Result.append(f"检测结果已保存到: {output_path}")

        except Exception as e:
            self.ui.textEdit_Result.append(f"检测失败: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI_main_1()
    sys.exit(app.exec_())
