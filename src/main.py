import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit, QMenuBar, QMessageBox, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_bar = None
        self.text_edit = None
        self.current_path = None  # <- inicjalizacja ścieżki pliku

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

        # podpięcie akcji
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Otwórz plik", "", "Text Files (*.txt);;All Files (*)")

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_edit.setText(content)
                self.current_path = path
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie można otworzyć pliku:\n{e}")

    def save_file(self):
        if self.current_path:
            try:
                with open(self.current_path, "w", encoding="utf-8") as f:
                    f.write(self.text_edit.toPlainText())
                return
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie można zapisać pliku:\n{e}")
                return
        self.save_file_as()

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Zapisz jako", "", "Text Files (*.txt);;All Files (*)")

        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())
            self.current_path = path
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie można zapisać pliku:\n{e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
