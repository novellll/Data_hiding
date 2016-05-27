#!/usr/bin/python
# -*- coding:utf-8 -*-

from PIL import Image
import matplotlib.pyplot as plt
from cmath import sqrt
from fs import getallfile
from re import search

#Sample Pairs Analysis method

def sample_analyze(im):
    d = divide_img(im)
    r = d['W'] + d['Z']
    P = reduce(lambda x, y:x+y, d.values())
    b = 2 * d['X'] - P
    c = d['V']+ d['W'] - d['X']
    re1 = (-b + sqrt(pow(b, 2) - 2*r*c).real) / float(r)
    re2 = (-b - sqrt(pow(b, 2) - 2*r*c).real) / float(r)
    return max(0, min(re1, re2))

#Divide image with pairs of two pixels
def divide_img(im):
    d = {'X':0, 'W':0, 'V':0, 'Z':0}
    w, h = im.size
    for x in xrange(0, w):
        for y in xrange(0, h, 2):
            u = im.getpixel((x,y))
            v = im.getpixel((x,y+1))
            if (u < v and v % 2 == 0) or (u > v and v % 2 == 1):
                d['X'] += 1
            elif (u < v and v % 2 == 1) or (u > v and v % 2 == 0):
                if abs(u - v) == 1:
                    d['W'] += 1
                else:
                    d['V'] += 1
            elif u ==v:
                d['Z'] += 1
    return d

def analyze_all():
    y1 = []
    y2 = []
    y3 = []
    for v in getallfile("result_stm/jpeg/50/"):
        im = Image.open(v)
        y1.append(sample_analyze(im))
        im.close()
    for v in getallfile("result_stm/jpeg/25/"):
        im = Image.open(v)
        y2.append(sample_analyze(im))
        im.close()
    for v in getallfile("result/jpeg/5/"):
        im = Image.open(v)
        y3.append(sample_analyze(im))
        im.close()
    return y1,y2,y3

def show_analysis(title, y1, y2, y3):
    x1 = [i for i in xrange(len(y1))]
    x2 = [i for i in xrange(len(y2))]
    x3 = [i for i in xrange(len(y3))]
    plt.title(title)
    plt.xlabel("Detection value")
    plt.ylabel("q")
    #plt.xlim(-5, 0.6)
    plt.plot(x1, y1, 'rd', x2 , y2, 'b+', x3, y3, 'gs')
    plt.show() 

if __name__ == '__main__':
    pass
    #y1,y2,y3 = analyze_all()
    #show_analysis("STM JPEG analyze", y1,y2,y3)
    y1=y2=y3 = []
    for i in getallfile('B/'):
        print i
        im = Image.open(i)
        y1.append(sample_analyze(im))
        im.close()
    print len(y1)
    show_analysis("Normal_img", y1, y2, y3)
