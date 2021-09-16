from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from lib.connect import MySQLdb
import pymysql

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

    def clickButton_login(self):
        account = self.ui.lineEdit_loginAccount.text().strip()
        password = self.ui.lineEdit_loginPassword.text().strip()
        userType = self.ui.comboBox_accountType.currentText()
        if userType == '用户':
            SQL = 'SELECT * FROM users WHERE Account = %s;'
        elif userType == '员工':
            SQL = 'SELECT * FROM personnel WHERE Account = %s;'
        elif userType == '经理':
            SQL = 'SELECT * FROM manager WHERE Account = %s;'
        else:
            SQL = 'SELECT * FROM admins WHERE Account = %s;'
        cur.execute(SQL, [account])
        result = cur.fetchone()
        try:
            if result['Passwords'] == password:
                QMessageBox.information(
                self.ui,'登录成功',f'''登录成功！''')
                pass # 进入主界面
            else:
                QMessageBox.warning(self.ui,'登录失败',f'''登录失败！\n账号与密码不匹配，请检查后重新登录''')
        except TypeError:
            QMessageBox.warning(self.ui,'登录失败',f'''登录失败！\n没有该账号''')
        except  Exception as e:
            print('出错类型：', type(e))

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
        except Exception as e:
            print('出错类型：', type(e))
        else:
            QMessageBox.information(
                self.ui,'注册成功',f'''恭喜你，注册成功！\n欢迎成为芒果超市的用户！\n请点击上方登录按钮回到登录界面进行登录''')
            con.commit()

app = QApplication([])
loginWindow = Login()
loginWindow.ui.show()
app.exec_()

