#common constants
CELL_SIZE = 80
WIDTH = CELL_SIZE * 8
HEIGHT = CELL_SIZE * 8

PATH_TO_SRC = "../src"
#common constansts

#COLORS
TEXT_TO_COLORS = {"BLACK":(0, 0, 0),
                  "ALMOST_BLACK":(32, 32, 32),
                  "WHITE":(255, 255, 255),
                  "RED":(255, 0, 0),
                  "ORANGE":(255, 128, 0),
                  "GREEN":(0, 255, 0),
                  "BLACK_GREEN":(0, 153, 0),
                  "BLUE":(0, 0, 255),
                  "GREY":(128, 128, 128),
                  "YELLOW":(255, 255, 0)}
COLORS_TO_TEXT = {}
for key, val in TEXT_TO_COLORS.items(): COLORS_TO_TEXT[val] = key
COLORS = [val[:] for val in TEXT_TO_COLORS.values()]


BLACK = TEXT_TO_COLORS["BLACK"]
ALMOST_BLACK = TEXT_TO_COLORS["ALMOST_BLACK"]
WHITE = TEXT_TO_COLORS["WHITE"]
RED = TEXT_TO_COLORS["RED"]
ORANGE = TEXT_TO_COLORS["ORANGE"]
GREEN = TEXT_TO_COLORS["GREEN"]
BLACK_GREEN = TEXT_TO_COLORS["BLACK_GREEN"]
BLUE = TEXT_TO_COLORS["BLUE"]
GREY = TEXT_TO_COLORS["GREY"]
YELLOW = TEXT_TO_COLORS["YELLOW"]

TRANSPARENT = (-1, -1, -1)

DEFAULT_CLEAR_SCREEN = ALMOST_BLACK[:]
#COLORS

#OTHER
DEFAULT_FONT = None
DEFAULT_FONT_SIZE = CELL_SIZE * 500 // 800
#OTHER
