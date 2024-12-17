from PyQt5.QtWidgets import QTableView, QVBoxLayout, QPushButton, QDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import requests


class TableViewWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the table view and model
        self.table_view = QTableView(self)
        self.table_model = QStandardItemModel()
        self.table_view.setModel(self.table_model)

        # Set up layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table_view)

        # Add a delete button
        self.delete_button = QPushButton("DELETE", self)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-family: "Arial", sans-serif;
                font-size: 14px;
                border: 1px solid #cc0000;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #cc0000;
                border-color: #990000;
            }
            QPushButton:pressed {
                background-color: #990000;
                border-color: #660000;
            }
        """)
        self.layout.addWidget(self.delete_button)

        # Connect delete button
        self.delete_button.clicked.connect(self.delete_selected_row)

    def set_headers(self, headers):
        """Set headers for the table."""
        self.table_model.setHorizontalHeaderLabels(headers)

    def populate_table(self, data):
        """Populate the table with a list of dictionaries."""
        self.table_model.removeRows(0, self.table_model.rowCount())  # Clear only the data, not headers
        for record in data:
            row = [QStandardItem(str(record.get(key, ""))) for key in ["id", "username", "password"]]
            self.table_model.appendRow(row)

        # Make columns adjustable to fit content
        self.resize_table()

    def resize_table(self):
        """Resize columns and rows to fit content dynamically."""
        # Resize columns to fit content
        self.table_view.resizeColumnsToContents()

        # Resize rows to fit content
        self.table_view.resizeRowsToContents()

        # Optionally, set a minimum width for the columns if needed
        self.table_view.setColumnWidth(0, 100)  # Minimum width for the ID column
        self.table_view.setColumnWidth(1, 150)  # Minimum width for the Username column
        self.table_view.setColumnWidth(2, 150)  # Minimum width for the Password column

    def delete_selected_row(self):
        """Delete the selected row from the table and database."""
        selection_model = self.table_view.selectionModel()
        selected_rows = selection_model.selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Delete", "No row selected to delete.")
            return

        for index in sorted(selected_rows, key=lambda x: x.row(), reverse=True):
            # Get user ID from the selected row
            user_id = self.table_model.item(index.row(), 0).text()

            if not user_id:
                QMessageBox.warning(self, "Error", "Cannot delete a user without a valid ID.")
                continue

            # Confirmation before deletion
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete user with ID {user_id}?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                try:
                    # Send DELETE request to server
                    response = requests.delete(f"https://zhanyysh.pythonanywhere.com/users/{user_id}")
                    if response.status_code == 200:
                        # Remove row from the table model
                        self.table_model.removeRow(index.row())
                        QMessageBox.information(self, "Success", "User deleted successfully.")
                    else:
                        try:
                            error_message = response.json().get("error", "Failed to delete user.")
                        except ValueError:
                            error_message = "Unexpected response format."
                        QMessageBox.warning(self, "Error", error_message)
                except requests.RequestException as e:
                    QMessageBox.critical(self, "Error", f"An error occurred: {e}")
