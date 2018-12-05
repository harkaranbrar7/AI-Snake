from tkinter import*
from snakeGameComponents import*
from random import randint
from value_iteration import ValueIteration
from policy_iteration import PolicyIteration
from qLearning import qLearningAgent
from approximateQLearning import approximateQLearning
from policy_configuration import PolicyConfiguration
from agent import Agent

#control variables are at the end of the document
class Master(Canvas):

    COLORHEAD = "blue"
    COLORTAIL = "green"
    COLORFOOD = "red"
    COLORWALL = "white"
    BG_COLOR = 'black'
    CANVASSIZE = 500
    
    # constants for keyboard input
    UP = 'Up'
    DOWN = 'Down'
    RIGHT = 'Right'
    LEFT = 'Left'
    # a dictionary to ease access to 'directions'
    DIRECTIONS = {UP: [0, -1], DOWN: [0, 1], RIGHT: [1, 0], LEFT: [-1, 0]}
    AXES = {UP: 'Vertical', DOWN: 'Vertical', RIGHT: 'Horizontal', LEFT: 'Horizontal'}

    def __init__(self,boss=None, inpWorldSize=6, inpAIType=0):
        super().__init__(boss)
        self.configure(width=self.CANVASSIZE, height=self.CANVASSIZE, bg=self.BG_COLOR)
        self.running = 0
        self.gameEnd = False
        self.snake = None
        self.head = None
        self.tail = None
        self.Food = None
        self.wall = None
        self.direction = None
        self.current = None
        self.score = Scores(boss)
        self.gameData = None
        self.WORLDSIZE = inpWorldSize
        self.aiType = inpAIType

    def start(self):
        """start snake game"""
        if self.running == 0:
            self.gameData = snakeGameComponents()
            self.gameData.initializeGameData(self.WORLDSIZE)

            self.gameEnd = False
            tmpLocation = self.gameData.getHeadLocation()
            self.head = Head(self, tmpLocation[0], tmpLocation[1], self.COLORHEAD, self.CANVASSIZE, self.WORLDSIZE)
            self.tail = []
            self.updateTail()
            tmpLocation = self.gameData.getFoodLocation()
            self.Food = Food(self, tmpLocation[0], tmpLocation[1], self.COLORFOOD, self.CANVASSIZE, self.WORLDSIZE)
            self.wall = []
            self.updateWall()
                
            self.direction = self.RIGHT
            self.current = Movement(self, self.DIRECTIONS[self.RIGHT], self.aiType)
            self.current.begin()
            self.running = 1



    def clean(self):
        if self.running == 1:
            self.current.stop()
            self.running = 0
            self.Food.delete()
            self.head.delete()
            for tailSegment in self.tail:
                tailSegment.delete()
            for wallSegment in self.wall:
                wallSegment.delete()

    def redirect(self, event):
        """taking keyboard inputs and moving the snake accordingly"""
        if 1 == self.running and \
                event.keysym in self.AXES.keys() and \
                self.AXES[event.keysym] != self.AXES[self.direction]:
            self.current.flag = 0
            self.direction = event.keysym
            self.current = Movement(self, self.DIRECTIONS[event.keysym], self.aiType)  # a new instance at each turn to avoid confusion/tricking
            self.current.begin()  # program gets tricked if the user presses two arrow keys really quickly
            
    def updateTail(self):
        tmpTailList = self.gameData.getTailListLocation()
        for i in range(len(tmpTailList)):
            if i < len(self.tail):
                self.tail[i].modify(tmpTailList[i][0], tmpTailList[i][1])
            else:
                self.tail.append(TailSegment(self, tmpTailList[i][0], tmpTailList[i][1], self.COLORTAIL, self.CANVASSIZE, self.WORLDSIZE))
    
    def updateWall(self):
        tmpWallList = self.gameData.getWallListLocation()
        for i in range(len(tmpWallList)):
            if i < len(self.wall):
                self.wall[i].modify(tmpWallList[i][0], tmpWallList[i][1])
            else:
                self.wall.append(WallSegment(self, tmpWallList[i][0], tmpWallList[i][1], self.COLORWALL, self.CANVASSIZE, self.WORLDSIZE))
                
    def updateHead(self):
        tmpLocation = self.gameData.getHeadLocation()
        self.head.modify(tmpLocation[0], tmpLocation[1])
        
    def updateFood(self):
        tmpLocation = self.gameData.getFoodLocation()
        self.Food.modify(tmpLocation[0], tmpLocation[1])
        self.score.increment(self.gameData.getScore())
        
    def updateGameState(self, inpX, inpY):
        self.gameData.gameLogicIteration(inpX, inpY)
        self.gameEnd = self.gameData.getGameEnd()
    
    def copyGameState(self):
        return self.gameData.copyGameState()



class Scores:
    """Objects that keep track of the score and high score"""
    def __init__(self, boss=None):
        self.counter = StringVar(boss, '0')

    def increment(self, inpScore):
        score = inpScore
        #maximum = max(score, int(self.maximum.get()))
        self.counter.set(str(score))
        #self.maximum.set(str(maximum))


