import requests
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

# URL API для получения данных о покупках
base_url = "https://zhanyysh.pythonanywhere.com"

class UserPurchasesDialog(QDialog):
    def __init__(self,username):
        super().__init__()
        self.setWindowTitle(username)
        self.setGeometry(100, 100, 700, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.username = username 
        # Создание компонентов UI
        self.layout = QVBoxLayout(self)
        self.purchases_table = QTableWidget(self)

        self.purchases_table.setColumnCount(5)
        self.purchases_table.setHorizontalHeaderLabels([
            "Movie Title", "Session Time", "Ticket Count", "Total Profit", "Seat Names"
        ])

        # Добавление компонентов в layout
        self.layout.addWidget(self.purchases_table)

        # Стили
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa; /* Светлый фон */
            }
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #ddd;
                font-size: 12px;
            }
        """
        )

        # Сигналы
        self.fetch_purchases()

    def fetch_purchases(self):
        try:
            response = requests.get(f"{base_url}/user/purchases", params={"username": self.username})

            if response.status_code == 200:
                data = response.json()
                purchases = data.get("purchases", [])

                if not purchases:
                    QMessageBox.information(self, "No Data", "No purchases found for this user.")
                    self.purchases_table.setRowCount(0)
                    return

                # Обновляем таблицу
                self.purchases_table.setRowCount(0)

                for purchase in purchases:
                    row_position = self.purchases_table.rowCount()
                    self.purchases_table.insertRow(row_position)
                    self.purchases_table.setItem(row_position, 0, QTableWidgetItem(f"{purchase["movie_title"]}"))
                    self.purchases_table.setItem(row_position, 1, QTableWidgetItem(purchase["session_time"]))
                    self.purchases_table.setItem(row_position, 2, QTableWidgetItem(str(purchase["ticket_count"])))
                    self.purchases_table.setItem(row_position, 3, QTableWidgetItem(str(f"{purchase["total_profit"]}$",)))
                    self.purchases_table.setItem(row_position, 4, QTableWidgetItem(purchase["seat_names"]))

            elif response.status_code == 404:
                QMessageBox.critical(self, "Error", "User not found.")
            elif response.status_code == 400:
                QMessageBox.critical(self, "Error", "Invalid request. Please check the username.")
            else:
                QMessageBox.critical(self, "Error", "Failed to fetch data from server.")

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication([])
    dialog = UserPurchasesDialog()
    dialog.exec_()
