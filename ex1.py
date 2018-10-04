import click
import requests
import os
import re

def echo():
    path = os.path.abspath('.') + os.sep + '1.mp3'
    print(path)
    response = requests.get('http://www.baidu.com/1.zip')
    length = response.headers.get('content-length')
    label = '正在下载,共{}kb'.format(length/1024)

    with click.progressbar(length=length, label=label) as progressbar:
        with open('1.txt', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progressbar.update(1024)



pattern = '[^(a-z)]'
strings = 'jw111aAO91a'
s2 = re.sub(pattern, '#', strings)
print(s2)


