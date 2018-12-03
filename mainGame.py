from snakeGameComponents import snakeGameComponents
from value_iteration import ValueIteration
from policy_iteration import PolicyIteration
from policy_configuration import PolicyConfiguration
from display import Display
from agent import Agent
import threading


class Game:

    def __init__(self):
        self.agent = None
        self.GINPUTTYPE = 1
        self.GWORLDSIZE = 6
        self.GVISUALIZE = True
        self.GGATHERREWARD = False
        self.gPreviousScore = None
        self.gProbList = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.display = None
        self.game_thread = threading.Thread(target=self.mainLoop)
        pass


    def parseInput(self):
        retCoordinates = []
        #keyPressed = None

        keyPressed = input('Enter command\n')
        if len(keyPressed) < 1:
            retCoordinates.append(0)
            retCoordinates.append(-1)
        elif keyPressed[0] == 'w':
            retCoordinates.append(0)
            retCoordinates.append(-1)
        elif keyPressed[0] == 'a':
            retCoordinates.append(-1)
            retCoordinates.append(0)
        elif keyPressed[0] == 's':
            retCoordinates.append(0)
            retCoordinates.append(1)
        elif keyPressed[0] == 'd':
            retCoordinates.append(1)
            retCoordinates.append(0)
        else:
            retCoordinates.append(0)
            retCoordinates.append(-1)
        #print (keyPressed)

        return retCoordinates

    def aiInterceptor(self,inpLoc, inpDir, inpGraph, inpIter, inpProbList, inpDiscount):
        retCoordinates = []
        if GINPUTTYPE == 1:
            #print ("nothing value iteration")
            localValueIteration = valueIteration()
            retCoordinates = localValueIteration.valIterRoot(inpLoc, inpDir, inpGraph, inpIter, inpProbList, inpDiscount)
        elif GINPUTTYPE == 2:
            print ("nothing q learning")
        elif GINPUTTYPE == 3:
            print ("nothing approximate q learning")

        return retCoordinates

    def start(self):

        # Game Logic Runs In It's Own Thread
        self.game_thread.start()

        # Rendering Logic Runs on Main Thread (Since It Blocks Like A Mofo!)
        self.display = Display()

    def mainLoop(self):

        gameData = snakeGameComponents()
        gameData.initializeGameData(self.GWORLDSIZE)
        gameData.drawGraph(gameData.gGraph)
        gPreviousScore = 0

        while (gameData.gGameDone == False):
            new_location = None
            if self.GINPUTTYPE == 0:
                new_location = self.parseInput()
            else:

                # Process AI Actions
                new_location = self.agent.move(gameData.copyGameState())

                # Rendering Code

                input('press to unpause')
            gameData.gameLogicIteration(new_location[0], new_location[1])
            if self.GVISUALIZE:
                gameData.drawGraph(gameData.gGraph)
            if self.GGATHERREWARD:
                print("gather the reward data after action")
                #gameData.gScore vs previousScore



def main():
    game = Game()

    pc = PolicyConfiguration()
    #policy = ValueIteration()
    policy = PolicyIteration()
    policy.config = pc

    agent = Agent()
    agent.policy = policy

    game.agent = agent
    game.start()


main()
