import pygame
import random
import math
import os
import tkinter as tk
from tkinter import messagebox

pygame.init()

global current_number
current_number = 1

WIDTH = 1200
HEIGHT = 900
FPS = 60
gap = 200
max_line_length = 450
node_list = []
line_list = []
button_list = []

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (28,28,28)
RED = (255,0,0)

window = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Node Path Finder")

node_img = pygame.image.load('node.png')
font = pygame.font.Font('freesansbold.ttf', 25)
background = pygame.Rect(gap,0,WIDTH-gap,HEIGHT)


class Line(object):

    def __init__(self,start,end,startNode,endNode,colour):
        self.start = start
        self.end = end
        self.length = self.getLength()
        self.startNode = startNode
        self.endNode = endNode
        self.colour = colour

    def getLength(self):

        x1 = self.start[0]
        x2 = self.end[0]

        y1 = self.start[1]
        y2 = self.end[1]

        length = math.hypot(x2-x1, y2-y1)
        return length

    def changeColour(self,colour):
        self.colour = colour


class Node(object):

    def __init__(self,x,y,number):
        self.x = x - 50
        self.y = y - 50
        self.number = number
        self.neighbours = []
        self.length = 0               # total length from previous to end

    def addNeighbour(self,node):
        self.neighbours.append(node)

    def getLength(self,startNode,endNode):  # startnode is just the previous node not the very first node
        
        x1 = startNode.x
        x2 = self.x

        y1 = startNode.y
        y2 = self.y

        ax1 = self.x
        ax2 = endNode.x

        ay1 = self.y
        ay2 = endNode.y

        length1 = math.hypot(x2-x1, y2-y1)          #   length from startnode to this node
        length2 = math.hypot(ax2-ax1, ay2-ay1)      #   length from this node to end node
        return length1 + length2


class Button(object):

    def __init__(self, color, x,y,width,height,text,text_color):
        self.color = color
        self.text_color = text_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def Draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, self.text_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


class PriorityQueue(object):

    def __init__(self):
        self.queue = []     #   contains tuples (object , total length)
        self.paths = []     #   contains the taken paths
        self.lines = []     #   contains the lines taken

    def addItem(self,item,length):     # item will be node object
        self.queue.append((item, length))

    def clearList(self):
        self.queue = []

    def clearPath(self):
        self.paths = []

    def clearLines(self):
        self.lines = []

    def sortList(self):
        self.queue.sort(key = lambda x: x[1])       #   sort by length (element 2)
    
    def addPath(self,item):             # item is node taken
        self.paths.append(item)

    def addLine(self,line):
        self.lines.append(line)

Pqueue = PriorityQueue()

def draw_window(node_list,line_list,background,path_button):

    pygame.draw.rect(window, GREY, background)

    for line in line_list:
        pygame.draw.line(window, line.colour, line.start, line.end, 5)

    for line in line_list:
        if line.colour == RED:
            pygame.draw.line(window, line.colour, line.start, line.end, 5)

    for node in node_list:
        window.blit(node_img,(node.x , node.y))
        over_text = font.render(str(node.number), True, BLACK)
        window.blit(over_text,(node.x +43 , node.y +43))

    for button in button_list:
        button.Draw(window,WHITE)


def find_next_path(startNode , endNode):    # start node is the current node end is target node
    global line_list
    
    for node in startNode.neighbours:
        Pqueue.addItem(node, node.getLength(startNode,endNode))
    Pqueue.sortList()

    for line in line_list:
        if (line.startNode == startNode or line.startNode == Pqueue.queue[0][0]) and (line.endNode == startNode or line.endNode == Pqueue.queue[0][0]):
            Pqueue.addLine(line)
            break

    return Pqueue.queue[0][0]


def path_message():
    global line_list

    result = messagebox.askokcancel("Shortest Path Found","The shortest path was found\n")

    for item in Pqueue.paths:
            print(item.number)

    for line in line_list:
        if line in Pqueue.lines:
            line.changeColour(RED)


