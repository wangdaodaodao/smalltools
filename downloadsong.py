import base64
import json
import os
import re
from binascii import hexlify

import click
import requests
from Crypto.Cipher import AES
from scrapy.selector import Selector


class Encrypyed():
    '''
    传入歌曲的ID，加密生成'params'、'encSecKey 返回
    '''
    def __init__(self):
        self.pub_key = '010001'
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'

    def create_secret_key(self, size):
        return hexlify(os.urandom(size))[:16].decode('utf-8')

    def aes_encrypt(self, text, key):
        iv = '0102030405060708'
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        result = encryptor.encrypt(text)
        result_str = base64.b64encode(result).decode('utf-8')
        return result_str

    def rsa_encrpt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(hexlify(text.encode('utf-8')), 16),
                 int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    def work(self, text):
        text = json.dumps(text)
        i = self.create_secret_key(16)
        encText = self.aes_encrypt(text, self.nonce)
        encText = self.aes_encrypt(encText, i)
        encSecKey = self.rsa_encrpt(i, self.pub_key, self.modulus)
        data = {'params': encText, 'encSecKey': encSecKey}
        return data


class wangyiyun():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/\
                    55.0.2883.87 Safari/537.36',
            'Referer': 'http://music.163.com/',
            # # 'Cookie': '_iuqxldmzr_=32; _ntes_nnid=8d4ef0883a3\
            #     bcc9d3a2889b0bf36766a,1533782432391; _ntes_nui\
            #         d=8d4ef0883a3bcc9d3a2889b0bf36766a; __utmc\
            #         =94650624; WM_TID=GzmBlbRkRGQXeQiYuDVCf\
            #         oEatU6VSsKC; playerid=19729878; __utma=94650\
            #         624.1180067615.1533782433.1533816989.15338228\
            #         58.9; __utmz=94650624.1533822858.9.7.utmcsr=cn\
            #         .bing.com|utmccn=(referral)|utmcmd=referral|ut\
            #         mcct=/; WM_NI=S5gViyNVs14K%2BZoVerGK69gLlmtnH5N\
            #         qzyHcCUY%2BiWm2ZaHATeI1gfsEnK%2BQ1jyP%2FROz\
            #         bzDV0AyJHR4YQfBetXSRipyrYCFn%2BNdA%2FA8Mv80riS3cu\
            #         MVJi%2BAFgCpXTiHBNHE%3D; WM_NIKE=9ca17ae2e6ffcda1\
            #         70e2e6ee84b674afedfbd3cd7d98b8e1d0f554f888a4abc769\
            #         90b184badc4f89e7af8ece2af0fea7c3b92a91eba9b7ec738e8\
            #         abdd2b741e986a1b7e87a8595fadae648b0b3bc8fcb3f8eafb6\
            #         9acb69818b97ccec5dafee9682cb4b98bb87d2e66eb19ba2aca\
            #         a5bf3b6b7b1ae5a8da6ae9bc75ef49fb7abcb5af8879f87c16f\
            #         b8889db3ec7cbbae97a4c566e992aca2ae4bfc93bad9b37aab8\
            #         dfd84f8479696a7ccc44ea59dc0b9d7638c9e82a9c837e2a3;\
            #         JSESSIONID-WYYY=sHwCKYJYxz6ODfURChA471BMF%5CSVf3%5C\
            #         Tc8Qcy9h9Whj6CfMxw4YWTMV7CIx5g6rqW8OBv04YGHwwq%2B%5\
            #         CD1N61qknTP%2Fym%2BHJZ1ylSH1EabbQASc9ywIT8YvOr%2FpMg\
            #         vmm1cbr2%2Bd6ssMYXuTlpOIrKqp%5C%2FM611EhmfAfU47%5CSQ\
            #         WAs%2BYzgY%3A1533828139236'

        }
        self.main_url = 'http://music.163.com/'
        self.session = requests.Session()
        self.session.headers = self.headers
        self.ep = Encrypyed()

    def get_songurls(self, playlist):
        '''
        进入所选歌单页面，得出歌单里每首歌各自的ID 形式就是“song?id=64006"
        '''
        url = self.main_url+'playlist?id={}'.format(playlist)
        re = self.session.get(url)
        sel = Selector(text=re.text)
        songurls = sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        title = sel.xpath('//div[@class="tit"]/h2/text()').extract_first()
        return songurls, title
        # 所有歌曲组成的list
        # ['/song?id=64006', '/song?id=63959', '/song?id=25642714', '/song?
        # id=63914', '/song?id=4878122', '/song?id=63650']

    def get_songinfo(self, songurl):
        '''
        根据songid进入每首歌信息的网址，得到歌曲的信息
        return：'64006'，'陈小春-失恋王
        '''
        url = self.main_url+songurl
        re = self.session.get(url)
        sel = Selector(text=re.text)
        song_id = url.split('=')[1]
        song_name = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
        singer = '&'.join(
            sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
        songname = singer+'-'+song_name
        return str(song_id), songname

    def get_url(self, ids, br=128000):
        '''
        self.ep.work输入歌曲ID，解码后返回data，{params 'encSecKey}
        然后post，得出歌曲所在url
        '''
        text = {'ids': [ids], 'br': br, 'csrf_token': ''}
        data = self.ep.work(text)
        url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        req = self.session.post(url, data=data)
        song_url = req.json()['data'][0]['url']
        return song_url

    def download_song(self, songurl, dir_path):
        '''
        根据歌曲url，下载mp3文件
        '''
        song_id, songname = self.get_songinfo(songurl)  # 根据歌曲url得出ID、歌名
        song_url = self.get_url(song_id)  # 根据ID得到歌曲的实质URL
        # print(song_url)
        path = dir_path + songname + '.mp3'  # 文件路径
        validname = re.sub(r'[<>:/\\|?*]', '', songname)
        if validname != songname:
            path = dir_path + validname + '.mp3'
        if not os.path.exists(path):
            if song_url:
                resp = requests.get(song_url)
                length = int(resp.headers.get('content-length'))
                label = '正在下载<{}>,{:.2f}Mb'.format(songname, length/1024000)
                with click.progressbar(length=length, label=label) as progressbar:
                    with open(path, 'wb') as code:  # 下载文件
                        for chunk in resp.iter_content(chunk_size=1024):
                            if chunk:
                                code.write(chunk)
                                progressbar.update(1024)
            else:
                print('没有{}哦.'.format(songname))
        else:
            print('{}已存在'.format(songname))

    def work(self, playlist):
        songs = self.get_songurls(playlist)  # 输入歌单编号，得到歌单所有歌曲的url
        path = '/Volumes/My Sata/音乐/{}/'.format(songs[1])  # 文件路径
        # threads = []
        if not os.path.exists(path):
            os.mkdir(path)
        for songurl in songs[0]:
            # t = Thread(target=self.download_song, args=[songurl, path])
            self.download_song(songurl, path)  # 下载歌曲
            # t.start()
        #     threads.append(t)
        # for t in threads:
        #     t.join()


if __name__ == '__main__':
    d = wangyiyun()
    d.work(2489251059)
