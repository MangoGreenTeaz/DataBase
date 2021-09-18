import pymysql

def MySQLdb():
    connection = pymysql.connect(host = 'localhost',
                     port = 3306,
                     user = 'root',
                     passwd = 'root',
                     db = 'test',
                     charset="utf8")
    return connection