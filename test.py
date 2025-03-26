from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setGeometry(100, 100, 800, 600)

        # 添加自定义标题栏（包含最小化、最大化、关闭按钮）
        self.title_bar = QWidget(self)
        self.title_bar.setGeometry(0, 0, 800, 30)
        self.title_bar.setStyleSheet("background-color: #333;")

        # 最小化按钮
        self.min_btn = QPushButton("－", self.title_bar)
        self.min_btn.setGeometry(700, 0, 30, 30)
        self.min_btn.clicked.connect(self.showMinimized)

        # 最大化按钮
        self.max_btn = QPushButton("□", self.title_bar)
        self.max_btn.setGeometry(730, 0, 30, 30)
        self.max_btn.clicked.connect(self.toggle_maximize)

        # 关闭按钮
        self.close_btn = QPushButton("×", self.title_bar)
        self.close_btn.setGeometry(760, 0, 30, 30)
        self.close_btn.clicked.connect(self.close)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # 实现窗口拖动（鼠标按住标题栏拖动）
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start') and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start)
            event.accept()

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()