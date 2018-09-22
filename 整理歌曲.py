import os
import shutil
import re


def move():
    dirs = '/Volumes/My Sata/音乐/Music/music'
    for x, y, z in os.walk(dirs):
        for zz in z:
            if 'mp3' in zz:
                old_file_dir = x + '/{}'.format(zz)
                new_file_dir = '/Volumes/My Sata/音乐/Music/{}'.format(zz)
                print('{}---->{}'.format(old_file_dir, new_file_dir))
                if not os.path.exists(new_file_dir):
                    shutil.move(old_file_dir, new_file_dir)
                    print('Have Moved!')


# 通过俩个名字不一样,可实现文件重命名
def rename(dirs='/Volumes/My Sata/音乐/Music'):

    for x, y, z in os.walk(dirs):
        for zz in z:
            # print(zz)
            if 'mp3' in zz and '._' not in zz:
                '''
                切割字符函数
                split和join的应用
                '''
                # old_file_dir = x + '/{}'.format(zz)
                # #分割字符,再拼接
                # xx = ''.join(zz.split(' ')[1:])
                # #获得新命名
                # new_file_dir = x + '/{}'.format(xx)
                # if not os.path.exists(new_file_dir):
                #     shutil.move(old_file_dir, new_file_dir)

                '''
                -----re正则法替换字符----
                (1）过滤出字母的正则表达式
                    [^(A-Za-z)]
                （2） 过滤出 数字 的正则表达式
                [^(0-9)]
                （3） 过滤出 中文 的正则表达式
                    [^(\\u4e00-\\u9fa5)]
                （4） 过滤出字母、数字和中文的正则表达式
                    [^(a-zA-Z0-9\\u4e00-\\u9fa5)]
                '''
                pattern = '[(0-9)]'
                new_zz = re.sub(pattern, '', zz.split('.mp3')[0]) + '.mp3'
                print('{}---->{}'.format(zz, new_zz))
                old_file_dir = x + '/{}'.format(zz)
                new_file_dir = x + '/{}'.format(new_zz)
                shutil.move(old_file_dir, new_file_dir)


def chachong():
    dirs = '/Volumes/My Sata/音乐/Jay'
    dirs2 = '/Volumes/My Sata/音乐/Jay/music'

    for x, y, z in os.walk(dirs):
        for zz in z:
            if 'ive' in zz:
                new_file_dir = dirs2 + '/{}'.format(zz)
                old_file_dir = dirs + '/{}'.format(zz)
                if not os.path.exists(new_file_dir):
                    shutil.move(old_file_dir, new_file_dir)
                    print('{}----->{}'.format(old_file_dir, new_file_dir))


def move2():
    dirs = '/Volumes/My Sata/图片'
    for x, y, z in os.walk(dirs):
        for zz in z:
            if 'mp3' in zz:
                print(zz)
                old_file_dir = x + '/{}'.format(zz)
                new_file_dir = dirs + '/{}'.format(zz)
                if os.path.exists(old_file_dir):
                    print('234567654')

                    if not os.path.exists(new_file_dir):
                        print('{}----->{}'.format(old_file_dir, new_file_dir))
                        shutil.move(old_file_dir, new_file_dir)


# dirss = '/Volumes/My Sata/图片'
# rename(dirss)