def no_path_message():

    result = messagebox.askokcancel("No Path Found","No path has been found\n")

def find_path():
    os.system('cls')

    for line in line_list:
        if line.colour == RED:
            line.changeColour(WHITE)

    def onCall():
        path = True
        
        for node in node_list:
            if node.number == int(start_entry.get()):
                start_node = node
            if node.number == int(end_entry.get()):
                end_node = node
        
        try:
            current_node = start_node
            Pqueue.addPath(current_node)
            while current_node != end_node:
                current_node = find_next_path(current_node,end_node)
                if current_node in Pqueue.paths:
                    path = False
                    break
                Pqueue.addPath(current_node)
                Pqueue.clearList()

            if path == True:
                path_message()
                root.destroy()
                Pqueue.clearList()
                Pqueue.clearPath()
                Pqueue.clearLines()

            elif path == False:
                no_path_message()
                root.destroy()
                Pqueue.clearList()
                Pqueue.clearPath()
                Pqueue.clearLines()
        
        except UnboundLocalError:
            result = messagebox.askokcancel("","Nodes not found\n")
            root.destroy()

    root = tk.Tk()

    start_node_label = tk.Label(root, text='Start Node: ',font=("",15))
    start_entry = tk.Entry(root,font=("",15))
    end_node_label = tk.Label(root, text='End Node: ',font=("",15))
    end_entry = tk.Entry(root,font=("",15))
    submit = tk.Button(root, text='Submit',font=("",15),command=lambda: onCall())

    submit.grid(columnspan=2, row=3)
    end_node_label.grid(row=1, pady=3)
    end_entry.grid(row=1, column=1, pady=3)
    start_entry.grid(row=0, column=1, pady=3)
    start_node_label.grid(row=0, pady=3)

    root.mainloop()

def clear_window():

    global stage
    global line_list
    global node_list
    global current_number
    line_list=[]
    node_list=[]
    stage = "placing"
    current_number = 1
    Pqueue.clearList()
    Pqueue.clearPath()
    Pqueue.clearLines()
    os.system('cls')

def random_nodes():
    global node_list
    clear_window()

    def onCall():
        global current_number
        global node_list

        number_of_nodes = int(number_entry.get())
        for i in range(number_of_nodes):                    #   generate nodes

            nodeX = random.randint(gap+50,WIDTH-50)
            nodeY = random.randint(50,HEIGHT-50)

            for node in node_list:
                if (nodeX-50 > node.x-100 and nodeX-50 < node.x+100) and (nodeY-50 > node.y-100 and nodeY-50 < node.y+100):
                    print(current_number,"to close to",node.number)

            node = Node(nodeX , nodeY , current_number)
            node_list.append(node)
            current_number += 1
            test = False

        root.destroy()

    root = tk.Tk()

    number_of_nodes_label = tk.Label(root, text='Number Of Nodes: ',font=("",15))
    number_entry = tk.Entry(root,font=("",15))
    submit = tk.Button(root, text='Submit',font=("",15),command=lambda: onCall())

    number_of_nodes_label.grid(row=0, pady=3)
    number_entry.grid(row=0,column=1,pady=3)
    submit.grid(row=1,columnspan=2)

    root.mainloop()


