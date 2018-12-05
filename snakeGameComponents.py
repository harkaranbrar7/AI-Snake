from tkinter import *
import random


#location object
class cartesianLocation:
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y
    def copyNew(self):
        return (cartesianLocation(self.x, self.y))
    def copyValue(self, inpLocation):
        self.x = inpLocation.x
        self.y = inpLocation.y
    def __add__(self, inpLocation):
        retLocation = cartesianLocation(self.x + inpLocation.x, self.y + inpLocation.y)
        return retLocation
    def __iadd__(self, inpLocation):
        self.x += inpLocation.x
        self.y += inpLocation.y
        return self
    def __eq__(self, inpLocation):
        return (self.x == inpLocation.x and self.y == inpLocation.y)
    def __ne__(self, inpLocation):
        return (self.x != inpLocation.x or self.y != inpLocation.y)

#head object
class snakeHead:
    def __init__(self, inpLocation, inpOrientation):
        self.location = inpLocation
        self.direction = inpOrientation
        self.dead = False
    def copyObject(self):
        retObject = snakeHead(self.location.copyNew(), self.direction.copyNew())
        retObject.dead = self.dead
        return retObject
#tail joint object
class snakeTailJoint:
    def __init__(self, inpLocation, inpOrientation):
        self.location = inpLocation
        self.direction = inpOrientation
    def copyObject(self):
        retObject = snakeTailJoint(self.location.copyNew(), self.direction.copyNew())
        return retObject

#food object
class food:
    def __init__(self, inpLocation):
        self.location = inpLocation
        self.dead = False
    def copyObject(self):
        retObject = food(self.location.copyNew())
        retObject.dead = self.dead
        return retObject

#wall object
class wall:
    def __init__(self, inpLocation):
        self.location = inpLocation
    def copyObject(self):
        retObject = wall(self.location.copyNew())
        return retObject

#graph element object
class graphPoint:
    def __init__(self):
        self.wall = False
        self.food = False
        self.tail = False
        self.head = False
    def copyObject(self):
        retObject = graphPoint()
        retObject.wall = self.wall
        retObject.food = self.food
        retObject.tail = self.tail
        retObject.head = self.head
        return retObject
    def isHazard(self):
        return (self.wall == True or self.tail == True)
    def isReward(self):
        return (self.food == True)
    def isEmpty(self):
        return (self.wall == False and self.food == False and self.tail == False and self.head == False)

#components of game object
    #i.e. the rules of the game