class Shape:

    

    """This is a template to make Foods and snake body parts"""
    def __init__(self, can, inpX, inpY, inpColor, canSize, worldSize):
        self.can = can
        self.x, self.y = inpX, inpY
        self.color = inpColor
        self.scale = canSize / worldSize
        self.borderwidth = self.scale / 50

    def modify(self, inpX, inpY):
        self.x, self.y = inpX, inpY
        graphicLocation = self.locationToGraphicLocation(self.x, self.y)
        self.can.coords(self.ref,
                        graphicLocation[0][0], graphicLocation[0][1],
                        graphicLocation[1][0], graphicLocation[1][1])

    def drawOval(self):
        graphicLocation = self.locationToGraphicLocation(self.x, self.y)
        self.ref = Canvas.create_oval(self.can,
                                          graphicLocation[0][0], graphicLocation[0][1],
                                          graphicLocation[1][0], graphicLocation[1][1],
                                          fill=self.color,
                                          width=0)
                                          
    def drawRectangle(self):
        graphicLocation = self.locationToGraphicLocation(self.x, self.y)
        self.ref = Canvas.create_rectangle(self.can,
                                          graphicLocation[0][0], graphicLocation[0][1],
                                          graphicLocation[1][0], graphicLocation[1][1],
                                          fill=self.color,
                                          width=0)
                        
    def delete(self):
        self.can.delete(self.ref)
        
    def locationToGraphicLocation(self, inpX, inpY):
        beginX = inpX*self.scale + self.borderwidth
        beginY = inpY*self.scale + self.borderwidth
        endX = inpX*self.scale + self.scale - self.borderwidth
        endY = inpY*self.scale + self.scale - self.borderwidth
        return ((beginX, beginY),(endX, endY))


class Food(Shape):
    def __init__(self, can, inpX, inpY, inpColor, inpCanvasSize, inpWorldSize):
        self.can = can
        super().__init__(can, inpX, inpY, inpColor, inpCanvasSize, inpWorldSize)
        super().drawOval()

class Head(Shape):
    def __init__(self, can, inpX, inpY, inpColor, inpCanvasSize, inpWorldSize):
        self.can = can
        super().__init__(can, inpX, inpY, inpColor, inpCanvasSize, inpWorldSize)
        super().drawRectangle()
        
class TailSegment(Shape):
    def __init__(self, can, inpX, inpY, inpColor, inpCanvasSize, inpWorldSize):
        self.can = can
        super().__init__(can, inpX, inpY, inpColor, inpCanvasSize, inpWorldSize)
        super().drawRectangle()
        
class WallSegment(Shape):
    def __init__(self, can, inpX, inpY, inpColor, inpCanvasSize, inpWorldSize):
        self.can = can
        super().__init__(can, inpX, inpY, inpColor, inpCanvasSize, inpWorldSize)
        super().drawRectangle()

class Movement:

    #to simulate motion
    REFRESH_TIME = 100

    def __init__(self, can, direction, inpAIType):
        self.flag = 1
        self.can = can
        self.direction = direction
        self.aiType = inpAIType
        self.agent = Agent()
        pc = None
        policy = None
        #inpRewards = [food reward, hazard reward, living reward, good location reward, bad location reward]
            #good and bad location is only used for qlearning
                #tried to use to cause graph searching
            #not really used and can give wonky results
        #inpDiscounts = [gamma discount, alpha discount, epsilon explore chance]
        #inpStochastic = [forward action[forward chance, left chance, right chance]
        #left action[forward chance, left chance, right chance]
        #right action[forward chance, left chance, right chance]]
        #inpFile file for weight or qvalues
        if self.aiType == 1:
            policy = ValueIteration()
            pc = PolicyConfiguration(inpRewards = [1,-1,0,10,-1], inpDiscounts = [1,.1,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]])
        elif self.aiType == 2:
            policy = PolicyIteration()
            pc = PolicyConfiguration(inpRewards = [1,-1,0,10,-1], inpDiscounts = [1,.1,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]])
        elif self.aiType == 3:
            policy = qLearningAgent()
            #risk aversion aka rarely go off best path seems to work best
            #This one seemed to work #pc = PolicyConfiguration(inpRewards = [2,-1,0,0,-1], inpDiscounts = [0.9,.2,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]])
            pc = PolicyConfiguration(inpRewards = [2,-1,0,0,0], inpDiscounts = [0.9,.2,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]], inpFile = None, inpTrainingLimit = 20000)
        elif self.aiType == 4:
            policy = approximateQLearning()
            pc = PolicyConfiguration(inpRewards = [2,-1,0,0,-1], inpDiscounts = [0.9,.2,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]], inpFile = None, inpTrainingLimit = 5000)
        else:
            policy = ValueIteration()
            pc = PolicyConfiguration()
        policy.config = pc
            
        self.agent.policy = policy

    def begin(self):
        if self.flag > 0:
            if not self.can.gameEnd:
                new_location = self.direction
                if  self.aiType > 0:
                    new_location = self.agent.move(self.can.copyGameState())
                #gameData.gameLogicIteration(new_location[0],new_location[1]);
                self.can.updateGameState(new_location[0],new_location[1])
                #self.can.snake.move(gameData.getHeadLocation())
                self.can.updateHead()
                self.can.updateTail()
                self.can.updateFood()
                self.can.updateWall()
                self.can.after(self.REFRESH_TIME, self.begin)
            else:
                self.flag = 0;


    def stop(self):
        self.flag = 0


root = Tk()
root.title("Snake Game")

#####
#root is the canvas object
#second parameter is world size
#third parameter is ai switch
game = Master(root, 6, 4) #second parameter is world size, third is ai type

######
root.bind("<Key>", game.redirect)
game.grid(column=1, row=0, rowspan=4)
buttons = Frame(root, width=35, height=3*game.CANVASSIZE/5)
Button(buttons, text='Start', command=game.start).grid()
Button(buttons, text='Stop', command=game.clean).grid()
buttons.grid(column=0, row=0)
scoreboard = Frame(root, width=35, height=2*game.CANVASSIZE/5)
Label(scoreboard, text='Game Score').grid()
Label(scoreboard, textvariable=game.score.counter).grid()
scoreboard.grid(column=0, row=2)
#Button(buttons, text='Quit', command=root.destroy).grid()

root.mainloop()