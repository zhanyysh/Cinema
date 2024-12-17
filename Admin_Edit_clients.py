import requests
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox
from users_table import TableViewWidget  # Импортируем TableViewWidget


class UsersDialog(TableViewWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client Edit")
        self.set_headers(["ID", "Username", "Password"])  # Устанавливаем заголовки таблицы

        # Устанавливаем фиксированный размер окна
        self.setFixedSize(400, 400)

        # Удаляем знак вопроса из окна (контекстная справка)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        # Загрузка данных из API
        self.get_users()

    def get_users(self):
        """Fetch users from the API and populate the table."""
        try:
            response = requests.get("https://zhanyysh.pythonanywhere.com/users")
            if response.status_code == 200:
                users = response.json()  # Данные предполагаются в виде списка словарей
                self.populate_table(users)
            else:
                QMessageBox.warning(self, "Error", "Failed to fetch users")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"API request failed: {e}")
