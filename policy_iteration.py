# policy_extraction.py
from policy import Policy


class PolicyIteration(Policy):

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


    ##
    #   @param gamestate The current gamestate
    #   @return an Absolute direction
    def best_move(self, gamestate):

        results = self.policy_iteration(gamestate, 10)
        scrambledMove = self.moveScrambler(results[1])
        move = self.relativeToAbsoluteDirection(
            gamestate.getAbsoluteHeadDirection(),
            scrambledMove
        )
        return move


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


    ##
    #   @param gamestate The current gamestate
    #   @param iteration The number of iterations to run
    #   @return a tuple containing value and absolute direction best move (value, move)
    #
    def policy_iteration(self, gamestate, iteration):

        # Base Case
        if iteration <= 0:
            return 0, None

        localRewardList = {}
        highest_reward = float("-inf")
        best_action = None

        # Loop through Each Possible Action
        # Calculate corresponding value
        for action, possible_actions in self._config.stochastic.directions.items():
            localReward = 0

            localProbTotal = 0  # Used for Normalization

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
                tempIteration = iteration
                if probability == 0:
                    tempIteration = 0
                if possible_gamestate.getGameEnd():
                    tempIteration = 0

                # Dynamic Programming
                # Use Cached values if it exists
                # otherwise, Recursive Call
                head = tuple(gamestate.getHeadLocation())
                food = tuple(gamestate.getFoodLocation())
                tail = tuple([tuple(list) for list in gamestate.getTailListLocation()])
                key = ((head, food, tail))

                if (key) in self.policy_results:
                    current_value = self.policy_results[key][0]
                else:
                    current_value = self.policy_iteration(possible_gamestate, tempIteration - 1)[0]

                localReward += probability * (current_reward + self._config.discount.gamma * current_value)
                localProbTotal += probability
            localReward /= localProbTotal  # Normalization

            # Find highest value & return it
            reward_value = localReward
            if reward_value > highest_reward:
                highest_reward = reward_value
                best_action = action
            localRewardList[action] = localReward

        # In the event all action have same value, GO Forward!
        if localRewardList[best_action] == localRewardList["FORWARD"]:
            best_action = "FORWARD"

        # Cache Results
        head = tuple(gamestate.getHeadLocation())
        food = tuple(gamestate.getFoodLocation())
        tail = tuple([tuple(list) for list in gamestate.getTailListLocation()])
        key = ((head,food,tail))

        self.policy_results[key] = (highest_reward, best_action)

        return highest_reward, best_action


