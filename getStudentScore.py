import requests
from bs4 import BeautifulSoup
import csv,time,re,math
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
def getScore():
    cookie = "JSESSIONID=AE9029BE20920E54399350EB7C13D7AF; Hm_lvt_c09b7f26e29f23a8e4c2c74fc98ca736=1526317044,1527310349,1527498285,1527844527"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 
            'Cookie':cookie
        }
    url = "http://kdjw.hnust.edu.cn/kdjw/cjzkAction.do?method=tofindCj0708ByXNZY"
    params = {
        #排名方式：
        'pmfs': '3',
        #排序方式
        'pxfs': '1',
        'rxnf': '2017',
        'xjzt': '01',
        'xsfs': '1',
        'xh':'1716030417',
        #专业方向：
        'zyfx':'',
        'xqmc':'',
        'xnxq': '2017-2018-2',
        'xnxqs': '2017-2018-2',
        'yx': '16',
        'zy': '7460476E105C4753B73B6559D7E43193',#'4BB9933ADA87451FA433A850C17DFD5D',
        'zymc': '[2017]音乐学'
    }
    req = requests.post(url,headers=headers,verify=False,data=params)
    #print(req.text)
    soup = BeautifulSoup(req.content, 'html.parser')
    for item in soup.find_all("tr",class_="smartTr"):
        with open("2.html","a",encoding="utf-8") as fd:
            fd.write(str(item))
        info_list = item.find_all("td")
        student_no = info_list[1].text
        student_name = info_list[2].text
        print(student_name,student_no)
    tbcontent = soup.find("div",id="tblHeadDiv")
    th_list = tbcontent.find_all("th")
    for item2 in th_list:
        print(item2.text)
        with open("1.html","a",encoding="utf-8") as fd:
            fd.write(str(item2))

if __name__ == "__main__":
    getScore()