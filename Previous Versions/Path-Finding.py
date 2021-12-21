#!/usr/bin/env python
import pygame as pg
from math import sqrt,floor
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
foundDest = False


initiate = False
opened = []
closed = []
done = []
def distance(x1,y1,x2,y2):
    d = sqrt((x2-x1)**2 + (y2-y1)**2)
    return d

class Node:
    def __init__(self,parent,x,y):
        self.parent = parent
        self.x = x
        self.y = y
        self.gcost = distance(startx,starty,self.x,self.y)
        self.hcost = distance(endx,endy,self.x,self.y)
        self.fcost = self.gcost+self.hcost


down = False
def grid():
    #Along X-Axis  
    for i in range(50):
        #Along Y-Axis       
        for j in range(30):
            if j == 0 or j == 1:
                pg.draw.rect(win,(0,102,204),(i*20,j*20,20,20))
            else:
                pg.draw.rect(win,(255,255,255),(i*20,j*20,19,19))
    '''hcost = distance(endx,endy,self.x,self.y)
    fcost = gcost + hcost'''
def round20(n):
    f = float(n)/20 - n//20
    return int(n - f*20) + 40


def nodeIn(node,listOfNodes):
    found = False
    for i in listOfNodes:
        if i.x == node.x and i.y == node.y:
            found = True
    if found == False:
        return False
    else:
        return True


run = True
while run:
    win.fill((160,160,160))
    grid()

    if start == None:
            text("Choose A Starting Point",350,2)
    elif end == None:
            text("Choose A Ending Point",350,2)

    if start != None:
        pg.draw.rect(win,(153,255,51),(startx,starty,19,19))
    if end != None:
        pg.draw.rect(win,(255,51,51),(endx,endy,19,19))
    if placedWall == True:
        for i in range(len(wallsx)):
            pg.draw.rect(win,(0,25,51),(wallsx[i],wallsy[i],20,20))
        if initiate == False:
            text("Create Walls And Press The Down Arrow Key To Start",150,2)
        else:
            text("",-600,-600)

    if opened != []:        
        for i in opened:
            pg.draw.rect(win,(255,255,51),(i.x,i.y,19,19))
    for i in closed:
        if (i.x,i.y) != (start.x,start.y):
            pg.draw.rect(win,(255,128,0),(i.x,i.y,19,19)) 

    #pg.draw.rect(win,(0,102,204),(32,32,32,32))
    pg.display.update()
    count = 0
    if initiate:
        print('End is',(end.x,end.y))
        opened.append(start)
        while opened != []:
            current = opened[0]
            #current is the node with the least fcost
            for i in opened:
                if i.fcost < current.fcost:
                        current = i
            opened.remove(current)
            closed.append(current)
            print('Reached till',(current.x,current.y))
            if current.x == end.x and current.y == end.y:
                path = []
                while current is not None:
                    path.append((current.x,current.y))
                    current = current.parent
                foundDest = True
                break
                
            successors = [Node(current,current.x+20,current.y),Node(current,current.x-20,current.y),Node(current,current.x,current.y+20),Node(current,current.x,current.y-20),
                          Node(current,current.x+20,current.y+20),Node(current,current.x-20,current.y-20),Node(current,current.x+20,current.y-20),Node(current,current.x-20,current.y+20)]
            for node in successors:
                if 0<node.x<1000 and 0<node.y<560:
                    if nodeIn(node,closed):
                        continue
                    for open_node in opened:
                        if open_node == node and node.g > open_node.g:
                            continue
                    opened.append(node)
                            
        if foundDest == False:
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
            if (mousex,mousey) not in zip(wallsx,wallsy):
                wallsx.append(mousex)
                wallsy.append(mousey)
        
        if event.type == pg.MOUSEBUTTONDOWN:
            down = True
            mousex,mousey = pg.mouse.get_pos()
            mousey -= 40 #To adjust for the top border
            mousex = round20(mousex) - 40
            mousey = round20(mousey)

            if start == None:
                startx = mousex
                starty = mousey
                start = True
            elif end == None:
                endx = mousex
                endy = mousey
                end = True
                placedWall = True
            if start == True and end == True:
                start = Node(None,startx,starty)
                end = Node(None,endx,endy)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                if start != None and end != None and down == True:
                    initiate = True

pg.quit()
       
