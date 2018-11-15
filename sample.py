
import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract
import requests

#下载验证码
def get_code():
    url ="http://kdjw.hnust.cn/kdjw/verifycode.servlet"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',       
    }
    img=requests.get(url,headers = headers).content
    with open('./images/code.jpg','wb') as fd:
        fd.write((img))
   
#二值化
def convert_image(image):
    image=image.convert('L')
    image2=Image.new('L',image.size,255)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix=image.getpixel((x,y))
            if pix<120:
                image2.putpixel((x,y),0)
    image2.save("./images/code.jpg")
    #return image2
#去掉边框
def removeFrame(img, width):
    w, h = img.size
    pixdata = img.load()
    for x in range(width):
        for y in range(0, h):
            pixdata[x, y] = 255
    for x in range(w - width, w):
        for y in range(0, h):
            pixdata[x, y] = 255
    for x in range(0, w):
        for y in range(0, width):
            pixdata[x, y] = 255
    for x in range(0, w):
        for y in range(h - width, h):
            pixdata[x, y] = 255
    img.save("./images/code.jpg")
#识别 
def recognize_text(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #二值化
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    #矩形：MORPH_RECT
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 2))
    binl = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 1))
    open_out = cv.morphologyEx(binl, cv.MORPH_OPEN, kernel)
    cv.bitwise_not(open_out, open_out)  # 背景变为白色
    textImage = Image.fromarray(open_out)
    #cv.imwrite("./images/233.png",open_out)
    text = pytesseract.image_to_string(textImage).strip()#.encode("utf-8")
    #print("This OK:%s"%text)
    return text
 
def main():
    get_code()
    image=Image.open('./images/code.jpg' )
    convert_image(image)
    image2=Image.open('./images/code.jpg' )
    removeFrame(image2, 1)
    img = cv.imread('./images/code.jpg')
    text = recognize_text(img)
    #对于识别错误的 采用该表进行修正
    rep={
        'e':'c',
        'i':'1',
        'y':'v'
    }
    verify_value = ''
    for r in rep:
        text = text.replace(r,rep[r])
        verify_value=text.lower()
    #简单判断是否识别为空或者小于4位长度，否则重新执行
    if verify_value == '' or len(verify_value) !=4:
        main()
    return verify_value

if __name__ == "__main__":
    print(main())