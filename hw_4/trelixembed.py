#/usr/bin/python
#-*- coding: utf-8 -*-

from random import gauss, seed
from PIL import Image
from fs import get_dirfile
from os import mkdir
from sys import argv, maxint

BLOCKSIZE = 64
DIMENSION = 64**2
WIDTH = 512
ALPHA = 1
SAVE_PATH = "result/msg_"
EMBED_MSG = [0, 255, 101, 154, 128, 127]
#Wtv = []
Wm = []

def get_state(curstate, msg):
    ret = 0;
    if curstate == 'A':
        if msg == '0':
            ret= 0;
        else: 
            ret= 1;
            curstate = 'B'
    elif curstate == 'B':
        if msg == '0':
            ret= 12
            curstate = 'C'
        else: 
            ret= 3
            curstate = 'D'
    elif curstate == 'C':
        if msg == '0':
            ret= 10
            curstate = 'E'
        else: 
            ret= 15
            curstate = 'F'
    elif curstate == 'D':
        if msg == '0':
            ret= 8
            curstate = 'G'
        else: 
            ret= 5
            curstate = 'H'
    elif curstate == 'E':
        if msg == '0':
            ret= 2
            curstate = 'A'
        else:
            ret= 9 
            curstate = 'B'
    elif curstate == 'F':
        if msg == '0':
            ret= 14
            curstate = 'C'
        else:
            ret= 13
            curstate = 'D'
    elif curstate == 'G':
        if msg == '0':
            ret= 4
            curstate = 'E'
        else: 
            ret= 11
            curstate = 'F'
    elif curstate == 'H':
        if msg == '0':
            ret= 6
            curstate = 'G'
        else: 
            ret= 7
            curstate = 'H'
    return curstate, ret

def find_prevstate(state):
    if state == 'A':
        return {'A':0,'E':2}
    elif state == 'B':
        return {'A':1, 'E':9}
    elif state == 'C':
        return {'B':12 , 'F':14}
    elif state == 'D':
        return {'B':3, 'F':13}
    elif state == 'E':
        return {'C':10 , 'G':4}
    elif state == 'F':
        return {'C':15, 'G':11}
    elif state == 'G':
        return {'D':8, 'H':6}
    elif state == 'H':
        return {'D':5, 'H':7}

def check_path(path):
    check = ""
    path = path[::-1]
    for i,state in enumerate(path):
        if state == 'A':
            if path[i+1] == 'A' or path[i+1] == 'E':
               check += '0'
            else:
                return False
        elif state == 'C':
            if path[i+1] == 'B' or path[i+1] == 'F':
               check += '0'
            else:
                return False
        elif state == 'E':
            if path[i+1] == 'C' or path[i+1] == 'G':
               check += '0'
            else:
                return False
        elif state == 'G':
            if path[i+1] == 'H' or path[i+1] == 'D':
               check += '0'
            else:
                return False
        else:
            return False
        if check == "00":
            return True

def msg_to_trellix(msg):
    msg = bin(msg)[2:].zfill(8)+ '00'
    #print msg
    symbols = []
    states = []
    state = 'A' 
    for i in msg:
        state,ret = get_state(state, i)
        states.append(state)
        symbols.append(ret)
    print states
    return symbols
def trellix_to_msg(path):
    msg = '' 
    for i, s in enumerate(path):
        if i+1 > len(path)-1:
            break;
        else:
            nextstate = path[i+1]
        if s == 'A':
            if nextstate == 'A':
                msg += '0'
            elif nextstate == 'B':
                msg += '1'
        elif s == 'B':
            if nextstate == 'C':
                msg += '0'
            elif nextstate == 'D':
                msg += '1'
        elif s == 'C':
            if nextstate == 'E':
                msg += '0'
            elif nextstate == 'F':
                msg += '1'
        elif s == 'D':
            if nextstate == 'G':
                msg += '0'
            elif nextstate == 'H':
                msg += '1'
        elif s == 'E':
            if nextstate == 'A':
                msg += '0'
            elif nextstate == 'B':
                msg += '1'
        elif s == 'F':
            if nextstate == 'C':
                msg += '0'
            elif nextstate == 'D':
                msg += '1'
        elif s == 'G':
            if nextstate == 'E':
                msg += '0'
            elif nextstate == 'F':
                msg += '1'
        elif s == 'H':
            if nextstate == 'G':
                msg += '0'
            elif nextstate == 'H':
                msg += '1'
    msg =  msg[0:8]
#    print msg
    return int(msg, 2)

