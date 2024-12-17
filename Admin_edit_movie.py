import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from Admin_add_movie_part import add_part_Dialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
SERVER = "https://zhanyysh.pythonanywhere.com"

class admin_Movie_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("taran.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(624, 483)
        self.setWindowTitle("Edit Movie")
        self.ui = Ui_Edit_movie_Dialog()
        self.ui.setupUi(self)
        self.load_movies()
        
        # Связываем действия с кнопками
        self.ui.add_sessin_movie_button.clicked.connect(self.open_add_window)
        self.ui.delete_movie_button.clicked.connect(self.delete_movie)
        self.ui.delete_session_button.clicked.connect(self.delete_session)
        self.dialog_add_movie_instance = None

    def load_movies(self):
    
        self.ui.movie_combobox.clear()
        response = requests.get(f"{SERVER}/movies")
        if response.status_code != 200:
            print(f"Error: Failed to fetch movies. Status code: {response.status_code}")
            return

        try:
            movies = response.json()
        except ValueError as e:
            print(f"Error: Failed to parse JSON response. Response Text: {response.text}")
            return

        for movie in movies:
            self.ui.movie_combobox.addItem(movie['title'], movie['id'])  # Добавляем фильмы в комбобокс

    # Связываем сигнал изменения фильма с методом загрузки сеансов
        self.ui.movie_combobox.currentIndexChanged.connect(self.load_sessions)

        if movies:  # Если фильмы есть, загружаем сеансы для первого фильма
            self.load_sessions()

    def load_sessions(self):
        """Загружает сеансы для выбранного фильма в таблицу."""
        movie_id = self.ui.movie_combobox.currentData()
        if not movie_id:  # Если нет выбранного фильма, ничего не делаем
            self.ui.table.setRowCount(0)
            return

        response = requests.get(f"{SERVER}/load_sessions/{movie_id}")
        if response.status_code != 200:
            print(f"Error: Failed to fetch sessions. Status code: {response.status_code}")
            print(f"Response Text: {response.text}")
            self.ui.table.setRowCount(0)
            return

        try:
            sessions = response.json()
        except ValueError as e:
            print(f"Error: Failed to parse JSON response. Response Text: {response.text}")
            self.ui.table.setRowCount(0)
            return

    # Обновляем таблицу
        self.ui.table.setRowCount(len(sessions))
        for row, session in enumerate(sessions):
            self.ui.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(session['session_id'])))  # ID сеанса
            self.ui.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(session['tickets'])))  # Количество билетов
            self.ui.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(session['price'])))  # Цена
            self.ui.table.setItem(row, 3, QtWidgets.QTableWidgetItem(session['session_time']))  # Время сеанса

    def delete_movie(self):
        movie_id = self.ui.movie_combobox.currentData()
        if not movie_id:
            return
        response = requests.delete(f"{SERVER}/movies/{movie_id}")
        if response.status_code == 200:
            self.load_movies()  # Перезагружаем список фильмов

    def delete_session(self):
        current_row = self.ui.table.currentRow()
        if current_row == -1:
                return  # No session selected

    # Получаем ID сеанса из таблицы (предполагается, что ID сеанса находится в первой колонке)
        session_id = self.ui.table.item(current_row, 0).text()

    # Отправляем запрос DELETE на сервер
        response = requests.delete(f"{SERVER}/delete_session/{session_id}")
    
    # Проверяем статус ответа
        if response.status_code == 200:
                self.load_sessions()  # Перезагружаем список сеансов после успешного удаления
        else:
                print(f"Error: Failed to delete session. Status code: {response.status_code}")
                print(f"Response Text: {response.text}")  # Логирование для отладки

    def open_add_window(self):
        if self.dialog_add_movie_instance is None:
            self.dialog_add_movie_instance = add_part_Dialog()
        self.dialog_add_movie_instance.show()


class Ui_Edit_movie_Dialog(object):
    def setupUi(self, Edit_movie_Dialog):
        Edit_movie_Dialog.setObjectName("Edit_movie_Dialog")
        Edit_movie_Dialog.resize(624, 483)
        
        # Создание UI элементов
        self.movie_combobox = QtWidgets.QComboBox(Edit_movie_Dialog)
        self.movie_combobox.setGeometry(QtCore.QRect(40, 20, 181, 31))
        self.movie_combobox.setObjectName("movie_combobox")
        
        self.table = QtWidgets.QTableWidget(Edit_movie_Dialog)  # Изменено с QTableView на QTableWidget
        self.table.setGeometry(QtCore.QRect(45, 80, 521, 271))
        self.table.setObjectName("table")
        self.table.setColumnCount(4)  # Устанавливаем количество столбцов в таблице
        self.table.setHorizontalHeaderLabels(["ID", "Количество билетов", "Цена", "Время сеанса"])

        # Кнопка добавления фильма/сеанса
        self.add_sessin_movie_button = QtWidgets.QPushButton(Edit_movie_Dialog)
        self.add_sessin_movie_button.setGeometry(QtCore.QRect(60, 380, 141, 51))
        self.add_sessin_movie_button.setStyleSheet("background-color: red; color: white; font-size: 14px;")
        self.add_sessin_movie_button.setObjectName("add_sessin_movie_button")
        
        # Кнопка удаления фильма
        self.delete_movie_button = QtWidgets.QPushButton(Edit_movie_Dialog)
        self.delete_movie_button.setGeometry(QtCore.QRect(240, 380, 141, 51))
        self.delete_movie_button.setStyleSheet("background-color: red; color: white; font-size: 14px;")
        self.delete_movie_button.setObjectName("delete_movie_button")

        # Кнопка удаления сеанса
        self.delete_session_button = QtWidgets.QPushButton(Edit_movie_Dialog)
        self.delete_session_button.setGeometry(QtCore.QRect(412, 380, 141, 51))
        self.delete_session_button.setStyleSheet("background-color: red; color: white; font-size: 14px;")
        self.delete_session_button.setObjectName("delete_session_button")

        self.retranslateUi(Edit_movie_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Edit_movie_Dialog)

    def retranslateUi(self, Edit_movie_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Edit_movie_Dialog.setWindowTitle(_translate("Edit_movie_Dialog", "Dialog"))
        self.add_sessin_movie_button.setText(_translate("Edit_movie_Dialog", "Add Movie/Session"))
        self.delete_movie_button.setText(_translate("Edit_movie_Dialog", "Delete Movie"))
        self.delete_session_button.setText(_translate("Edit_movie_Dialog", "Delete Session"))


