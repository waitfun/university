import mysqldb as db
import json,re
cursor,connect = db.dbconnect()

# try:
#     sql ="select student_no from users"
#     cursor.execute(sql)
#     results = cursor.fetchall()
    
# except:
#    print ("Error: unable to fetch data")
# for item in results:
#     sql_1 = "update users set style=1 where student_no =%s" % item[0]
#     cursor.execute(sql_1)
#     connect.commit()
f = open("dat.json", encoding='UTF-8') 
json = json.loads(f.read())
#print(json["data"]["contact_list"]["list"])
for item in json["data"]["contact_list"]["list"]:
    phone = (item["mobile"])
    student_no = item["acctid"]
    try:
        qq = re.findall('\d+',item["alias"])[0]
    except:
        qq = ""
    print(qq)
    email = item["alias"]
    #print(email)
    sql_1 = "update hnust_student set phone='%s',qq='%s',email='%s' where student_no ='%s'" % (phone,qq,email,student_no)
   # print(sql_1)
    cursor.execute(sql_1)
    connect.commit()
   