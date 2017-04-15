#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = 'dcje'

from tkinter import *
import time

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

# up left down right  
uldr = {87:Pos(0,-1), 65:Pos(-1,0), 83:Pos(0,1), 68:Pos(1,0),  }
L = [Pos(60,60), Pos(45,60), Pos(30,60)]
root = Tk()
cv = Canvas(root, width=300, height=300, background='black')

# move right on start
direct = 68
def self_move(d):
    L.insert(0, Pos(L[0].x + uldr[d].x*14, L[0].y + uldr[d].y*14))
    show()

# w:87 a:65 s:83 d:68
def move(event):
    print('event.char:', event.char)
    print('event.keycode:',event.keycode)
    # move in a reverse way is forbidden
    global direct
    if 87 == event.keycode:
        direct = 83 if 83 == direct else 87
    elif 83 == event.keycode:
        direct = 87 if 87 == direct else 83
    elif 65 == event.keycode:
        direct = 68 if 68 == direct else 65
    elif 68 == event.keycode:
        direct = 65 if 65 == direct else 68
    else:
        direct
    #self_move(direct)

cv.bind('<Key>', move)
cv.focus_set()

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

while True:
    self_move(direct)
    cv.after(200)
root.mainloop()
