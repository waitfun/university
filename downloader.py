import requests,os,re
from contextlib import closing

#创建一个目录
downloader_path = './downloader/'
if os.path.exists(downloader_path) is False:
    os.mkdir(downloader_path)
class ProgressBar(object):
    def __init__(self,file_name,file_size = 100.0,unit = 'KB',chunk_size = 1024,run_status = '',finish_status = '',count=0.0, sep='/'):
        super(ProgressBar, self).__init__()  
        self.info = "[%s] [%.2f %s %s %.2f %s] %.2f%s %s"
        #文件名
        self.file_name = file_name
        #文件大小
        self.file_size = file_size  
        self.count = count
        #切片大小
        self.chunk_size = chunk_size
        #下载状态
        self.status = run_status 
        self.run_status = run_status   
        self.finish_status = finish_status 
        #单位，KB
        self.unit = unit
        #分割线
        self.seq = sep
        self.percent = '%'
    def __get_info(self):
        #[8C5C5A6CE173C9B89C33DC5901307461-20.mp4] 81848.35 KB / 34831.00 KB 42.56%
        _info = self.info % (self.file_name,  self.file_size/self.chunk_size, self.unit, self.seq, self.count/self.chunk_size, self.unit,(self.count/self.chunk_size)/(self.file_size/self.chunk_size)*100,self.percent, self.status)  
        return _info
    def refresh(self, count = 1, status = None):
        #下载中的标志状态 
        self.count += count  
        self.status = status or self.run_status  
        end_str = "\r"  
        #下载完成的状态
        if self.count >= self.file_size:  
            end_str = '\n'  
            self.status = self.finish_status  
        print(self.__get_info(), end=end_str, )
def downloader(url):
    filename = url.split('/')[-1]
    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            #print('file_size:%0.2f KB' % (content_size / chunk_size/chunk_size))
            progress = ProgressBar("%s" % filename, file_size = content_size , chunk_size = chunk_size)  
            with open(downloader_path+filename, "wb") as file:  
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))  
        else:
            print('url error')
if __name__ == '__main__':
	#url = "http://aqiniu.tangdou.com/8C5C5A6CE173C9B89C33DC5901307461-20.mp4"
    url = input("输入有效的url:\n")
    downloader(url)
  
    