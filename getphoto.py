
import requests,pymysql
import downloader as down
#http://kdjw.hnust.edu.cn/kdjw/uploadfile/studentphoto/pic/1805050231.JPG?r=1541034060642

connect = pymysql.Connection(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='hnust_student',
        charset='utf8')
cursor = connect.cursor()
def get_photo(grade):
    _grade = grade+'%'
    sql = "select student_no from hnust_student where student_no like '%s'" % _grade
    try:

        cursor.execute(sql)
        results = cursor.fetchall()
        
    except:
        print ("Error: unable to fetch data")
    for item in results:
        url = "http://kdjw.hnust.edu.cn/kdjw/uploadfile/studentphoto/pic/%s.JPG"% item[0]
        r = requests.get(url)
        if r.status_code == 200:
           down.downloader(url)
        else:
            url2 = "http://kdjw.hnust.edu.cn/kdjw/uploadfile/studentphoto/pic/%s.jpg" % item[0]
            r2 = requests.get(url2)
            if r2.status_code == 200:
                down.downloader(url2)
            else:
                pass
        
if __name__ == '__main__':
    grade = input("输入年份（例如：18):\n")
    get_photo(grade)
