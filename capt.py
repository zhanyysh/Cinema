from PyQt5 import QtCore, QtGui, QtWidgets
from captcha.image import ImageCaptcha
import random
import string
import os


class CaptchaWindow(QtWidgets.QDialog):
    """Окно CAPTCHA с проверкой."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CAPTCHA")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #FFFFFF; color: #000000; font-size: 14px;")
        
        # Заголовок
        self.label_title = QtWidgets.QLabel("Ты не робот?", self)
        self.label_title.setGeometry(100, 20, 200, 40)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #000000;")
        
        # Место для изображения CAPTCHA
        self.captcha_image_label = QtWidgets.QLabel(self)
        self.captcha_image_label.setGeometry(100, 80, 200, 80)
        self.captcha_image_label.setStyleSheet("border: 1px solid #000000;")
        self.captcha_image_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Поле для ввода CAPTCHA
        self.captcha_input = QtWidgets.QLineEdit(self)
        self.captcha_input.setGeometry(100, 180, 200, 30)
        self.captcha_input.setPlaceholderText("Введите текст")
        self.captcha_input.setStyleSheet("""
            background-color: #EEEEEE; 
            color: #000000; 
            padding: 5px; 
            border: 1px solid #AAAAAA;
        """)

        # Кнопка проверки
        self.verify_button = QtWidgets.QPushButton("Verify", self)
        self.verify_button.setGeometry(150, 230, 100, 30)
        self.verify_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000; 
                color: #FFFFFF; 
                font-size: 14px; 
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        self.verify_button.clicked.connect(self.verify_captcha)

        # Переменная для хранения текста CAPTCHA
        self.captcha_text = ""
        
        # Генерация CAPTCHA
        self.generate_captcha()

    def generate_captcha(self):
        """Генерация CAPTCHA и отображение изображения."""
        self.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))  # Текст CAPTCHA
        captcha = ImageCaptcha()
        captcha_image_path = "captcha_image.png"
        captcha.write(self.captcha_text, captcha_image_path)
        
        # Отображение изображения CAPTCHA
        pixmap = QtGui.QPixmap(captcha_image_path)
        self.captcha_image_label.setPixmap(pixmap.scaled(200, 80, QtCore.Qt.KeepAspectRatio))
        
        # Удаляем временный файл
        os.remove(captcha_image_path)

    def verify_captcha(self):
        """Проверка введенного текста."""
        user_input = self.captcha_input.text().strip()
        if user_input == self.captcha_text:
            QtWidgets.QMessageBox.information(self, "Success", "CAPTCHA Verified!")
            self.accept()  # Закрыть окно CAPTCHA с успехом
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid CAPTCHA. Try again.")
            self.generate_captcha()  # Сгенерировать новую CAPTCHA
            self.captcha_input.clear()