def get_watermark(msg, Wtv):
    WM = []
    symbols = msg_to_trellix(msg)
    print symbols
    for vi in xrange(BLOCKSIZE):
        wm = 0.0
        for index, wi in enumerate(symbols):
            wm += Wtv[16*index+wi][vi]
        WM.append(wm)
#    print Wm
    return WM
    
def init_wmstate(sed):
    Wtv = []
    seed(sed)
    for i in xrange(160):
        Wtv.append([round(gauss(0, 0.5)) for x in xrange(BLOCKSIZE)])
    return Wtv
    
def embed_watermark(img, msg, Wtv):
    nimg = img.copy()
    WM = get_watermark(msg, Wtv)
    pixels = list(img.getdata())
    outpixels = []
    for index, v in enumerate(pixels):
        x = index % 512
        y = index // 512
        bx = x % 8
        by = y % 8
        outpixels.append(int(v + ALPHA * WM[bx*8+by]))
    nimg.putdata(outpixels)
    nimg.save(SAVE_PATH + str(msg) + "/" + img.filename.strip("testimage/"))

def viterbi_decode(w_img):
    wpixels = list(w_img.getdata())
    wv = [0.0] * BLOCKSIZE 
    for index,  wp in enumerate( wpixels):
        x = index % 512
        y = index // 512
        bx = x % 8
        by = y % 8
        wv[bx*8+by] += wp
    wv = map(lambda x: x/DIMENSION, wv)
    l = len(wv)
    aveg = sum(wv) / l
    wv = map(lambda x:(x-aveg), wv)
#    print wv
    return wv

def find_path(wv, Wtv):
    P  = {}
    Z = {} 
    path = {}
    for i in xrange(65, 73):
        ch = chr(i)
        Z.update({ch:-1000})
        path.update({ch:""})
        P.update({ch :[""]*11})
    P["A"][0] = 'A'
    Z['A'] = 0
    path['A'] = 'A'
    for l in xrange(1,11):
        record = {}
        for si in xrange(8):
            values = []
            c = chr(65+si)
            dic = dict(find_prevstate(c))
            t = {}
            for k, v in dic.items():
                if path[k] == "":
                   continue
                t.update({k:abs(reduce(lambda sm,(x,y):sm+x*y, zip(wv, Wtv[16*(l-1)+v]), 0.0))+abs(Z[k])})
#                print "*"*30
#                print c, k, v, t
#                print "*"* 30
            sortT = sorted(t.items(), lambda x,y:cmp(x[1], y[1]), reverse=True)
            if sortT: 
                tmpst, z = sortT[0]
                record.update({c:(tmpst, z)})
#        print record
        lastZ = Z.copy()
        lastP = path.copy()
#        print Z
        for i,(s, z) in record.items():
            Z[i] = z
#            print ("loc:%d\tsymbol:%s\tpresymb%s\tz:%.4f\tpreZ:%.4f   " %(l, i , s , z, lastZ[s]))
            P[i][l] = P[s][l-1] + i 
            path[i] = lastP[s] + i 
#        for k,v in record.items():
#            path[k] += k
    maxS,maxV = sorted(Z.items(), lambda x,y:cmp(x[1], y[1]), reverse=True)[0]
#    print path
#    print path[maxS]
    maxdict = {}
    for i in xrange(65, 73):
        maxdict.update({chr(i):Z[chr(i)]})
    sortZ = sorted(maxdict.items(), lambda x,y:cmp(x[1], y[1]), reverse=True)
    realpath = ''
    for k, v in sortZ:
        if check_path(P[k][10]):
            realpath += P[k][10]
            break
    print "Real Path:%s" %realpath
    return realpath

def embed_allimg(wtv):
    print "Start Embed with alpha %d" %ALPHA 
    for m in EMBED_MSG:
        try:
            mkdir("result/msg_%s" %m)
        except OSError:
            pass
        for path in get_dirfile("testimage/"):
            img = Image.open(path)
            embed_watermark(img,  int(m), wtv)
            img.close()
    print "Embed all image end."

if __name__ == "__main__":
    wtv = init_wmstate(float(argv[1]))
#    img = Image.open("testimage/1.tif")
#    embed_watermark(img, int(argv[2]), wtv)
#    cimg = Image.open("result/msg_"+argv[2] + "/1.tif")
#    wv = viterbi_decode(cimg)
#    print wv
#    path = find_path(wv, wtv)
#    print trellix_to_msg(path)
#    img.close()
#    cimg.close()
    embed_allimg(wtv)
