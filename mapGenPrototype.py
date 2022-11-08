####################################################
#          mapGen prototype - square grid          #
####################################################

#libraries
import pygame
import random


#Generate a random seed for all random calculations
seed = random.randint(1000000,9999999)
random.seed(seed)

#Screen
#Values must match and be multiples of 25
SCREENWIDTH = 500
SCREENHEIGHT = 500

#Initialising pygame
pygame.init() #Initialise pygame
pygame.display.set_caption("mapGen Prototype")
screen = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])

#constants
TILEWIDTH = 25
GRASS = (103,148,54)
MOUNTAIN = (114,112,114)
RIVER = (0,0,200)
WOODS = (83,128,34)
CITY = (83, 50, 11)
ROAD = (103,70,31)

#Splits the screen into rows  and columns
NUMROWS = int(SCREENHEIGHT / TILEWIDTH)
NUMCOLS = int(SCREENWIDTH / TILEWIDTH)

#Tile class with type and positions.
class tile:
    def __init__(self, tileType, xpos, ypos):
        self.tileType = tileType
        self.xpos = xpos
        self.ypos = ypos

#Grass tiles. Green.
class grassTile(tile):
    def draw(self):
        pygame.draw.rect(screen,(GRASS),[self.xpos,self.ypos,TILEWIDTH,TILEWIDTH])

#Mountain tiles. Grey.
class mountainTile(tile):
    def draw(self):
        pygame.draw.rect(screen,(MOUNTAIN),[self.xpos,self.ypos,TILEWIDTH,TILEWIDTH])

#River tiles. Blue.
class riverTile(tile):
    def draw(self):
        pygame.draw.rect(screen,(RIVER),[self.xpos,self.ypos,TILEWIDTH,TILEWIDTH])

#Woods tile. Dark Green.
class woodsTile(tile):
    def draw(self):
        pygame.draw.rect(screen,(WOODS),[self.xpos,self.ypos,TILEWIDTH,TILEWIDTH])

#City tile. Brown.
class cityTile(tile):
    def draw(self):
        pygame.draw.rect(screen,(CITY),[self.xpos,self.ypos,TILEWIDTH,TILEWIDTH])

#Road tile. Light brown.
class roadTile(tile):
    def draw(self):
        pygame.draw.rect(screen,(ROAD),[self.xpos,self.ypos,TILEWIDTH,TILEWIDTH])

#Utilities

#Scan 4 tiles
def scan4(varMap,x,y):
    """Returns an array of the type of 4 tiles. Top left, top right, bottom left, bottom right"""
    scan = [varMap[x][y].tileType,varMap[x + 1][y].tileType, varMap[x][y + 1].tileType, varMap[x +1][y + 1].tileType]
    return scan

def scan9(varMap,x,y):
    """Returns an array of the type of 9 tiles."""

    if x == 0 and y == 0:
        scan = ["Edge","Edge","Edge",
                "Edge",varMap[x][y].tileType, varMap[x][y+1].tileType,
                "Edge",varMap[x+1][y].tileType, varMap[x+1][y+1].tileType]

    elif x == NUMCOLS-1 and y == NUMROWS-1:
        scan = [varMap[x-1][y-1].tileType,varMap[x-1][y].tileType, "Edge",
                varMap[x][y-1].tileType,varMap[x][y].tileType, "Edge",
                "Edge","Edge","Edge"]

    elif y == 0:
        scan = ["Edge",varMap[x-1][y].tileType, varMap[x-1][y+1].tileType,
                "Edge",varMap[x][y].tileType, varMap[x][y+1].tileType,
                "Edge",varMap[x+1][y].tileType, varMap[x+1][y+1].tileType]

    elif x == 0:
        scan = ["Edge","Edge","Edge",
                varMap[x][y-1].tileType,varMap[x][y].tileType, varMap[x][y+1].tileType,
                varMap[x+1][y-1].tileType,varMap[x+1][y].tileType, varMap[x+1][y+1].tileType]

    elif y == NUMROWS-1:
        scan = [varMap[x-1][y-1].tileType,varMap[x-1][y].tileType, "Edge",
                varMap[x][y-1].tileType,varMap[x][y].tileType, "Edge",
                varMap[x+1][y-1].tileType,varMap[x+1][y].tileType, "Edge"]

    elif x == NUMCOLS-1:
        scan = [varMap[x-1][y-1].tileType,varMap[x-1][y].tileType, varMap[x-1][y+1].tileType,
                varMap[x][y-1].tileType,varMap[x][y].tileType, varMap[x][y+1].tileType,
                "Edge","Edge","Edge"]

    else:
        scan = [varMap[x-1][y-1].tileType,varMap[x-1][y].tileType, varMap[x-1][y+1].tileType,
                varMap[x][y-1].tileType,varMap[x][y].tileType, varMap[x][y+1].tileType,
                varMap[x+1][y-1].tileType,varMap[x+1][y].tileType, varMap[x+1][y+1].tileType]
    
    
    return scan

