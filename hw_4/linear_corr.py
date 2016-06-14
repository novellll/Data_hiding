#! /usr/bin/python
# -*- coding:utf-8 -*-

from PIL import Image
from fs import get_dirfile
from re import search
import matplotlib.pyplot as plt
from time import time
from trelixembed import get_watermark, viterbi_decode,  find_path, trellix_to_msg
from sys import argv
from math import sqrt
from random import seed, gauss

TITLE = "Trellis Code Correlation"
RESULT = {}
EMBED_MSG = [0, 255, 101, 154, 128, 127, 'N']
BLOCKSIZE = 64

def init_var(sed):
    wtv = []
    seed(sed)
    for i in EMBED_MSG:
        RESULT.update({i:list()})
    RESULT.update({"N":list()})
    print RESULT
    for i in xrange(160):
        wtv.append([round(gauss(0, 0.5)) for x in xrange(BLOCKSIZE)])
    return wtv
def normal_correlation(vm, wr):
    aveg = sum(wr)/len(wr)
    wr = map(lambda x:x-aveg, wr)
    distvm = sqrt(reduce(lambda sm,x:sm+pow(x,2), vm))
    distwr = sqrt(reduce(lambda sm,x:sm+pow(x,2), wr))
    value = reduce(lambda sm, (x, y):sm+x*y, zip(vm, wr), 0.0)
    value /= distvm * distwr 
    print value
    return value

def count_percent(values):
    values = map(lambda x:float("{:.2f}".format(float(x))), values)
    d  = {}
    dv = []
    fq = []
#get val list and count it with set and list.count
    indset = set(values)
    for v in sorted(indset):
        dv.append(v)
        fq.append(values.count(v))
    return dv, fq

def correlation(m, WTV):
    ret = []
    for path in get_dirfile("result/msg_%s/" %str(m)):
        print type(m),m
        img = Image.open(path)
        wv = viterbi_decode(img)
        pt = find_path(wv, WTV) 
        msg = trellix_to_msg(pt)
        print msg, pt,path 
        wm = get_watermark(msg, WTV)
        va = normal_correlation(wv, wm)
        ret.append(va)
        img.close()
    return ret

def show_result( wtv):
    analysis = []
    for i in EMBED_MSG:
        RESULT.update({i:correlation(i, wtv)})
    with open("result.txt", "w+") as f:
        f.write(str(RESULT))
    for v in RESULT.values():
        analysis.append(count_percent(v))
    with open("analysis.txt", "w+") as f:
        f.write(str(analysis))
    plt.title(TITLE)
    plt.xlabel("Dection value")
    plt.ylabel("Percentage of images")
#    max1 = max(fq)
#    plt.ylim(1, m)
    plt.plot(analysis[0][0], analysis[0][1], 'r-', analysis[1][0], analysis[1][1], 'm-', \
            analysis[2][0],analysis[2][1], 'p-', analysis[3][0], analysis[3][1], 'y-', \
            analysis[4][0], analysis[4][1], 'c-', analysis[5][0], analysis[5][1], 'g-', \
             analysis[6][0], analysis[6][1], 'b-')
    plt.show()
    
        
if __name__ == "__main__":
    WTV = init_var(float(argv[1]))
#    r = correlation(int(argv[2]), WTV)
#    dv, fq =count_percent(r)
    show_result(WTV)
