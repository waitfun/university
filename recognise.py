
import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract
import requests
'''验证码识别程序'''
def get_code():
    verify_url='http://kdjw.hnust.edu.cn/kdjw/verifycode.servlet'
    header={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3)'}
   
    #下载验证码到本地
    verify = requests.get(verify_url,headers=header,verify=False)
    cookies = (verify.cookies)
    cookie = ('; '.join(['='.join(item) for item in cookies.items()]))
    with open('./images/code.jpg', 'wb') as f:
        f.write(verify.content)
    return cookie
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
#不带cookie处理，直接处理图片识别
def no_cookies():
   
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
    
    return verify_value
#带cookie,
def main():
    cookie = get_code()
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
    # if verify_value == '' or len(verify_value) !=4:
    #     print(2333)
    #     main()
    #     #return verify_value,cookie
    # else:
    return verify_value,cookie

if __name__ == "__main__":
    print(main())