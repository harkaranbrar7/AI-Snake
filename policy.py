#   policy.py
#   ----------
#   Abstract Class
#
from enumerations import Enumerations
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
    #   Determines the best move given the current gamestate
    #   @param location a tuple representing a location in the game
    #   @return the recommended move
    #
    @abstractmethod
    def best_move(self, location):
        pass

    ##
    #   Accessor Method For Instance Variable: location
    #   location is a dictionary containing tuples of the form (location, value, best move)
    #   return self.location
    #
    @property
    @abstractmethod
    def location(self):
        pass

    ##
    #   Returns the current policy
    #   @return self.location_
    #
    @abstractmethod
    def policy(self):
        pass
