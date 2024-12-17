from loginWindow import Dialog_Login,Dialog_Register
import sys 
from PyQt5.QtWidgets import QApplication
if __name__ =="__main__":
    app = QApplication(sys.argv)
    dialog = Dialog_Login()
    dialog.show()
    sys.exit(app.exec_())
