
import requests,pymysql,base64,time
import mysqldb as db

cursor,connect = db.dbconnect()
#http://kdjw.hnust.edu.cn/kdjw/uploadfile/studentphoto/pic/1805050231.JPG?r=1541034060642

sql = "select student_no from hnust_student where style=1 and student_no like '15%'"
cursor.execute(sql)
dact = cursor.fetchall()
picture = ""
for item in dact:
    time.sleep(2)
    if len(str(item[0])) >=9:
        url = "http://kdjw.hnust.edu.cn/kdjw/uploadfile/studentphoto/pic/%s.JPG"% item[0]
        r = requests.get(url)
        if r.status_code == 200:
            picture_base64 = base64.b64encode(r.content)
            picture = "data:image/jpg;base64,%s" %picture_base64.decode().split("xMTE")[0]
            img_path = "./photo/%s.jpg" % item[0]
            with open(img_path,"wb") as fd:
                fd.write(r.content)
        else:
            url2 = "http://kdjw.hnust.edu.cn/kdjw/uploadfile/studentphoto/pic/%s.jpg" % item[0]
            r2 = requests.get(url2)
            if r2.status_code == 200:
                picture2_base64 = base64.b64encode(r2.content)
                picture = "data:image/jpg;base64,%s" %picture2_base64.decode().split("xMTE")[0]
                img_path = "./photo/%s.jpg" % item[0]
                with open(img_path,"wb") as fd:
                    fd.write(r2.content)
            else:
                pass
        #print(picture)
        print(url)
        photo = str(item[0])+".jpg"
        sql_1 = "insert into hnust_student_images (student_no,picture,photo)values('%s','%s','%s')"%(item[0],picture,photo)
        cursor.execute(sql_1)
        connect.commit()
    else:
        pass