def scanMap(varMap, numSq):
    """Scans the whole map and returns a 2D array of each 4 scan. Scans overlap."""
    fullScan = []

    if numSq == 4:
        
        for row in range(len(varMap) - 2):
            for col in range(len(varMap[row])-2):
                fullScan.append(scan4(varMap,row,col))

    return fullScan


def growRiver(varMap,x,y):
    """Recursive river generator"""

    #Base cases - have we gone off the map?
    if x == NUMCOLS-1:
        xpos = varMap[x][y].xpos
        ypos = varMap[x][y].ypos
        varMap[x][y] = riverTile("River",xpos,ypos)
        return varMap

    if x == 0:
        xpos = varMap[x][y].xpos
        ypos = varMap[x][y].ypos
        varMap[x][y] = riverTile("River",xpos,ypos)
        return varMap

    if y == NUMROWS -1:
        xpos = varMap[x][y].xpos
        ypos = varMap[x][y].ypos
        varMap[x][y] = riverTile("River",xpos,ypos)
        return varMap

    if y == 0:
        xpos = varMap[x][y].xpos
        ypos = varMap[x][y].ypos
        varMap[x][y] = riverTile("River",xpos,ypos)
        return varMap


    #Base case - is there nowhere left to go?
    scan = scan9(varMap,x,y)
    if "Grass" not in scan:
        return varMap

    #Grow the river
    looking = True
    while looking:
        xdir = random.randint(-1,1)
        ydir = random.randint(-1,1)

        if varMap[x + xdir][y + ydir].tileType == "Grass":
            looking = False
            xpos = varMap[x + xdir][y + ydir].xpos
            ypos = varMap[x + xdir][y+ ydir].ypos
            varMap[x + xdir][y + ydir] = riverTile("River",xpos,ypos)
            return growRiver (varMap,x + xdir,y+ydir)

#Base chance 100
def growWoods(varMap,x,y,chance):
    """Recursive function to grow woods. Grows until it hits an obstacle or runs out of chance."""

    #Base case
    if x == 0 or y == 0 or x == NUMCOLS-1 or y == NUMROWS -1:
        if random.uniform(0,chance) > 10:
            xpos = varMap[x][y].xpos
            ypos = varMap[x][y].ypos
            varMap[x][y] = woodsTile("Woods",xpos,ypos)
            return varMap
        else:
            return varMap

    elif varMap[x][y].tileType != "Grass":
        return varMap

    elif random.uniform(0,chance) < 10:
        return varMap


    else:
        chance = chance * 0.6

        xpos = varMap[x][y].xpos
        ypos = varMap[x][y].ypos
        varMap[x][y] = woodsTile("Woods",xpos,ypos)

        growWoods(varMap,x-1,y,chance)
        growWoods(varMap,x,y-1,chance)
        growWoods(varMap,x,y+1,chance)
        growWoods(varMap,x+1,y,chance)

    

#Fills the grid with grass. The first layer.
def fillGrass(rows,cols):
    varMap = []
    for i in range(rows):        
        row = []
        for j in range(cols):
            row.append(grassTile("Grass",j*TILEWIDTH,i*TILEWIDTH))
        varMap.append(row)

    return varMap

#Adds some mountains. The second layer.
def addMountains(varMap):
    numMountains = random.randint(3,7)
    for i in range(numMountains):

        #Pick the mountain location
        row = random.randint(0,len(varMap)-1)
        col = random.randint(0,len(varMap[row])-1)
        xpos = varMap[row][col].xpos
        ypos = varMap[row][col].ypos
        varMap[row][col] = mountainTile("Mountain",xpos,ypos)

        #Create submountains
        for i in range(4):
            xdirection = random.randint(-1,1)
            ydirection = random.randint(-1,1)

            #Prevent mountains from falling off the edge
            if row == 0:
                ydirection = random.randint(0,1)
            if col == 0:
                xdirection = random.randint(0,1)
            if row == NUMROWS - 1:
                ydirection = random.randint(-1,0)
            if col == NUMCOLS -1:
                xdirection = random.randint(-1,0)

            row = row + ydirection
            col = col + xdirection
            xpos = varMap[row][col].xpos
            ypos = varMap[row][col].ypos
            varMap[row][col] = mountainTile("Mountain",xpos,ypos)
            
    return varMap


