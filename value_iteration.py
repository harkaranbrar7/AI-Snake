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
    
        bestMove = self.policy_extraction(gamestate, int(len(gamestate.gGraph)/2 + 1))
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


    #what is the value of the current state and action
    def value_iteration_action_value(self, gamestate, iteration, action):

        if iteration <= 0:
            return 0

        # Loop through Each Possible Action
        # Calculate corresponding value
        localReward = 0
        localProbTotal = 0              # Used for Normalization
        # Loop through each Possible Direction
        for possible_action, probability in self._config.stochastic.directions[action].items():
            localIteration = iteration
            localNewDirection = self.relativeToAbsoluteDirection(
                gamestate.getAbsoluteHeadDirection(),
                possible_action
            )

            possible_gamestate = gamestate.copyGameState()

            # (x,y) = (localNewDirection[0], localNewDirection[1])
            possible_gamestate.gameLogicIteration(localNewDirection[0], localNewDirection[1])
            current_reward = self.rewardValue(possible_gamestate)
            if probability == 0:
                localIteration = 0
            if possible_gamestate.getGameEnd():
                localIteration = 0
            current_value = self.value_iteration_explore(possible_gamestate, localIteration - 1)

            localReward += probability * (current_reward + self._config.discount.gamma * current_value)
            localProbTotal += probability
        localReward /= localProbTotal # Normalization
        return localReward

    #what actions can be taken from the current game state
    def value_iteration_explore(self, gamestate, iteration):

        if iteration <= 0:
            return 0

        highest_reward = float("-inf")

        # Loop through Each Possible Action
        # Calculate corresponding value
        for action, possible_actions in self._config.stochastic.directions.items():

            reward_value = self.value_iteration_action_value(gamestate, iteration, action)
            if reward_value > highest_reward:
                highest_reward = reward_value

        return highest_reward

    #determine the policy based on the action values
    def policy_extraction(self, gamestate, iteration):
        if iteration <= 0:
            return None
        localRewardList = {}

        highest_reward = float("-inf")
        highest_action = list(self._config.stochastic.directions.keys())[0]

        # Loop through Each Possible Action
        # Calculate corresponding value
        for action, possible_actions in self._config.stochastic.directions.items():
            
            gameStateCopy = gamestate.copyGameState()
            reward_value = self.value_iteration_action_value(gameStateCopy, iteration, action)

            # Find highest value & return it
            if reward_value > highest_reward:
                highest_reward = reward_value
                highest_action = action

            localRewardList[action] = reward_value
            #print(action)
            #print(reward_value)

        if localRewardList[highest_action] == localRewardList["FORWARD"]:
            highest_action = "FORWARD"
        
        return highest_action

