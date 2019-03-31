import click
import requests
import os

headers = {
    'User-Agnet': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36 QQBrowser/4.5.122.400'}


def echo(url):
    name = url.split('/')[-1]
    path = os.path.abspath('.') + os.sep + name
    if not os.path.exists(path):
        try:
            response = requests.get(url, headers=headers)
            length = int(response.headers.get('content-length'))
            label = '正在下载<{}>,共{:.2f}kb'.format(name, length/1024)
            # print(response.headers, length, response.status_code)
            with click.progressbar(length=length, label=label) as progressbar:
                with open(name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            progressbar.update(1024)
        except:
            return None

    else:
        print('<{}>已存在'.format(name))
