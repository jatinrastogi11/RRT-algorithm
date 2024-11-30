import pygame
import random
import math

class Map:
    def __init__(self,start,goal,obsdim,obsnum):
        self.start = start
        self.goal = goal
        
        
       
       
        self.nodeRad = 2
        self.nodeThickness = 0
        self.edgeThickness = 1
        
        self.obstacles = []
        self.obsdim = obsdim
        self.obsNumber = obsnum

        self.grey = (70,70,70)
        self.Blue = (0,0,255)
        self.Green = (0,255,0)
        self.Red = (255,0,0)
        self.White = (255,255,255)

    def drawMap(self,surface):
        pygame.draw.circle(surface,self.Green,self.start,self.nodeRad+10,0)
        pygame.draw.circle(surface,self.Green,self.goal,self.nodeRad+20,1)
        #self.drawObs(obstacles,surface)
    def drawPath(self):
        pass
    '''
    def drawObs(self,obstacles,surface):
        obstaclesList = obstacles.copy()
        while(len(obstaclesList)>0):
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(surface,self.grey,obstacle)

    '''
class Graph:
    def __init__(self,start,goal,MapDimensions,obsdim,lineobs,circleobs,rectangleobs):
        (x,y) = start
        self.start = start
        self.goal = goal
        self.lineobs = lineobs
        self.circleobs = circleobs
        self.rectangleobs = rectangleobs
        self.goalFlag = False
        self.maph,self.mapw = MapDimensions
        self.x = []
        self.y = []
        self.parent = []
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        self.obstacles = []
        self.obsDim = obsdim
        self.obsNum = len(self.lineobs) + len(self.circleobs) + len(self.rectangleobs)

        self.goalstate = None
        self.path = []

    
    '''
    def makeObs(self):
        obs = []

        for _ in range(self.obsNum):
            rectang = None
            startgoalcol = True
            while startgoalcol:
                upper = self.makeRandomRect()
                rectang = pygame.Rect(upper,(self.obsDim,self.obsDim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol = True
                else:
                    startgoalcol = False

            obs.append(rectang)

        self.obstacles = obs.copy()
        return obs
    '''

    def setstart(self,start):
        (x,y) = start
        self.start = (x,y)
        self.x[0] = x
        self.y[0] = y

    def add_node(self,n,x,y):
        self.x.insert(n, x)
        self.y.append(y)
    def remove_node(self,n):
        self.x.pop(n)
        self.y.pop(n)
    def add_edge(self,parent,child):
        self.parent.insert(child, parent)
    def remove_edge(self,n):
        self.parent.pop(n)
    
    def number_of_nodes(self):
        return len(self.x)

    def number_of_obs(self):
        return len(self.lineobs) + len(self.circleobs) + len(self.rectangleobs)
    def distance(self,n1,n2):
        (x1,y1) = (self.x[n1],self.y[n1])
        (x2,y2) = (self.x[n2],self.y[n2])
        px = (float(x1)-float(x2))**2
        py = (float(y1)-float(y2))**2
        return (px+py)**(0.5)
    def sample_envir(self):
        x = int(random.uniform(100, self.mapw))
        y = int(random.uniform(0, self.maph))
        return x,y
    
    def nearest(self,n):
        dmin = self.distance(0, n)
        nnear = 0
        for i in range(n):
            if self.distance(i, n) < dmin:
                dmin = self.distance(i, n)
                nnear = i
        return nnear
    def isFree(self):
        n = self.number_of_nodes() - 1
        (x,y) = (self.x[n],self.y[n])
        #------for rectangle-------
        rectobs = self.rectangleobs.copy()
        while len(rectobs)>0:
            rectang = rectobs.pop(0)
            if rectang.collidepoint(x,y):
                self.remove_node(n)
                return False
        #-----for line---------
        lineobs = self.lineobs.copy()
        while len(lineobs)>0:
            ((x1,y1),(x2,y2)) = lineobs.pop(0)
            m = (y2-y1)/(x2-x1)
            if float(y) == float(m*x+y1 - m*x1):
                self.remove_node(n)
                return False
        #-------for circle--------
        circleobs = self.circleobs.copy()
        while len(circleobs)>0:
            center = circleobs.pop(0)
            px = (center[0]- x)**2
            py = (center[1]-y)**2
            d = float((px+py) ** (0.5))
            if d<=10.0:
                self.remove_node(n)
                return False
        return True
    def crossObstacle(self,x1,y1,x2,y2):
        
        #----FOR RECTANGLE---------------
        rectobs = self.rectangleobs.copy()
        while len(rectobs)>0:
            rectang = rectobs.pop(0)
            for i in range(101):
                u = i/100
                x = x1*u + x2*(1-u)
                y = y1*u + y2*(1-u)
                if rectang.collidepoint(x, y):
                    return True
        #---------FOR LINE----------------
        lineobs = self.lineobs.copy()
        while len(lineobs)>0:
            ((x3,y3),(x4,y4)) = lineobs.pop(0)
            div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if div == 0:
                # Parallel
                continue

            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / div
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / div

            # Check if there is an intersection point
            if 0.0 < t and u > 0.0 and u < 1:
                return True
        #-------for circle----------------
        circleobs = self.circleobs.copy()
        while len(circleobs)>0:
            center = circleobs.pop(0)
            (p1x, p1y), (p2x, p2y), (cx, cy) = (x1,y1), (x2,y2), center
            (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
            dx, dy = (x2 - x1), (y2 - y1)
            dr = (dx ** 2 + dy ** 2)**.5
            big_d = x1 * y2 - x2 * y1
            discriminant = 10 ** 2 * dr ** 2 - big_d ** 2
            if discriminant>=0:
                return True
        
        return False

    def connect(self,n1,n2):
        (x1,y1) = (self.x[n1],self.y[n1])
        (x2,y2) = (self.x[n2],self.y[n2])
        if self.crossObstacle(x1, y1, x2, y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1, n2)
            return True
    def step(self,nnear,nrand,dmax=20):
        d = self.distance(nnear, nrand)
        if d>dmax:
            u = dmax/d
            (xnear,ynear) = (self.x[nnear],self.y[nnear])
            (xrand,yrand) = (self.x[nrand],self.y[nrand])
            px,py = (xrand-xnear,yrand-ynear)
            theta = math.atan2(py, px)
            (x,y) = (int(xnear+ dmax*math.cos(theta)),
                    int(ynear+dmax*math.sin(theta)))
            self.remove_node(nrand)
            if abs(x-self.goal[0])<dmax and abs(y-self.goal[1])<dmax:
                self.add_node(nrand, self.goal[0], self.goal[1])
                self.goalstate = nrand
                self.goalFlag = True
            else:
                self.add_node(nrand, x, y)
    def path_to_goal(self):
        if self.goalFlag:
            self.path = []
            self.path.append(self.goalstate)
            newpos = self.parent[self.goalstate]
            while newpos !=0:
                self.path.append(newpos)
                newpos = self.parent[newpos]
            self.path.append(0)
        return self.goalFlag
    def getPathCoords(self):
        pathcoords = []
        for node in self.path:
            (x,y) = (self.x[node],self.y[node])
            pathcoords.append((x,y))
        return pathcoords

    def bias(self,ngoal):
        n = self.number_of_nodes()
        self.add_node(n, ngoal[0], ngoal[1])
        nnear = self.nearest(n)
        self.step(nnear, n)
        self.connect(nnear, n)
        return self.x,self.y,self.parent

    def expand(self):
        n = self.number_of_nodes()
        x,y = self.sample_envir()
        self.add_node(n, x, y)
        if self.isFree():
            xnearest = self.nearest(n)
            self.step(xnearest, n)
            self.connect(xnearest, n)
        return self.x,self.y,self.parent

    def cost(self):
        pass
    
class Button():
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, t):
        # Render new label
        self._text = t
        self.label = pygame.font.SysFont("monospace", 15).render(t, 1, (0, 0, 0))

    def values(self):
        return (self.x, self.y, self.width, self.height)

    def draw(self, surface):
        # Draw button
        pygame.draw.rect(surface, self.color, self.values())
        # Draw label
        surface.blit(self.label, (self.x + (self.width/2 - self.label.get_width()/2), self.y+(self.height/2 - self.label.get_height()/2)))
    
    def clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False