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
