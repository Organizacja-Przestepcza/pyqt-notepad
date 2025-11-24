import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit, QStatusBar
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 600, 600)

        # QTextEdit
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Po zmianie tekstu aktualizujemy status bar
        self.text_edit.textChanged.connect(self.update_status_bar)

        # Pierwsze ustawienie status bar
        self.update_status_bar()

    def update_status_bar(self):
        text = self.text_edit.toPlainText()
        lines = text.count("\n") + 1 if text else 0
        chars = len(text)
        self.status_bar.showMessage(f"Linii: {lines} | Znaków: {chars}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
