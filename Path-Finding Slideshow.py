
#importing required modules
import pygame as pg
from pygame import gfxdraw 
from tkinter import * 
from tkinter import ttk  
from tkinter.filedialog import asksaveasfile,askopenfilename
import pickle

#initializing pygame
pg.init()
#creating a pygame window
win = pg.display.set_mode((1000,650))
pg.display.set_caption('Path Finding')


#function for displaying text
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
walls = []
path = []
foundDest = False


initiate = False
opened = []
closed = []
done = []
#function for calculating heuristic
def distance(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)

#defining Node class
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
        if self.parent != None:
            self.font = pg.font.Font('Quicksand-VariableFont_wght.ttf',10)

    def showF(self):
        self.text = self.font.render(str(self.fcost),True,(32,32,32))
        win.blit(self.text,(self.x,self.y))

#defining Button class
class Button:
    def __init__(self,x,y,width,height,col1,col2,label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.col1 = col1
        self.col2 = col2
        self.colour = self.col1
        self.label = label
        self.font = pg.font.Font('Quicksand-VariableFont_wght.ttf',16)
    def draw(self):
        pg.draw.rect(win,self.colour,(self.x,self.y,self.width,self.height))
        text = self.font.render(self.label,True,(32,32,32))
        win.blit(text,(self.x+15,self.y+15))
    def isClicked(self):
        mx,my = pg.mouse.get_pos()
        if self.x<mx<self.x+self.width and self.y<my<self.y+self.height:
            if pg.mouse.get_pressed()[0]:
                self.colour = self.col2
                return True      
            else:
               self.colour = self.col1 
        
        


down = False
#function for drawing a grid
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

#function for drawing a circle
def circle(surface, x, y, r, color):
    gfxdraw.filled_circle(surface, x, y, r, color)
#function to check whether a node exists in a list of nodes
def nodeIn(node,listOfNodes):
    found = False
    for i in listOfNodes:
        if i.x == node.x and i.y == node.y:
            found = True
    if found == False:
        return False
    else:
        return True
#function to show save file pop up
def save():
    root = Tk() 
    root.geometry('0x0') 
    files = [('Binary Files', '*.dat')] 
    file = asksaveasfile(mode = 'wb+',filetypes = files, defaultextension = files)
    root.destroy()
    return file
#function to show open file pop up
def openf():
    root = Tk() 
    root.geometry('0x0') 
    filename = askopenfilename(initialdir = 'C:',title = 'Open Grid')
    root.destroy()
    return filename
        

        
#variables for animations
coltime = 0
col = [0,102,255]
pathcount = 0
pathtimer = 0
toDraw = []
#creating instances of button class
loadBut = Button(0,600,200,50,(0,102,204),(255,255,255),'Load Walls')
saveBut = Button(201,600,200,50,(0,102,204),(255,255,255),'Save Walls')
clearGridBut = Button(402,600,200,50,(0,102,204),(255,255,255),'Clear Grid')
aStarBut = Button(603,600,200,50,(0,102,204),(255,255,255),'A*')
dijkstraBut = Button(804,600,200,50,(0,102,204),(255,255,255),'Dijsktra')
algo = ''
nextFrame = False
run = True
while run:
    win.fill((160,160,160))
    grid()
    #code for animation
    coltime += 1
    if coltime%3 == 0:
        if col[1] != 255:
            col[1] += 1
        elif col[1] == 255 and col[2] != 128:
            col[2] -= 1
    if path != [] and pathtimer != len(path) -1:
        pathtimer += 1

    #displaying text
    if algo == '':
        text("Select A Algorithm",370,2)
    elif start == None:
            text("Choose A Starting Point",350,2)
    elif end == None:
            text("Choose A Ending Point",350,2)
    #drawing starting node       
    if type(start) == Node:
        if start.anicount != 19:
            start.anicount += 1
        pg.draw.rect(win,(153,255,51),(startx,starty,start.anicount,start.anicount))
    #drawing ending node
    if type(end) == Node:
        if end.anicount != 19:
            end.anicount += 1
        pg.draw.rect(win,(255,51,51),(endx,endy,end.anicount,end.anicount))
    #drawing walls
    if placedWall == True:
        for wall in walls:
            pg.draw.rect(win,(0,25,51),(wall.x,wall.y,20,20))
        #display text
        if initiate == False and down == True and closed == []:
            text("Create\Load Walls And Press The Down Arrow Key To Start",120,2)
        elif  initiate == False and down == True and closed != []:
            if foundDest:
                text("Destination Has Been Found",330,2)
            else:
                text("Destination Was Not Found",330,2)

    #if there are any open nodes, then draw them
    if opened != []:        
        for i in opened:
            if i.anicount != 19:
                i.anicount += 1
            pg.draw.rect(win,tuple(col),(i.x,i.y,i.anicount,i.anicount))
            i.showF()
    #drawing closed nodes
    for i in closed:
        if (i.x,i.y) != (start.x,start.y):
            if i.anicount != 19:
                i.anicount += 1 
            pg.draw.rect(win,tuple(col),(i.x,i.y,i.anicount,i.anicount))
            i.showF()
    
    #if a path has been found, draw it
    if path != []:
        toDraw.append(pathtimer)
    for i in toDraw:
        pg.draw.rect(win,(153,51,255),(path[i][0],path[i][1],19,19))

    #drawing buttons
    loadBut.draw()
    saveBut.draw()
    clearGridBut.draw()
    aStarBut.draw()
    dijkstraBut.draw()
    #if mouse is pressed
    if pg.MOUSEBUTTONDOWN:
        #check if 'Load Walls' button is clicked
        if loadBut.isClicked():
            fname = openf()
            if fname is not None or fname not in ('',' '):
                try:
                    with open(fname,'rb+') as file:
                        #open the file and load the walls
                        walls = pickle.load(file)
                        for wall in walls:
                            if wall.x == start.x and wall.y == start.y:
                                walls.remove(wall)
                            elif wall.x == end.x and wall.y == end.y:
                                walls.remove(wall)                            
                except (EOFError,FileNotFoundError) as e:
                    print(e)
        #check if 'Save Walls' button is clicked
        elif saveBut.isClicked():
            fname = save()
            if fname is not None:
                #open the file and write the walls to the file
                pickle.dump(walls,fname)
                fname.close()
        #check if 'Clear Grid' button is clicked
        #if it is then re-initialize all variables again
        elif clearGridBut.isClicked() and down:
            start = None
            end = None
            startx = None
            starty = None
            endx = None
            endy = None
            placedWall = False
            walls = []
            path = []
            foundDest = False
            initiate = False
            opened = []
            closed = []
            coltime = 0
            col = [0,102,255]
            pathcount = 0
            pathtimer = 0
            toDraw = []
            algo = ''
        #check which algorithm is selected
        elif aStarBut.isClicked() and algo == '':
            algo = 'A*'
        elif dijkstraBut.isClicked() and algo == '':
            algo = 'Dijktra'

    #update window
    pg.display.update()
    count = 0
    #if the user has pressed the down arrow key, execute the algorithm each iteration of the while loop
    #the code for the algorithm has not been put inside a function so as to show the working of the algorithm
    #in real time
    if initiate:
        #check if starting node is in the opened list
        if start.open == False:
            #add the starting node to the opened list
            opened.append(start)
            start.open = True

        #check whether there are no more nodes to evaluate
        if opened != []:
            current = opened[0]
            #current is the node with the least fcost
            for i in opened:
                if i.fcost < current.fcost:
                        current = i
            #remove the current node from opened and add it to the closed
            opened.remove(current)
            closed.append(current)
            current.close = True
            #check whether the current node is the end
            if current.x == end.x and current.y == end.y:
                #getting the parent of each closed node to get construct the path
                while current is not None:
                    path.append((current.x,current.y))
                    current = current.parent
                foundDest = True
                initiate = False
                pathcount = len(path)
            #check if path has been found
            if foundDest == False:
                #generate successor of each node
                successors = [Node(current,current.x+20,current.y),Node(current,current.x-20,current.y),Node(current,current.x,current.y+20),Node(current,current.x,current.y-20)]
                #for every node
                for node in successors:
                    #check if the node is valid
                    if 0<=node.x<1000 and 40<=node.y<600 and nodeIn(node,walls) == False:
                        #if the node has already been evaluated then skip this node
                        if nodeIn(node,closed):
                            continue
                        #the distance between a parent node and a child node is 1
                        node.gcost = current.gcost + 1
                        #if the algorithm chosen by the user is A* then calculate a heuristic else don't
                        if algo == 'A*':
                            node.hcost = distance(endx,endy,node.x,node.y)
                        elif algo == 'Dijkstra':
                            node.hcost = 0
                        node.fcost = node.gcost + node.hcost
                        found = False
                        #check if there is a node better than the current node
                        #if there is then skip the current node or else add it to the opened list
                        for open_node in range(len(opened)):
                            if opened[open_node].x == node.x and opened[open_node].y == node.y:
                                if node.gcost < opened[open_node].gcost:
                                    opened[open_node] = node
                                    node.open = True
                                found = True 
                  
                        if found == False:
                            opened.append(node)
                            node.open = True
            #uncomment the line below this to slow down the program
            #pg.time.wait(10)
            nextFrame = False
        #if the end node has been reached then make sure that this code is not executed again

        elif foundDest == False and opened == []:
            print('Not Found!')
            initiate = False
    
    if nextFrame == False:
        initiate = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        #To check if the mouse is held down
        if pg.mouse.get_pressed()[0] and placedWall == True and down == True and initiate == False and closed == []:
            mousex,mousey = pg.mouse.get_pos()
            mousey -= 40 
            mousex = round20(mousex) - 40
            mousey = round20(mousey)
            if nodeIn(Node(None,mousex,mousey),walls) == False and (mousex,mousey) != (start.x,start.y) and (mousex,mousey) != (end.x,end.y):            
                if mousey >= 40 and mousey < 600:
                    walls.append(Node(None,mousex,mousey))
        if pg.mouse.get_pressed()[2]:
            mousex,mousey = pg.mouse.get_pos()
            mousey -= 40 
            mousex = round20(mousex) - 40
            mousey = round20(mousey)
            if nodeIn(Node(None,mousex,mousey),walls):
                for wall in walls:
                    if wall.x == mousex and wall.y == mousey:
                        walls.remove(wall)
            
        if event.type == pg.MOUSEBUTTONDOWN:
            down = True
            mousex,mousey = pg.mouse.get_pos()
            mousey -= 40 #To adjust for the top border
            mousex = round20(mousex) - 40
            mousey = round20(mousey)

            if 40 <= mousey < 600:
                if start == None and algo != '':
                    startx = mousex
                    starty = mousey
                    start = Node(None,startx,starty)
                elif end == None and algo != '':
                    endx = mousex
                    endy = mousey
                    end = Node(None,endx,endy)
                    placedWall = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                if type(start) == Node and type(end) == Node and down == True:
                    initiate = True
            if event.key == pg.K_RIGHT:
                if type(start) == Node and type(end) == Node and down == True:
                    nextFrame = True

pg.quit()
       
