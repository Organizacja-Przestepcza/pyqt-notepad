import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit, QMenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_bar = None
        self.text_edit = None

        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 600, 600)
        self.setup_editor()
        self.setup_menu()

    def setup_editor(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

    def setup_menu(self):
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        file_menu = self.menu_bar.addMenu("Plik")

        open_action = QAction("Otwórz", self)
        save_action = QAction("Zapisz", self)
        exit_action = QAction("Zamknij", self)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        exit_action.triggered.connect(self.close)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
