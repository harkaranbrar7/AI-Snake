# policy_configurations.py


class PolicyConfiguration:

    actions = {
        "LEFT": 0,
        "FORWARD": 1,
        "RIGHT": 2
    }
    movementsShortValue = {
        "NORTH": 0,
        "EAST": 1,
        "SOUTH": 2,
        "WEST": 3
    }
    rawMovementValue = {
        "NORTH": (0,-1),
        "EAST": (1,0),
        "SOUTH": (0,1),
        "WEST": (-1,0)
    }

    def __init__(self):
        self.reward = Reward()
        self.discount = Discount()
        self.stochastic = Stochastic()

class Reward:
    def __init__(self):
        #self.food = 1
        #self.hazard = -1
        #self.living = 0
        
        #qLearning
        self.food = 1
        self.hazard = -1
        self.living = 0
        self.goodLocation = 1


class Discount:
    def __init__(self):
        self.alpha = 0.5
        self.gamma = 0.99
        self.epsilon = 0.2
        
        #qLearning
        #self.alpha = 0.01
        #self.gamma = 0.99
        #self.epsilon = 0.05


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
