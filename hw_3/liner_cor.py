#! /usr/bin/python
# -*- coding:utf-8 -*-

from PIL import Image
from fs import get_dirfile
from blindemb import get_watermark
import matplotlib.pyplot as plt

COUNT = 0
TITLE = "Linear Correlation"


def detect_blind(wm_img, og_img, wr):
    N = 2
    w, h = og_img.size
    value = 0.0;
    for x in xrange(w):
        for y in xrange(h):
            #detect wn and let whole image to be a vetcor to dot
            wn = wm_img.getpixel((x, y)) - og_img.getpixel((x, y))
            value += wn * wr[x*w+y] 
    value /= w*h
    return value

def linear_correlation():
    watermark = get_watermark("Watermark.txt")
    result = []
    for wm, om in zip(get_dirfile("result/nm/"), get_dirfile("testimage/")):
        wm_img = Image.open(wm)
        om_img = Image.open(om)
        result.append(detect_blind(wm_img, om_img, watermark))
        wm_img.close()
        om_img.close()
    print result
    
    return result

def count_percent(values):
    d  = {}
    dv = []
    fq = []
    for i in values:
        d[i] = values.count(i)
    for x, y in sorted(d.items()):
        dv.append(x)
        fq.append(y)
    return dv, fq

def show_result():
    with open("data.txt",'r') as f:
       s = f.read().strip('\'')
    #linear_correlation()
    #x2 = [i for i in xrange(len(y2))]
    #x3 = [i for i in xrange(len(y3))]
    x1 = map(lambda x:"{:.2f}".format(float(x)), s.split(','))
    dv, fq = count_percent(x1)
    plt.title(TITLE)
    plt.xlabel("Dection value")
    plt.ylabel("Percentage of images")
    #plt.xlim(-2.50, 2.5)
    plt.plot(dv, fq, 'b-')
    plt.show()
if __name__ == '__main__':
    show_result()