def addRivers(varMap):

    numRivers = random.randint(1,3)
    
    riverStarts = []

    for row in range(len(varMap) - 2):
        for col in range(len(varMap[row])-2):
            grid = scan4(varMap,row,col)
            if grid[0] == "Mountain" and grid [1] == "Mountain" and grid[2] == "Mountain" and grid[3] != "Mountain":
                riverStarts.append([row+1,col+1])
            elif grid[1] == "Mountain" and grid [2] == "Mountain" and grid[3] == "Mountain" and grid[0] != "Mountain":
                riverStarts.append([row,col])
            elif grid[0] == "Mountain" and grid [2] == "Mountain" and grid[3] == "Mountain" and grid[1] != "Mountain":
                riverStarts.append([row,col+1])
            elif grid[1] == "Mountain" and grid [0] == "Mountain" and grid[3] == "Mountain" and grid[2] != "Mountain":
                riverStarts.append([row,col+1])

    if riverStarts == []:
        #just pick any mountain
        #Not yet implemented
        pass

    else:

        if numRivers > len(riverStarts):
            numRivers = len(riverStarts)
        
        for i in range(numRivers):
            choice = random.choice(riverStarts)
            location = choice
            riverStarts.remove(choice)
            row = location[0]
            col = location[1]
            xpos = varMap[row][col].xpos
            ypos = varMap[row][col].ypos
            varMap[row][col] = riverTile("River",xpos,ypos)
            growRiver(varMap,row,col)

    return varMap

def addWoods(varMap):
    numWoods = random.randint(2,4)
    growChance = 100


    for i in range(numWoods):
        looking = True

        while looking:
        
            x = random.randint(0,NUMCOLS-1)
            y = random.randint(0,NUMROWS-1)

            if varMap[x][y].tileType == "Grass":
                looking = False
                xpos = varMap[x][y].xpos
                ypos = varMap[x][y].ypos
                varMap[x][y] = woodsTile("Woods",xpos,ypos)

                if x != 0:              
                    growWoods(varMap,x-1,y,growChance)
                if x != NUMCOLS-1:
                    growWoods(varMap,x+1,y,growChance)
                if y != 0:
                    growWoods(varMap,x,y-1,growChance)
                if y != NUMROWS -1:
                    growWoods(varMap,x,y+1,growChance)
                
    return varMap
        

def addCities(varMap):
    numCities = 3
    cities = []


    for i in range(numCities):
        looking = True

        while looking:

            y = random.randint(1, NUMROWS-2)
            x = random.randint(1, NUMCOLS-2)

            if varMap[y][x].tileType == "Grass" and "City" not in scan9(varMap,x,y):
                xpos = varMap[x][y].xpos
                ypos = varMap[x][y].ypos
                varMap[x][y] = cityTile("City",xpos,ypos)
                cities.append([x,y])
                looking = False

    addRoads(varMap, cities[0],cities[1])
    addRoads(varMap, cities[1],cities[2])
    addRoads(varMap, cities[2],cities[0])
    
    return varMap
            

def addRoads(varMap,start,end):
    """Recursively add roads"""
    xDir = 0
    yDir = 0
    
    row = start[0]
    col = start[1]


    if start[0] > end[0]:
        xDir = -1

    elif start[0] < end[0]:
        xDir = 1

    if start[1] > end[1]:
        yDir = -1

    elif start[1] < end[1]:
        yDir = 1

    row = start[0] + xDir
    col = start[1] + yDir

    if varMap[row][col].tileType == "City":
        return varMap

    xpos = varMap[row][col].xpos
    ypos = varMap[row][col].ypos
    varMap[row][col] = roadTile("Road",xpos,ypos)
    

    addRoads(varMap,[row,col],end)
    

varMap = fillGrass(NUMROWS,NUMCOLS)
varMap = addMountains(varMap)
varMap = addRivers(varMap)
varMap = addWoods(varMap)
varMap = addCities(varMap)

#pygame loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        #generates a new map every time you hit space.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            varMap = fillGrass(NUMROWS,NUMCOLS)
            varMap = addMountains(varMap)
            varMap = addRivers(varMap)
            varMap = addWoods(varMap)
            varMap = addCities(varMap)


    for i in range(len(varMap)):
        for j in range(len(varMap)):
            varMap[i][j].draw()

    pygame.display.update()
