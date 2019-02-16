import jieba, os
import re
import requests
from bs4 import BeautifulSoup

url = 'https://news.baidu.com'


response = requests.get(url)
response.encoding = 'utf-8'
html = response.text
#print(html)

pattern = re.compile('require.resourceMap({(.*?)});')

txt = pattern.findall(html)

print(txt)