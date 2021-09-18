# -*- encoding: utf-8 -*-

'''
@File    :   userWindow.py
@Time    :   2021/09/08 15:29:01
@Author  :   Hu Lei 
@Version :   1.0
@Contact :   hulei15082452670@gmail.com
@Desc    :   None
'''

# import lib
from PySide2.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QPushButton, QWidget, QHBoxLayout 
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
from lib.connect import MySQLdb
import pymysql

con = MySQLdb()
cur = con.cursor(cursor=pymysql.cursors.DictCursor)










SQL_getCommodity = 'SELECT commodity.ID,commodity.Names,commodity.Brand,commodity.Weights,commodity.Types,stock.Amount,commodity.Price FROM commodity,stock WHERE commodity.ID = stock.commodityID AND stock.shopID = %s;'
cur1 = con.cursor()
cur1.execute(SQL_getCommodity,[1])
result_getCommodity = cur1.fetchall()
print(result_getCommodity)