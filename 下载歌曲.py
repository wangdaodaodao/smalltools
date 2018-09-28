# -*- coding:utf-8 -*-
# 项目地址:https://github.com/Jack-Cherish/python-spider/blob/master/Netease/Netease.py

import base64
import binascii
import hashlib
import json
import os
import re
import sys

import click
import requests
from Crypto.Cipher import AES
from http import cookiejar


class Encrypyed():
    """
    解密算法
    """

    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pub_key = '010001'

    def encrypted_request(self, text):
        text = json.dumps(text)
        sec_key = self.create_secret_key(16)
        enc_text = self.aes_encrypt(self.aes_encrypt(
            text, self.nonce), sec_key.decode('utf-8'))
        enc_sec_key = self.rsa_encrpt(sec_key, self.pub_key, self.modulus)
        data = {
            'params': enc_text, 'encSecKey': enc_sec_key
        }
        return data

    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16),
                 int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def aes_encrypt(self, text, secKey):
        # pad 为要不起16倍数的,
        pad = 16 - len(text) % 16
        # chr() 用一个范围在 range（256）内的（就是0～255）整数作参数，返回一个对应的字符。
        text = text + chr(pad) * pad
        #
        encryptor = AES.new(secKey.encode('utf-8'),
                            AES.MODE_CBC, b'0102030405060708')
        ciphertext = encryptor.encrypt(text.encode('utf-8'))
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    # 随机产生一个字符串,然后进行十六进制转换
    def create_secret_key(self, size):
        return binascii.hexlify(os.urandom(size))[:16]


class Song():
    """
    歌曲对象,用于储存歌曲的信息
    """

    def __init__(self, song_id, song_name, song_num, song_url=None):
        self.song_id = song_id
        self.song_name = song_name
        self.song_num = song_num
        self.song_url = '' if song_url is None else song_url


class Crawler():
    """
    网易云爬取API
    """

    def __init__(self, timeout=60, cookie_path='.'):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

        self.session = requests.Session()

        self.session.headers.update(self.headers)
        self.session.cookies = cookiejar.LWPCookieJar(cookie_path)
        self.download_session = requests.Session()
        self.timeout = timeout
        self.ep = Encrypyed()

    def post_request(self, url, params):
        """
        post 请求
        """
        data = self.ep.encrypted_request(params)
        print(url)
        resp = self.session.post(url, data=data, timeout=self.timeout)
        result = resp.json()
        if result['code'] != 200:
            click.echo('post error')
        else:
            return result
        print(result)
    def search(self, search_content, search_type, limit=9):
        """
        搜索api
        """
        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        params = {
            's': search_content,
            'type': search_type,
            'offset': 0,
            'sub': 'false',
            'limit': limit
        }
        result = self.post_request(url, params)
        return result

    def search_song(self, song_name, song_num, quiet=True, limit=9):
        """
        根据 音乐名搜索
        """
        result = self.search(song_name, search_type=1, limit=limit)
        if result['result']['songCount'] <= 0:
            click.echo('歌曲不存在!')
        else:
            song = result['result']['songs']
            if quiet:
                song_id, song_name = song[0]['id'], song[0]['name']
                song = Song(song_id=song_id, song_name=song_name,
                            song_num=song_num)
                return song

    def get_song_url(self, song_id, bit_rate=320000):
        """
        通过id获取歌曲地址
        """
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        csrf = ''
        params = {
            'ids': [song_id],
            'br': bit_rate,
            'csrf_token': csrf
        }
        result = self.post_request(url, params)
        print(result)
        song_url = result['data'][0]['url']
        if song_url is None:
            click.echo('歌曲不存在!')
        else:
            return song_url

    def get_song_by_url(self, url, song_name, song_num, folder):
        """
        下载歌曲到本地
        """
        if not os.path.exists(folder):
            os.mkdir(folder)
        fpath = os.path.join(
            folder, '{}-{}.mp3'.format(str(song_num), song_name))

        # 判断文件名中,是否有特殊字符
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            validname = re.sub(r'[<>:/\\|?*]', '', song_name)
            if validname != song_name:
                fpath = os.path.join(
                    floder, '{}-{}.mp3'.format(str(song_num), song_name))

        # 储存文件的方法,要判断文件是否存在,在用click库下载
        if not os.path.exists(fpath):
            resp = self.download_session.get(
                url, timeout=self.timeout, stream=True)
            length = int(resp.headers.get('content-length'))
            label = '正在下载{},{}kb'.format(song_name, int(length/1024))

            with click.progressbar(length=length, label=label) as progressbar:
                with open(fpath, 'wb') as song_file:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            song_file.write(chunk)
                            progressbar.update(1024)


class Netease():
    """
    网易云下载
    """

    def __init__(self, timeout, folder, quiet, coolie_paht):
        self.crawler = Crawler(timeout, cookie_path)
        self.folder = '.' if folder is None else folder
        self.quiet = quiet

    def download_song_by_search(self, song_name, song_num):
        """
        """
    
        song = self.crawler.search_song(song_name, song_num, self.quiet)
        
        if song != None:
            self.download_song_by_id(
                song.song_id, song.song_name, song.song_num, self.folder)

    def download_song_by_id(self, song_id, song_name, song_num, folder='.'):
        """
        通过id下载歌曲
        """
        url = self.crawler.get_song_url(song_id)
        song_name = song_name.replace('/', '')
        song_name = song_name.replace('.', '')
        print(url)
        self.crawler.get_song_by_url(url, song_name, song_num, folder)





if __name__ == '__main__':
    timeout = 60
    output = 'Music'
    quiet = True
    cookie_path = 'Cookie'
    netease = Netease(timeout, output, quiet, cookie_path)
    music_list = '1.txt'
    if os.path.exists(music_list):
        with open(music_list, 'r') as f:
            music_list = list(map(lambda x : x.strip(), f.readlines()))
            for song_num, song_name in enumerate(music_list):
                netease.download_song_by_search(song_name, song_num+1)
    else:
        click.echo('列表不存在')




