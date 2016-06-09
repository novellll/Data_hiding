#! /usr/bin/python 
# -*- coding:utf-8 -*-

from myrand import get_gauss_seq
from PIL import Image
from fs import get_dirfile
from os import sys
from time import time
from math import ceil
#ALPHA = 2.0 
DISTORG = 5
SIZE = 262144
HALF = 512
SAVE_PATH = "result/impv/"
MSG = ''
TAUB = 0.7 

#get watermark pattern line by line in txt
def get_watermark(filename):
    rmtoken = "\r\n"
    with open(filename, "r") as f:
        watermark = [int(x.strip(rmtoken)) for x in f ]
    return watermark

#blind embedding algorithm
def blind_embed(im, wm, distortions, msg, alpha):
    print "Alpha :%f" %alpha
    nim = im.copy()
    w, h = im.size
    alpha_list = [alpha] * SIZE
    data_list = list(nim.getdata())
    out_list = map(lambda (p, a, w, d):p+a*w+d, zip(data_list, alpha_list, wm, distortions))
    nim.putdata(out_list)
    nim.save(SAVE_PATH + msg + im.filename.strip("Project3test/"));
    return nim

# Change alpha with an tau and beta(𝜏+β) defined tauo
def improve_effective(oimg, wm_list, alpha):
    print "Using improive_effective to change ALPHA"
    alpha_list = [alpha] * SIZE
    data_list = list(oimg.getdata())
    nalpha = reduce(lambda sm, (p, w): sm + (p * w) ,zip(data_list, wm_list), 0.0)
    div = reduce(lambda di, w: di+w*w, wm_list, 0.0)
    if div != 0.0:
        return  ceil((SIZE * TAUB - nalpha) / div)
    return alpha

#filter with 111/111/111
#center average value with filter 
def lowpass_filter(wm):
    lwmlist = []
    for i in xrange(SIZE):
        lwm= 0.0
        x = i // HALF
        y = i % HALF
        sqlist = []
        for ix in xrange(x-1, x+2):
            if(ix < 0 or ix > HALF-1):
                continue
            for iy in xrange(y-1, y+2):
                if iy < 0 or iy > HALF-1:
                    continue
                index = ix * HALF + iy
                lwm += wm[index] 
        lwm /= 9 
        lwmlist.append(lwm)
    return  lwmlist

#embed in all images
#mode:0 no watermark mode:1 wr pass low fiiter mode:2 change ALPHA
#MSG: used to check embed msg B:1 0:0 N:no embed
def embed_images(wm_path, mode, msg, alpha):
    wm = get_watermark(wm_path)
    distortion = get_gauss_seq(10, SIZE, 0, 1.5, DISTORG)
    MSG = "_"
    if mode == 1:
        print "In mode 1 use low-pass filter"
        wm = lowpass_filter(wm)
    #msg to define wm to -wr or wr
    if not msg:
        MSG = "0"
        wm = map(lambda x:-x, wm);
    #no embedding watermark
    elif msg == -1:
        MSG = "N"
        wm = [0] * SIZE

    print "Start to embed with ALPHA %d \tn-range:%d - %d " %(alpha, -DISTORG, DISTORG) 
    for i, img_path in enumerate(get_dirfile('Project3test/')):
        im = Image.open(img_path)
        if mode == 2 and msg != -1:
            alpha = improve_effective(im, wm, alpha)
        blind_embed(im, wm, distortion, MSG, alpha)
        im.close()
    print "End:embed_success"
    
if __name__ == '__main__':
    st = time()
    for i in xrange(-1, 2):
        embed_images("Watermark.txt", 2, i, 1)
    print "Complete time: %f sec" %(time()-st)
