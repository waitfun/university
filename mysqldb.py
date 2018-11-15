import requests,pymysql

def dbconnect():
    connect = pymysql.Connection(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='hnust_student',
            charset='utf8')
    cursor = connect.cursor()
    return cursor,connect