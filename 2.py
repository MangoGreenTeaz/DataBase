import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.Qt import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import time


class Communicate(QObject):
    closeApp = pyqtSignal()


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.c = Communicate()
        self.c.closeApp.connect(self.showMsg)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.lable = QLabel("hello", self)
        self.show()

    def mousePressEvent(self, event):

        self.c.closeApp.emit()

    def showMsg(self):
        print("ok")
        self.lable.setText("hahah")
        QApplication.processEvents()
        time.sleep(10)
        self.lable.setText("wait")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())