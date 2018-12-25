import os
import shutil
import re


def move(old_dir, new_dir):
    # old_dir = '/Volumes/My Sata/音乐/Music/张韶涵'
    # new_dir = '/Volumes/My Sata/音乐/Music/'

    i = 1
    for x, y, z in os.walk(old_dir):
        for zz in z:
            # print(zz)
            
            old_files_name = '{}/{}'.format(x, zz)
            new_files_name = '{}/{}-{}'.format(new_dir, i, zz)
            print('{}---->{}'.format(old_files_name, new_files_name))
            if not os.path.exists(new_files_name):
                
                shutil.move(old_files_name, new_files_name)
                print('Have Moved!')
            i += 1


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
                pattern = '[(0-9)]|-|Live|(|)|live| '
                pattern2 = '[^(\\u4e00-\\u9fa5)|()]'
                new_zz = re.sub(pattern2, '', zz.split('.mp3')[0]) + '.mp3'
                print('{}---->{}'.format(zz, new_zz))
                old_file_dir = x + '/{}'.format(zz)
                new_file_dir = x + '/{}'.format(new_zz)
                # shutil.move(old_file_dir, new_file_dir)


def chachong():
    dirs = '/Volumes/My Sata/音乐/热门中文'
    dirs2 = '/Volumes/My Sata/音乐/Jay/music'

    for x, y, z in os.walk(dirs):
        for zz in z:
            # if 'ive' in zz:
            #     new_file_dir = dirs2 + '/{}'.format(zz)
            #     old_file_dir = x + '/{}'.format(zz)
            #     if not os.path.exists(new_file_dir):
            #         shutil.move(old_file_dir, new_file_dir)
            #         print('{}----->{}'.format(old_file_dir, new_file_dir))
            print(zz)

            if '周杰伦' in zz:
                print(zz)
                new_file_dir = new_file_dir = dirs + '/1/{}'.format(zz)
                old_file_dir = x + '/{}'.format(zz)
                if not os.path.exists(new_file_dir):
                    # shutil.move(old_file_dir, new_file_dir)
                    print('{}----->{}'.format(old_file_dir, new_file_dir))
                

def got():
    dirs = dirs = '/Volumes/My Mac/user/aklex'
    for x, y, z in os.walk(dirs):
        # print(len(z))
        for zz in z:
            if 'mp3' in zz and '._' in zz:
                print('{}-------->{}'.format(x, zz))
                # if os.path.exists(zz):
                    # os.remove('{}/{}'.format(x, zz))
                    # continue
                # print(zz)


old_dir = '/Volumes/My Sata/Photography/姿势/摄影师与模特的完美摆姿教学/美姿68套图/李妍静68套美姿套图'
new_dir = '/Volumes/My Sata/Photography/姿势/摄影师与模特的完美摆姿教学/美姿68套图'

move(old_dir, new_dir)