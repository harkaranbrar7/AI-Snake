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
        return self.policy_extraction(gamestate, 3)

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


    def value_iteration_recursion(self, gamestate, iteration):

        if iteration <= 0:
            return 0

        highest_reward = float("-inf")

        # Loop through Each Possible Action
        # Calculate corresponding value
        for action, possible_actions in self._config.stochastic.directions.items():
            localReward = 0
            localProbTotal = 0              # Used for Normalization

            # Loop through each Possible Direction
            for possible_action, probability in possible_actions.items():

                localNewDirection = self.relativeToAbsoluteDirection(
                    gamestate.getAbsoluteHeadDirection(),
                    possible_action
                )

                possible_gamestate = gamestate.copyGameState()

                # (x,y) = (localNewDirection[0], localNewDirection[1])
                possible_gamestate.gameLogicIteration(localNewDirection[0], localNewDirection[1])

                current_reward = self.rewardValue(possible_gamestate)
                if possible_gamestate.getGameEnd():
                    iteration = 0

                current_value = self.value_iteration_recursion(possible_gamestate, iteration - 1)

                localReward += probability * (current_reward + self._config.discount.gamma * current_value)
                localProbTotal += probability
            localReward /= localProbTotal # Normalization

            # Find highest value & return it
            reward_value = localReward
            if reward_value > highest_reward:
                highest_reward = reward_value

        # Cache Results
        self.policy_results[gamestate] = (highest_reward, None)

        return highest_reward


    def policy_extraction(self, gamestate, k):
        iteration = k
        if iteration <= 0:
            return None
        localRewardList = []

        highest_index = current_index = forward_index = 0
        highest_reward = float("-inf")
        highest_action = list(self._config.stochastic.directions.keys())[0]

        # Loop through Each Possible Action
        # Calculate corresponding value
        for action, possible_actions in self._config.stochastic.directions.items():
            localReward = 0
            localProbTotal = 0

            # Loop through each Possible Direction
            for possible_action, probability in possible_actions.items():

                localNewDirection = self.relativeToAbsoluteDirection(
                    gamestate.getAbsoluteHeadDirection(),
                    possible_action
                )

                possible_gamestate = gamestate.copyGameState()
                
                # (x,y) = (localNewDirection[0], localNewDirection[1])
                possible_gamestate.gameLogicIteration(localNewDirection[0], localNewDirection[1])

                current_reward = self.rewardValue(possible_gamestate)
                if possible_gamestate.getGameEnd():
                    iteration = 0

                current_value = self.value_iteration_recursion(possible_gamestate.copyGameState(), iteration - 1)

                localReward += probability * (current_reward + self._config.discount.gamma * current_value)
                localProbTotal += probability
            localReward /= localProbTotal  # Normalization

            # Find highest value & return it
            reward_value = localReward
            if reward_value > highest_reward:
                highest_reward = reward_value
                highest_action = action
                highest_index = current_index

            if action == "FORWARD":
                forward_index = current_index
            current_index += 1
            localRewardList.append(localReward)
                

        # Cache Results
        # self.policy_results[gamestate] = (highest_reward, None)

        if localRewardList[forward_index] == localRewardList[highest_index]:
            highest_action = "FORWARD"
        
        returnDirection = self.relativeToAbsoluteDirection(
                    gamestate.getAbsoluteHeadDirection(),
                    highest_action
                )
        return returnDirection
        
        #return PolicyConfiguration.actions[highest_action]
        #return highest_reward

