# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QScrollArea, QWidget, QGridLayout, QDialog, QDialogButtonBox, QHBoxLayout, QMessageBox, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from Client_Session import SeatSelectionDialog
import requests
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QDialog, QMessageBox, QComboBox, QLineEdit, QPushButton, QWidget
import time
class Movie_Main_window(QMainWindow):
    
    def __init__(self, username):
        super().__init__()
        self.setFixedSize(900, 720)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user_history = None
        self.ui.pushButton.clicked.connect(self.open_history)
        self.username = username
        self.setWindowIcon(QIcon("taran.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.ui.welcome_label.setStyleSheet("color:white;")
        self.ui.welcome_label.setText(f"   WELCOME TO AIT-WOOD, {username}!")
        self.movies = []  # Initialize an empty list for movies
        self.genres = ["All"]  # Initialize genres with "All"
        self.genre_cache = {}  # Cache for genre-based filtered movies
        self.search_cache = {}  # Cache for search results
        self.fetch_movies()  # Fetch movies from the API
        self.populate_genres()  # Populate genres in the combo box
        self.display_movies()  # Display all movies initially
        
        # Connect genre combo box to filter action
        self.ui.comboBox.currentIndexChanged.connect(self.filter_movies)
        self.ui.log_out.clicked.connect(self.open_login)
        self.ui.refresh_button.clicked.connect(self.refresh)
        # Connect the line edit to search functionality
        self.ui.lineEdit.textChanged.connect(self.search_movie)
    def refresh(self):
        self.dialog = Movie_Main_window(self.username)
        self.close()
        self.dialog.show()

    def open_history(self):
        from client_history import UserPurchasesDialog
        if self.user_history == None:
            self.user_history = UserPurchasesDialog(self.username)
        self.user_history.show()
        
    def open_login(self):
        from loginWindow import Dialog_Login
        self.login_window = None
        if self.login_window == None:
            self.login_window = Dialog_Login()
        self.close()
        self.login_window.show()

    def fetch_movies(self):
        """Fetch movies from the API."""
        try:
            response = requests.get("https://zhanyysh.pythonanywhere.com/movies")  # Replace with your Flask API URL
            if response.status_code == 200:
                movie_data = response.json()
                self.movies = [
                    (
                        movie["id"],
                        movie["title"],
                        movie["description"],
                        movie.get("poster", ""),  # Default to an empty string if poster is missing
                        movie["genre"],
                    )
                    for movie in movie_data
                ]
                # Populate genres dynamically
                self.genres.extend(sorted(set(movie["genre"] for movie in movie_data)))
            else:
                self.show_error_message("Failed to fetch movies", f"Error: {response.status_code}")
        except Exception as e:
            self.show_error_message("Failed to connect to the server", str(e))

    def populate_genres(self):
        """Populate the genre combo box."""
        self.ui.comboBox.addItems(self.genres)

    def filter_movies(self):
        """Filter movies based on the selected genre."""
        selected_genre = self.ui.comboBox.currentText()
        
        # Check if the genre filter is cached
        if selected_genre in self.genre_cache:
            filtered_movies = self.genre_cache[selected_genre]
        else:
            if selected_genre == "All":
                filtered_movies = self.movies
            else:
                filtered_movies = [movie for movie in self.movies if movie[4] == selected_genre]
            
            # Cache the filtered list by genre
            self.genre_cache[selected_genre] = filtered_movies
        
        self.display_movies(filtered_movies)

    def search_movie(self):
        """Search for a movie by title."""
        search_text = self.ui.lineEdit.text().lower()

        # Check if the search term is already cached
        if search_text in self.search_cache:
            filtered_movies = self.search_cache[search_text]
        else:
            if search_text:
                filtered_movies = [movie for movie in self.movies if search_text in movie[1].lower()]
            else:
                filtered_movies = self.movies
            
            # Cache the search result by search term
            self.search_cache[search_text] = filtered_movies
        
        if filtered_movies:
            self.display_movies(filtered_movies)
        else:
            self.display_no_movie_found()

    def display_movies(self, movies=None):
        """Display movies in a grid layout."""
        if movies is None:
            movies = self.movies

        row = 0
        col = 0
        max_columns = 4  # Number of images per row

        self.scrollAreaWidgetContents = QWidget()
        self.grid_layout = QGridLayout(self.scrollAreaWidgetContents)
        self.grid_layout.setSpacing(20)
        self.ui.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.grid_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

        for movie in movies:
            movie_id, title, description, image_url, genre = movie

            # Create image label
            image_label = QLabel(self)
            self.load_image(image_url, image_label, 140, 180)  # Increased image size
            image_label.setCursor(QtCore.Qt.PointingHandCursor)
            image_label.setStyleSheet("border: none;")  # Remove border and background
            image_label.mousePressEvent = lambda event, movie=movie: self.show_movie_dialog(movie)

            # Create title label
            title_label = QLabel(title, self)
            title_label.setAlignment(QtCore.Qt.AlignCenter)
            title_label.setStyleSheet("font-size: 12px; font-weight: bold; color:white;")

            # Add widgets to grid
            movie_widget = QWidget(self)
            movie_layout = QVBoxLayout(movie_widget)
            movie_layout.addWidget(image_label)
            movie_layout.addWidget(title_label)
            movie_widget.setStyleSheet("border: none; padding: 0px;")  # Remove background

            self.grid_layout.addWidget(movie_widget, row, col)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

    def load_image(self, image_url, image_label, width=140, height=180):
        """Download and load image from URL."""
        try:
            if image_url:  # Check if image URL exists
                response = requests.get(image_url)
                image_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                image_label.setPixmap(
                    pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                )
                image_label.setScaledContents(True)
            else:
                # Set a placeholder if the image URL is missing
                image_label.setText("No Image")
                image_label.setAlignment(QtCore.Qt.AlignCenter)
        except Exception as e:
            print(f"Error loading image: {e}")

    def show_movie_dialog(self, movie):
        """Show a dialog with a larger image, title, genre, description, and sessions when a poster is clicked."""
        movie_id, title, description, image_url, genre = movie
        dialog = QDialog(self)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setWindowTitle(title)
        dialog_layout = QHBoxLayout(dialog)

        # Left side: Movie poster
        image_label = QLabel(dialog)
        self.load_image(image_url, image_label, 200, 300)
        dialog_layout.addWidget(image_label)

        # Right side: Movie details
        details_layout = QVBoxLayout()

        # Title
        title_label = QLabel(title, dialog)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        details_layout.addWidget(title_label)

        # Genre
        genre_label = QLabel(f"Genre: {genre}", dialog)
        genre_label.setStyleSheet("font-size: 14px; color: white;")
        details_layout.addWidget(genre_label)

        # Description with word wrapping
        description_label = QLabel(description, dialog)
        description_label.setStyleSheet("font-size: 14px; color: white;")
        description_label.setWordWrap(True)  # Enable text wrapping
        description_label.setFixedWidth(300)  # Set a maximum width to ensure proper wrapping
        details_layout.addWidget(description_label)

        # Fetch and display sessions for the movie
        self.load_sessions_for_movie(movie_id, details_layout)

        # Adding details layout to the dialog
        dialog_layout.addLayout(details_layout)

        dialog.exec_()


    def load_sessions_for_movie(self, movie_id, details_layout):
        """Fetch movie sessions from the server and display them in the dialog."""
        try:
            # Make the API request to fetch sessions
            response = requests.get(f"https://zhanyysh.pythonanywhere.com/load_sessions/{movie_id}")
            if response.status_code == 200:
                sessions = response.json()
                
                if sessions:
                    sessions_label = QLabel("Sessions:", details_layout.parent())
                    sessions_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
                    details_layout.addWidget(sessions_label)

                    for session in sessions:
                        session_time = session['session_time']
                        price = session['price']
                        
                        session_info = QLabel(f"Time: {session_time}, Price: {price}", details_layout.parent())
                        details_layout.addWidget(session_info)

                        # You can add buttons or other functionality for each session
                        session_button = QPushButton(f"{session_time}", details_layout.parent())
                        session_button.setStyleSheet("color:white;")
                        session_button.clicked.connect(lambda _, s=session: self.book_session(s))
                        details_layout.addWidget(session_button)

                else:
                    no_sessions_label = QLabel("No sessions available.", details_layout.parent())
                    details_layout.addWidget(no_sessions_label)
            else:
                self.show_error_message("Error", "Failed to load sessions.")
        except Exception as e:
            self.show_error_message("Error", f"Failed to fetch sessions: {str(e)}")

    def book_session(self, session):
        # Open the seat selection dialog
        session_id = session['session_id']  # Assume you have session_id to pass
        seat_dialog = SeatSelectionDialog(session_id,self.username)
        seat_dialog.exec_()

    def show_error_message(self, title, message):
        """Show an error message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def display_no_movie_found(self):
        """Display a message when no movies match the search."""
        self.grid_layout.addWidget(QLabel("No movies found.", self), 0, 0)

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 720)  # Slightly reduced window size
        MainWindow.setStyleSheet("background-color: #2c3e50;")  # Темноватый белый для фона

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Horizontal Layout for top area (Log out and title)
        top_layout = QtWidgets.QHBoxLayout()

        # "Log out" button (aligned to the left) with extra margin from the edge
        self.log_out = QtWidgets.QPushButton("Log out", self.centralwidget)
        self.log_out.setStyleSheet("""
            QPushButton {
                font-family: 'Alumni Sans', sans-serif;
                font-size: 18px;
                color: white;
                background-color: #e74c3c;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        top_layout.addWidget(self.log_out, alignment=QtCore.Qt.AlignLeft)

        # Adding some space between the buttons and edges
        top_layout.addSpacing(50)  # Adds more spacing to the right of the "Log out" button

        # Welcome label (main title centered) with larger font
        self.welcome_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont("Alumni Sans", 16, QtGui.QFont.Bold)  # Use QFont to set the font size and style
        self.welcome_label.setFont(font)
        self.welcome_label.setText("Welcome to Movie Catalog")
        self.welcome_label.setAlignment(QtCore.Qt.AlignCenter)  # Set alignment programmatically
        top_layout.addWidget(self.welcome_label, alignment=QtCore.Qt.AlignCenter)

        # Adding more space between the title and the "My History" button
        top_layout.addSpacing(50)  # Adds more spacing to the left of the "My History" button

        # "My History" button (aligned to the right) with extra margin from the edge
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setStyleSheet("""
            QPushButton {
                font-family: 'Alumni Sans', sans-serif;
                font-size: 18px;
                color: white;
                background-color: #e74c3c;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.pushButton.setText("My History")
        top_layout.addWidget(self.pushButton, alignment=QtCore.Qt.AlignRight)

        # Set the margins of the layout for better spacing
        top_layout.setContentsMargins(20, 0, 20, 0)  # Left, Top, Right, Bottom margins

        # Add the top layout to the main layout
        top_container = QtWidgets.QWidget(self.centralwidget)
        top_container.setLayout(top_layout)
        top_container.setGeometry(QtCore.QRect(0, 0, 900, 60))  # Adjust the height of the top bar

        # Search line edit (style consistency with other input fields)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(670, 80, 180, 35))
        self.lineEdit.setPlaceholderText("Search by title...")
        self.lineEdit.setStyleSheet("""
            QLineEdit {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                padding: 5px 10px;
                font-size: 16px;
                color: #2c3e50;
                border-radius: 5px;
            }
        """)

        # ComboBox for categories (consistent styling)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(480, 80, 160, 35))
        self.comboBox.setStyleSheet("""
            QComboBox {
                background-color: #ecf0f1;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
            QComboBox::drop-down {
                background-color: #bdc3c7;
            }
        """)

        # Scroll area for movie list (consistent styling for the scroll bar and area)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(50, 120, 800, 500))  # Adjusted size to fit within new window size
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("""
            QScrollArea {
                background-color: #ecf0f1;
                border-radius: 2px;
                padding: 10px;
            }
            QScrollBar:vertical {
                background-color: #bdc3c7;
                width: 12px;
                margin: 10px 0;
                border-radius:3px;
            }
            QScrollBar::handle:vertical {
                background-color: #2980b9;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3498db;
            }
        """)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 899, 499))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Refresh button in the lower-left part of the window
        self.refresh_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_button.setGeometry(QtCore.QRect(20, 640, 100, 40))  # Positioned at the bottom-left corner
        self.refresh_button.setText("Refresh")
        self.refresh_button.setStyleSheet("""
            QPushButton {
                font-family: 'Alumni Sans', sans-serif;
                font-size: 18px;
                color: white;
                background-color: #27ae60;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)

        # Layout adjustments for consistent positioning
        self.centralwidget.setLayout(QtWidgets.QVBoxLayout())

        # Apply layout and add widgets accordingly
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Movie Catalog"))
