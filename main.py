import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles import set_app_stylesheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    set_app_stylesheet(app)  # 应用样式
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
