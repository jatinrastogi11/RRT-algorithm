import pygame
from classes import Graph,Map,Button


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)
SNOW = (255,250,250)
BLUE = (50,50,255)
GREY = (70,70,70)

#------CUSTOMIZING VARIABLES------
dimensions = (1000,1000)
start = (300,300)
goal = (510,510)
obsdim = 30
obsnum = 50
menusize = (100,1000)
starting_pos = (0,0)
carryOn = True
draw_line = False
draw_circle = False
draw_rectangle = False
play = False
d1 = False
d2  =False
d3 = False
lineobs = []
circleobs = []
rectangleobs = []
start1 = False
goal1 = False
nodes = []
edges = []
path = []
#----- INITIALIZING EVERYTHING------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("RRT path planning")
map1 = pygame.display.set_mode((dimensions[0],dimensions[1]))
menuSurface = pygame.Surface(menusize)
map2 = Map(start, goal, obsdim, obsnum)
graph = Graph(start, goal, dimensions, obsdim, lineobs,circleobs,rectangleobs)
#obs = graph.makeObs()
####------BUTTONS--------

resetButton = Button(10,10, 70, 45, 'Reset', RED)
playButton = Button(10, resetButton.y+10+resetButton.height, 70, 45, 'Play', GREEN)
lineButton = Button(10, playButton.y+100+playButton.height, 70, 45, 'Line', YELLOW)
circleButton = Button(10, lineButton.y+10+lineButton.height, 70, 45, 'Circle', YELLOW)
rectButton = Button(10, circleButton.y+10+circleButton.height, 80, 45, 'Rectangle', YELLOW)
startButton = Button(10, rectButton.y+100+rectButton.height, 70, 45, 'Start', BLUE)
goalButton = Button(10, startButton.y+10+startButton.height, 70, 45, 'Goal', BLUE)


def play1():


    path = []
    iteration = int(input("Write Here The Number Of Nodes : "))
    while (iteration>0):
        if iteration%10==0:
            X,Y,Parent = graph.bias(graph.goal)
            pygame.draw.circle(map1, GREY, (X[-1],Y[-1]), map2.nodeRad+2,0)
            pygame.draw.line(map1, BLUE, (X[-1],Y[-1]), (X[Parent[-1]],Y[Parent[-1]]),map2.edgeThickness)
            nodes.append((X[-1],Y[-1]))
            edges.append(((X[-1],Y[-1]), (X[Parent[-1]],Y[Parent[-1]])))
        else:
            X,Y,Parent = graph.expand()
            pygame.draw.circle(map1, GREY, (X[-1],Y[-1]), map2.nodeRad+2,0)
            pygame.draw.line(map1, BLUE, (X[-1],Y[-1]), (X[Parent[-1]],Y[Parent[-1]]),map2.edgeThickness)
            nodes.append((X[-1],Y[-1]))
            edges.append(((X[-1],Y[-1]), (X[Parent[-1]],Y[Parent[-1]])))
        if iteration%5==0:
            pygame.display.update()
        iteration -= 1
    if graph.path_to_goal():
        path = graph.getPathCoords()
        for node in path:
            pygame.draw.circle(map1, RED, node, map2.nodeRad+3)
            print((node[0],node[1]))
        
    else:
        print("*********Path Was Not Found***********")
    
    carryOn = True
    pygame.display.update()
    return path
    #pygame.display.flip()
    #pygame.event.wait(0)  
#
def drawmenu():
    menuSurface.set_alpha(126)
    menuSurface.fill((0,0,0))
    map1.blit(menuSurface, (0, 0))
    playButton.draw(map1)
    lineButton.draw(map1)
    circleButton.draw(map1)
    resetButton.draw(map1)
    rectButton.draw(map1)
    startButton.draw(map1)
    goalButton.draw(map1)
def drawgraph():
    pass
