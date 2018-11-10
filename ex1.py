import click
import requests
import os
import re

def echo():
    path = os.path.abspath('.') + os.sep + '1.mp3'
    print(path)
    url = 'https://dldir1.qq.com/invc/tt/QQBrowser_for_Mac.dmg'
    response = requests.get(url)
    length = int(response.headers.get('content-length'))
    label = '正在下载,共{}kb'.format(length/1024)
    name = url.split('/')[-1]
    print(name)
    with click.progressbar(length=length, label=label) as progressbar:
        with open(name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progressbar.update(1024)


echo()
pattern = '[^(a-z)]'
strings = 'jw111aAO91a'
s2 = re.sub(pattern, '#', strings)
print(s2)


