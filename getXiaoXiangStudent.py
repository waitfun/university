import requests,pymysql
from bs4 import BeautifulSoup
import csv,time,re,math
import sys
import io
import mysqldb as db
import threading
#改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
cookie = "JSESSIONID=E144E083905DBCD87C3DDF5B803C04E4"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 
        'Cookie':cookie
    }

#入学年份
rxnf = ""
def getInfo(yx):
    url = "http://xxjw.hnust.cn/xxjw/xszhxxAction.do?method=goSosoXsxx&xjzt=00&yx=%s&rxnf=&zy=&bj=&dqzt=&zzmm=&gjdqm=&xb=&xm=&xh=&sfzhm=&hasZp="%(yx)
    content1 = requests.post(url,headers=headers,verify=False)
    url2 ="http://xxjw.hnust.cn/xxjw/xszhxxAction.do?method=goQuerXsjbxx"
    content = requests.post(url2,headers=headers,verify=False)
    soup = BeautifulSoup(content.content, 'html.parser')
    #总页数，取出总条数/每页数量，向上取整
    page_total = math.ceil(int(soup.find("div",id="PageNavigation").text.split("共")[1].split("条")[0])/100)
    url = "http://xxjw.hnust.cn/xxjw/xszhxxAction.do?method=goSosoXsxx&xjzt=00&yx=%s&rxnf=&zy=&bj=&dqzt=&zzmm=&gjdqm=&xb=&xm=&xh=&sfzhm=&hasZp="%(yx)
    for page in range(1,int(page_total)+1):
        params = {
            "PageNum":page,
        }
        content1 = requests.post(url,headers=headers,verify=False)
        url2 ="http://xxjw.hnust.cn/xxjw/xszhxxAction.do?method=goQuerXsjbxx"
        content = requests.post(url2,headers=headers,verify=False,data=params)
        soup = BeautifulSoup(content.content, 'html.parser')
        tr_list = soup.find_all("tr",class_="smartTr")
        for item in soup.find_all("tr",class_="smartTr"):
            info_list = item.find_all("td")
            #学号
            student_no = info_list[2].text
            #姓名
            student_name = info_list[3].text
            #性别
            sex =   info_list[6].text
            #学院
            xy = info_list[7].text
            #专业
            zy = info_list[8].text
            #班级
            class_name  = info_list[10].text
            #出生日期
            birthday = info_list[11].text
            #身份证
            card_no = info_list[12].text
             #入学时间
            entrance_time = info_list[16].text
            #民族
            nation = info_list[21].text
             #籍贯
            native_place = info_list[22].text
            #政治面貌
            political = info_list[24].text
            #电话
            phone = info_list[31].text
            #类型,1本部，2潇湘
            style = 2
            print("学号："+student_no,"姓名："+student_name,"性别："+sex,"班级："+class_name,"院系:"+xy)  
            cursor,connect = db.dbconnect()
            sql = "insert into hnust_student (student_no,student_name,sex,xy,zy,class_name,birthday,card_no,entrance_time,nation,native_place,political,phone,style) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (student_no,student_name,sex,xy,zy,class_name,birthday,card_no,entrance_time,nation,native_place,political,phone,style)
            cursor.execute(sql)
            connect.commit()
if __name__ =="__main__":
    params = ['70']#['29','30','31','32','33','34','35','36','37','38','21','22','23','24','25','26','27','28','39','70']
    threads = [threading.Thread(target=getInfo,args=(param,)) for param in params]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
   