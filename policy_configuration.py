# policy_configurations.py


class PolicyConfiguration:

    actions = {
        "LEFT": 0,
        "FORWARD": 1,
        "RIGHT": 2
    }
    movements = {
        "NORTH": 0,
        "EAST": 1,
        "SOUTH": 2,
        "WEST": 3
    }

    def __init__(self):
        self.reward = Reward()
        self.discount = Discount()
        self.stochastic = Stochastic()
        self.actions = {
            "LEFT": 0,
            "FORWARD": 1,
            "RIGHT": 2
        }
        self.movements = {
            "NORTH": 0,
            "EAST": 1,
            "SOUTH": 2,
            "WEST": 3
        }


class Reward:
    def __init__(self):
        self.food = 1
        self.hazard = -1
        self.living = 0


class Discount:
    def __init__(self):
        self.alpha = 1
        self.gamma = 1


class Stochastic:

    def __init__(self):
        self.directions = {
            "FORWARD" : {
                "FORWARD" : 100,
                "LEFT" : 0,
                "RIGHT" : 0
            },

            "LEFT": {
                "FORWARD": 0,
                "LEFT": 100,
                "RIGHT": 0
            },

            "RIGHT": {
                "FORWARD": 0,
                "LEFT": 0,
                "RIGHT": 100
            }
        }
