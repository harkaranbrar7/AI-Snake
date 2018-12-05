# agent.py
# ----------

import policy


class Agent:

    def __init__(self):
        self._policy = policy
        pass

    @property
    def policy(self):
        return policy

    @policy.setter
    def policy(self, policy):
        self._policy = policy

    ##
    #
    #   @return returns a location [x,y]
    def move(self, gamestate):

        best_move = self._policy.best_move(gamestate)

        return best_move
