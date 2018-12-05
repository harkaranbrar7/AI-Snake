#   policy.py
#   ----------
#   Abstract Class
#

from abc import ABC, abstractmethod
import random


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

    #takes absolute direction [x,y] and turns it into location [x,y]
    def directionToLocation(self, inpLoc, inpDirection):
        retLocation = [x + y for x, y in zip(inpLoc, inpDirection)]
        return retLocation

    #not used
    def listToTuple():
        return retTuple

    #helper function
    def absDirToShort(self, inpDir):
        retShort = None
        
        inpDir = tuple(inpDir)
        
        if inpDir == self._config.rawMovementValue["NORTH"]:
            retShort = self._config.movementsShortValue["NORTH"]
        elif inpDir == self._config.rawMovementValue["EAST"]:
            retShort = self._config.movementsShortValue["EAST"]
        elif inpDir == self._config.rawMovementValue["SOUTH"]:
            retShort = self._config.movementsShortValue["SOUTH"]
        elif inpDir == self._config.rawMovementValue["WEST"]:
            retShort = self._config.movementsShortValue["WEST"]
        
        return retShort


    #helper function
    def shortToAbsDir(self, inpShort):
        retDir = None
        if inpShort == self._config.movementsShortValue["NORTH"]:
            retDir = self._config.rawMovementValue["NORTH"]
        elif inpShort == self._config.movementsShortValue["EAST"]:
            retDir = self._config.rawMovementValue["EAST"]
        elif inpShort == self._config.movementsShortValue["SOUTH"]:
            retDir = self._config.rawMovementValue["SOUTH"]
        elif inpShort == self._config.movementsShortValue["WEST"]:
            retDir = self._config.rawMovementValue["WEST"]
        return retDir

    #calculate the reward of states
    def rewardValue(self, gamestate):
        retReward = 0
        location = gamestate.getHeadLocation()
        if gamestate.isScoreChange():
            retReward += self._config.reward.food
        if gamestate.isHazardSpot(location):
            retReward += self._config.reward.hazard
        retReward += self._config.reward.living
        return retReward
        
    #scrambles the direction of the action
    def moveScrambler(self, inpRelativeDirection):
        probabilityTotal = 0
        for direction in self._config.stochastic.directions[inpRelativeDirection]:
            probabilityTotal += self._config.stochastic.directions[inpRelativeDirection][direction]
        randomValue = random.random()*(probabilityTotal)
        probabilitySegment = 0
        for direction in self._config.stochastic.directions[inpRelativeDirection]:
            tempValue = self._config.stochastic.directions[inpRelativeDirection][direction]
            if randomValue >= probabilitySegment and randomValue < probabilitySegment + tempValue:
                return direction
            probabilitySegment += tempValue
        return list(self._config.stochastic.directions.keys())[0]