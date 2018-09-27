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
    def __init__(self, timeout=60, cookie_path = '.'):
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
        self.seesion.headers.update(self.headers)
        self.session.cookies = cookiejar.LWPCookieJar(cookie_path)
        self.download_session = requests.Session()
        self.timeout = timeout
        self.ep = Encrypyed()

    def post_request(self, url, params):
        """
        post 请求
        """
        data = self.ep.encrypted_request(params)
        resp = self.session.post(url, data, timeout=self.timeout)
        result = resp.json()
        if result['code'] != 200:
            click.echo('post error')
        else:
            return result

    def search(self, search_content, search_type, limit=9):
        """
        搜索api
        """
        url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        params = {
            's':search_content,
            'type':search_type,
            'offset':0,
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
        if reslut['result']['songCount'] <= 0:
            click.echo('歌曲不存在!')
        else:
            songs = result['result']['songs']
            if quiet:
                song_id, song_name = song[0]['id'],song[0]['name']
                song = Song(song_id=song_id, song_name = song_name, song_num=song_num)

        
click.echo('ppp')