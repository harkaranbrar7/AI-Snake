from tkinter import*
from snakeGameComponents import*
from random import randint





# constants that go in the making of the grid used for the snake's movment
GRADUATION = 60
PIXEL = 10
STEP = 2 * PIXEL
WD = PIXEL * GRADUATION
HT = PIXEL * GRADUATION
# constants that go into specifying the shapes' sizes
OB_SIZE_FACTOR = 0.7
SN_SIZE_FACTOR = 0.9
OB_SIZE = PIXEL * OB_SIZE_FACTOR
SN_SIZE = PIXEL * SN_SIZE_FACTOR
# color constants
BG_COLOR = 'black'
OB_COLOR = 'red'
SN_COLOR = 'white'
# a dictionary to ease access to a shape's type in the Shape class
SN = 'snake'
OB = 'Food'
SIZE = {SN: SN_SIZE, OB: OB_SIZE}


# constants for keyboard input
UP = 'Up'
DOWN = 'Down'
RIGHT = 'Right'
LEFT = 'Left'
# a dictionary to ease access to 'directions'
DIRECTIONS = {UP: [0, -1], DOWN: [0, 1], RIGHT: [1, 0], LEFT: [-1, 0]}
AXES = {UP: 'Vertical', DOWN: 'Vertical', RIGHT: 'Horizontal', LEFT: 'Horizontal'}
# refresh time for the perpetual motion
REFRESH_TIME = 100

gameData = snakeGameComponents();


class Master(Canvas):
    def __init__(self,boss=None):
        super().__init__(boss)
        self.configure(width=WD, height=HT, bg=BG_COLOR)
        self.running = 0
        self.snake = None
        self.Food = None
        self.direction = None
        self.current = None
        # self.score = Scores(boss)

    def start(self):
        """start snake game"""
        if self.running == 0:
            gameData.initializeGameData(GRADUATION);
            self.snake = Snake(self)
            self.Food = Food(self)
            self.direction = RIGHT
            self.current = Movement(self, RIGHT)
            self.current.begin()
            self.running = 1

    def clean(self):
        if self.running == 1:
            self.current.stop()
            self.running = 0
            self.Food.delete()
            for block in self.snake.blocks:
                block.delete()

    def redirect(self, event):
        """taking keyboard inputs and moving the snake accordingly"""
        if 1 == self.running and \
                event.keysym in AXES.keys() and \
                AXES[event.keysym] != AXES[self.direction]:
            self.current.flag = 0
            self.direction = event.keysym
            self.current = Movement(self, event.keysym)  # a new instance at each turn to avoid confusion/tricking
            self.current.begin()  # program gets tricked if the user presses two arrow keys really quickly



class Shape:
    """This is a template to make Foods and snake body parts"""
    def __init__(self, can, a, b, kind):
        self.can = can
        self.x, self.y = a, b
        self.kind = kind
        if kind == SN:
            self.ref = Canvas.create_rectangle(self.can,
                                               a - SN_SIZE, b - SN_SIZE,
                                               a + SN_SIZE, b + SN_SIZE,
                                               fill=SN_COLOR,
                                               width=2)
        elif kind == OB:
            self.ref = Canvas.create_oval(self.can,
                                          a - OB_SIZE, b - OB_SIZE,
                                          a + SN_SIZE, b + SN_SIZE,
                                          fill=OB_COLOR,
                                          width=2)

    def modify(self, a, b):
        self.x, self.y = a, b
        self.can.coords(self.ref,
                        a - SIZE[self.kind], b - SIZE[self.kind],
                        a + SIZE[self.kind], b + SIZE[self.kind])

    def delete(self):
        self.can.delete(self.ref)


class Food(Shape):
    """snake food"""
    def __init__(self, can):
        """only create the Foods where there is no snake body part"""
        self.can = can
        foodLocation = gameData.getFoodLocation();
        a = PIXEL  * foodLocation[0]
        b = PIXEL  * foodLocation[1]
        # p = int(GRADUATION/2 - 1)
        # n, m = randint(0, p), randint(0, p)
        # a, b = PIXEL * (2 * n + 1), PIXEL * (2 * m + 1)
        while [a, b] in [[block.x, block.y] for block in self.can.snake.blocks]:
            #     n, m = randint(0, p), randint(0, p)
            a = PIXEL + 2 * foodLocation[0]
            b = PIXEL + 2 * foodLocation[1]
            a, b = PIXEL * (2 * a + 1), PIXEL * (2 * b + 1)
        super().__init__(can, a, b, OB)


class Block(Shape):
    def __init__(self, can, a, y):
        super().__init__(can, a, y, SN)



class Snake(Shape):
    def __init__(self,can):
        self.can = can
        headLocation = gameData.getHeadLocation();
        a = PIXEL + 2 * headLocation[0]/4 * PIXEL
        b = PIXEL + 2 * headLocation[1]/4 * PIXEL
        self.blocks = [Block(can, a, a), Block(can, a, a)]


    def move(self, path):
        #a = (self.blocks[-1].x + STEP * path[0]) % WD
        #b = (self.blocks[-1].y + STEP * path[1]) % HT
        a = (PIXEL * path[0]) % WD
        b = (PIXEL * path[1]) % HT
        if a == self.can.Food.x and b == self.can.Food.y:  # check if we find food
        #     self.can.score.increment()
             self.can.Food.delete()
        #     self.blocks.append(Block(self.can, a, b))
             self.can.Food = Food(self.can)
        # #elif [a, b] in [[block.x, block.y] for block in self.blocks]:  # check if we hit a body part
        #     #self.can.clean()
        # else:
        # tab them -----
        self.blocks[0].modify(a, b)
        self.blocks = self.blocks[1:] + [self.blocks[0]]



class Movement:
    def __init__(self, can, direction):
        self.flag = 1
        self.can = can
        self.direction = direction

    def begin(self):
        if self.flag > 0:
            x = gameData.getScore()
            print(x)
            if not gameData.getGameEnd():
                gameData.gameLogicIteration(DIRECTIONS[self.direction][0],DIRECTIONS[self.direction][1]);
                self.can.snake.move(gameData.getHeadLocation())
                self.can.after(REFRESH_TIME, self.begin)
            else:
                self.flag = 0;



    def stop(self):
        self.flag = 0


root = Tk()
root.title("Snake Game")
game = Master(root)
root.bind("<Key>", game.redirect)
game.grid(column=1, row=0, rowspan=4)
buttons = Frame(root, width=35, height=3*HT/5)
Button(buttons, text='Start', command=game.start).grid()
Button(buttons, text='Stop', command=game.clean).grid()
#Button(buttons, text='Quit', command=root.destroy).grid()
buttons.grid(column=0, row=0)
root.mainloop()