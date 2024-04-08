import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette

class TextSearchTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("文本查询工具")
        self.setGeometry(100, 100, 640, 480)
        self.setWindowIcon(QIcon('1.jpg'))  # 设置窗口图标

        self.setFont(QFont("Segoe UI", 10))  # Segoe UI是一种干净且现代的字体
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f0f0"))  # 背景颜色
        palette.setColor(QPalette.WindowText, QColor("#2e2e2e"))  # 文本颜色
        self.setPalette(palette)

        # 使用样式表来进一步定义元素的外观
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QLabel {
                color: #5e5e5e;
            }
            QLineEdit {
                border: 1px solid #d3d3d3;
                padding: 5px;
                border-radius: 5px;
                background-color: #ffffff;
            }
             QPushButton {
                background-color: #E0F7FA;  # 淡蓝色背景
                color: #eceff4;  # 深蓝色文字
                border: 1px solid #B2EBF2;  # 边框颜色
                border-radius: 5px;  # 圆角边框
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #B2EBF2;  # 鼠标悬停时的背景颜色
            }
            QPushButton:pressed {
                background-color: #81D4FA;  # 鼠标按下时的背景颜色
            }
            QTextEdit {
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                background-color: #ffffff;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        # 创建组件并使用水平布局进行组织
        pathLayout = QHBoxLayout()
        self.label_path = QLabel("文件夹路径：")
        pathLayout.addWidget(self.label_path)
        self.entry_path = QLineEdit(self)
        self.entry_path.setPlaceholderText(r"D:\公司系统\Daily reports")
        pathLayout.addWidget(self.entry_path)
        layout.addLayout(pathLayout)

        extensionLayout = QHBoxLayout()
        self.label_extension = QLabel("文件后缀：")
        extensionLayout.addWidget(self.label_extension)
        self.entry_extension = QLineEdit(self)
        self.entry_extension.setPlaceholderText(".txt")
        extensionLayout.addWidget(self.entry_extension)
        layout.addLayout(extensionLayout)

        searchLayout = QHBoxLayout()
        self.label_search = QLabel("查询字符串：")
        searchLayout.addWidget(self.label_search)
        self.entry_search = QLineEdit(self)
        searchLayout.addWidget(self.entry_search)
        layout.addLayout(searchLayout)



        self.search_button = QPushButton("开始查询", self)
        self.search_button.setFont(QFont('Segoe UI', 15))
        # 设置回车键触发搜索
        self.entry_search.returnPressed.connect(self.on_search_button_click)
        self.search_button.clicked.connect(self.on_search_button_click)
        layout.addWidget(self.search_button)

        # 查询结果显示区
        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)


    # 包含搜索逻辑的函数以及按钮点击事件处理略...
    def search_string_in_files(self, folder_path, file_extension, search_string):
            results = []
            for root, dirs, files in os.walk(folder_path):
                for file_name in files:
                    if file_name.endswith(file_extension):
                        file_path = os.path.join(root, file_name)
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                            for line_number, line in enumerate(file, 1):
                                if search_string in line:
                                    results.append((file_path, line_number, line.strip()))
            return results

    def on_search_button_click(self):
        folder_path = self.entry_path.text() or r"D:\公司系统\Daily reports"
        file_extension = self.entry_extension.text() or ".txt"
        search_string = self.entry_search.text()

        search_results = self.search_string_in_files(folder_path, file_extension, search_string)

        self.result_text.clear()
        if search_results:
            for result in search_results:
                self.result_text.append(f"文件：{result[0]}，行数：{result[1]}，内容：{result[2]}")
                self.result_text.append("-" * 40)  # 添加横线隔开搜索结果
        else:
            QMessageBox.information(self, "查询结果", "未在文件中找到指定字符串。")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextSearchTool()
    ex.show()
    sys.exit(app.exec_())