#   policy.py
#   ----------
#   Abstract Class
#

from abc import ABC, abstractmethod


class Policy(ABC):

    def __init__(self):
        pass

    ##
    #   Accessor Method For Instance Variable: self.reward
    #
    @property
    @abstractmethod
    def reward(self):
        return

    ##
    #   Mutator Method For Instance Variable: self.reward
    #
    @reward.setter
    @abstractmethod
    def reward(self, reward):
        pass

    ##
    #   Accessor Method For Instance Variable: self.config
    #
    @property
    @abstractmethod
    def config(self):
        return

    ##
    #   Mutator Method For Instance Variable: self.config
    #
    @config.setter
    @abstractmethod
    def config(self, config):
        pass

    ##
    #   Determines the best move given the current gamestate
    #   @param location a tuple representing a location in the game
    #   @return the recommended move
    #
    @abstractmethod
    def best_move(self, gamestate):
        pass


    ##
    #   Returns the current policy
    #   @return self.location_
    #
    @abstractmethod
    def policy(self):
        pass

    ##
    # Converts Relative Directions to Absolute Directions
    # @param prior_absolution_direction The (absolute) direction last taken
    # @param relative_direction the relative direction to be converted into absolute
    # @return the new absolute direction

    def relativeToAbsoluteDirection(self, prior_absolute_direction, relative_direction):
        direction_index = self._config.actions[relative_direction] - 1
        retDirection = self.shortToAbsDir((self.absDirToShort(prior_absolute_direction) + direction_index) % 4)
        return retDirection


    def directionToLocation(self, inpLoc, inpDirection):
        retLocation = [x + y for x, y in zip(inpLoc, inpDirection)]
        return retLocation

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

    def rewardValue(self, gamestate):
        retReward = 0
        location = gamestate.getHeadLocation()
        if gamestate.isScoreChange():
            retReward += self._config.reward.food
        if gamestate.isHazardSpot(location):
            retReward += self._config.reward.hazard
        retReward += self._config.reward.living
        return retReward