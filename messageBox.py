from PyQt5.QtWidgets import QMessageBox

def show_message(message, title="Message"):
    """Показывает сообщение пользователю с минимальным дизайном"""
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)  # Устанавливаем заголовок окна
    msg_box.setText(message)  # Устанавливаем текст сообщения
    msg_box.setStandardButtons(QMessageBox.Ok)  # Добавляем кнопку Ok
    msg_box.exec_()

def show_ui_not_ready_message():
    """Сообщение о том, что пользовательский интерфейс не готов"""
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Сообщение")
    msg_box.setText("Пользовательский интерфейс еще не готов.")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
