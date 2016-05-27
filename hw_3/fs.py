#! /usr/bin/python 
# -*- coding:utf-8 -*-

from os import listdir

def get_dirfile(mydir):
    try:
        return [mydir+str(f) for f in listdir(mydir) if not f.startswith('.')]
    except OSError:
        return None
        
if __name__ == '__main__':
    print getallfile('test_images/')
