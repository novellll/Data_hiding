#! /usr/bin/python 
# -*- coding:utf-8 -*-

from myrand import get_gauss_seq
from PIL import Image
from fs import get_dirfile
from os import sys

ALPHA = 3
SIZE = 262144
PROCESS_IMG = 1;
SAVE_PATH = "result/nm/"
#get watermark pattern line by line in txt
def get_watermark(filename):
    rmtoken = "\r\n"
    with open(filename, "r") as f:
        watermark = [int(x.strip(rmtoken)) for x in f ]
    return watermark

#blind embedding with different mode
#mode:0 no watermark mode:1 wr pass low fiiter mode:2 change ALPHA
def blind_embed(im, wm, msg, distortion, mode):
    #msg to define wm to -wr or wr
    if not msg:
        wm = map(lambda x:-x, wm);
    nim = im.copy()
    w, h = im.size
    #no embedding watermark
    if mode == 0:
        wm = [0]*SIZE
    elif mode == 1:
        wm = lowpass_filter(nim, wm)
    elif mode == 2:
        improve_effective()
    for i, wr in enumerate(wm):
        x = i // w
        y = i % w
        pixel = nim.getpixel((x,y))
        #distortion is a gauss distribution
        pixel += ALPHA * wr + distortion[i]
        nim.putpixel((x,y), pixel)
    nim.save(SAVE_PATH + im.filename.strip("testimage/"));
    return nim

def improve_effective(oimg, wm , ):
    global ALPHA
    reurn None
def lowpass_filter(im):
    return None

#embed in all images
def embed_images(wm_path):
    distortion = get_gauss_seq(1, SIZE, 0, 1.5, 5)
    watermark = get_watermark(wm_path)
    global PROCESS_IMG
    print "Start to embed with ALPHA %d" %(ALPHA)
    for img_path in get_dirfile('testimage/'):
        im = Image.open(img_path)
        blind_embed(im, watermark, 0, distortion)
        im.close()
    print "End:embed_success"
    
if __name__ == '__main__':
   embed_images("Watermark.txt");

