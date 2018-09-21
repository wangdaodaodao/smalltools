import os
import shutil
import re

def move():
    dirs = '/Volumes/My Sata/音乐/Music/music'

    for x, y, z in os.walk(dirs):
        for zz in z:
            if 'mp3' in zz:
                old_file_dir = x + '/{}'.format(zz)
                new_file_dir =  '/Volumes/My Sata/音乐/Music/{}'.format(zz)

                print('{}---->{}'.format(old_file_dir,new_file_dir ))
                if not os.path.exists(new_file_dir):
                    shutil.move(old_file_dir, new_file_dir)
                    print('done')
                else:
                    print('exist!')

#过滤指定字符
def rename():
    dirs = '/Volumes/My Sata/音乐/Music'
    for x, y, z in os.walk(dirs):
        for zz in z:
            old_file_dir = x + '/{}'.format(zz)

            xx = ''.join(zz.split(' ')[1:])
            
            print(xx)
            new_file_dir = x + '/{}'.format(xx)
            if not os.path.exists(new_file_dir):
                shutil.move(old_file_dir, new_file_dir)

 


            #用filter函数过滤方法
            # xx = filter(zz.isdigit, zz)
            # print(zz)
            #用repalce方法过滤
            """
            (1）过滤出字母的正则表达式
                [^(A-Za-z)]
            （2） 过滤出 数字 的正则表达式
            [^(0-9)]
            （3） 过滤出 中文 的正则表达式
                [^(\\u4e00-\\u9fa5)]
            （4） 过滤出字母、数字和中文的正则表达式
                [^(a-zA-Z0-9\\u4e00-\\u9fa5)]
            """
            #用re过滤
            # pattern  = '[(a-zA-Z0-9)]'
            # txt = re.sub(pattern, '', zz)
            # print(txt)



rename()
