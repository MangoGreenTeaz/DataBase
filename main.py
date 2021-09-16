import pymysql
from loginWindow import Login
from lib.win import Window
from lib.connect import MySQLdb
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

con = MySQLdb()
cur = con.cursor(cursor=pymysql.cursors.DictCursor)


window = Window()
window.loginWindow = Login()


con.commit()
#关闭游标连接
cur.close()
#关闭数据库连接
con.close()
