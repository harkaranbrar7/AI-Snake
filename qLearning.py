from policy import Policy
from policy_configuration import PolicyConfiguration
import random, time
import json
import pickle

class qLearningAgent(Policy):

    def __init__(self):
        super().__init__()
        self._config = None
        self._policy_results = {}
        self.gQValues = {}
        self.gTrainingIteration = 0
        self.gTrainingLimit = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.saveResults = True
        self.saveFile = "QLValues.p"
        pass
    
    @property
    def policy_results(self):
        return self._policy_results

    @property
    def reward(self):
        #return self.rewardValue(gamestate)
        return None

    @reward.setter
    def reward(self, reward):
        self._reward = reward

    def best_move(self, gamestate):
    
        if self.isInTraining():
            self.runTraining(gamestate.copyGameState(), self.gTrainingLimit)
            input("press enter to continue")
        #print("end of training")
        #print(self.gQValues)
        bestMove = self.getBestActionFromQValue(gamestate)
        scrambledMove = self.moveScrambler(bestMove)
        returnDirection = self.relativeToAbsoluteDirection(
                    gamestate.getAbsoluteHeadDirection(),
                    scrambledMove
                )
        return returnDirection
        pass

    def policy(self):
        return self.location_

    ##
    #   Accessor Method For Instance Variable: self.config
    #
    @property
    def config(self):
        return

    ##
    #   Mutator Method For Instance Variable: self.config
    #
    @config.setter
    def config(self, config):
        self._config = config
        if self._config.file != None:
            self.loadQValuesFromFile(self._config.file)
        self.gTrainingLimit = self._config.trainingLimit
        pass

    ##
    #   Accessor Method For Instance Variable: self.gamestate
    #   Note: returns a copy of the game state
    #
    @property
    def gamestate(self):
        return self._gamestate.copyGameState()

    ##
    #   Mutator Method For Instance Variable: self.gamestate
    #
    @reward.setter
    def gamestate(self, gamestate):
        self._gamestate = gamestate
    
    #inpFile is the file name
    def loadQValuesFromFile(self, inpFile):
        with open(inpFile, 'rb') as fp:
            self.gQValues = pickle.load(fp)
        return None
        
    #inpFile is the file name
    def saveQValuesToFile(self, inpFile):
        with open(inpFile, 'wb') as fp:
            pickle.dump(self.gQValues, fp, protocol=pickle.HIGHEST_PROTOCOL)
        return None
    
    #if spot has not been explored
    def isUnexploredSpot(self, inpState):
        return self.getBestValueFromQValue(inpState) == 0
    
    #implement rewards
    def rewardQValue(self, inpGameState, inpOldGameState, inpAction):
        retReward = self.rewardValue(inpGameState)
        location = inpGameState.getHeadLocation()
        if not inpGameState.isHazardSpot(location):
            if self.getQValue(inpOldGameState, inpAction) == 0:
            #if self.isUnexploredSpot(inpGameState):
                retReward += self._config.reward.goodLocation
        return retReward
            
    #not needed, because now dynamically initialized
    def initQValues(self, gamestate):
        for i in range(len(gamestate.gGraph)):
            for j in range(len(gamestate.gGraph[i])):
                for moveKey, moveValue in self._config.rawMovementValue.items():
                    for actionKey in self._config.actions:
                        self.gQValues[(((j, i), moveValue), actionKey)]
    
    #takes a long number and shortens it to the bounds of inpDivisor
    def longToShort(self, inpLong, inpBound, inpDivisor):
        retShort = int (inpDivisor * inpLong / inpBound )
        return retShort
        
    #shortens the food coordinates
    def simplifyFoodLocation(self, inpFoodLocation, inpSize, inpDivisor):
        retList = []
        retList.append(self.longToShort(inpFoodLocation[0], inpSize, inpDivisor))
        retList.append(self.longToShort(inpFoodLocation[1], inpSize, inpDivisor))
        """
        #old code: should be equivalent to the new code
        tempFoodLocation = inpFoodLocation
        
        tempWorldSize = inpSize
        localQuotient = int(tempWorldSize / inpDivisor)
        localRemainder = tempWorldSize % inpDivisor
        counter00 = 0
        tempSection = 0
        while (tempFoodLocation[0] >= tempSection):
            if (counter00 < localRemainder):
                tempSection += (localQuotient + 1)
            else:
                tempSection += localQuotient
            counter00 += 1
        retList = []
        retList.append(counter00 - 1)
        counter00 = 0
        tempSection = 0
        while (tempFoodLocation[1] >= tempSection):
            if (counter00 < localRemainder):
                tempSection += (localQuotient + 1)
            else:
                tempSection += localQuotient
            counter00 += 1
        retList.append(counter00 - 1)
        """
        return tuple(retList)
        
    
    #takes a game state and shortens to relevent state information
    def stateToShortState(self, inpState):
        location = tuple(inpState.getHeadLocation())
        direction = tuple(inpState.getHeadDirection())
        simpleFoodLocation = tuple(self.simplifyFoodLocation(inpState.getFoodLocation(), len(inpState.gGraph), 2))
        return (location, direction, simpleFoodLocation)
    
    def getQValue(self, inpState, inpAction):
        localState = self.stateToShortState(inpState)
        qValueIndex = (localState, inpAction)
        if qValueIndex not in self.gQValues:
            #self.gQValues[qValueIndex] = self._config.reward.food * 10
            self.gQValues[qValueIndex] = 0
        return self.gQValues[qValueIndex]
        
    def setQValue(self, inpState, inpAction, inpValue):
        localState = self.stateToShortState(inpState)
        qValueIndex = (localState, inpAction)
        self.gQValues[qValueIndex] = inpValue
        
    def getBestValueFromQValue(self, inpState):
        values = []
        for action in self._config.actions:
            values.append(self.getQValue(inpState,action))
        return max(values)
        
    def getBestActionFromQValue(self, inpState):
        actions = {}
        for action in self._config.actions:
            actions[action] = self.getQValue(inpState,action)
        bestAction = max(actions, key=(lambda key: actions[key]))
        if actions[bestAction] == actions["FORWARD"]:
            bestAction = "FORWARD"
        #print(actions)
        #print(bestAction)
        return bestAction

    def getExperimentalAction(self, state):
        legalActions = self._config.actions
        action = None
        randomChoice = random.random()
        #print(list(legalActions))
        #input('press to unpause')
        if randomChoice < self._config.discount.epsilon:
            #action = random.choice(legalActions.keys())
            action = random.choice(list(legalActions))
        else:
            action = self.getBestActionFromQValue(state)
        return action

    #updates the qValue
    def update(self, state, action, nextState, reward):
        currentQValue = reward + self._config.discount.gamma * self.getBestValueFromQValue(nextState)
        qvalue = (1-self._config.discount.alpha) * self.getQValue(state,action) + self._config.discount.alpha * currentQValue
        #self.gQValues[(state,action)] = qvalue
        self.setQValue(state, action, qvalue)

    #not used
    def getNextState(self, state, action):
        nextState = state.copyGameState()
        localNewDirection = self.relativeToAbsoluteDirection(
                gamestate.getAbsoluteHeadDirection(),
                action
        )
        nextState = possible_gamestate.gameLogicIteration(localNewDirection[0], localNewDirection[1])
        return nextState
        
    #episode rewards is just to overall compare differences in performance scoring
    def observeTransition(self, state,action,nextState,deltaReward):
        """
            Called to inform agent that a transition has
            been observed. This will result in a call to self.update
            on the same arguments
        """
        self.episodeRewards += deltaReward
        self.update(state,action,nextState,deltaReward)

    def startEpisode(self):
        self.episodeRewards = 0.0

    def stopEpisode(self):
        self.accumTrainRewards += self.episodeRewards

    def stopEpisodeTest(self):
        self.accumTestRewards += self.episodeRewards
        
    def stopTraining(self):
        # Take off the training wheels
        self._config.discount.epsilon = 0.0    # no exploration
        self._config.discount.alpha = 0.0      # no learning
        
    def runTraining(self, inpGameState, inpIterations):
        for i in range(inpIterations):
            self.startEpisode()
            self.runEpisode(inpGameState.copyGameState())
            self.stopEpisode()
            self.gTrainingIteration += 1
            if i % 100 == 0:
                print ("training iteration ", i, " of ", inpIterations)
        self.stopTraining()
        if self.saveResults:
            self.saveQValuesToFile(self.saveFile)
                
        return None
        
    #This is until game over
    def runEpisode(self, inpGameState):
        localGameState = inpGameState.copyGameState()
        localGameState.initializeGameData(len(inpGameState.gGraph))
        terminateCounter = 0
        terminateLimit = len(localGameState.gGraph) * len(localGameState.gGraph) * 100
        while (not localGameState.getGameEnd() and terminateCounter < terminateLimit):
            newAction = self.getExperimentalAction(localGameState)
            oldGameState = localGameState.copyGameState()
            scrambledMove = self.moveScrambler(newAction)
            newDirection = self.relativeToAbsoluteDirection(
                localGameState.getAbsoluteHeadDirection(),
                scrambledMove
            )
            localGameState.gameLogicIteration(newDirection[0], newDirection[1])
            #localDeltaReward = self.reward(localGameState)
            localDeltaReward = self.rewardQValue(localGameState, oldGameState, newAction)
            self.observeTransition(oldGameState, newAction, localGameState, localDeltaReward)
            #localGameState.drawGraph(localGameState.gGraph)
            terminateCounter += 1
            #input('press to unpause')
            #print (terminateCounter)
        return None

    def runTesting(self, inpGameState, inpIterations):
        for i in range(inpIterations):
            self.startEpisode()
            self.runEpisode(inpGameState.copyGameState())
            self.stopEpisodeTest()
        return None

    def isInTraining(self):
        return self.gTrainingIteration < self.gTrainingLimit

    def isInTesting(self):
        return not self.isInTraining()
    