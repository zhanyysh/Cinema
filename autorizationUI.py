from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogRegister(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setGeometry(300, 250, 400, 300)
        Dialog.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);\n"
                             "border-radius: 10px;")
                             
        # Кнопка "sign in"
        self.signin_button = QtWidgets.QPushButton(Dialog)
        self.signin_button.setGeometry(QtCore.QRect(170, 260, 93, 28))
        self.signin_button.setStyleSheet("""
            QPushButton {
                background-color: #CCCCCC;
                color: #000000;
                font-size: 14px;
                border-radius: 2px;
                transition: 0.3s ease;
            }
            QPushButton:hover {
                background-color: #AAAAAA;  /* Более темный оттенок серого */
                color: #333333;  /* Изменение цвета текста */
            }
        """)
        self.signin_button.setObjectName("signin_button")

        # Кнопка "sign up"
        self.signup_button = QtWidgets.QPushButton(Dialog)
        self.signup_button.setGeometry(QtCore.QRect(50, 210, 211, 31))
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
                border-radius: 2px;
                transition: 0.3s ease;
            }
            QPushButton:hover {
                background-color: #FF5555;  /* Ярче красный */
                color: #FFFFFF;
            }
        """)
        self.signup_button.setObjectName("signup_button")

        # Поле "password"
        self.password_line = QtWidgets.QLineEdit(Dialog)
        self.password_line.setGeometry(QtCore.QRect(50, 140, 211, 51))
        self.password_line.setStyleSheet("""
    QLineEdit {
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #555555;
        border-radius: 2px;
        padding: 5px;
        font-size: 14px;
        transition: border-color 0.3s ease;
    }
    QLineEdit:focus {
        border-color: #00AAFF;  /* Цвет рамки при фокусе */
    }
""")

        self.password_line.setObjectName("password_line")

        # Поле "nickname"
        self.nickname_line = QtWidgets.QLineEdit(Dialog)
        self.nickname_line.setGeometry(QtCore.QRect(50, 70, 211, 51))
        self.nickname_line.setStyleSheet("""
    QLineEdit {
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #555555;
        border-radius: 2px;
        padding: 5px;
        font-size: 14px;
        transition: border-color 0.3s ease;
    }
    QLineEdit:focus {
        border-color: #00AAFF;  /* Цвет рамки при фокусе */
    }
""")

        self.nickname_line.setObjectName("nickname_line")

        # Метка "already have acc?"
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 270, 101, 20))
        self.label.setStyleSheet("color: #00FF00;\n"
                                 "font-size: 12px;\n"
                                 "text-decoration: underline;\n"
                                 "")
        self.label.setObjectName("label")

        # Заголовок "SIGN UP"
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 20, 161, 31))
        self.label_2.setStyleSheet("color: #ffffff;\n"
                                   "font-size: 20px;\n"
                                   "font-weight: bold;\n"
                                   "")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Sign up"))
        self.signin_button.setText(_translate("Dialog", "sign in"))
        self.signup_button.setText(_translate("Dialog", "sign up"))
        self.password_line.setPlaceholderText(_translate("Dialog", "password"))
        self.nickname_line.setPlaceholderText(_translate("Dialog", "nickname"))
        self.label.setText(_translate("Dialog", "already have acc?"))
        self.label_2.setText(_translate("Dialog", "SIGN UP"))
class Ui_DialogLogin(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(313, 314)
        Dialog.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);\n"
                             "border-radius: 5px;")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(172, 260, 93, 28))  # Сдвинуто на 2 пикселя вправо
        self.pushButton.setStyleSheet("""
            background-color: #CCCCCC;
            color: #000000;
            font-size: 14px;
            border-radius: 2px;
            transition: 0.3s ease;
                    }
            QPushButton:hover {
            background-color: #AAAAAA;  /* Цвет становится более заметным */
            color: #333333;  /* Темный текст при наведении */
            }
            """)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 210, 211, 31))
        self.pushButton_2.setStyleSheet("""
                    background-color: #FF0000;
                    color: #FFFFFF;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 2px;
                    transition: 0.3s ease;
                }
                    QPushButton:hover {
                background-color: #FF5555;  /* Ярче красный при наведении */
                color: #FFFFFF;  /* Белый текст остается */
                }
                    """)
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(50, 140, 211, 51))
        self.lineEdit.setStyleSheet("""
    QLineEdit {
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #555555;
        border-radius: 2px;
        padding: 5px;
        font-size: 14px;
        transition: border-color 0.3s ease;
    }
    QLineEdit:focus {
        border-color: #00AAFF;  /* Цвет рамки при фокусе */
    }
""")

        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 70, 211, 51))
        self.lineEdit_2.setStyleSheet("""
    QLineEdit {
        background-color: #000000;
        color: #ffffff;
        border: 2px solid #555555;
        border-radius: 2px;
        padding: 5px;
        font-size: 14px;
        transition: border-color 0.3s ease;
    }
    QLineEdit:focus {
        border-color: #00AAFF;  /* Цвет рамки при фокусе */
    }
""")

        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 270, 121, 16))
        self.label.setStyleSheet("color: #00FF00;\n"
                                 "font-size: 12px;\n"
                                 "text-decoration: underline;\n"
                                 "")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 20, 161, 31))
        self.label_2.setStyleSheet("color: #ffffff;\n"
                                   "font-size: 20px;\n"
                                   "font-weight: bold;\n"
                                   "")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Login"))
        self.pushButton.setText(_translate("Dialog", "sign up"))
        self.pushButton_2.setText(_translate("Dialog", "sign in"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "password"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "nickname"))
        self.label.setText(_translate("Dialog", "new to AIT-WOOD?"))
        self.label_2.setText(_translate("Dialog", "SIGN IN"))


