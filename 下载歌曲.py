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


class 