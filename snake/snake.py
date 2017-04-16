#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = 'dcje'

from tkinter import *
import time, random

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake(object):
    def __init__(self):
        self.BGCOLOR = 'BLACK'
        self.COLOR = 'WHITE'
        self.TEXTCOLOR = 'ORANGE'
        self.NODELEN = 20
        self.MAPWIDTH = 300
        self.MAPHEIGHT = 300
        # up:38 left:37 down:40 right:39 w:87 a:65 s:83 d:68
        self.uldr = {87:Pos(0,-1), 65:Pos(-1,0), 83:Pos(0,1), 68:Pos(1,0),
                     38:Pos(0,-1), 37:Pos(-1,0), 40:Pos(0,1), 39:Pos(1,0),  }
        root = Tk()
        root.maxsize(self.MAPWIDTH, self.MAPHEIGHT)
        root.minsize(self.MAPWIDTH, self.MAPHEIGHT)
        self.cv = Canvas(root, width=self.MAPWIDTH, height=self.MAPHEIGHT, background=self.BGCOLOR, state=DISABLED)
        self.cv.bind('<Key>', self.move)
        self.cv.focus_set()
        self.cv.pack()
        self.start()
        root.mainloop()

    def start(self):
        # 随机蛇身
        headX = random.randint(3, self.MAPWIDTH/self.NODELEN//2)*self.NODELEN
        headY = random.randint(3, self.MAPHEIGHT/self.NODELEN//2)*self.NODELEN
        self.body = [Pos(headX,headY), Pos(headX-self.NODELEN,headY), Pos(headX-self.NODELEN*2,headY)]
        # 保存没有蛇的网格，方便生成食物
        self.mapgrid = set()
        for x in range(0, self.MAPWIDTH, self.NODELEN):
            for y in range(0, self.MAPHEIGHT, self.NODELEN):
                self.mapgrid.add((x,y))
        for pos in self.body:
            self.mapgrid.remove((pos.x,pos.y))
        # move right on start
        self.direct = 68
        self.foodpos = Pos(-1,-1)
        for pos in self.body:
            self.cv.create_rectangle(pos.x, pos.y, pos.x+(self.NODELEN-1), pos.y+(self.NODELEN-1), fill=self.COLOR, outline=self.BGCOLOR)
        self.make_food()
        self.play()

    def snake_move(self, d):
        self.body.insert(0, Pos(self.body[0].x + self.uldr[d].x*self.NODELEN, self.body[0].y + self.uldr[d].y*self.NODELEN))

    def isalive(self):
        head = self.body[0]
        if (head.x,head.y) in [ (pos.x,pos.y) for pos in self.body[1:] ]:
            return False
        return head.x > 0 and head.y > 0 and head.x < self.MAPWIDTH and head.y < self.MAPHEIGHT

    def make_food(self):
        rand = random.randint(0, len(list(self.mapgrid))-1)
        self.foodpos.x, self.foodpos.y = list(self.mapgrid)[rand]
        self.cv.create_oval(self.foodpos.x, self.foodpos.y,
                    self.foodpos.x+self.NODELEN-1, self.foodpos.y+self.NODELEN-1,fill=self.COLOR)

    def move(self, event):
        # move in a reverse way is forbidden
        # press Q
        if 81 == event.keycode:
            pass
        elif 87 == event.keycode or 38 == event.keycode:
            self.direct = 83 if 83 == self.direct else 87
        elif 83 == event.keycode or 40 == event.keycode:
            self.direct = 87 if 87 == self.direct else 83
        elif 65 == event.keycode or 37 == event.keycode:
            self.direct = 68 if 68 == self.direct else 65
        elif 68 == event.keycode or 39 == event.keycode:
            self.direct = 65 if 65 == self.direct else 68
        else:
            self.direct

    def show(self):
        tail = self.body.pop()
        head = self.body[0]
        if (head.x, head.y) in self.mapgrid:
            self.mapgrid.remove((head.x,head.y))
        if head.x == self.foodpos.x and head.y == self.foodpos.y:
            self.body.append(tail)
            self.make_food()
        else:
            self.mapgrid.add((tail.x,tail.y))
            self.cv.create_rectangle(tail.x, tail.y, tail.x+(self.NODELEN-1), tail.y+(self.NODELEN-1), fill=self.BGCOLOR, outline=self.BGCOLOR)
        self.cv.create_rectangle(head.x, head.y, head.x+(self.NODELEN-1), head.y+(self.NODELEN-1), fill=self.COLOR, outline=self.BGCOLOR)
        self.cv.update()

    def play(self):
        while self.isalive():
            self.snake_move(self.direct)
            self.show()
            self.cv.after(200)
        self.gameover()

    def gameover(self):
        self.cv.unbind('<Key>')
        self.cv.bind('<Key-space>', self.restart)
        self.cv.create_text(self.MAPWIDTH//2,self.MAPWIDTH//2-self.NODELEN,text='YOU LOSE!',
                font='time 22 bold',fill=self.TEXTCOLOR, tags='text_lose')
        self.cv.create_text(self.MAPWIDTH//2,self.MAPWIDTH//2+self.NODELEN,text='Press SPACE to restart',
                font='time 14 bold', fill=self.TEXTCOLOR, tags='text_restart')
        print('lose')
        self.cv.update()
        
    def restart(self, event):
        for pos in self.body:
            self.cv.create_rectangle(pos.x, pos.y, pos.x+(self.NODELEN-1), pos.y+(self.NODELEN-1), fill=self.BGCOLOR, outline=self.BGCOLOR)
        self.cv.create_oval(self.foodpos.x, self.foodpos.y,
                    self.foodpos.x+self.NODELEN, self.foodpos.y+self.NODELEN,fill=self.BGCOLOR, outline=self.BGCOLOR)
        self.cv.delete('text_lose', 'text_restart')
        self.cv.bind('<Key>', self.move)
        self.start()

Snake()