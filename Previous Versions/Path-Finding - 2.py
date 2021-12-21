#!/usr/bin/env python
import pygame as pg
from pygame import gfxdraw
from math import sqrt,floor
from random import randrange
pg.init()
win = pg.display.set_mode((1000,600))
pg.display.set_caption('Path Finding')


font = pg.font.Font('Quicksand-VariableFont_wght.ttf',30)
def text(string,x,y):
    global font
    text = font.render(string,True,(32,32,32))
    win.blit(text,(x,y))

start = None
end = None
startx = None
starty = None
endx = None
endy = None
placedWall = False
wallsx = []
wallsy = []
path = []
foundDest = False


initiate = False
opened = []
closed = []
done = []
def distance(x1,y1,x2,y2):
    return abs(x1-x2)**2+abs(y1-y2)**2

class Node:
    def __init__(self,parent,x,y):
        self.parent = parent
        self.x = x
        self.y = y
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0
        self.close = False
        self.open = False
        self.anicount = 0


class Button:
    def __init__(self,x,y,width,height,col1,col2,label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.col1 = col1
        self.col2 = col2
        self.label = label
    def draw(self):
        pg.draw.rect(win,self.col1,(self.x,self.y,self.width,self.height))
        text(self.label,self.x,self.y)


down = False
def grid():
    #Along X-Axis  
    for i in range(50):
        #Along Y-Axis       
        for j in range(30):
            if j == 0 or j == 1:
                pg.draw.rect(win,(255,255,51),(i*20,j*20,20,20))
            else:
                pg.draw.rect(win,(255,255,255),(i*20,j*20,19,19))
def round20(n):
    f = float(n)/20 - n//20
    return int(n - f*20) + 40

def circle(surface, x, y, r, color):
    #gfxdraw.aacircle(surface, x, y, r, color)
    gfxdraw.filled_circle(surface, x, y, r, color)
    
def nodeIn(node,listOfNodes):
    found = False
    for i in listOfNodes:
        if i.x == node.x and i.y == node.y:
            found = True
    if found == False:
        return False
    else:
        return True
def surroundWall(node):
    conditions = 0
    if (node.x+20,node.y) in zip(wallsx,wallsy) and (node.x,node.y-20) in zip(wallsx,wallsy) :
        conditions += 1
    if (node.x-20,node.y) in zip(wallsx,wallsy) and (node.x,node.y-20) in zip(wallsx,wallsy) :
        conditions += 1
    if (node.x-20,node.y) in zip(wallsx,wallsy) and (node.x,node.y+20) in zip(wallsx,wallsy) :
        conditions += 1
    if (node.x+20,node.y) in zip(wallsx,wallsy) and (node.x,node.y+20) in zip(wallsx,wallsy) :
        conditions += 1
    if conditions > 0:
        return True
    else:
        return False
    
'''colourcount = 0
colours = [(0,255,128),(51,255,153),(102,255,178),(102,255,255),(51,255,255),(0,255,255)
           ,(102,178,255),(51,153,255),(0,128,255)]
colours = colours[::-1]'''
coltime = 0
col = [0,102,255]
pathcount = 0
pathtimer = 0
toDraw = []
testBut = Button(300,300,50,30,(255,255,51),(255,255,255),'Radhe!')
run = True
while run:
    win.fill((160,160,160))
    grid()
    '''if colourcount == 44:
        colourcount = 0
    elif colourcount%5 != 0:
        colour = colours[colourcount//5]
    colourcount += 1'''
    coltime += 1
    if coltime%3 == 0:
        if col[1] != 255:
            col[1] += 1
        elif col[1] == 255 and col[2] != 128:
            col[2] -= 1
    if path != [] and pathtimer != len(path) -1:
        pathtimer += 1
    if start == None:
            text("Choose A Starting Point",350,2)
    elif end == None:
            text("Choose A Ending Point",350,2)
            
    if type(start) == Node:
        if start.anicount != 19:
            start.anicount += 1
        pg.draw.rect(win,(153,255,51),(startx,starty,start.anicount,start.anicount))
    if type(end) == Node:
        if end.anicount != 19:
            end.anicount += 1
        pg.draw.rect(win,(255,51,51),(endx,endy,end.anicount,end.anicount))
    if placedWall == True:
        for i in range(len(wallsx)):
            pg.draw.rect(win,(0,25,51),(wallsx[i],wallsy[i],20,20))
        if initiate == False:
            text("Create Walls And Press The Down Arrow Key To Start",150,2)
        else:
            text("",-600,-600)

    if opened != []:        
        for i in opened:
            if i.anicount != 19:
                i.anicount += 1
            pg.draw.rect(win,tuple(col),(i.x,i.y,i.anicount,i.anicount))
    for i in closed:
        if (i.x,i.y) != (start.x,start.y):
            if i.anicount != 19:
                i.anicount += 1
            pg.draw.rect(win,tuple(col),(i.x,i.y,i.anicount,i.anicount))            
    

    if path != []:
        toDraw.append(pathtimer)
    for i in toDraw:
        pg.draw.rect(win,(153,51,255),(path[i][0],path[i][1],19,19))
    

    #pg.draw.rect(win,(0,102,204),(32,32,32,32))
    pg.display.update()
    count = 0
    if initiate:
        if start.open == False:
            opened.append(start)
            start.open = True
        #print(len(opened))
        if opened != []:
            current = opened[0]
            #current is the node with the least fcost
            for i in opened:
                if i.fcost < current.fcost:
                        current = i
            opened.remove(current)
            closed.append(current)
            current.close = True
            #print('Reached till',(current.x,current.y))
            if current.x == end.x and current.y == end.y:
                while current is not None:
                    path.append((current.x,current.y))
                    current = current.parent
                foundDest = True
                initiate = False
                pathcount = len(path)
            if foundDest == False:   
                successors = [Node(current,current.x+20,current.y),Node(current,current.x-20,current.y),Node(current,current.x,current.y+20),Node(current,current.x,current.y-20),
                              Node(current,current.x+20,current.y+20),Node(current,current.x-20,current.y-20),Node(current,current.x+20,current.y-20),Node(current,current.x-20,current.y+20)]
                for node in successors:
                    if 0<=node.x<1000 and 40<=node.y<600 and (node.x,node.y) not in zip(wallsx,wallsy) and surroundWall(node) == False:
                        if nodeIn(node,closed):
                            continue
                        node.gcost = current.gcost + 1
                        node.hcost = distance(endx,endy,node.x,node.y)
                        #node.hcost = 0
                        node.fcost = node.gcost + node.hcost
                        found = False
                        for open_node in range(len(opened)):
                            if opened[open_node].x == node.x and opened[open_node].y == node.y:
                                if node.gcost < opened[open_node].gcost:
                                    opened[open_node] = node
                                    node.open = True
                                found = True
                  
                        if found == False:
                            opened.append(node)
                            node.open = True
            #pg.time.wait(10)
                            
        if foundDest == False and opened == []:
            print('Not Found!')
            initiate = False


    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        #To check if the mouse is held down
        if pg.mouse.get_pressed()[0] and placedWall == True and down == True and initiate == False:
            mousex,mousey = pg.mouse.get_pos()
            mousey -= 40 
            mousex = round20(mousex) - 40
            mousey = round20(mousey)
            if (mousex,mousey) not in zip(wallsx,wallsy) and (mousex,mousey) != (start.x,start.y) and (mousex,mousey) != (end.x,end.y):
                if mousey >= 40:
                    wallsx.append(mousex)
                    wallsy.append(mousey)
        if pg.mouse.get_pressed()[2]:
            mousex,mousey = pg.mouse.get_pos()
            mousey -= 40 
            mousex = round20(mousex) - 40
            mousey = round20(mousey)
            if (mousex,mousey) in zip(wallsx,wallsy):
                wallsx.remove(mousex)
                wallsy.remove(mousey)       
        
        if event.type == pg.MOUSEBUTTONDOWN:
            down = True
            mousex,mousey = pg.mouse.get_pos()
            mousey -= 40 #To adjust for the top border
            mousex = round20(mousex) - 40
            mousey = round20(mousey)

            if start == None:
                startx = mousex
                starty = mousey
                start = Node(None,startx,starty)
            elif end == None:
                endx = mousex
                endy = mousey
                end = Node(None,endx,endy)
                placedWall = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                if type(start) == Node and type(end) == Node and down == True:
                    initiate = True

pg.quit()
       
