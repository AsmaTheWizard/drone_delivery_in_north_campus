import random
import math
import pygame

class RRTMap:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        self.start = start
        self.goal = goal
        self.MapDimensions = MapDimensions
        self.Maph, self.Mapw = self.MapDimensions

        # window settings
        self.MapWindowName = 'RRT path planning'
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.Mapw, self.Maph))
        self.map.fill((255, 255, 255))
        self.nodeRad = 2
        self.nodeThickness = 0
        self.edgeThickness = 1

        self.obstacles = []
        self.obsDim = obsdim
        self.obsNumber = obsnum

        #Colors
        self.grey  = (70, 70, 70)
        self.Blue  = (0, 0, 255)
        self.Green = (0, 255, 0)
        self.Red   = (255, 0, 0)
        self.white = (255, 255, 255)



    def drawMap(self,obstacles):
        pygame.draw.circle(self.map, self.Green, self.start, self.nodeRad+5,0)
        pygame.draw.circle(self.map, self.Red, self.goal, self.nodeRad+20, 1)
        self.drawObs(obstacles)

    def drawPath(self, path):
        node_og = path[0]
        for node in path:
            pygame.draw.circle(self.map, self.Red, node, self.nodeRad+3, 0)
            pygame.draw.line(self.map, self.Red, node_og, node, 2)
            node_og = node

    def drawPathG(self, path):
        node_og = path[0]
        for node in path:
            pygame.draw.circle(self.map, self.Green, node, self.nodeRad+3, 0)
            pygame.draw.line(self.map, self.Green, node_og, node, 2)
            node_og = node


    def drawObs(self, obstacles):
        obstaclesList = obstacles.copy()
        while (len(obstaclesList)>0):
            obstacle = obstaclesList.pop(0)
            pygame.draw.rect(self.map, self.grey, obstacle)




