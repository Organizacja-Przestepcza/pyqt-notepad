import sys
from PyQt6.QtGui import QAction, QKeySequence, QTextCursor
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QTextEdit, QMenuBar, QWidget,
    QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
)


class SearchBar(QWidget):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit
        self.setup_ui()
        self.hide()  # domyślnie ukryty

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Znajdź...")
        self.find_button = QPushButton("Znajdź")

        layout.addWidget(self.input_field)
        layout.addWidget(self.find_button)

        self.setLayout(layout)

        # Po kliknięciu przycisku lub Enter w polu wyszukiwania
        self.find_button.clicked.connect(self.find_text)
        self.input_field.returnPressed.connect(self.find_text)

    def find_text(self):
        needle = self.input_field.text()
        if not needle:
            return

        cursor = self.text_edit.textCursor()
        document = self.text_edit.document()

        found = document.find(needle, cursor)

        if found.isNull():  # jeśli nie znaleziono, zacznij od początku
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            found = document.find(needle, cursor)

        if not found.isNull():
            self.text_edit.setTextCursor(found)
        else:
            self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)
            self.input_field.setText("Nie znaleziono!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_bar = None
        self.text_edit = None
        self.search_bar = None

        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 600, 600)
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()

    def setup_ui(self):
        # Central widget z layoutem pionowym
        central_widget = QWidget()
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)

        # Pasek wyszukiwania
        self.search_bar = SearchBar(None)  # placeholder, podłączymy później
        self.v_layout.addWidget(self.search_bar)

        # QTextEdit
        self.text_edit = QTextEdit()
        self.search_bar.text_edit = self.text_edit  # podłącz do paska wyszukiwania
        self.v_layout.addWidget(self.text_edit)

        central_widget.setLayout(self.v_layout)
        self.setCentralWidget(central_widget)

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

    def setup_shortcuts(self):
        # Ctrl+F pokaże/ukryje pasek wyszukiwania
        find_action = QAction(self)
        find_action.setShortcut(QKeySequence("Ctrl+F"))
        find_action.triggered.connect(self.toggle_search_bar)
        self.addAction(find_action)

    def toggle_search_bar(self):
        if self.search_bar.isVisible():
            self.search_bar.hide()
        else:
            self.search_bar.show()
            self.search_bar.input_field.setFocus()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