#-------MAIN EVENT LOOP----------#
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                if resetButton.clicked(pos):
                    graph.lineobs = []
                    graph.circleobs = []
                    graph.rectangleobs = []
                    edges = []
                    path = []
                    nodes = []
                    graph.x = [graph.start[0]]
                    graph.y = [graph.start[1]]
                    graph.parent = [0]
                    #print(graph.parent)
                    start1 = False
                    goal1 = False
                    play = False
                    map2.start = (300,300)
                    map2.goal = (510,510)
                    graph.setstart(map2.start)
                    graph.goal = (510,510)
                    playButton.color = GREEN
                    playButton.text = 'Play'
                elif playButton.clicked(pos):
                    if play:
                        playButton.color = GREEN
                        playButton.text = 'Play'
                        edges = []
                        path = []
                        nodes = []
                        graph.x = [graph.start[0]]
                        graph.y = [graph.start[1]]
                        graph.parent = [0]
                        #print(graph.parent)
                        
                        
                    else:
                        
                        playButton.color = YELLOW
                        playButton.text = 'Stop'
                        #carryOn = False
                        result = False
                        while not result:
                            try:
                                path = play1()
                                result = True
                            except:
                                result = False    
                    play = not play
                    draw_line = False
                    draw_circle = False
                    draw_rectangle = False                        
                    start1 = False
                    goal1 = False
                elif lineButton.clicked(pos):
                    draw_line = True
                    draw_circle = False
                    draw_rectangle = False
                    start1 = False
                    goal1 = False
                elif circleButton.clicked(pos):
                    draw_line = False
                    draw_circle = True
                    draw_rectangle = False
                    start1 = False
                    goal1 = False
                elif rectButton.clicked(pos):
                    draw_line = False
                    draw_circle = False
                    draw_rectangle = True
                    start1 = False
                    goal1 = False
                elif startButton.clicked(pos):
                    start1 = True
                    play = False
                    draw_line = False
                    draw_circle = False
                    draw_rectangle = False                        
                    goal1 = False
                elif goalButton.clicked(pos):
                    start1 = False
                    play = False
                    draw_line = False
                    draw_circle = False
                    draw_rectangle = False                        
                    goal1 = True
                elif not play:
                    if draw_line:
                        if d1:
                            d1 = False
                            graph.lineobs.append((starting_pos,pos))
                            #print(graph.number_of_obs())     
                        else:
                            d1 = True
                            starting_pos = pos
                            #pygame.draw.line(map1,BLACK , starting_pos, pygame.mouse.get_pos(), 1)
                    if start1:
                        map2.start = pos
                        graph.setstart(pos)
                        #print(graph.x)
                        graph.start = pos
                        start1 = False
                    if goal1:
                        map2.goal = pos
                        graph.goal = pos
                        goal1 = False
                    if draw_circle:
                        graph.circleobs.append(pos)
                        draw_circle = False
                    if draw_rectangle:
                        rect = pygame.Rect(pos,(30,30)) 
                        graph.rectangleobs.append(rect)                                       
                        draw_rectangle = False
            elif event.button == 3:
                d1 = False
                d2 = False
                d3 = False                
    #map2.drawObs(obs, map1)
    map1.fill((255,255,255))
    map2.drawMap(map1)
    if d1 == True and draw_line:
        pygame.draw.line(map1,GREY , starting_pos, pygame.mouse.get_pos(), 1)
    if draw_circle:
        pygame.draw.circle(map1, GREY, pygame.mouse.get_pos(), 10) 
    if draw_rectangle:
        rect = pygame.Rect(pygame.mouse.get_pos(), (30,30))
        pygame.draw.rect(map1,GREY,rect)
    for l in graph.lineobs:
        pygame.draw.line(map1, GREY, l[0], l[1],1)
    for c in graph.circleobs:
        pygame.draw.circle(map1, GREY, c, 10)
    for r in graph.rectangleobs:
        pygame.draw.rect(map1,GREY,r)
    drawmenu()
    #pygame.draw.circle(map1, RED, pygame.mouse.get_pos(), 2)
    for n in nodes:
        pygame.draw.circle(map1, GREY, n, map2.nodeRad+2,0)
    for e in edges:
        pygame.draw.line(map1, BLUE, e[0], e[1],map2.edgeThickness)
    for node in path:
        pygame.draw.circle(map1, RED, node, map2.nodeRad+3)
    #clock.tick(60)  
    #pygame.display.flip()
    pygame.display.update()




      

pygame.quit()
