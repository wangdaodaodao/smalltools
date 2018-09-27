#-*- coding:utf-8 -*-
#项目地址:https://github.com/Jack-Cherish/python-spider/blob/master/Netease/Netease.py

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
		text = json.dums(text)
		sec_key = self.create_secret_key(16)
		enc_text = self.aes_encrypt(self.aes_encrypt)






	def rsa_encrpt(self, text, pubKey, modulus):
		text = text[::-1]
		rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
		return format(rs, 'x').zfill(256)

	def aes_encrypt(self, text, secKey):
		#pad 为要不起16倍数的,
		pad = 16 - len(text) % 16
		#chr() 用一个范围在 range（256）内的（就是0～255）整数作参数，返回一个对应的字符。
		text = text + chr(pad) * pad
		#
		encryptor = AES.new(secKey.encode('utf-8'), AES.MODE_CBC, b'0102030405060708')
		ciphertext = encryptor.encrypt(text.encode('utf-8'))
		ciphertext = base64.b64encode(ciphertext).decode('utf-8')
		return ciphertext


	#随机产生一个字符串,然后进行十六进制转换
	def create_secret_key(self, size):
		return binascii.hexlify(os.urandom(size)) [ :16]





