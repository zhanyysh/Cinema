from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
import requests  # Make sure to import requests for API calls
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
SERVER_URL = "https://zhanyysh.pythonanywhere.com"  # Replace with your actual server URL

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(506, 461)
        Dialog.setWindowIcon(QIcon("taran.png"))
        Dialog.setWindowFlags(Dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 0, 491, 231))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Title, genre, description, and poster fields
        self.title = QtWidgets.QLineEdit(self.frame)
        self.title.setGeometry(QtCore.QRect(32, 51, 131, 31))
        self.title.setPlaceholderText("Название фильма")  # Placeholder
        self.title.setObjectName("title")

        self.genre = QtWidgets.QLineEdit(self.frame)
        self.genre.setGeometry(QtCore.QRect(32, 91, 131, 31))
        self.genre.setPlaceholderText("Жанр фильма")  # Placeholder
        self.genre.setObjectName("genre")

        self.description = QtWidgets.QLineEdit(self.frame)
        self.description.setGeometry(QtCore.QRect(220, 50, 241, 71))
        self.description.setPlaceholderText("Описание фильма")  # Placeholder
        self.description.setObjectName("description")

        self.poster = QtWidgets.QLineEdit(self.frame)
        self.poster.setGeometry(QtCore.QRect(30, 130, 131, 31))
        self.poster.setPlaceholderText("Путь к постеру (опционально)")  # Placeholder
        self.poster.setObjectName("poster")

        # Button to add the movie
        self.add_movie_button = QtWidgets.QPushButton(self.frame)
        self.add_movie_button.setGeometry(QtCore.QRect(270, 140, 121, 41))
        self.add_movie_button.setText("Добавить фильм")
        self.add_movie_button.clicked.connect(self.add_movie)

        # Frame for session inputs
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(9, 229, 491, 301))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # Movie selection combobox
        self.movie_combobox = QtWidgets.QComboBox(self.frame_2)
        self.movie_combobox.setGeometry(QtCore.QRect(30, 10, 131, 31))
        self.movie_combobox.setObjectName("movie_combobox")

        # Ticket quantity and cost inputs
        self.ticket_quantity = QtWidgets.QLineEdit(self.frame_2)
        self.ticket_quantity.setGeometry(QtCore.QRect(340, 10, 141, 31))
        self.ticket_quantity.setPlaceholderText("Количество билетов")  # Placeholder
        self.ticket_quantity.setObjectName("ticket_quantity")

        self.ticket_cost = QtWidgets.QLineEdit(self.frame_2)
        self.ticket_cost.setGeometry(QtCore.QRect(190, 10, 141, 31))
        self.ticket_cost.setPlaceholderText("Цена билета")  # Placeholder
        self.ticket_cost.setObjectName("ticket_cost")

        # Session time input
        self.sessiontime = QtWidgets.QLineEdit(self.frame_2)
        self.sessiontime.setGeometry(QtCore.QRect(260, 60, 141, 31))
        self.sessiontime.setPlaceholderText("Время сеанса")  # Placeholder
        self.sessiontime.setObjectName("sessiontime")

        # Button to add the session
        self.add_session_button = QtWidgets.QPushButton(self.frame_2)
        self.add_session_button.setGeometry(QtCore.QRect(270, 110, 121, 41))
        self.add_session_button.setText("Добавить сеанс")
        self.add_session_button.clicked.connect(self.add_session)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()

    def add_movie(self):
        data = {
            "title": self.title.text(),
            "description": self.description.text(),
            "genre": self.genre.text(),
            "poster": self.poster.text()
        }

        try:
            response = requests.post(f"{SERVER_URL}/add_movie", json=data)
            if response.status_code == 201:
                self.show_message("Success", "Movie added successfully.")
                self.load_movies()
                self.clear_movie_inputs()
            else:
                error_message = response.json().get('error', 'Unknown error occurred.')
                self.show_message("Error", f"Failed to add movie: {error_message}", QMessageBox.Critical)
        except Exception as e:
            self.show_message("Error", f"Failed to add movie: {str(e)}", QMessageBox.Critical)

    def add_session(self):
        movie_id = self.movie_combobox.currentData()  # Get the movie ID from the combobox
        if not movie_id:
            self.show_message("Error", "Please select a movie to add a session.", QMessageBox.Critical)
            return

        try:
            data = {
                "movie_id": movie_id,
                "session_time": self.sessiontime.text(),
                "price": int(self.ticket_cost.text()),
                "tickets": int(self.ticket_quantity.text())
            }

            response = requests.post(f"{SERVER_URL}/add_session", json=data)
            if response.status_code == 201:
                self.show_message("Success", "Session added successfully.")
                self.load_sessions()
                self.clear_session_inputs()
            else:
                error_message = response.json().get('error', 'Unknown error occurred.')
                self.show_message("Error", f"Failed to add session: {error_message}", QMessageBox.Critical)
        except Exception as e:
            pass

    def load_movies(self):
        self.movie_combobox.clear()
        try:
            response = requests.get(f"{SERVER_URL}/movies")
            if response.status_code == 200:
                movies = response.json()
                for movie in movies:
                    self.movie_combobox.addItem(movie['title'], movie['id'])
            else:
                self.show_message("Error", "Failed to load movies.", QMessageBox.Critical)
        except Exception as e:
            self.show_message("Error", f"Failed to load movies: {str(e)}", QMessageBox.Critical)

    def clear_movie_inputs(self):
        self.title.clear()
        self.description.clear()
        self.genre.clear()
        self.poster.clear()

    def clear_session_inputs(self):
        self.ticket_quantity.clear()
        self.ticket_cost.clear()
        self.sessiontime.clear()

class add_part_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Load movies into the combobox after the UI setup
        self.ui.load_movies()
