#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = 'dcje'

from tkinter import *
import time

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

L = [Pos(60,60), Pos(45,60), Pos(30,60)]
root = Tk()
cv = Canvas(root, width=300, height=300, background='black')

def show():
    tail = L.pop()
    cv.create_rectangle(tail.x, tail.y, tail.x+14, tail.y+14, fill='black')
    cv.create_rectangle(L[0].x, L[0].y, L[0].x+14, L[0].y+14, fill='white')
    cv.update()

def init():
    for pos in L:
        cv.create_rectangle(pos.x, pos.y, pos.x+14, pos.y+14, fill='white')
init()
cv.pack()
for x in range(10):
    L.insert(0, Pos(L[0].x,L[0].y+14))
    show()
    time.sleep(0.5)
root.mainloop()
