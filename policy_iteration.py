# policy_extraction.py
from policy import Policy


class PolicyIteration(Policy):

    def __init__(self):
        super().__init__()
        self._reward = None
        self.location_ = []
        pass

    @property
    def location(self):
        return

    @property
    def reward(self):
        return

    @reward.setter
    def reward(self, reward):
        self._reward = reward

    def best_move(self, location):
        pass

    def policy(self):
        return self.location_
