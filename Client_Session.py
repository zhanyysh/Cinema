import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QScrollArea, QWidget, QGridLayout, QDialog, QDialogButtonBox, QHBoxLayout, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap 
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class SeatSelectionDialog(QDialog):
    def __init__(self, session_id, username):
        super().__init__()
        self.username = username
        self.setWindowIcon(QIcon("taran.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Select Seats")
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")  # Dark background with white text
        self.setFixedSize(800, 600)  # Fixed size for the dialog

        layout = QVBoxLayout()
        self.session_id = session_id
        self.seats = {}
        self.selected_seats = []  # List to track selected seats
        self.seat_buttons = {}  # Store buttons by seat_name

        # Fetch seats from the server
        self.fetch_seats()

        # Add a legend to explain seat colors
        legend_layout = QHBoxLayout()

        def create_legend_item(color, text):
            item_layout = QHBoxLayout()
            color_label = QLabel()
            color_label.setFixedSize(25, 25)
            color_label.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
            text_label = QLabel(text)
            text_label.setStyleSheet("color: #ffffff; margin-left: 10px; font-size: 14px;")
            item_layout.addWidget(color_label)
            item_layout.addWidget(text_label)
            item_layout.addStretch()
            return item_layout

        legend_layout.addLayout(create_legend_item("#4CAF50", "Available"))
        legend_layout.addLayout(create_legend_item("#D32F2F", "Occupied"))
        legend_layout.addLayout(create_legend_item("#FFC107", "Selected"))
        layout.addLayout(legend_layout)

        # Create a container for seats with grid layout
        self.seat_grid_widget = QWidget(self)
        self.seat_grid_layout = QGridLayout(self.seat_grid_widget)
        self.seat_grid_layout.setSpacing(15)  # Increase spacing between seats

        # Create seat buttons dynamically based on fetched seat data
        row, col = 0, 0
        for seat_name, status in self.seats.items():
            seat_button = QPushButton(seat_name)
            seat_button.setFixedSize(QSize(60, 50))  # Larger buttons
            seat_button.setStyleSheet(self.get_button_style(status))
            seat_button.setEnabled(status)  # Enable only if the seat is available
            seat_button.clicked.connect(lambda checked, seat=seat_name: self.select_seat(seat))

            self.seat_buttons[seat_name] = seat_button
            self.seat_grid_layout.addWidget(seat_button, row, col)

            col += 1
            if col >= 8:  # Adjust grid width to 8 seats per row for better spacing
                col = 0
                row += 1

        layout.addWidget(self.seat_grid_widget)

        # Add "Buy" button
        self.buy_button = QPushButton("Buy", self)
        self.buy_button.setFixedSize(QSize(100, 50))
        self.buy_button.setStyleSheet("background-color: #007BFF; color: white; font-size: 14px; border-radius: 10px;")
        self.buy_button.clicked.connect(self.buy)
        layout.addWidget(self.buy_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def fetch_seats(self):
        """Fetch seat data from the Flask API."""
        try:
            url = f"https://zhanyysh.pythonanywhere.com/get_seats?session_id={self.session_id}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.seats = {seat["seat_id"]: seat["available"] for seat in data["seats"]}
            else:
                QMessageBox.critical(self, "Error", "Failed to fetch seat data.")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.close()

    def get_button_style(self, available):
        """Return button style based on availability."""
        if available:
            return "background-color: #4CAF50; color: white; font-weight: bold; border: 1px solid #aaa; border-radius: 5px;"
        else:
            return "background-color: #D32F2F; color: white; font-weight: bold; border: 1px solid #444; border-radius: 5px;"

    def select_seat(self, seat_name):
        """Handle seat selection."""
        if self.seats.get(seat_name):
            if seat_name not in self.selected_seats:
                self.selected_seats.append(seat_name)
                button = self.seat_buttons.get(seat_name)
                if button:
                    button.setStyleSheet("background-color: #FFC107; color: black; font-weight: bold; border: 1px solid #aaa; border-radius: 5px;")
            else:
                self.selected_seats.remove(seat_name)
                button = self.seat_buttons.get(seat_name)
                if button:
                    button.setStyleSheet(self.get_button_style(True))

    def buy(self):
        """Send purchase request for all selected seats to the API and update seat colors."""
        if self.selected_seats:
            try:
                url = "https://zhanyysh.pythonanywhere.com/purchase_ticket"
                data = {
                    "session_id": self.session_id,
                    "seat_ids": self.selected_seats,  # Send the list of selected seats
                    "username": self.username
                }

                # Send the request to the server
                response = requests.post(url, json=data)

                if response.status_code == 201:
                    # Get successfully purchased seats from the response
                    purchased_seats = response.json().get("purchased_seats", [])
                    failed_seats = response.json().get("failed_seats", [])

                    # Update styles for successfully purchased seats
                    for seat_name in purchased_seats:
                        button = self.seat_buttons.get(seat_name)
                        if button:
                            button.setStyleSheet("background-color: #D32F2F; color: white; border: 1px solid #444; border-radius: 5px;")
                            button.setEnabled(False)
                            self.close()

                    # Notify about failed purchases
                    if failed_seats:
                        failed_seats_str = ", ".join(failed_seats)
                        QMessageBox.warning(self, "Partial Purchase", f"Some seats could not be purchased: {failed_seats_str}")

                    # Clear the selected seats list
                    self.selected_seats = [seat for seat in self.selected_seats if seat not in purchased_seats]

                    # Show success message
                    QMessageBox.information(self, "Success", "Seats purchased successfully!")
                else:
                    # Handle server errors
                    error_message = response.json().get("error", "Unknown error occurred.")
                    QMessageBox.critical(self, "Error", f"Failed to purchase seats: {error_message}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "No Seats Selected", "Please select at least one seat to purchase.")
