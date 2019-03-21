import json
import re
import requests
from bs4 import BeautifulSoup

url = 'https://news.baidu.com'


response = requests.get(url)
response.encoding = 'utf-8'
html = response.text
# print(html)

# 转义字符的使用，正则匹配的使用
pattern = re.compile(r'require.resourceMap((.*?));')
txt2 = pattern.findall(response.text)
print(len(txt2))

soup = BeautifulSoup(response.text, 'lxml')
txt = soup.findAll('a', attrs={'target': '_blank'})
# 按属性查找的使用

# jj = json.loads(txt2)
# print(jj.get('res'), type(jj))
for x in txt:
    # print(x)

    if '' in x.text:
        print(x.text.replace('w', ''))
