import requests
from PyQt5.Qt import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from autorizationUI import Ui_DialogRegister, Ui_DialogLogin
from capt import CaptchaWindow
from AdminMainPage import Admin_Main_Page
from messageBox import show_message, show_ui_not_ready_message
class Dialog_Register(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(313)
        self.setFixedHeight(342)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QIcon("taran.png"))
        self.ui = Ui_DialogRegister()
        self.ui.setupUi(self)
        self.ui.signin_button.clicked.connect(self.login_window)
        self.login_window_instance = None
        self.ui.signup_button.clicked.connect(self.register)
        self.ui.password_line.setEchoMode(QtWidgets.QLineEdit.Password)

    def login_window(self):
        if self.login_window_instance is None:
            self.login_window_instance = Dialog_Login()
        self.close()
        self.login_window_instance.show()

    def register(self):
        """Реализуем регистрацию с предварительной проверкой CAPTCHA"""
        username = self.ui.nickname_line.text()
        password = self.ui.password_line.text()

        if not username or not password:
            show_message("Username and password are required", "Error")
            return

        # Окно с CAPTCHA
        captcha_window = CaptchaWindow()
        captcha_window.show()

        # Проверка CAPTCHA перед отправкой данных регистрации
        if captcha_window.exec_() == QtWidgets.QDialog.Accepted and captcha_window.result:
            data = {'username': username, 'password': password}
            try:
                response = requests.post("https://zhanyysh.pythonanywhere.com/register", json=data)
                if response.status_code == 201:
                    show_message("Registration successful")
                    self.login_window()
                else:
                    show_message(response.json().get("error", "An error occurred"), "Error")
            except Exception as e:
                show_message(f"Request failed: {e}", "Error")
        else:
            show_message("CAPTCHA not passed", "Error")

class Dialog_Login(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(313)
        self.setFixedHeight(342)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QIcon("taran.png"))

        self.ui = Ui_DialogLogin()
        self.ui.setupUi(self)
        self.ui.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.movie_window = None
        self.ui.pushButton_2.clicked.connect(self.login)
        self.ui.pushButton.clicked.connect(self.register_window)

        self.register_window_instance = None

    def register_window(self):
        """Открытие окна регистрации"""
        if self.register_window_instance is None:
            self.register_window_instance = Dialog_Register()
        self.close()
        self.register_window_instance.show()

    def login(self):
        """Обработка нажатия на кнопку 'sign in'"""
        username = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit.text()

        if not username or not password:
            show_message("Username and password are required", "Error")
            return

        data = {'username': username, 'password': password}
        try:
            response = requests.post("https://zhanyysh.pythonanywhere.com/login", json=data)
            if response.status_code == 200:
                show_message("Login successful", "Success")
                if username == "NURMUHAMMED" and password =="12345":
                    self.open_admin_main_page(username)
                else:
                    from Client_Movie import Movie_Main_window
                    if self.movie_window ==  None:
                        self.movie_window = Movie_Main_window(username)
                    self.close()
                    self.movie_window.show()

            else:
                error_message = response.json().get("error", "An error occurred")
                show_message(error_message, "Error")
        except Exception as e:
            show_message(f"Request failed: {e}", "Error")

    def open_admin_main_page(self, name):
        self.admin_page = Admin_Main_Page()
        self.admin_page.ui.admin_name_label.setText(f"admin: {name}")
        self.close()
        self.admin_page.show()
