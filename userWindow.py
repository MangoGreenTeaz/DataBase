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
from PySide2.QtWidgets import QApplication, QTableWidgetItem, QMessageBox
from PySide2.QtUiTools import QUiLoader
from lib.connect import MySQLdb
import pymysql

con = MySQLdb()
cur = con.cursor(cursor=pymysql.cursors.DictCursor)


class User:

    def __init__(self):
        # 从文件中加载UI
        self.ui = QUiLoader().load('./ui/userWindow.ui')

        #
        self.addShop()
        self.ui.comboBox_shop.currentIndexChanged.connect(self.shopChanged)
        self.shopID = 1

        self.setTable_commodity()

    # 分店选择

    def addShop(self):
        SQL_getShops = 'SELECT * FROM shop;'
        cur.execute(SQL_getShops)
        result_getShops = cur.fetchall()
        for i in range(len(result_getShops)):
            self.ui.comboBox_shop.addItem(result_getShops[i]['Address'])

    # 更改分店
    def shopChanged(self):
        shopName = self.ui.comboBox_shop.currentText()
        SQL_getShopID = 'SELECT ID FROM shop WHERE address = %s;'
        cur.execute(SQL_getShopID, [shopName])
        result_getShopID = cur.fetchone()
        self.shopID = result_getShopID['ID']

    # 设置商品表格
    def setTable_commodity(self):
        # 查询商品信息和库存
        SQL_getCommodity = 'SELECT commodity.ID,commodity.Names,commodity.Brand,commodity.Weights,commodity.Types,stock.Amount,commodity.Price FROM commodity,stock WHERE commodity.ID = stock.commodityID AND stock.shopID = %s;'
        cur1 = con.cursor()
        cur1.execute(SQL_getCommodity, [self.shopID])
        result_getCommodity = cur1.fetchall()
        row = cur1.rowcount  # 取得记录个数，用于设置表格的行数
        vol = len(result_getCommodity[0])  # 取得字段数，用于设置表格的列数

        # 设置表格长宽
        self.ui.tableWidget_commodity.setRowCount(row)
        self.ui.tableWidget_commodity.setColumnCount(vol+1)

        # 设置表格列宽
        self.ui.tableWidget_commodity.setColumnWidth(0, 150)
        self.ui.tableWidget_commodity.setColumnWidth(1, 150)
        self.ui.tableWidget_commodity.setColumnWidth(2, 150)
        self.ui.tableWidget_commodity.setColumnWidth(3, 150)
        self.ui.tableWidget_commodity.setColumnWidth(4, 150)
        self.ui.tableWidget_commodity.setColumnWidth(5, 150)
        self.ui.tableWidget_commodity.setColumnWidth(6, 150)
        self.ui.tableWidget_commodity.setColumnWidth(7, 150)

        # 设置表头
        self.ui.tableWidget_commodity.setHorizontalHeaderLabels(
            ['条形码', '商品名称', '商品品牌', '净含量(g/ml)', '商品种类', '商品库存', '单价(元)', '操作'])

        self.ui.tableWidget_commodity.setHorizontalHeaderLabels(
            ['条形码', '商品名称', '商品品牌', '净含量(g/ml)', '商品种类', '商品库存', '单价(元)', '操作'])

        self.ui.tableWidget_commodity.horizontalHeader().setStyleSheet(
            "QHeaderView::section{background-color:rgb(155, 194, 230);font:11pt '宋体';color: black;};")

        # 插入数据
        for i in range(row):
            self.ui.tableWidget_commodity.setCellWidget(
                i, 7, self.buttonForRow(str(result_getCommodity[0])))
            for j in range(vol):
                # 临时记录，不能直接插入表格，转换后可插入表格
                temp_data = result_getCommodity[i][j]
                # 转换
                data = QTableWidgetItem(str(temp_data))
                # 插入
                self.ui.tableWidget_commodity.setItem(i, j, data)
                # 居中
                self.ui.tableWidget_commodity.item(
                    i, j).setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    # 列表内添加按钮
    def buttonForRow(self, id):
        widget = QWidget()
        # 添加
        button_update = QPushButton('+')
        button_update.setStyleSheet(''' text-align : center;
                                          background-color : NavajoWhite;
                                          height : 30px;
                                          border-style: outset;
                                          font : 13px  ''')

        button_update.clicked.connect(lambda: self.updateTable(id))

        # 减少
        button_view = QPushButton('-')
        button_view.setStyleSheet(''' text-align : center;
                                  background-color : DarkSeaGreen;
                                  height : 30px;
                                  border-style: outset;
                                  font : 13px; ''')

        button_view.clicked.connect(lambda: self.viewTable(id))

        # 清空
        button_delete = QPushButton('清空')
        button_delete.setStyleSheet(''' text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')

        hLayout = QHBoxLayout()
        hLayout.addWidget(button_update)

        hLayout.addWidget(button_view)
        hLayout.addWidget(button_delete)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget


app = QApplication([])
userWindow = User()
userWindow.ui.show()
app.exec_()
