from snakeGameComponents import snakeGameComponents
from value_iteration import ValueIteration
from policy_iteration import PolicyIteration
from qLearning import qLearningAgent
from approximateQLearning import approximateQLearning
from policy_configuration import PolicyConfiguration
from agent import Agent


#mostly a display for debugging
#superceded by snakeGraphics
class Game:

    def __init__(self, inpType = 1, worldSize = 6):
        self.agent = None
        self.GINPUTTYPE = inpType
        self.GWORLDSIZE = worldSize
        self.GVISUALIZE = True
        self.GGATHERREWARD = False
        self.gPreviousScore = None
        self.gProbList = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
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

                input('press to unpause')
            gameData.gameLogicIteration(new_location[0], new_location[1])
            if self.GVISUALIZE:
                gameData.drawGraph(gameData.gGraph)
            if self.GGATHERREWARD:
                print("gather the reward data after action")
                #gameData.gScore vs previousScore



def main():
    aiType = 3
    worldSize = 6
    game = Game(aiType, worldSize)
    
    agent = Agent()
    pc = None
    policy = None
    if aiType == 1:
        policy = ValueIteration()
        pc = PolicyConfiguration(inpRewards = [1,-1,0,10,-1], inpDiscounts = [1,.1,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]])
    elif aiType == 2:
        policy = PolicyIteration()
        pc = PolicyConfiguration(inpRewards = [1,-1,0,10,-1], inpDiscounts = [1,.1,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]])
    elif aiType == 3:
        policy = qLearningAgent()
        pc = PolicyConfiguration(inpRewards = [0,-1,0,10,-1], inpDiscounts = [1,.1,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]], inpFile = "QLValues.p", inpTrainingLimit = 1000)
    elif aiType == 4:
        policy = approximateQLearning()
        pc = PolicyConfiguration(inpRewards = [2,-1,0,0,-1], inpDiscounts = [0.9,.2,.1], inpStochastic = [[100,0,0],[0,100,0],[0,0,100]], inpFile = "AQLWeights.json", inpTrainingLimit = 500)
    else:
        policy = ValueIteration()
        pc = PolicyConfiguration()
    policy.config = pc
        
    agent.policy = policy
    
    game.agent = agent
    
    game.mainLoop()



main()