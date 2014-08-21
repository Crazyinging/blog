# coding: utf-8
import os
import shutil

for i in range(2, 60):
#    s ='2014_01_%02d_tmp%d_测试%d.html'%(i, i, i) 
#    os.remove(s)
#    f = open(u'2014_01_%d_tmp%d_测试%d.html'%(i, i, i), 'w')
    shutil.copy('2014_01_01_tmp1_测试1.html', '2014_01_%02d_tmp%d_测试%d.html'%(i,i,i))
