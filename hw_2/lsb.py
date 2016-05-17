#! /usr/bin/python
# -*- coding : utf-8 -*-

from PIL import Image
from random import choice, randint, seed, sample
from fs import getallfile
from smpl_anlz import show_analysis, sample_analyze 
import re
import cv2
secret = []
def lsb_replace(sed, im, perc):
    nim = im.copy()
    w,h = im.size
    size = w * h
    se = rand_sequece(sed, int(size * perc), False)
    rand_list = random_walk(sed, w*h, int(size * perc))
    s = set(rand_list);
    for s, r in zip(se, rand_list):
        x = r / w;
        y = r % w;
        pixel = nim.getpixel((x, y))
        pixel = (pixel & 0xfe) | s
        nim.putpixel((x, y), pixel);
    fn = (re.search("[0-9]*\.(.*)", im.filename)).group(0)
    path = 'result/' + im.format + '/' + str(perc) + '_' + fn 
    nim.save(path)      #profile needed to store otherwise the brightness would not same.
    return nim, path

def random_walk(sed, im_size, msg_size):
    seed(sed+1)
    return sample(xrange(im_size), msg_size);

def rand_sequece(sed, n, nonzero):
    seed(sed)
    if nonzero:
        return [choice((-1,1)) for x in xrange(n)]
    else:
        return [choice((0,1)) for x in xrange(n)]

def extratlsb(sed, im, perc):
    w,h = im.size
    size = w * h
    se = rand_sequece(sed, int(size * perc), False)
    origin_list = random_walk(sed, size, len(se))
    sim = 0
    for s, r in zip(se, origin_list):
        x = r / w
        y = r % w
        pixel = im.getpixel((x, y))
        if pixel & 1 == s:
            sim += 1
    return sim / float(len(se))

if __name__ == "__main__":
    y1 = []
    y2 = []
    y3 = []
    
    im = Image.open("test_images/png/1.png")
    fn,path = lsb_replace(3, im, 0.5)
    print rand_sequece(1, 100, True)
    print extratlsb(3, fn, 0.5)
    y1.append(sample_analyze(fn))
    im.close()
    fn.close()
    '''
    for i in getallfile('test_images/jpeg/'):
        im = Image.open(i)
        fn = lsb_replace(3, im, 0.5)
        fn1 = lsb_replace(3, im, 0.25)
        fn2 = lsb_replace(3, im, 0.05)
        y1.append(sample_analyze(fn))
        y2.append(sample_analyze(fn1))
        y3.append(sample_analyze(fn2))
        im.close()
        fn.close()
        fn1.close()
        fn2.close()
    '''
    show_analysis("LSB_analysis", y1, y2, y3)
    
