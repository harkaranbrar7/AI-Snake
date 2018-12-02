# value_iteration.py
from policy import Policy
from policy_configuration import PolicyConfiguration



class ValueIteration(Policy):

    def __init__(self):
        super().__init__()
        self._config = None
        self._policy_results = {}
        pass

    @property
    def policy_results(self):
        return self._policy_results

    @property
    def reward(self):
        return

    @reward.setter
    def reward(self, reward):
        self._reward = reward

    def best_move(self, gamestate):

        best_value = self.value_iteration_recursion(gamestate, 3)
        return self.value_iteration_recursion(gamestate, 3)

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

    def initBasicList(self, inpLength, inpBase, inpIncrement):
        retList = []
        for i in range(inpLength):
            retList.append(inpBase + i * inpIncrement)
        return retList

    def rewardValue(self, gamestate):
        retReward = 0
        location = gamestate.getHeadLocation()
        if gamestate.isRewardSpot(location):
            retReward += self._config.reward.food
        if gamestate.isHazardSpot(location):
            retReward += self._config.reward.hazard
        retReward += self._config.reward.living
        return retReward


    def absDirToShort(self, inpDir):
        retShort = None
        if inpDir[0] == 0 and inpDir[1] < 0:
            retShort = 0
        elif inpDir[0] > 0 and inpDir[1] == 0:
            retShort = 1
        elif inpDir[0] == 0 and inpDir[1] > 0:
            retShort = 2
        elif inpDir[0] < 0 and inpDir[1] == 0:
            retShort = 3
        return retShort


    def shortToAbsDir(self, inpShort):
        retDir = None
        if inpShort == 0:
            retDir = [0, -1]
        elif inpShort == 1:
            retDir = [1, 0]
        elif inpShort == 2:
            retDir = [0, 1]
        elif inpShort == 3:
            retDir = [-1, 0]
        return retDir

    ##
    # Converts Relative Directions to Absolute Directions
    # @param prior_absolution_direction The (absolute) direction last taken
    # @param relative_direction the relative direction to be converted into absolute
    # @return the new absolute direction

    def relativeToAbsoluteDirection(self, prior_absolute_direction, relative_direction):
        direction_index = self._config.actions[relative_direction]
        retDirection = self.shortToAbsDir((self.absDirToShort(prior_absolute_direction) + direction_index) % 4)
        return retDirection


    def directionToLocation(self, inpLoc, inpDirection):
        retLocation = [x + y for x, y in zip(inpLoc, inpDirection)]
        return retLocation

    def value_iteration_recursion(self, gamestate, k):

        iteration = k
                    #(self, inpLoc, inpDir, inpGraph, inpIter, inpActList, inpProbList, inpDiscount):
        if iteration <= 0:
            return 0
        localRewardList = []

        highest_reward = float("-inf")

        # Loop through Each Possible Action
        # Calculate corresponding value
        for action, possible_actions in self._config.stochastic.directions.items():
            localRewardList = {action: 0}
            localProbTotal = 0

            # Loop through each Possible Direction
            for possible_action, probability in possible_actions.items():

                localNewDirection = self.relativeToAbsoluteDirection(
                    gamestate.getAbsoluteHeadDirection(),
                    possible_action
                )

                # (x,y) = (localNewDirection[0], localNewDirection[1])
                gamestate.gameLogicIteration(localNewDirection[0], localNewDirection[1])

                current_reward = self.rewardValue(gamestate)
                if current_reward < 0:
                    iteration = 0

                current_value = self.value_iteration_recursion(gamestate.copyGameState(), iteration - 1)

                localRewardList[action] += probability * (current_reward + self._config.discount.gamma * current_value)
                localProbTotal += probability
            localRewardList[action] /= localProbTotal # Normalization

            # Find highest value & return it
            reward_value = localRewardList[action]
            if reward_value > highest_reward:
                highest_reward = reward_value

        # Cache Results
        self.policy_results[gamestate] = (highest_reward, None)

        return highest_reward


    def parseActionList(self, inpActionList):
        retList = []
        if inpActionList[0] == "left":
            retList.append(-1)
        if inpActionList[1] == "straight":
            retList.append(0)
        if inpActionList[2] == "right":
            retList.append(1)
        return retList


    def policy_extraction(self, gamestate, k):
        iteration = k
        # (self, inpLoc, inpDir, inpGraph, inpIter, inpActList, inpProbList, inpDiscount):
        if iteration <= 0:
            return 0
        localRewardList = []

        highest_reward = float("-inf")

        highest_action = PolicyConfiguration.actions.get("FORWARD")

        # Loop through Each Possible Action
        # Calculate corresponding value
        for action, possible_actions in self._config.stochastic.directions.items():
            localRewardList = {action: 0}
            localProbTotal = 0

            # Loop through each Possible Direction
            for possible_action, probability in possible_actions.items():

                localNewDirection = self.relativeToAbsoluteDirection(
                    gamestate.getAbsoluteHeadDirection(),
                    possible_action
                )

                # (x,y) = (localNewDirection[0], localNewDirection[1])
                gamestate.gameLogicIteration(localNewDirection[0], localNewDirection[1])

                current_reward = self.rewardValue(gamestate)
                if current_reward < 0:
                    iteration = 0

                current_value = self.value_iteration_recursion(gamestate.copyGameState(), iteration - 1)

                localRewardList[action] += probability * (current_reward + self._config.discount.gamma * current_value)
                localProbTotal += probability
            localRewardList[action] /= localProbTotal  # Normalization

            # Find highest value & return it
            reward_value = localRewardList[action]
            if reward_value > highest_reward:
                highest_reward = reward_value

            if localRewardList[action] > localRewardList[highest_action]:
                highest_action = action

        # Cache Results
        # self.policy_results[gamestate] = (highest_reward, None)

        return PolicyConfiguration.actions[highest_action]
        #return highest_reward


gGoodReward = 10
gBadReward = -100
gLivingReward = 0
gActionList = None
gProbabilityList = None
