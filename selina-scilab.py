# coding:utf-8
#!/usr/bin/python3

import sys

import time
'''
import cv2
import paddlex as pdx
'''
def main(argv):
    pass


def usages(prg_name):
    print("Usage:")
    print("python  ./%s  <cmd> <params>" %prg_name)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usages(sys.argv[0])
    else:
      main(sys.argv[1:])
