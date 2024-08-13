import os

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QMessageBox, QHBoxLayout, QTextEdit, QApplication, QListWidgetItem, QInputDialog
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from core.search import search_string_in_files
from core.create import create_new_file
from resources.icons import icon_path
from ui.styles import set_app_stylesheet


class SearchThread(QThread):
    update_results = pyqtSignal(list)

    def __init__(self, folder_path, file_extension, search_string):
        super().__init__()
        self.folder_path = folder_path
        self.file_extension = file_extension
        self.search_string = search_string

    def run(self):
        results = search_string_in_files(self.folder_path, self.file_extension, self.search_string)
        self.update_results.emit(results)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.text_edit = None
        self.result_list = None
        self.search_button = None
        self.entry_search = None
        self.label_search = None
        self.label_extension = None
        self.entry_extension = None
        self.entry_path = None
        self.label_path = None
        set_app_stylesheet(QApplication.instance())
        self.initUI()
        self.search_history = []
        self.current_file_path = None  # 保存当前编辑的文件路径
        self.original_content = None  # 保存文件的原始内容

    def initUI(self):
        self.setWindowTitle("文本查询工具")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon(icon_path('1.jpg')))
        self.setupLayout()

    def setupLayout(self):
        layout = QHBoxLayout()

        # 左侧布局：搜索输入和结果列表
        leftLayout = QVBoxLayout()
        leftLayout.setSpacing(10)

        pathLayout = QHBoxLayout()
        self.label_path = QLabel("文件夹路径：")
        pathLayout.addWidget(self.label_path)
        self.entry_path = QLineEdit(self)
        self.entry_path.setPlaceholderText(r"D:\公司系统\Daily reports")
        pathLayout.addWidget(self.entry_path)
        leftLayout.addLayout(pathLayout)

        extensionLayout = QHBoxLayout()
        self.label_extension = QLabel("文件后缀：")
        extensionLayout.addWidget(self.label_extension)
        self.entry_extension = QLineEdit(self)
        self.entry_extension.setPlaceholderText(".txt")
        extensionLayout.addWidget(self.entry_extension)
        leftLayout.addLayout(extensionLayout)

        searchLayout = QHBoxLayout()
        self.label_search = QLabel("查询字符串：")
        searchLayout.addWidget(self.label_search)
        self.entry_search = QLineEdit(self)
        self.entry_search.returnPressed.connect(self.on_search_button_click)
        searchLayout.addWidget(self.entry_search)
        leftLayout.addLayout(searchLayout)

        self.search_button = QPushButton("开始查询", self)
        self.search_button.setFont(QFont('Segoe UI', 15))
        self.search_button.clicked.connect(self.on_search_button_click)
        leftLayout.addWidget(self.search_button)

        self.result_list = QListWidget(self)
        self.result_list.itemClicked.connect(self.show_file_preview)
        leftLayout.addWidget(self.result_list)

        # 右侧布局：文件编辑框和操作按钮
        rightLayout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        rightLayout.addWidget(self.text_edit)

        # 按钮布局
        buttonLayout = QHBoxLayout()

        self.save_button = QPushButton("保存", self)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_file)
        buttonLayout.addWidget(self.save_button)

        self.undo_button = QPushButton("回退", self)
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self.undo_changes)
        buttonLayout.addWidget(self.undo_button)

        self.new_file_button = QPushButton("新建文件", self)
        self.new_file_button.clicked.connect(self.create_new_file)
        buttonLayout.addWidget(self.new_file_button)

        rightLayout.addLayout(buttonLayout)

        layout.addLayout(leftLayout, 1)
        layout.addLayout(rightLayout, 2)

        self.setLayout(layout)

    def on_search_button_click(self):
        folder_path = self.entry_path.text() or r"D:\公司系统\Daily reports"
        file_extension = self.entry_extension.text() or ".txt"
        search_string = self.entry_search.text()

        self.search_history.append((folder_path, file_extension, search_string))

        self.search_thread = SearchThread(folder_path, file_extension, search_string)
        self.search_thread.update_results.connect(self.update_results)
        self.search_thread.start()

    def update_results(self, results):
        self.result_list.clear()
        self.text_edit.clear()
        self.text_edit.setReadOnly(True)
        self.save_button.setEnabled(False)
        self.undo_button.setEnabled(False)
        if results:
            for result in results:
                file_path = result[0]  # 完整的文件路径
                if result[1] == 'Filename Match':
                    item_text = f"{os.path.basename(file_path)}"
                else:
                    item_text = f"{os.path.basename(file_path)}：{result[1]}：{result[2]}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, file_path)  # 将完整路径存储在 item 的 UserRole 数据中
                self.result_list.addItem(item)
        else:
            QMessageBox.information(self, "查询结果", "未在文件中找到指定字符串。")

    def show_file_preview(self, item):
        try:
            # 从 item 中获取存储的完整文件路径
            file_path = item.data(Qt.UserRole)
            if not file_path or not os.path.exists(file_path):
                raise FileNotFoundError(f"文件 {file_path} 未找到")

            self.current_file_path = file_path

            # 尝试打开文件并显示内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                self.text_edit.setPlainText(content)
                self.original_content = content  # 保存原始内容
            self.text_edit.setReadOnly(False)
            self.save_button.setEnabled(True)
            self.undo_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开文件：{str(e)}")
            self.text_edit.clear()
            self.text_edit.setReadOnly(True)
            self.save_button.setEnabled(False)
            self.undo_button.setEnabled(False)

    def save_file(self):
        if self.current_file_path:
            content = self.text_edit.toPlainText()
            with open(self.current_file_path, 'w', encoding='utf-8', errors='ignore') as file:
                file.write(content)
            QMessageBox.information(self, "保存成功", "文件已成功保存。")
            self.original_content = content  # 更新原始内容

    def undo_changes(self):
        if self.original_content is not None:
            self.text_edit.setPlainText(self.original_content)
            QMessageBox.information(self, "回退成功", "内容已回退至上次保存状态。")

    def create_new_file(self):
        # 弹出输入框让用户输入文件名
        file_name, ok = QInputDialog.getText(self, "新建文件", "请输入文件名（包括后缀）：")
        if ok and file_name:
            folder_path = self.entry_path.text() or r"D:\公司系统\Daily reports"
            file_path = os.path.join(folder_path, file_name)

            # 调用 core.create 中的 create_new_file 方法
            try:
                create_new_file(file_path)
                QMessageBox.information(self, "文件创建成功", f"文件 {file_name} 已成功创建。")

                # 更新界面
                self.current_file_path = file_path
                self.text_edit.clear()
                self.text_edit.setReadOnly(False)
                self.save_button.setEnabled(True)
                self.undo_button.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建文件：{str(e)}")