def make_line():
    global stage

    def onCall():
        global stage

        for node in node_list:
            if node.number == int(node1_box.get()):
                node1 = node
            if node.number == int(node2_box.get()):
                node2 = node

        try:
            line = Line((node1.x + 50 , node1.y + 50),(node2.x + 50 , node2.y + 50),node1,node2,WHITE)
            line_list.append(line)
            node1.neighbours.append(node2)
            node2.neighbours.append(node1)
            root.destroy()

        except UnboundLocalError:
            result = messagebox.askokcancel("","Nodes not found\n")
            if len(node_list) == 0:
                stage = "placing"
            root.destroy()

    stage = "lines"
    root = tk.Tk()

    node1_label = tk.Label(root, text='Node 1: ',font=("",15))
    node1_box = tk.Entry(root,font=("",15))
    node2_label = tk.Label(root, text='Node 2: ',font=("",15))
    node2_box = tk.Entry(root,font=("",15))
    submit = tk.Button(root, text='Submit',font=("",15),command=lambda: onCall())

    submit.grid(columnspan=2, row=3)
    node2_label.grid(row=1, pady=3)
    node2_box.grid(row=1, column=1, pady=3)
    node1_box.grid(row=0, column=1, pady=3)
    node1_label.grid(row=0, pady=3)

    root.mainloop()

def remove_line():

    def onCall():

        for node in node_list:
            if node.number == int(node1_box.get()):
                node1 = node
            if node.number == int(node2_box.get()):
                node2 = node

        try:
            if node2 in node1.neighbours:
                node1.neighbours.remove(node2)

            if node1 in node2.neighbours:
                node2.neighbours.remove(node1)
            
            for line in line_list:
                if (line.startNode == node1 or line.startNode == node2) and (line.endNode == node1 or line.endNode == node2):
                    line_list.remove(line)
            
            root.destroy()

        except UnboundLocalError:
            result = messagebox.askokcancel("","Nodes not found\n")
            root.destroy()

    root = tk.Tk()

    node1_label = tk.Label(root, text='Node 1: ',font=("",15))
    node1_box = tk.Entry(root,font=("",15))
    node2_label = tk.Label(root, text='Node 2: ',font=("",15))
    node2_box = tk.Entry(root,font=("",15))
    submit = tk.Button(root, text='Submit',font=("",15),command=lambda: onCall())

    submit.grid(columnspan=2, row=3)
    node2_label.grid(row=1, pady=3)
    node2_box.grid(row=1, column=1, pady=3)
    node1_box.grid(row=0, column=1, pady=3)
    node1_label.grid(row=0, pady=3)

    root.mainloop()


def main():

    global stage
    global line_list
    global node_list
    global current_number
    stage = "placing"

    running = True
    clock = pygame.time.Clock()

    path_button = Button(BLACK,10,56,180,100,"Find Path",WHITE)
    button_list.append(path_button)
    clear_button = Button(BLACK,10,228,180,100,"Clear",WHITE)
    button_list.append(clear_button)
    random_button = Button(BLACK,10,400,180,100,"Random Nodes",WHITE)
    button_list.append(random_button)
    make_button = Button(BLACK,10,572,180,100,"Make Line",WHITE)
    button_list.append(make_button)
    remove_button = Button(BLACK,10,744,180,100,"Remove Line",WHITE)
    button_list.append(remove_button)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            coordinate = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and stage == "placing":   #   create node
                if coordinate[0] >= gap+50:
                    node = Node(coordinate[0] , coordinate[1] , current_number)
                    node_list.append(node)
                    current_number += 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      #   buttons
                if path_button.isOver(coordinate):
                    find_path()

                elif clear_button.isOver(coordinate):
                    clear_window()

                elif random_button.isOver(coordinate):
                    random_nodes()

                elif make_button.isOver(coordinate):
                    make_line()

                elif remove_button.isOver(coordinate):
                    remove_line()

            if event.type == pygame.MOUSEMOTION:        #   change button colour

                for button in button_list:
                    if button.isOver(coordinate):
                        button.color = GREY
                    else:
                        button.color = BLACK


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and stage == "placing":          #   create lines
                    stage = "lines"
                    for node in node_list:
                        for item in node_list:
                            if node == item:
                                pass
                            else:
                                line = Line((node.x + 50 , node.y + 50),(item.x + 50 , item.y + 50),node,item,WHITE)
                                if line.length <= max_line_length:
                                    line_list.append(line)
                                    node.neighbours.append(item)

        draw_window(node_list,line_list,background,path_button)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
