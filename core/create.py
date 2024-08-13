import os

from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox


def create_new_file(file_path):
    if os.path.exists(file_path):
        raise FileExistsError("文件已存在。")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("")  # 创建空文件
