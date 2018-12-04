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
        self.discount = Discount(inpGamma = 1)
        self.stochastic = Stochastic()

class Reward:
    def __init__(self, inpFood = 1, inpHazard = -1, inpLiving = 0, inpGoodLoc = 10, inpBadLoc = -1):
        self.food = inpFood
        self.hazard = inpHazard
        self.living = inpLiving
        
        #qLearning
        self.goodLocation = inpGoodLoc
        self.badLocation = inpBadLoc


class Discount:
    def __init__(self, inpGamma = 0.99, inpAlpha= 0.1, inpEpsilon = 0.1):
        self.gamma = inpGamma
        
        #qLearning
        self.alpha = inpAlpha
        self.epsilon = inpEpsilon


class Stochastic:

    def __init__(self, inpFW = [100, 0, 0], inpLT = [0, 100, 0], inpRT = [0, 0, 100]):
        self.directions = {
            "FORWARD" : {
                "FORWARD" : inpFW[0],
                "LEFT" : inpFW[1],
                "RIGHT" : inpFW[2]
            },

            "LEFT": {
                "FORWARD": inpLT[0],
                "LEFT": inpLT[1],
                "RIGHT": inpLT[2]
            },

            "RIGHT": {
                "FORWARD": inpRT[0],
                "LEFT": inpRT[1],
                "RIGHT": inpRT[2]
            }
        }
