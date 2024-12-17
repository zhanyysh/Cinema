import requests
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
base_url = "https://zhanyysh.pythonanywhere.com"


class ReportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Report Window")
        self.setGeometry(100, 100, 600, 500)
        self.setWindowIcon(QIcon("taran.png"))
        # UI Components
        self.layout = QVBoxLayout(self)
        self.movie_label = QLabel("Select Movie:", self)
        self.movie_combobox = QComboBox(self)
        self.session_label = QLabel("Select Session:", self)
        self.session_combobox = QComboBox(self)
        self.user_table = QTableWidget(self)
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(["Username", "Ticket Count", "Profit","Seat_name"])
        self.user_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Add Components to Layout
        self.layout.addWidget(self.movie_label)
        self.layout.addWidget(self.movie_combobox)
        self.layout.addWidget(self.session_label)
        self.layout.addWidget(self.session_combobox)
        self.layout.addWidget(self.user_table)

        # Styles
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0; /* Light background */
            }
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                margin: 5px;
            }
            QComboBox {
                font-size: 14px;
                border: 1px solid #4CAF50;
                padding: 5px;
                margin: 5px;
                border-radius: 5px;
            }
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 12px;
                margin: 10px;
                gridline-color: #ddd;
            }
        """)

        # Signals
        self.movie_combobox.currentIndexChanged.connect(self.load_sessions)
        self.session_combobox.currentIndexChanged.connect(self.generate_report)

        # Initialize Data
        self.movies = []
        self.sessions = []
        self.load_movies()

    def load_movies(self):
        try:
            response = requests.get(f"{base_url}/movies")
            if response.status_code == 200:
                self.movies = response.json()
                if not self.movies:
                    QMessageBox.information(self, "Info", "No movies available.")
                self.movie_combobox.clear()
                for movie in self.movies:
                    self.movie_combobox.addItem(movie.get('title', 'Unknown Title'), movie.get('id'))
            else:
                QMessageBox.critical(self, "Error", f"Failed to load movies. Status code: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred while fetching movies: {e}")

    def load_sessions(self):
        movie_id = self.movie_combobox.currentData()
        if not movie_id:
            QMessageBox.warning(self, "Warning", "No movie selected.")
            return
        try:
            response = requests.get(f"{base_url}/load_sessions/{movie_id}")
            if response.status_code == 200:
                self.sessions = response.json()
                if not self.sessions:
                    QMessageBox.information(self, "Info", "No sessions available for the selected movie.")
                self.session_combobox.clear()
                for session in self.sessions:
                    session_time = session.get('session_time', 'Unknown Time')
                    self.session_combobox.addItem(session_time, session)
            else:
                QMessageBox.critical(self, "Error", f"Failed to load sessions. Status code: {response.status_code}")
                self.session_combobox.clear()
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred while fetching sessions: {e}")
            self.session_combobox.clear()


    def generate_report(self):
        session_data = self.session_combobox.currentData()

        if not session_data:
            self.user_table.setRowCount(0)
            return

        session_id = session_data['session_id']
        try:
            response = requests.get(f"{base_url}/purchase/session/{session_id}?report_type=users")
            if response.status_code == 200:
                data = response.json()
                self.user_table.setRowCount(0)

                for user in data['users']:
                    row_position = self.user_table.rowCount()
                    self.user_table.insertRow(row_position)
                    self.user_table.setItem(row_position, 0, QTableWidgetItem(user['username']))
                    self.user_table.setItem(row_position, 1, QTableWidgetItem(str(user['ticket_count'])))
                    self.user_table.setItem(row_position, 2, QTableWidgetItem(str(user['profit'])))
                    self.user_table.setItem(row_position, 3, QTableWidgetItem(str(user['seat_name'])))

            else:
                pass
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication([])
    dialog = ReportDialog()
    dialog.exec_()

