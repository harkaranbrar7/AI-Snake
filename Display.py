import tkinter

class Display(tkinter.Canvas):

    # background color
    DRAW_SCREEN_COLOR = 'light sea green'
    GRID_COLOR = 'light grey'
    BG_COLOR = 'white'

    WINDOW_SIZE = 600  # pixels
    GRID_LINE_WIDTH = 2  # pixels

    CELL_SIZE = WINDOW_SIZE / 3

    def __init__(self):
        self.root = tkinter.Tk()
        super().__init__(self.root)
        self.root.title("SNAKE AI")
        self.configure(width=800, height=800, bg='white')
        self._gamestate = None
        self.pack()
        self.redraw()
        self.mainloop()

    def redraw(self):
        # draw grid
        for n in range(1, 3):
            # vertical
            self.create_line(
                Display.CELL_SIZE * n, 0,
                Display.CELL_SIZE * n, Display.WINDOW_SIZE,
                width=Display.GRID_LINE_WIDTH, fill=Display.GRID_COLOR)
            # horizontal
            self.create_line(
                0, Display.CELL_SIZE * n,
                Display.WINDOW_SIZE, Display.CELL_SIZE * n,
                width=Display.GRID_LINE_WIDTH, fill=Display.GRID_COLOR)

    @property
    def gamestate(self):
        return gamestate

    @gamestate.setter
    def reward(self, gamestate):
        self._gamestate = gamestate
