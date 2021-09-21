# -*- encoding: utf-8 -*-

'''
@File    :   loginWindow.py
@Time    :   2021/09/08 10:56:45
@Author  :   Hu Lei 
@Version :   1.0
@Contact :   hulei15082452670@gmail.com
@Desc    :   None
'''

# import lib
from PySide2.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QPushButton, QWidget, QHBoxLayout
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtCore
import sys
import pymysql

from lib.connect import MySQLdb
from lib.win import Window

con = MySQLdb()
cur = con.cursor(cursor=pymysql.cursors.DictCursor)


class Login:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = QUiLoader().load('./ui/login&register.ui')
        # 登录
        self.ui.button_login.clicked.connect(self.clickButton_login)
        self.ui.lineEdit_loginPassword.returnPressed.connect(self.clickButton_login)
        # 确认注册
        self.ui.button_confirmRegister.clicked.connect(self.clickButton_confirmRegister)
        self.ui.lineEdit_Phone.returnPressed.connect(self.clickButton_confirmRegister)

    # 用户登录
    def clickButton_login(self):
        account = self.ui.lineEdit_loginAccount.text().strip()
        password = self.ui.lineEdit_loginPassword.text().strip()
        userType = self.ui.comboBox_accountType.currentText()
        types = 0
        if userType == '用户':
            SQL = 'SELECT * FROM users WHERE Account = %s;'
            types = 1
        elif userType == '员工':
            SQL = 'SELECT * FROM personnel WHERE Account = %s;'
            types = 2
        elif userType == '经理':
            SQL = 'SELECT * FROM manager WHERE Account = %s;'
            types = 3
        else:
            SQL = 'SELECT * FROM admins WHERE Account = %s;'
            types = 4
        cur.execute(SQL, [account])
        result = cur.fetchone()
        try:
            if result['Passwords'] == password:
                QMessageBox.information(
                self.ui,'登录成功',f'''登录成功！''')
                window.userWindow = User(result['ID'])
                window.userWindow.ui.show()
                self.ui.close()
            else:
                QMessageBox.warning(self.ui,'登录失败',f'''登录失败！\n账号与密码不匹配，请检查后重新登录''')
        except TypeError:
            QMessageBox.warning(self.ui,'登录失败',f'''登录失败！\n没有该账号''')
        except  Exception as e:
            print('出错类型：', type(e))

    # 用户注册
    def clickButton_confirmRegister(self):
        registerAccount = self.ui.lineEdit_registerAccount.text().strip()
        registerPassword = self.ui.lineEdit_registerPassword.text().strip()
        realName = self.ui.lineEdit_realName.text().strip()
        sex = self.ui.lineEdit_sex.text().strip()
        if len(sex) == 0:
            sex = '男'
        nickName = self.ui.lineEdit_nickName.text().strip()
        if len(nickName) == 0 or len(nickName) >= 20:
            nickName = '游客'
        age = self.ui.lineEdit_age.text().strip()
        if len(age) == 0:
            age = 18
        phone = self.ui.lineEdit_Phone.text().strip()
        SQL = 'SELECT MAX(ID) FROM users'
        cur.execute(SQL)
        data = cur.fetchone()
        id = data['MAX(ID)'] + 1
        SQL = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 0, 0);'
        try:
            cur.execute(SQL, [id, registerAccount, registerPassword, realName, sex, nickName, phone, age])
        except pymysql.err.DataError:
            QMessageBox.warning(self.ui,'注册失败',f'''注册失败！\n请检查你输入的信息格式是否正确：\n账号：5-15位\n密码：5-15位\n真实姓名：不超过五位\n性别：男/女/不填\n电话号码：11位标准格式''')
        
        except pymysql.err.OperationalError:
            QMessageBox.warning(self.ui,'注册失败',f'''注册失败！\n请检查你输入的信息格式是否正确：\n账号：5-15位\n密码：5-15位\n真实姓名：不超过五位\n性别：男/女/不填\n电话号码：11位标准格式''')
        except pymysql.err.IntegrityError:
            sql1 = 'SELECT * FROM users WHERE Account = %s'
            cur.execute(sql1,[registerAccount])
            result1 = cur.fetchall()
            if len(result1):
                QMessageBox.warning(self.ui,'注册失败',f'''注册失败！\n该账号已被注册，请重新输入账号''')
            sql2 = 'SELECT * FROM users WHERE Phone = %s'
            cur.execute(sql2,[phone])
            result2 = cur.fetchall()
            if len(result2):
                QMessageBox.warning(self.ui,'注册失败',f'''注册失败！\n该手机号已绑定其他账号''')
        #except Exception as e:
            #print('出错类型：', type(e))
        else:
            QMessageBox.information(
                self.ui,'注册成功',f'''恭喜你，注册成功！\n欢迎成为芒果超市的用户！\n请点击上方登录按钮回到登录界面进行登录''')
            con.commit()


class User:
    
    def __init__(self, userID):
        # 从文件中加载UI
        self.ui = QUiLoader().load('./ui/userWindow.ui')
        self.ui.button_commodity.clicked.connect(self.clickButton_commodity)
        self.ui.button_shoppingCart.clicked.connect(self.clickButton_shoppingCart)
        self.ui.button_order.clicked.connect(self.clickButton_order)
        self.ui.button_mine.clicked.connect(self.clickButton_mine)
        self.userID = userID
        #
        self.addShop()
        self.ui.comboBox_shop.currentIndexChanged.connect(self.shopChanged)
        self.shopID = 1

        self.setTable_commodity()
        self.setTable_shoppingCart()



    def clickButton_commodity(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def clickButton_shoppingCart(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def clickButton_order(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def clickButton_mine(self):
        self.ui.stackedWidget.setCurrentIndex(3)

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
        button_add = QPushButton('+')
        button_add.setStyleSheet(''' text-align : center;
                                          background-color : NavajoWhite;
                                          height : 30px;
                                          border-style: outset;
                                          font : 13px  ''')

        button_add.clicked.connect()

        # 减少
        button_reduce = QPushButton('-')
        button_reduce.setStyleSheet(''' text-align : center;
                                  background-color : DarkSeaGreen;
                                  height : 30px;
                                  border-style: outset;
                                  font : 13px; ''')

        button_reduce.clicked.connect(lambda: self.viewTable(id))


        hLayout = QHBoxLayout()
        hLayout.addWidget(button_add)
        hLayout.addWidget(button_reduce)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    #def setTable_commodity(self):
        #SQL_getShoppingCart = 'SELECT commodity.ID,commodity.Names,commodity.Brand,commodity.Weights,commodity.Types,AmoutOfCommdity,AmoutOfMoney FROM commodity, WHERE commodity.ID = stock.commodityID AND stock.shopID = %s;'


app = QApplication([])
window = Window()
window.loginWindow = Login()
window.loginWindow.ui.show()
app.exec_()