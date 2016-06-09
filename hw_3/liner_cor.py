#! /usr/bin/python
# -*- coding:utf-8 -*-

from PIL import Image
from fs import get_dirfile
from blindemb import get_watermark
from re import search
import matplotlib.pyplot as plt
from time import time

TITLE = "Linear Correlation"
PATH = "result/impv/"
RESULT = [[],[],[]]
SIZE = 262144
    
def detect_blind(wm_img, og_img, wr):
    N = 2
    w, h = og_img.size
    data_list = list(wm_img.getdata())
    value = reduce(lambda sm, (x, y):sm+x*y, zip(data_list, wr), 0.0)
    value /= SIZE
    return value

def linear_correlation(watermark):
    r0_list, r1_list, rn_list = [], [], []
    ebd0_list = [x for x in get_dirfile(PATH) if search(".*/0([0-9]+\.tif)", x) !=None]
    ebd1_list = [x for x in get_dirfile(PATH) if search(".*/_([0-9]+\.tif)", x) !=None]
    ebdn_list= [x for x in get_dirfile(PATH) if search(".*/N([0-9]+\.tif)", x) !=None]
    for om, ebd0, ebd1, ebdn in zip(get_dirfile("testimage/"), ebd0_list, ebd1_list, ebdn_list):
        ebd0_img = Image.open(ebd0)
        ebd1_img = Image.open(ebd1)
        ebdn_img = Image.open(ebdn)
        om_img = Image.open(om)
        r0_list.append(detect_blind(ebd0_img, om_img, watermark))
        r1_list.append(detect_blind(ebd1_img, om_img, watermark))
        rn_list.append(detect_blind(ebdn_img, om_img, watermark))
        ebd0_img.close()
        ebd1_img.close()
        ebdn_img.close()
        om_img.close()
    return r0_list, r1_list, rn_list

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

def read_from_file(fname):
    with open(fname,'r') as f:
       s = f.read().strip('\'[]')
    return map(lambda x:"{:.2f}".format(float(x)), s.split(','))

def write_to_file(vl, fname):
    with open(fname, "w+") as f:
        f.write(str(vl))

def show_result():
    watermark = get_watermark("Watermark.txt")
    st = time()
    RESULT = linear_correlation(watermark)
    et = time()

    print "Complete time %f sec" %(et - st)
#    
    write_to_file(RESULT[0], "r0.txt")
    write_to_file(RESULT[1], "r1.txt")
    write_to_file(RESULT[2], "rn.txt")
#    RESULT[0] = read_from_file("r0.txt")
#    RESULT[1] = read_from_file("r1.txt")
#    RESULT[2] = read_from_file("rn.txt")
    dv0, fq0 = count_percent(RESULT[0])
    dv1, fq1 = count_percent(RESULT[1])
    dvn, fqn = count_percent(RESULT[2])
    plt.title(TITLE)
    plt.xlabel("Dection value")
    plt.ylabel("Percentage of images")
    max1 = max(fq0)
    max2 = max(fq1)
    max3 = max(fqn)
    m = max(max1, max2, max3)
    plt.ylim(1, m)
    plt.plot(dv0, fq0, 'r-', dvn, fqn, 'g-', dv1, fq1, 'b-')
    plt.show()
if __name__ == '__main__':
    show_result()
