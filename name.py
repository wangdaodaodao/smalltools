# coding = uft-8
import os
import shutil
from download import *

dir_s = '/Volumes/My Sata/苹果越狱/IconBundles/1'
if os.path.exists(dir_s):
    for x, y, z in os.walk(dir_s):
        for zz in z:
            # print(zz)
            zz2 = zz.split('.png')[0]
            zz3 = '{}@2x.png'.format(zz2)
            old_name = '{}{}'.format('', zz)
            new_name = '{}{}'.format('', zz3)
            # shutil.move(old_name, new_name)
            print(old_name, '->', new_name)
else:
    print('不存在')