class RRTGraph:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        (x,y) = start
        self.start = start
        self.goal = goal
        self.goalFlag = False
        self.Maph, self.Mapw = MapDimensions
        self.x = []
        self.y = []
        self.parent = []
        self.costs = []
        self.distStart = []
        self.weights = []
        
        # initialize the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)
        self.distStart.append(0)
        self.weights.append(0)
        
        # the obstacles 
        self.obstacles = [] 
        self.obsDim = obsdim
        self.obsNum = obsnum

        # path
        self.goalstate = None
        self.path = []



    def makeRandomRect(self):
        uppercornerx = int(random.uniform(0, self.Mapw-self.obsDim))
        uppercornery = int(random.uniform(0, self.Maph-self.obsDim))
        return(uppercornerx, uppercornery)

    def makeobs(self,TLy_data,TLx_data,width_data,height_data):
        obs = []
        for i in range(0,self.obsNum):
            rectang = None
            startgoalcol = True
            while startgoalcol:
                rectang = pygame.Rect(int(TLx_data[i]), int(TLy_data[i]), int(width_data[i]), int(height_data[i]))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol = True
                else:
                    startgoalcol = False
            obs.append(rectang)
        self.obstacles = obs.copy()
        return obs

    # Receives node ID and (x,y) coordinates
    # Adds a node
    def add_node(self, n, x, y):
        self.x.insert(n, x)
        self.y.append(y)

    def remove_node(self, n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self,parent,child):
        self.parent.insert(child,parent)
        self.weights.insert(child,self.distance(parent,child))
        self.mkCostfrmStrt()

    def add_edge2(self,parent,child):
        self.parent[child] = parent
        self.weights[child] = self.distance(parent,child)
        self.mkCostfrmStrt()

    def remove_edge(self, n):
        self.parent.pop(n)
        self.weights.pop(n)

    # Gives number of nodes
    # Useful for finding latest member of the tree
    def number_of_nodes(self):
        return len(self.x)

    def distance(self, n1, n2):
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        px = (float(x1) - float(x2)) ** 2
        py = (float(y1) - float(y2)) ** 2
        return (px + py) ** 0.5

    # Generate random sample from the map
    def sample_envir(self):
        x = int(random.uniform(0, self.Mapw))
        y = int(random.uniform(0, self.Maph))
        return x, y

    def nearest(self, n):
        dmin = self.distance(0, n)
        nnear = 0
        for i in range(0, n):
            if self.distance(i, n) < dmin:
                dmin = self.distance(i, n)
                nnear = i
        return nnear

    # Returns an array of nodes within the radius of a given node
    def nearestSet(self,n,radius = 70):
        nset = []
        for i in range(0,n):
            if self.distance(i,n) <= radius:
                nset.append(i)
        return nset

    # Returns an array of indices for nodes of the path within the radius of a given node
    def nearestPath(self,n,radius = 70):
        nset = []
        for i in range(0,len(self.path)):
            if self.distance(self.path[i],n) <= radius:
                nset.append(i)
        return nset
    
    def nearestPathIron(self,n):
        dmin = self.distance(self.path[0],n)
        nnear = 0
        for i in range(0,len(self.path)):
            if self.distance(self.path[i],n) < dmin:
                dmin = self.distance(self.path[i],n)
                nnear = self.path[i]
        return nnear

    # Check if most recent node is in a valid location
    def isFree(self):
        n = self.number_of_nodes()-1
        (x, y) = (self.x[n], self.y[n])
        obs = self.obstacles.copy()
        while (len(obs) > 0):
            rectang = obs.pop(0)
            if rectang.collidepoint(x, y):
                self.remove_node(n)
                return False
        return True

    def crossObstacle(self, x1, x2, y1, y2):
        obs = self.obstacles.copy()
        while (len(obs) > 0):
            rectang = obs.pop(0)
            for i in range(0, 101):
                u = i/100
                x = x1 * u + x2 * (1 - u)
                y = y1 * u + y2 * (1 - u)
                if rectang.collidepoint(x, y):
                    return True
        return False

    # Connect two given nodes
    # n1 parent, n2 child
    def connect(self,n1,n2):
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        if self.crossObstacle(x1, x2, y1, y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2)
            return True

    # We want connect functionality, but without removing the child node
    def connect2(self,n1,n2):
        (x1,y1) = (self.x[n1],self.y[n1])
        (x2,y2) = (self.x[n2],self.y[n2])

        if self.crossObstacle(x1,x2,y1,y2):
            #self.remove_node(n1)
            return False
        else:
            self.add_edge2(n1,n2)
            return True

    def step(self, nnear, nrand, dmax = 30):
        d = self.distance(nnear, nrand)
        if d > dmax:
            u = dmax/d
            (xnear, ynear) = (self.x[nnear], self.y[nnear])
            (xrand, yrand) = (self.x[nrand], self.y[nrand])
            (px, py) = (xrand-xnear, yrand-ynear)
            theta = math.atan2(py, px)
            (x, y) = (int(xnear + dmax * math.cos(theta)),
                      int(ynear + dmax * math.sin(theta)))
            self.remove_node(nrand)
            if abs(x - self.goal[0]) < dmax and abs(y - self.goal[1]) < dmax:
                self.add_node(nrand, self.goal[0], self.goal[1])
                self.goalstate = nrand
                self.goalFlag = True
            else:
                self.add_node(nrand, x, y)

    # Bias expansion of tree in direction of the goal
    def bias(self,ngoal):
        n = self.number_of_nodes()
        self.add_node(n, ngoal[0], ngoal[1])
        nnear = self.nearest(n)
        self.step(nnear,n)
        self.connect(nnear,n)
        return self.x,self.y,self.parent

    def biasStar(self,ngoal):
        n = self.number_of_nodes()
        self.add_node(n,ngoal[0],ngoal[1])
        nnear = self.nearest(n)
        self.step(nnear,n)

        inSet = self.nearestSet(n)
        outSet = self.nearestPath(n)
        inNode = []
        outNode = [] 
        if len(inSet) == 0 or len(outSet) == 0:
            self.connect(nnear,n)
        else:
            inNode,outNode = self.chooseInOut(n,inSet,outSet)
            if inNode == [] or outNode == []:
                self.connect(nnear,n)
            elif self.connect(inNode,n):
                if inNode != outNode:
                    self.connect2(n,outNode)
                    self.bldPath()
                    self.mkCost()
        return self.x,self.y,self.parent

    def expand(self):
        n = self.number_of_nodes()
        x, y = self.sample_envir()
        self.add_node(n, x, y)
        if self.isFree():
            xnearest = self.nearest(n)
            self.step(xnearest,n)
            self.connect(xnearest,n)
        return self.x,self.y,self.parent

    def expandStar(self):
        n = self.number_of_nodes()
        x,y = self.sample_envir()
        self.add_node(n,x,y)
        if self.isFree():
            xnearest = self.nearest(n)
            self.step(xnearest,n)

            inSet = self.nearestSet(n)
            outSet = self.nearestPath(n)

            inNode = []
            outNode = []
            if len(inSet) == 0 or len(outSet) == 0:
                self.connect(xnearest,n)
            else:
                inNode,outNode = self.chooseInOut(n,inSet,outSet)

                if inNode == [] or outNode == []:
                    self.connect(xnearest,n)
                elif self.connect(inNode,n):                    
                    if inNode != outNode:
                        self.connect2(n,outNode)
                        self.bldPath()
                        self.mkCost()


        return self.x,self.y,self.parent
    
    # Tries to 'iron out' existing path by only adding random nodes to the path
    def expandStarIron(self):
        n = self.number_of_nodes()
        x,y = self.sample_envir()
        self.add_node(n,x,y)
        if self.isFree():
            xnearest = self.nearestPathIron(n)
            self.step(xnearest,n)

            inSet = self.nearestSet(n)
            outSet = self.nearestPath(n)
            inNode = []
            outNode = []
            if len(inSet) == 0 or len(outSet) == 0:
                self.connect(xnearest,n)
            else:
                inNode,outNode = self.chooseInOut(n,inSet,outSet)
                if inNode == [] or outNode == []:
                    self.connect(xnearest,n)
                elif self.connect(inNode,n):                    
                    if inNode != outNode:
                        self.connect2(n,outNode)
                        self.bldPath()
                        self.mkCost()

        return self.x,self.y,self.parent

    # If goal has been found, add the parents of each node to path object
    def path_to_goal(self):
        if self.goalFlag:
            self.path = []
            self.path.append(self.goalstate)
            newpos = self.parent[self.goalstate]
            while ( newpos != 0):
                self.path.append(newpos)
                newpos = self.parent[newpos]
            self.path.append(0)
        return self.goalFlag

    def bldPath(self):
        if self.goalFlag:
            self.path = []
            self.path.append(self.goalstate)
            newpos = self.parent[self.goalstate]
            while (newpos != 0):
                self.path.append(newpos)
                newpos = self.parent[newpos]
            self.path.append(0)

    # Get coordinates of each of the nodes in the path
    def getPathCoords(self):
        pathCoords = []
        for node in self.path:
            x, y = (self.x[node], self.y[node])
            pathCoords.append((x, y))
        return pathCoords

    # Build vector for cost from start
    def mkCostfrmStrt(self):
        mkdistStart = []
        n = self.number_of_nodes()

        for indx in range(0,n):
            cntToStart = 0
            pos = indx
            while (pos != 0):
                cntToStart = cntToStart + self.weights[pos]
                pos = self.parent[pos]
            mkdistStart.append(cntToStart)

        self.distStart = mkdistStart

    # Cost from goal
    def mkCost(self):
        costs = []
        cprev = 0
        costs.append(cprev) 

        for node in self.path:

            cprev = self.weights[node] + cprev
            costs.append(cprev)

        costs.pop()
        self.costs = costs

    def chooseInOut(self, node, inSet, outSet):

        minCost = self.costs[-1]
        inNode = []
        outNode = []
        for i in range(0,len(inSet)):
            for j in range(0,len(outSet)):
                if inSet[i] != self.path[outSet[j]]:
                    costIn = self.distStart[inSet[i]]
                    costOut = self.costs[outSet[j]]
                    distIn = self.distance(inSet[i],node)
                    distOut = self.distance(self.path[outSet[j]],node)
                    Ctree = costIn + costOut + distIn + distOut

                    if Ctree < minCost:
                        minCost = Ctree
                        inNode = inSet[i]
                        outNode = self.path[outSet[j]]
        return inNode,outNode

    def getPath(self):
        print('\nPath')
        print('Length: ')
        print(len(self.path))
        #print('Values: ')
        #print(self.path)

    def getWeights(self):
        print('\nWeights')
        print('Length: ')
        print(len(self.weights))
        print('Values: ')
        print(self.weights)

    def getDistStart(self):
        self.mkCostfrmStrt()
        print('\nDistStart')
        print('Length: ')
        #print(len(self.distStart))
        #print('Values: ')
        print(self.distStart)

    def getCosts(self):
        self.mkCost()
        print('\nCosts')
        print('Length: ')
        print(len(self.costs))
        #print('Values: ')
        #print(self.costs)
        print('Last Value: ')
        print(self.costs[-1])

    def addCosts(self):
        self.mkCostfrmStrt()
        self.mkCost()
        for i in range(0,len(self.path)):
            print('Sum')
            sumCosts = self.costs[i] + self.distStart[self.path[i]]
            print(sumCosts)

    def getParent(self):
        print('\nParent')
        print('Length: ')
        print(len(self.parent))
        #print('Values: ')
        #print(self.parent)
        print('Last value: ')
        print(self.parent[-1])

    def getX(self):
        print('\nX:')
        print('Length: ')
        print(len(self.x))
        #print('Values: ')
        #print(self.x)
        print('Last value: ')
        print(self.x[-1])

    def getY(self):
        print('\nY:')
        print('Length: ')
        print(len(self.y))
        print('Values: ')
        print(self.y)