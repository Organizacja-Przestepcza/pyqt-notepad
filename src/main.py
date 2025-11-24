import sys

from PyQt6.QtGui import QAction, QTextCursor, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit, QMenuBar, QMessageBox, QFileDialog, QPushButton, \
    QHBoxLayout, QLineEdit, QWidget, QVBoxLayout
from PyQt6.QtWidgets import QStatusBar

class SearchBar(QWidget):
    def __init__(self, text_edit):
        super().__init__()
        self.find_button = None
        self.input_field = None
        self.text_edit = text_edit
        self.setup_ui()
        self.hide()

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
        self.current_path = None

        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 600, 600)
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.text_edit.textChanged.connect(self.update_status_bar)
        self.update_status_bar()

    def setup_ui(self):
        central_widget = QWidget()
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 0, 0, 0)

        self.search_bar = SearchBar(None)
        self.v_layout.addWidget(self.search_bar)

        # QTextEdit
        self.text_edit = QTextEdit()
        self.search_bar.text_edit = self.text_edit
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

        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)

    def update_status_bar(self):
        text = self.text_edit.toPlainText()
        lines = text.count("\n") + 1 if text else 0
        chars = len(text)
        self.status_bar.showMessage(f"Linii: {lines} | Znaków: {chars}")

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
