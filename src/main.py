import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 800, 600)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()