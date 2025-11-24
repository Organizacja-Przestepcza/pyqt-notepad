import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit, QMenuBar, QStatusBar, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_bar = None

        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 600, 600)

        # Edytor tekstu
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Menu
        self.setup_menu()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.text_edit.textChanged.connect(self.update_status_bar)
        self.update_status_bar()

        # Flaga zmian
        self.text_changed = False
        self.text_edit.textChanged.connect(self.on_text_changed)

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

    def update_status_bar(self):
        text = self.text_edit.toPlainText()
        lines = text.count("\n") + 1 if text else 0
        chars = len(text)
        self.status_bar.showMessage(f"Linii: {lines} | Znaków: {chars}")

    def on_text_changed(self):
        """Ustaw flagę, że tekst został zmieniony"""
        self.text_changed = True
        self.update_status_bar()

    def closeEvent(self, event):
        """Wywoływane przy zamykaniu okna"""
        if self.text_changed:
            reply = QMessageBox.question(
                self,
                "Zamknij notatnik",
                "Masz niezapisane zmiany. Czy chcesz wyjść bez zapisywania?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()  # zamknij program
            else:
                event.ignore()  # anuluj zamknięcie
        else:
            event.accept()  # brak zmian, zamknij normalnie


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
