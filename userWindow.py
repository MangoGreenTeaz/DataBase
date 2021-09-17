from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from lib.connect import MySQLdb
import pymysql

con = MySQLdb()
cur = con.cursor(cursor=pymysql.cursors.DictCursor)