from policy import Policy
from policy_configuration import PolicyConfiguration
import random, time
import json
import pickle

class approximateQLearning(Policy):

    def __init__(self):
        super().__init__()
        self._config = None
        self._policy_results = {}
        self.gQValues = {}
        self.weights = {}
        self.gTrainingIteration = 0
        self.gTrainingLimit = 5000
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.saveResults = True
        self.saveFile = "AQLWeights.json"
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
        
    def loadQValuesFromFile(self, inpFile):
        with open(inpFile, 'r') as fp:
            self.weights = json.load(fp)
        return None
        
    def saveQValuesToFile(self, inpFile):
        with open(inpFile, 'w') as fp:
            json.dump(self.weights, fp, sort_keys=True, indent=4)
        return None
    
    def isUnexploredSpot(self, inpState):
        return self.getBestValueFromQValue(inpState) == 0
    
    #def rewardQValue(self, inpGameState, inpOldGameState, inpAction):
    def rewardQValue(self, inpGameState):
        retReward = self.rewardValue(inpGameState)
        """
        location = inpGameState.getHeadLocation()
        if not inpGameState.isHazardSpot(location):
            if self.getQValue(inpOldGameState, inpAction) == 0:
            #if self.isUnexploredSpot(inpGameState):
                retReward += self._config.reward.goodLocation
        """
        return retReward
    
    def stateToShortState(self, inpState):
        location = tuple(inpState.getHeadLocation())
        direction = tuple(inpState.getHeadDirection())
        return (location, direction)
    """
    def getQValue(self, inpState, inpAction):
        localState = self.stateToShortState(inpState)
        qValueIndex = (localState, inpAction)
        if qValueIndex not in self.gQValues:
            self.gQValues[qValueIndex] = 0
        return self.gQValues[qValueIndex]
    """
    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        #return self.getFeatures(state, action) * self.getWeights()
        return self.dotProduct(self.getFeatures(state, action), self.getWeights())
        
    def setQValue(self, inpState, inpAction, inpValue):
        localState = self.stateToShortState(inpState)
        qValueIndex = (localState, inpAction)
        self.gQValues[qValueIndex] = inpValue
        
    def getWeights(self):
        return self.weights
        
    def incrementWeight(self, inpKey, inpValue):
        if inpKey not in self.weights:
            self.weights[inpKey] = 0.0
        self.weights[inpKey] += inpValue
            
        
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

    """
    def update(self, state, action, nextState, reward):
        currentQValue = reward + self._config.discount.gamma * self.getBestValueFromQValue(nextState)
        qvalue = (1-self._config.discount.alpha) * self.getQValue(state,action) + self._config.discount.alpha * currentQValue
        self.setQValue(state, action, qvalue)
    """
        
    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        #updating the weight vector based on approximate q learning
        #used assignment equation as a reference
        difference = reward + self._config.discount.gamma * self.getBestValueFromQValue(nextState) - self.getQValue(state, action)
        features = self.getFeatures(state, action)
        for feature, value in features.items():
            #self.weights[feature] += self._config.discount.alpha * difference * value
            tempValue = self._config.discount.alpha * difference * value
            self.incrementWeight(feature, tempValue)

    def getNextState(self, state, action):
        nextState = state.copyGameState()
        localNewDirection = self.relativeToAbsoluteDirection(
                gamestate.getAbsoluteHeadDirection(),
                action
        )
        nextState = possible_gamestate.gameLogicIteration(localNewDirection[0], localNewDirection[1])
        return nextState
        
    def observeTransition(self, state,action,nextState,deltaReward):
        """
            Called by environment to inform agent that a transition has
            been observed. This will result in a call to self.update
            on the same arguments

            NOTE: Do *not* override or call this function
        """
        self.episodeRewards += deltaReward
        self.update(state,action,nextState,deltaReward)

    def startEpisode(self):
        """
          Called by environment when new episode is starting
        """
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
            #localDeltaReward = self.rewardQValue(localGameState, oldGameState, newAction)
            localDeltaReward = self.rewardQValue(localGameState)
            self.observeTransition(oldGameState, newAction, localGameState, localDeltaReward)
            #localGameState.drawGraph(localGameState.gGraph)
            terminateCounter += 1
            #input('press to unpause')
            #print (terminateCounter)
        if terminateCounter >= terminateLimit:
            print("hit terminate limit")
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

    def getFeatures(self, state, action):
        features = {}
        
        features["bias"] = 1.0
        #if self.isExplicitSafeArea(state.copyGameState(), action):
        #    features["explicitSafeArea"] = 1.0
        if self.isImplicitSafeArea(state.copyGameState(), action):
            features["implicitSafeArea"] = 1.0
        if self.isTwoStepSafe(state.copyGameState(), action):
            features["twoStepSafe"] = 1.0
        features["foodDistance"] = self.getFoodDistance(state.copyGameState())
        if self.getIsHazard(state.copyGameState(), action):
            features["actionIsHazard"] = 1.0
        if self.getIsFood(state.copyGameState(), action):
            features["actionIsFood"] = 1.0
        if not self.getIsHazard(state.copyGameState(), action):
            features["actionIsSafe"] = 1.0
            
        for key in features:
            features[key] /= 10.0
        
        return features

    def addCoordinates(self, inpLoc1, inpLoc2):
        retLoc = []
        for i in range(len(inpLoc1)):
            retLoc.append(inpLoc1[i]+inpLoc2[i])
        return tuple(retLoc)
        
    def subCoordinates(self, inpLoc1, inpLoc2):
        retLoc = []
        for i in range(len(inpLoc1)):
            retLoc.append(inpLoc1[i]-inpLoc2[i])
        return tuple(retLoc)
        
    def isExplicitSafeArea(self, inpGameState, inpAction):
        localGameState = inpGameState.copyGameState()
       
        directionOfAction = self.relativeToAbsoluteDirection(
                    localGameState.getAbsoluteHeadDirection(),
                    inpAction
                )
        forwardDirection = self.relativeToAbsoluteDirection(
                    directionOfAction,
                    "FORWARD"
                )
        nearLeft = self.relativeToAbsoluteDirection(
                    directionOfAction,
                    "LEFT"
                )
        farLeft = self.relativeToAbsoluteDirection(
                    forwardDirection,
                    "LEFT"
                )
        nearRight = self.relativeToAbsoluteDirection(
                    directionOfAction,
                    "RIGHT"
                )
        farRight = self.relativeToAbsoluteDirection(
                    forwardDirection,
                    "RIGHT"
                )
        currentLocation = localGameState.getHeadLocation()
        
        actionLocation = self.addCoordinates(directionOfAction, currentLocation)
        #print(actionLocation)
        forwardDirection = self.addCoordinates(directionOfAction, forwardDirection)
        forwardLocation = self.addCoordinates(forwardDirection, currentLocation)
        
        nearLeftLocation = self.addCoordinates(self.addCoordinates(directionOfAction, nearLeft), currentLocation)
        nearRightLocation = self.addCoordinates(self.addCoordinates(directionOfAction, nearRight), currentLocation)
        
        farLeftLocation = self.addCoordinates(self.addCoordinates(forwardDirection, farLeft), currentLocation)
        farRightLocation = self.addCoordinates(self.addCoordinates(forwardDirection, farRight), currentLocation)
        
        isSafe = False
        if not localGameState.isHazardSpot(actionLocation) and not localGameState.isHazardSpot(forwardLocation):
            if not localGameState.isHazardSpot(nearLeftLocation) and not localGameState.isHazardSpot(farLeftLocation):
                isSafe = True
            if not localGameState.isHazardSpot(nearRightLocation) and not localGameState.isHazardSpot(farRightLocation):
                isSafe = True
                
        isSafe = True
                
    def isImplicitSafeArea(self, inpGameState, inpAction):
        isSafe = True
        
        localGameState = inpGameState.copyGameState()
        directionOfAction = self.relativeToAbsoluteDirection(
                    localGameState.getAbsoluteHeadDirection(),
                    inpAction
                )
        localGameState.gameLogicIteration(directionOfAction[0], directionOfAction[1])
        if localGameState.isHazardSpot(localGameState.getHeadLocation()):
            isSafe = False
        
        forwardGameState = localGameState.copyGameState()
        forwardDirection = self.relativeToAbsoluteDirection(
                    forwardGameState.getAbsoluteHeadDirection(),
                    "FORWARD"
                )
        forwardGameState.gameLogicIteration(forwardDirection[0], forwardDirection[1])
        if forwardGameState.isHazardSpot(forwardGameState.getHeadLocation()):
            isSafe = False
        
        tempSafeCheck = True
        
        #check if left is clear
        tempGameState = localGameState.copyGameState()
        tempDirection = self.relativeToAbsoluteDirection(
                    tempGameState.getAbsoluteHeadDirection(),
                    "LEFT"
                )
        tempGameState.gameLogicIteration(tempDirection[0], tempDirection[1])
        if tempGameState.isHazardSpot(tempGameState.getHeadLocation()):
            tempSafeCheck = False
            
        tempGameState = forwardGameState.copyGameState()
        tempDirection = self.relativeToAbsoluteDirection(
                    tempGameState.getAbsoluteHeadDirection(),
                    "LEFT"
                )
        
        tempGameState.gameLogicIteration(tempDirection[0], tempDirection[1])
        if tempGameState.isHazardSpot(tempGameState.getHeadLocation()):
            tempSafeCheck = False
        
        #if not check if right is clear
        if not tempSafeCheck:
            tempGameState = localGameState.copyGameState()
            tempDirection = self.relativeToAbsoluteDirection(
                        tempGameState.getAbsoluteHeadDirection(),
                        "RIGHT"
                    )
            tempGameState.gameLogicIteration(tempDirection[0], tempDirection[1])
            if tempGameState.isHazardSpot(tempGameState.getHeadLocation()):
                isSafe = False
                
            tempGameState = forwardGameState.copyGameState()
            tempDirection = self.relativeToAbsoluteDirection(
                        tempGameState.getAbsoluteHeadDirection(),
                        "RIGHT"
                    )
            
            tempGameState.gameLogicIteration(tempDirection[0], tempDirection[1])
            if tempGameState.isHazardSpot(tempGameState.getHeadLocation()):
                isSafe = False

        return isSafe
        
    def isTwoStepSafe(self, inpGameState, inpAction):
        isSafe = False
        tmpSafe = True
        localGameState = inpGameState.copyGameState()
        directionOfAction = self.relativeToAbsoluteDirection(
                    localGameState.getAbsoluteHeadDirection(),
                    inpAction
                )
        localGameState.gameLogicIteration(directionOfAction[0], directionOfAction[1])
        if localGameState.isHazardSpot(localGameState.getHeadLocation()):
            tmpSafe = False
        
        if (tmpSafe):
            isSafe = False
            forwardGameState = localGameState.copyGameState()
            forwardDirection = self.relativeToAbsoluteDirection(
                        forwardGameState.getAbsoluteHeadDirection(),
                        "FORWARD"
                    )
            forwardGameState.gameLogicIteration(forwardDirection[0], forwardDirection[1])
            if not forwardGameState.isHazardSpot(forwardGameState.getHeadLocation()):
                isSafe = True
            
            #check if left is clear
            tempGameState = localGameState.copyGameState()
            tempDirection = self.relativeToAbsoluteDirection(
                        tempGameState.getAbsoluteHeadDirection(),
                        "LEFT"
                    )
            tempGameState.gameLogicIteration(tempDirection[0], tempDirection[1])
            if not tempGameState.isHazardSpot(tempGameState.getHeadLocation()):
                isSafe = True
                
            #if not check if right is clear
            tempGameState = localGameState.copyGameState()
            tempDirection = self.relativeToAbsoluteDirection(
                        tempGameState.getAbsoluteHeadDirection(),
                        "RIGHT"
                    )
            tempGameState.gameLogicIteration(tempDirection[0], tempDirection[1])
            if not tempGameState.isHazardSpot(tempGameState.getHeadLocation()):
                isSafe = True

        return isSafe

    def getFoodDistance(self, state):
        localGameState = state.copyGameState()
        currentLocation = localGameState.getHeadLocation()
        foodLocation = localGameState.getFoodLocation()
        locationDifference = self.subCoordinates(currentLocation, foodLocation)
        #return abs(locationDifference[0]) + abs(locationDifference[1])
        return (abs(locationDifference[0]) + abs(locationDifference[1])) / (len(localGameState.gGraph) * 2)
        
    def getIsHazard(self, state, inpAction):
        localGameState = state.copyGameState()
        directionOfAction = self.relativeToAbsoluteDirection(
                    localGameState.getAbsoluteHeadDirection(),
                    inpAction
                )
        localGameState.gameLogicIteration(directionOfAction[0], directionOfAction[1])
        return localGameState.isHazardSpot(localGameState.getHeadLocation())
    
    def getIsFood(self, state, inpAction):
        localGameState = state.copyGameState()
        directionOfAction = self.relativeToAbsoluteDirection(
                    localGameState.getAbsoluteHeadDirection(),
                    inpAction
                )
        localGameState.gameLogicIteration(directionOfAction[0], directionOfAction[1])
        return localGameState.isScoreChange()
        
        
    def dotProduct(self, inpXDict, inpYDict ):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['second'] = 5
        >>> a['third'] = 1.5
        >>> a['fourth'] = 2.5
        >>> a * b
        14
        """
        sum = 0
        if len(inpXDict) > len(inpYDict):
            inpXDict,inpYDict = inpYDict,inpXDict
        for key in inpXDict:
            if key not in inpYDict:
                continue
            sum += inpXDict[key] * inpYDict[key]
        return sum