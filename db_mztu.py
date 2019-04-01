
from download import *
import os

headers['Referer'] = 'https://www.mzitu.com/xinggan/'
page_num = 1

if not os.path.exists('mztu'):
    os.mkdir('mztu')
os.chdir(os.getcwd() + os.sep + 'mztu')

while True:
    url = 'https://i.meizitu.net/2019/03/11a{page}.jpg'   
    if page_num < 10:
        url = url.format(page='0{}'.format(page_num))
    else:
        url = url.format(page=page_num)
    # url = url.format(page='0{}'.format(page_num)) if page_num < 10 else url.format(page=page_num)
    page_num += 1

    echo(url)
    # 增加本地文件大小判断，来结束循环,不用第二次访问网页来判断是否存在图片，
    file_name = os.getcwd() + os.sep + url.split('/')[-1]
    
    if os.path.getsize(file_name) < 1000:
        os.remove(file_name)
        break
