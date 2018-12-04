from policy import Policy
from policy_configuration import PolicyConfiguration
import random, time

class qLearningAgent(Policy):

    def __init__(self):
        super().__init__()
        self._config = None
        self._policy_results = {}
        self.gQValues = {}
        self.gTrainingIteration = 0
        self.gTrainingLimit = 20000
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
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
    
    def isUnexploredSpot(self, inpState):
        return self.getBestValueFromQValue(inpState) == 0
    
    def rewardQValue(self, inpGameState, inpOldGameState, inpAction):
        retReward = self.rewardValue(inpGameState)
        location = inpGameState.getHeadLocation()
        if not inpGameState.isHazardSpot(location):
            if self.isUnexploredSpot(inpGameState):
                retReward += self._config.reward.food * 100
        return retReward
        
    
    #not needed
    def initQValues(self, gamestate):
        for i in range(len(gamestate.gGraph)):
            for j in range(len(gamestate.gGraph[i])):
                for moveKey, moveValue in self._config.rawMovementValue.items():
                    for actionKey in self._config.actions:
                        self.gQValues[(((j, i), moveValue), actionKey)]
    
    def stateToShortState(self, inpState):
        location = tuple(inpState.getHeadLocation())
        direction = tuple(inpState.getHeadDirection())
        return (location, direction)
    
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

    def update(self, state, action, nextState, reward):
        currentQValue = reward + self._config.discount.gamma * self.getBestValueFromQValue(nextState)
        qvalue = (1-self._config.discount.alpha) * self.getQValue(state,action) + self._config.discount.alpha * currentQValue
        #self.gQValues[(state,action)] = qvalue
        self.setQValue(state, action, qvalue)

    def getNextState(self, state, action):
        nextState = state.copyGameState()
        localNewDirection = self.relativeToAbsoluteDirection(
                gamestate.getAbsoluteHeadDirection(),
                action
        )
        nextState = possible_gamestate.gameLogicIteration(localNewDirection[0], localNewDirection[1])
        return nextState
        
    #def doAction(self, state, action)
        #return None
    
    #iterate state
    #get reward of new state
    #do observeTransition
    
    #determine terminal by if the depth iteration is 0
    
    #on game logic iteration
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
        #self.lastState = None
        #self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        """
          Called by environment when episode is done
        """
        self.accumTrainRewards += self.episodeRewards
        """
        if self.gTrainingIteration < self.gTrainingLimit:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.gTrainingIteration += 1
        if self.gTrainingIteration >= self.gTrainingLimit:
            # Take off the training wheels
            self.epsilon = 0.0    # no exploration
            self.alpha = 0.0      # no learning
        """
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
    
    #currently not used
    def observationFunction(self, state):
        """
            This is where we ended up after our last action.
            The simulation should somehow ensure this is called
        """
        if not self.lastState is None:
            reward = state.getScore() - self.lastState.getScore()
            self.observeTransition(self.lastState, self.lastAction, state, reward)
        return state

