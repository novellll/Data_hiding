#! /usr/bin/python
# -*- coding:utf-8 -*-

from random import gauss, choice, seed
from PIL import Image
from lsb import random_walk, rand_sequece
from fs import getallfile
from smpl_anlz import show_analysis, sample_analyze 
import re

def embedmsg(sed, im, perc):
    nim = im.copy()
    w,h = nim.size
    size = w * h
    msglen = int(size * perc)
    rand_list = random_walk(sed, size, size-1)
    se = rand_sequece(sed, msglen, True)
    print "Len :%d" %len(se)
    r = getGaussSeq(sed, size-1, 0, 1.5, 5)
    s = getGaussSeq(2+sed, size-1, 0, 1.5, 5)
    i = 0
    j = 0
    while i < len(se):
        while True:
            x = rand_list[i+j] / w
            y = rand_list[i+j] % w
            pixel = nim.getpixel((x, y))
            k = r[i+j] - s[i+j]
            if not parity_func(pixel + r[i+j], k):
                pixel = checkbound(pixel, r[i+j], k, se[i])
                nim.putpixel((x,y), pixel)
                j += 1
                continue
            elif parity_func(pixel + r[i+j], k) == se[i]:
                pixel = checkbound(pixel, r[i+j], k, se[i])
                nim.putpixel((x,y), pixel)
                break
            else:
                pixel = checkbound(pixel, s[i+j], k, se[i])
                nim.putpixel((x,y), pixel)
                break

        i += 1;
    print "embeded pixel:%d" %(i+j)
    fn = (re.search("[0-9]*\.(.*)", im.filename)).group(0)
    path = 'result_stm/' + im.format + '/' + str(perc) + '_' + fn 
    nim.save(path)      #profile needed to store otherwise the brightness would not same.
    return nim, path

def extractmsg(sed, im, perc):
    total = 0.0
    w,h = im.size
    size = w * h
    se = rand_sequece(sed, int(size*perc), True)
    rand_list = random_walk(sed, size, size-1)
    r = getGaussSeq(sed, size-1, 0, 1.5, 5)
    s = getGaussSeq(2+sed, size-1, 0, 1.5, 5)
    i = 0
    j = 0
    while i < len(se):
        while True:
            x = rand_list[i+j] / w
            y = rand_list[i+j] % w
            pixel = im.getpixel((x, y))
            if not parity_func(pixel, r[i+j]-s[i+j]):
                j += 1
                continue
            elif parity_func(pixel, r[i+j]-s[i+j]) == se[i]:
                total += 1
                break
            else:
                break
        i+=1
    print "Extract pixel:%d" %(i+j)
    print "Total:%d Extract Percent:%f" %(total, total/(size*perc))

def checkbound(x, v, k, m):
    c = x + v
    flag = -1
    if c > 255:
        c = 255
        flag = 0
        if k == 0:
            return c
    elif c < 0:
        c = 0
        flag = 1
        if k == 0:
            return c
    else:
        return c

    while True:
        if parity_func(c, k) == m:
            break
        else:
            if flag == 0:
                c -= 1
            else:
                c += 1
    return c

def getGaussSeq(sed,n, mean, var, bound):
    seed(sed)
    gausslist = []
    while len(gausslist) < n:
        num = round(gauss(mean, var))
        if(num <= bound and num >= -bound):
            gausslist.append(int(num))
    return gausslist

def analyzeGauss(gausslist):
    a = [0]*11
    for i in gausslist:
        a[i+5] += 1;
    return a

def parity_func(x, k):
    m = pow(-1, k)
    if k == 0:
        return 0
    interval = x // k 
    if interval % 2:
        return -m
    else:
        return m
    
if __name__ == '__main__':
    '''
    y1 = y2 = y3 = []
    for i in getallfile('test_images/jpeg/'):
        im = Image.open(i)
        fn,path = embedmsg(3, im, 0.5)
        y1.append(sample_analyze(fn))
        fn1,path1 = embedmsg(10, im, 0.25)
        y2.append(sample_analyze(fn1))
        fn2,path2 = embedmsg(1, im, 0.05)
        y3.append(sample_analyze(fn2))
        im.close()
        fn.close()
        fn1.close()
        fn2.close()
    show_analysis("STM analyze", y1, y2, y3)
    '''
    im = Image.open("StM.png")
    fn,path = embedmsg(1, im, 0.5)
    extractmsg(1, fn, 0.5)
    im.close()
    fn.close()