class snakeGameComponents:
    gHead = None
    gTailList = None
    gFood = None
    gWallList = None
    gGraph = None
    gScore = None
    gPreviousScore = None
    gGameDone = None
    GSCOREINCREASEVALUE = 1

    #correct location if out of bounds
    def outOfBoundsCorrection(self, inpLocation, inpGraphBounds):
        retLocation = inpLocation
        while (retLocation.x > inpGraphBounds - 1):
            #retLocation.x = 0
            retLocation.x -= inpGraphBounds
        while (retLocation.y > inpGraphBounds - 1):
            #retLocation.y = 0
            retLocation.y -= inpGraphBounds
        while (retLocation.x < 0):
            #retLocation.x = inpGraphBounds - 1
            retLocation.x += inpGraphBounds
        while (retLocation.y < 0):
            #retLocation.y = inpGraphBounds - 1
            retLocation.y += inpGraphBounds
        return retLocation

    #move the head
    def moveHead (self, inpHead, inpDirection, inpGraphBounds):

        if inpDirection.x > 0:
            inpDirection.x = 1
        elif inpDirection.x < 0:
            inpDirection.x = -1
        if inpDirection.y > 0:
            inpDirection.y = 1
        elif inpDirection.y < 0:
            inpDirection.y = -1

        if (inpDirection.x * -1) != inpHead.direction.x or (inpDirection.y * -1) != inpHead.direction.y:
            inpHead.location += inpDirection
            inpHead.direction = inpDirection
        else:
            inpHead.location += inpHead.direction
        self.outOfBoundsCorrection(inpHead.location, inpGraphBounds)

    def moveTail(self, inpTailList, inpHead):
        for i in range ( len(inpTailList) - 1, 0, -1 ):
            inpTailList[i].location.copyValue(inpTailList[i - 1].location)
            inpTailList[i].direction.copyValue(inpTailList[i - 1].direction)
        if len(inpTailList) > 0:
            inpTailList[0].location.copyValue(inpHead.location)
            inpTailList[0].direction.copyValue(inpHead.direction)

    #move the head and the tail
    def moveSnake(self, inpTailList, inpHead, inpDirection, inpBounds):
        self.moveTail (inpTailList, inpHead)
        self.moveHead (inpHead, inpDirection, inpBounds)

    #add tail joint to the tail
    def growSnake(self, inpTailList, inpHead):
        newTailJoint = None
        newLocation = None
        newDirection = None
        if (len(inpTailList) > 0):
            newLocation = inpTailList[len(inpTailList) - 1].location.copyNew()
            newDirection = inpTailList[len(inpTailList) - 1].direction.copyNew()
        else:
            newLocation = inpHead.location.copyNew()
            newDirection = inpHead.direction.copyNew()
        newTailJoint = snakeTailJoint(newLocation, newDirection)
        inpTailList.append(newTailJoint)

    #increase the score
    def increaseScore(self, inpScore):
        retScore = inpScore
        retScore += self.GSCOREINCREASEVALUE #i.e. 1
        return retScore

    #find a list of empty location
    def findValidLocations (self, inpGraph):
        validLocationList = []
        for i in range(len(inpGraph)):
            for j in range(len(inpGraph[i])):
                if inpGraph[i][j].isEmpty():
                    validLocationList.append(cartesianLocation(j,i))
        return validLocationList

    #generate new food location
    def newFoodLocation(self, inpGraph):
        validLocationList = self.findValidLocations(inpGraph)
        foodLocation = None
        if len(validLocationList) > 0:
            foodLocation = random.choice(validLocationList)
        else:
            foodLocation = cartesianLocation(0, 0)
        return foodLocation

    #run the eating food game logic
    def eatFood(self, inpTailList, inpHead, inpFood, inpGraph):
        self.growSnake(inpTailList, inpHead)
        inpGraph[inpFood.location.y][inpFood.location.x].food = False
        tmpFoodLocation = self.newFoodLocation(inpGraph)
        inpGraph[tmpFoodLocation.y][tmpFoodLocation.x].food = True
        inpFood.location.copyValue(tmpFoodLocation)
        inpFood.dead = False

    #remove the snake components from the graph
    def clearSnake (self, inpGraph, inpHead, inpTailList):
        inpGraph[inpHead.location.y][inpHead.location.x].head = False
        for i in inpTailList:
            inpGraph[i.location.y][i.location.x].tail = False

    #add the snake components to the graph
    def updateGraphSnake (self, inpGraph, inpHead, inpTailList):
        for i in inpTailList:
            inpGraph[i.location.y][i.location.x].tail = True
        inpGraph[inpHead.location.y][inpHead.location.x].head = True

    #add wall components to the graph
    def updateGraphWall (self, inpGraph, inpWallList):
        for i in inpWallList:
            inpGraph[i.location.y][i.location.x].wall = True

    #flag dead if hit wall or tail
    def doDeathCollision(self, inpGraph, inpHead):
        if inpGraph[inpHead.location.y][inpHead.location.x].wall == True or inpGraph[inpHead.location.y][inpHead.location.x].tail == True:
            inpHead.dead = True
            
    #flag eaten if hit food and head
    def doFoodCollison(self, inpGraph, inpFood):
        if (inpGraph[inpFood.location.y][inpFood.location.x].head == True):
            inpFood.dead = True

    #debugging to draw graph
    def drawGraph(self, inpGraph):
        for i in range(len(inpGraph)):
            for j in range(len(inpGraph[i])):
                if inpGraph[i][j].head == True:
                    print("h", end="", flush=True)
                elif inpGraph[i][j].tail == True:
                    print("t", end="", flush=True)
                elif inpGraph[i][j].food == True:
                    print("f", end="", flush=True)
                elif inpGraph[i][j].wall == True:
                    print("w", end="", flush=True)
                else:
                    print(" ", end="", flush=True)
            print("")

    #initialize wall list
    def initializeWallData(self, inpGraphSize):
        retWallList = []
        for i in range(inpGraphSize):
            newWall = wall(cartesianLocation(i, 0))
            retWallList.append(newWall)
        for i in range(inpGraphSize):
            newWall = wall(cartesianLocation(i, inpGraphSize - 1))
            retWallList.append(newWall)
        for i in range(1, inpGraphSize - 1):
            newWall = wall(cartesianLocation(0, i))
            retWallList.append(newWall)
        for i in range(1, inpGraphSize - 1):
            newWall = wall(cartesianLocation(inpGraphSize - 1, i))
            retWallList.append(newWall)
        return retWallList

    #initialize all of the game data
        #everything is reinitialized
    def initializeGameData(self, inpGraphSize):
        self.gGraph = []
        for i in range(inpGraphSize):
            tmpGraphRow = []
            for j in range(inpGraphSize):
                tmpGraphRow.append(graphPoint())
            self.gGraph.append(tmpGraphRow)

        self.gWallList = self.initializeWallData(inpGraphSize)

        startPostion = cartesianLocation(int(inpGraphSize/2), int(inpGraphSize/2))

        self.gHead = snakeHead(startPostion, cartesianLocation(1, 0))

        self.gTailList = []
        for i in range(1):
            self.gTailList.append(snakeTailJoint(cartesianLocation(startPostion.x-1-i, startPostion.y), self.gHead.direction))

        self.updateGraphWall(self.gGraph, self.gWallList)
        self.updateGraphSnake(self.gGraph, self.gHead, self.gTailList)

        self.gFood = food(self.newFoodLocation(self.gGraph))
        self.gGraph[self.gFood.location.y][self.gFood.location.x].food = True
        self.gScore = 0
        self.gGameDone = False

    # do a game move, send in x direction and y direction of movement
    # i.e. x=0, y=-1 moves 1 spot north
    def gameLogicIteration(self, inpXChange, inpYChange):
        self.gPreviousScore = self.gScore
        self.clearSnake(self.gGraph, self.gHead, self.gTailList)
        localDirection = cartesianLocation(inpXChange, inpYChange)
        self.moveSnake(self.gTailList, self.gHead, localDirection, len(self.gGraph))
        self.updateGraphSnake(self.gGraph, self.gHead, self.gTailList)
        self.doDeathCollision(self.gGraph, self.gHead)
        self.doFoodCollison(self.gGraph, self.gFood)
        if(self.gFood.dead == True):
            self.eatFood(self.gTailList, self.gHead, self.gFood, self.gGraph)
            self.gScore = self.increaseScore(self.gScore)
        if(self.gHead.dead == True):
            self.gGameDone = True

    #get location of the head
    #[x,y]
    def getHeadLocation(self):
        retLocation = []
        retLocation.append(self.gHead.location.x)
        retLocation.append(self.gHead.location.y)
        return retLocation
        
    #get direction of the head
    #[x,y]
    def getHeadDirection(self):
        retDirection = []
        retDirection.append(self.gHead.direction.x)
        retDirection.append(self.gHead.direction.y)
        return retDirection
        
    #get direction of the head
    #[x,y]
    def getAbsoluteHeadDirection(self):
        retDirection = []
        retDirection.append(self.gHead.direction.x)
        retDirection.append(self.gHead.direction.y)
        return retDirection
    
    #get location of the food
    #[x,y]
    def getFoodLocation(self):
        retLocation = []
        retLocation.append(self.gFood.location.x)
        retLocation.append(self.gFood.location.y)
        return retLocation
        
    #get a list of tail locations
    #[[x,y],...]
    def getTailListLocation(self):
        retLocation = []
        for i in self.gTailList:
            tmpListElement = []
            tmpListElement.append(i.location.x)
            tmpListElement.append(i.location.y)
            retLocation.append(tmpListElement)
        return retLocation
        
    #get a list of wall locations
    #[[x,y],...]
    def getWallListLocation(self):
        retLocation = []
        for i in self.gWallList:
            tmpListElement = []
            tmpListElement.append(i.location.x)
            tmpListElement.append(i.location.y)
            retLocation.append(tmpListElement)
        return retLocation

    #copys the game data into a new game object
        #so that it doesn't reference the original object
    def copyGameState(self):
        retGame = snakeGameComponents()
        retGame.gHead = self.gHead.copyObject()
        retGame.gFood = self.gFood.copyObject()
        retGame.gTailList = []
        for i in self.gTailList:
            retGame.gTailList.append(i.copyObject())
        retGame.gWallList = []
        for i in self.gWallList:
            retGame.gWallList.append(i.copyObject())
        retGame.gGraph = []
        for i in self.gGraph:
            tmpRow = []
            for j in i:
                tmpRow.append(j.copyObject())
            retGame.gGraph.append(tmpRow)

        retGame.gGameDone = self.gGameDone
        retGame.gScore = self.gScore

        return retGame

    #if location is empty
    #[x,y]
    def isEmptySpot(self, location):
        tmpLoc = self.outOfBoundsCorrection(cartesianLocation(location[0], location[1]), len(self.gGraph))
        return self.gGraph[tmpLoc.x][tmpLoc.y].isEmpty()
    #if location is a hazard
    #[x,y]
    def isHazardSpot(self, location):
        tmpLoc = self.outOfBoundsCorrection(cartesianLocation(location[0], location[1]), len(self.gGraph))
        return self.gGraph[tmpLoc.x][tmpLoc.y].isHazard()
    #if location is food
    #[x,y]
    def isRewardSpot(self, location):
        tmpLoc = self.outOfBoundsCorrection(cartesianLocation(location[0], location[1]), len(self.gGraph))
        return self.gGraph[tmpLoc.x][tmpLoc.y].isReward()
        
    #if the score has changed
    def isScoreChange(self):
        return self.gPreviousScore != self.gScore
    
    #get current score
    def getScore(self):
        return self.gScore
        
    #get if game is over
    def getGameEnd(self):
        return self.gGameDone
