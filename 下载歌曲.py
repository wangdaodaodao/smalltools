import re
import requests
import json
import urllib.request
import urllib.error
import os
import sys

minimumsize = 10
# print("fetching msg from %s \n" % sys.argv[0])
# url = re.sub("#/", "", sys.argv[0])

url = 'http://music.163.com/playlist?id=13454597'

r = requests.get(url)
contents = r.text
res = r'<ul class="f-hide">(.*?)</ul>'
mm = re.findall(res, contents, re.S | re.M)
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
if(mm):
    contents = mm[0]
else:
    print('Can not fetch information form URL. Please make sure the URL is right.\n')
    os._exit(0)

res = r'<li><a .*?>(.*?)</a></li>'
mm = re.findall(res, contents, re.S | re.M)
print(mm)

n = 0
for value in mm:
    url = 'http://sug.music.baidu.com/info/suggestion'
    payload = {'word': value, 'version': '2', 'from': '0'}
    print(value)

    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")
    if d is not None and 'data' not in d:
        continue
    songid = d["data"]["song"][0]["songid"]
    print("find songid: {}" .format(songid))

    url = "http://music.baidu.com/data/music/fmlink"
    payload = {'songIds': songid, 'type': 'mp3'}
    r = requests.get(url, params=payload)
    contents = r.text
    d = json.loads(contents, encoding="utf-8")

    # print(d)
    if('data' not in d) or d['data'] == '':
        continue
    songlink = d["data"]["songList"][0]["songLink"]
    print("find songlink: ")
    if(len(songlink) < 10):
        print("\tdo not have flac\n")
        continue
    print(songlink)

    songdir = "songs_dir"
    if not os.path.exists(songdir):
        os.makedirs(songdir)

    songname = d["data"]["songList"][0]["songName"]
    artistName = d["data"]["songList"][0]["artistName"]
    filename = ("{}/{}/{}-{}.flac".format
                (CURRENT_PATH, songdir, songname, artistName))
    filename2 = ("{}/{}/{}-{}.mp3".format
                (CURRENT_PATH, songdir, songname, artistName))

    f = urllib.request.urlopen(songlink)
    headers = requests.head(songlink).headers
    size = round(int(headers['Content-Length']) / (1024 ** 2), 2)
    #Download unfinished Flacs again.
    if not os.path.isfile(filename) or os.path.getsize(filename) < minimumsize: #Delete useless flacs
        print("{}.正在下载歌曲<{}>......\n".format(n, songname))    
        if size >= minimumsize:
            with open(filename, "wb") as code:
                code.write(f.read())
        else:
            with open(filename2, 'wb') as code:
                code.write(f.read())
    else:
        print("{} is already downloaded. Finding next song...\n\n".format(songname))
    n += 1


print("\n================================================================\n")
print("Download finish!\nSongs' directory is {}/songs_dir".format(os.getcwd()))
