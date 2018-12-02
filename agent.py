# agent.py
# ----------

import policy
from enumerations import Enumerations

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

    def move(self):

        best_move = policy.best_move()

        # Map best move to corresponding game action
        if best_move == Enumerations.RIGHT:
            pass
        elif best_move == Enumerations.UP:
            pass
        elif best_move == Enumerations.LEFT:
            pass
        elif best_move == Enumerations.DOWN:
            pass
        else:
            raise Exception("invalid move")

