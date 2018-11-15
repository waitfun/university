import requests,math
from bs4 import BeautifulSoup
import recognise
import mysqldb as db
def login():
    url='http://kdjw.hnust.edu.cn/kdjw/Logon.do?method=logon'
    verify_url='http://kdjw.hnust.edu.cn/kdjw/verifycode.servlet'
    headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3)'}
    kdjw_session = requests.Session()
   
    #下载验证码到本地
    verify = kdjw_session.get(verify_url,headers=headers,verify=False)
    with open('./images/code.jpg', 'wb') as f:
        f.write(verify.content)
    verify_value = recognise.main()
   #简单判断是否识别为空或者小于4位长度，否则重新执行
    if verify_value == '' or len(verify_value) !=4:
        verify_value = recognise.main()
    print(verify_value)
    data = {
    'dlfl':'0',
    'USERNAME':'1061009',
    'PASSWORD':'1061009',
    'RANDOMCODE':verify_value,
    
    }
    
    result = kdjw_session.post(url,data=data,headers=headers)
    cookies = (result.cookies)
    cookie = ('; '.join(['='.join(item) for item in cookies.items()]))
   
    f = kdjw_session.get('http://kdjw.hnust.edu.cn/kdjw/ggxx/jzg/listJzgxx.jsp?jsd=JSD-JSXX-JSXXCK&sttype=1',headers=headers)
    #print(f.content.decode())
    
def login1():
    url='http://kdjw.hnust.edu.cn/kdjw/Logon.do?method=logon'
   
    verify_value,cookie = recognise.main()
   #简单判断是否识别为空或者小于4位长度，否则重新执行
    headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3)',
        'Cookie':cookie
    }
    #print(verify_value)
    for i in range(1,5):
        account = ['3010001']#['1010003','1020153','1030095','1040061','1051001','1061009','1070098','1081003','1090020','1100012','1110020','1120079','1130001','1140023','1150020','1161007','1170069','1180030','1190018','1200012','1300041','3010001']
        for acc in account:
            data = {
            'dlfl':'0',
            'USERNAME':acc,
            'PASSWORD':acc,
            'RANDOMCODE':verify_value,
            
            }
            
            result = requests.post(url,data=data,headers=headers)
            f = requests.get('http://kdjw.hnust.edu.cn/kdjw/ggxx/jzg/listJzgxx.jsp?jsd=JSD-JSXX-JSXXCK&sttype=1',headers=headers)
            soup = BeautifulSoup(f.content, 'html.parser')
            page_total = math.ceil(int(soup.find("div",id="PageNavigation").text.split("共")[1].split("条")[0])/100)
            cursor,connect = db.dbconnect()
            for page in range(1,int(page_total)+1):
                params = {
                    "PageNum":page,
                }
                url2 = "http://kdjw.hnust.edu.cn/kdjw/ggxx/jzg/listJzgxx.jsp?jsd=JSD-JSXX-JSXXCK&sttype=1&"
            
                content = requests.post(url2,headers=headers,verify=False,data=params)
                soup = BeautifulSoup(content.content, 'html.parser')
                tr_list = soup.find_all("tr",class_="smartTr")
                for item in soup.find_all("tr",class_="smartTr"):
                    info_list = item.find_all("td")
                    #学号
                    teacher_no = info_list[2].text
                    teacher_name = info_list[3].text
                    sex = info_list[5].text
                    nation = info_list[8].text
                    card_no = info_list[9].text
                    department = info_list[14].text
                    native_place = info_list[7].text
                    profess = info_list[13].text
                    #教学时间
                    jion_time = info_list[17].text
                    sql1 = " select teacher_no from hnust_teacher where teacher_no = '%s'" %(teacher_no)
                    cursor.execute(sql1)
                    # 获取所有记录列表
                    results = cursor.fetchone()
                    #print(results[0])#(1060128,)
                    if results == '':
                        sql2 = "insert into hnust_teacher(teacher_no,teacher_name,department,sex,card_no,nation,native_place,jion_time,profess)values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (teacher_no,teacher_name,department,sex,card_no,nation,native_place,jion_time,profess)
                        cursor.execute(sql2)
                        connect.commit()
                        print("add one data")
                    else:
                        sql3 = "update hnust_teacher set department='%s' ,sex='%s' ,card_no='%s' ,nation='%s',native_place='%s',jion_time='%s',profess='%s' where teacher_no ='%s'" %(department,sex,card_no,nation,native_place,jion_time,profess,teacher_no)
                        cursor.execute(sql3)
                        connect.commit()
                        print("update one data")
login1()