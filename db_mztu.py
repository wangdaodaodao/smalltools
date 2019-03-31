
from download import *
import os

headers['Referer'] = 'https://www.mzitu.com/xinggan/'

page_num = 1
if not os.path.exists('mztu'):
    os.mkdir('mztu')
os.chdir(os.getcwd() + os.sep + 'mztu')

while True:
    url = 'https://i.meizitu.net/2019/03/22b{page}.jpg'   
    if page_num < 10:
        page2 = '0{}'.format(page_num)
        url = url.format(page=page2)
    else:
        url = url.format(page=str(page_num))
    page_num += 1
    echo(url)
    # 增加本地文件大小判断，来结束循环
    name = url.split('/')[-1]
    file_name = os.getcwd() + os.sep + name
    # print(os.path.getsize(file_name))
    if os.path.getsize(file_name) < 1000:
        os.remove(file_name)
        break
