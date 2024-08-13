from PyQt5.QtGui import QColor, QPalette


def set_app_stylesheet(app):
    # 设置应用程序的调色板
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor("#f0f0f0"))  # 背景颜色
    palette.setColor(QPalette.WindowText, QColor("#2e2e2e"))  # 文本颜色
    palette.setColor(QPalette.Button, QColor("#E0F7FA"))  # 按钮背景颜色
    palette.setColor(QPalette.ButtonText, QColor("#2e2e2e"))  # 按钮文本颜色
    palette.setColor(QPalette.Highlight, QColor("#B2EBF2"))  # 高亮颜色
    palette.setColor(QPalette.HighlightedText, QColor("#2e2e2e"))  # 高亮文本颜色
    app.setPalette(palette)

    # 设置样式表
    app.setStyleSheet("""
        QWidget {
            font-family: "Segoe UI";
            font-size: 14px;
        }
        QLabel {
            color: #5e5e5e;
        }
        QLineEdit {
            border: 1px solid #d3d3d3;
            padding: 5px;
            border-radius: 10px;  # 圆角边框
            background-color: #ffffff;
        }
        QPushButton {
            background-color: #E0F7FA;  # 淡蓝色背景
            color: #2e2e2e;  # 深色文字
            border: 1px solid #B2EBF2;  # 边框颜色
            border-radius: 10px;  # 圆角边框
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #B2EBF2;  # 鼠标悬停时的背景颜色
        }
        QPushButton:pressed {
            background-color: #81D4FA;  # 鼠标按下时的背景颜色
        }
        QListWidget {
            border: 1px solid #d3d3d3;
            border-radius: 10px;  # 圆角边框
            background-color: #ffffff;
        }
    """)
