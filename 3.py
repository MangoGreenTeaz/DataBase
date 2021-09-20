import sys,time
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout

class WinForm(QWidget):
    def __init__(self,parent=None):
        super(WinForm, self).__init__(parent)
        #设置标题与布局方式
        self.setWindowTitle('实时刷新界面的例子')
        layout=QGridLayout()

        #实例化列表控件与按钮控件
        self.listFile=QListWidget()
        self.btnStart=QPushButton('开始')

        #添加到布局中指定位置
        layout.addWidget(self.listFile,0,0,1,2)
        layout.addWidget(self.btnStart,1,1)

        #按钮的点击信号触发自定义的函数
        self.btnStart.clicked.connect(self.slotAdd)
        self.setLayout(layout)
    def slotAdd(self):
        for n in range(10):
            #获取条目文本
            str_n='File index{0}'.format(n)
            #添加文本到列表控件中
            self.listFile.addItem(str_n)
            #实时刷新界面
            QApplication.processEvents()
            #睡眠一秒
            time.sleep(1)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    win=WinForm()
    win.show()
    sys.exit(app.exec_())

    # encoding=utf-8
import sys
import PyQt5.QtWidgets as qw
import ui_stack
class myForm(qw.QWidget, ui_stack.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.btn1_fun)
        self.pushButton2.clicked.connect(self.btn2_fun)
        self.pushButton3.clicked.connect(self.btn3_fun)
    def btn1_fun(self):
        self.stackedWidget.setCurrentIndex(0)
    def btn2_fun(self):
        self.stackedWidget.setCurrentIndex(1)
    def btn3_fun(self):
        self.stackedWidget.setCurrentIndex(2)
if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    w = myForm()
    w.show()
    sys.exit(app.exec_())