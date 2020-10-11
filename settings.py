from pygame.math import Vector2 as vec

class Settings:
    def __init__(self):
        # SCREEN CONSTANTS
        self.TOP_BOTTOM_BUFFER = 50
        self.WIDTH = 610
        self.HEIGHT = 670
        self.MAZE_WIDTH = self.WIDTH - self.TOP_BOTTOM_BUFFER
        self.MAZE_HEIGHT = self.HEIGHT - self.TOP_BOTTOM_BUFFER

        self.ROWS = 30
        self.COLS = 28

        #COLOUR CONSTANTS
        self.BLACK = (0, 0, 0)
        self.BLUE = (3, 57, 252)
        self.GREY = (107,107,107)
        self.RED = (208,22,22)
        self.WHITE = (240,240,240)
        self.ORANGE = (217, 155, 22)
        self.PLAYER_COLOUR = (222, 210, 42)
        self.AQUA = (0, 238, 255)
        self.LILAC = (196, 167, 194)
        #font settings
        self.START_FONT_SIZE = 18
        self.START_FONT = 'arial black'

        #player variable settings
        self.fps = 40


