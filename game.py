import sys
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')

import pygame
import random

#common constants
CELL_SIZE = 80
WIDTH = CELL_SIZE * 8
HEIGHT = CELL_SIZE * 8
FPS = 30

def SetNewSize(new_size):
    CELL_SIZE = new_size
    WIDTH = CELL_SIZE * 8
    HEIGHT = CELL_SIZE * 8

DEFAULT_HIGHLIGHTED = (-1, -1)
#common constansts

#pygame init
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
clock = pygame.time.Clock()
#pygame init

#COLORS
BLACK = (0, 0, 0)
ALMOST_BLACK = (32, 32, 32)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
COLORS = [BLACK, WHITE, RED, GREEN, BLUE]

WHITE_CELL = WHITE
BLACK_CELL = GREY
HIGHLIGHTED_CELL = GREEN
SELECTED_CELL = BLUE
FIELD_COLORS = [WHITE_CELL, BLACK_CELL, HIGHLIGHTED_CELL, SELECTED_CELL]

WHITE_PLAYER_COLOR = RED
BLACK_PLAYER_COLOR = ALMOST_BLACK
PLAYER_COLORS = [BLUE, WHITE_PLAYER_COLOR, BLACK_PLAYER_COLOR]
#COLORS

#CHECKERS_INFO
NO_CHECKER = 0
CHECKER_SIZE = CELL_SIZE / 16 * 5
CHECKER_SELECTED_SIZE = CELL_SIZE / 16 * 6
CHECKER_KING_SIZE = CELL_SIZE / 16 * 1
CHECKER_SELECTED_KOEF = 1.2
#CHECKERS_INFO

#global zone
state = []
is_reversed = False
player_turn = is_reversed
highlighted = DEFAULT_HIGHLIGHTED
avalible_tiles = []

ckeckers = [set(), set()]
#global zone

def ReverseField():
    global is_reversed
    for i in range(4):
        state[i], state[7 - i] = state[7 - i], state[i]
    is_reversed = not is_reversed

def ResetState(is_black=False):
    global state
    global is_reversed
    state = []
    is_reversed = is_black
    for i in range(8):
        state.append([])
        for j in range(8):
            state[i].append([(i + j) % 2, NO_CHECKER])
    for i in range(24):
        if (((i // 8) + (i % 8)) % 2):
            state[i // 8][i % 8] = [1, 2]
            state[(63 - i) // 8][(63 - i) % 8] = [1, 1]

    if (is_reversed): ReverseField()

def DrawCell(i, j, col=-1):
    if (col == -1): col = state[i][j][0]
    pygame.draw.rect(
                screen,
                FIELD_COLORS[col],
                (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

def DrawChecker(i, j, col=NO_CHECKER, is_king=False, sz=CHECKER_SIZE, king_sz=CHECKER_KING_SIZE, kf=1):
    if col == NO_CHECKER:
        col = abs(state[i][j][1])
        is_king = (state[i][j][1] < 0)
    if col == NO_CHECKER: return
    pygame.draw.circle(
                screen,
                PLAYER_COLORS[col],
                ((j + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE),
                sz * kf
            )
    if is_king:
        pygame.draw.circle(
                screen,
                YELLOW,
                ((j + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE),
                king_sz * kf
            )

def ReDrawItem(i, j):
    DrawCell(i, j)
    DrawChecker(i, j)

def DrawField():
    for i in range(64):
        ReDrawItem(i // 8, i % 8)

def PutChecker():
    global highlighted
    global avalible_tiles
    if (highlighted == DEFAULT_HIGHLIGHTED): return
    ReDrawItem(*highlighted)
    for pos in avalible_tiles:
        ReDrawItem(*pos)
    highlighted = DEFAULT_HIGHLIGHTED
    avalible_tiles = []

def AvalibleTiles(i, j):
    global avalible_tiles
    global highlighted
    PutChecker()
    is_eating = False
    highlighted = (i, j)
    avalible_tiles = []
    cur_col = state[i][j][1]
    simple_move_i_koef = -1 + 2 * (is_reversed ^ (abs(state[i][j][1]) == 2))
    avalible_length = 1 + 6 * (cur_col < 0)
    for i_koef in (-1, 1):
        for j_koef in (-1, 1):
            for length in range(1, avalible_length + 1):
                new_i = i + i_koef * length
                new_j = j + j_koef * length
                if (0 <= new_i <= 7) and (0 <= new_j <= 7):
                    if state[new_i][new_j][1] == NO_CHECKER:
                        if (cur_col < 0) or (i_koef == simple_move_i_koef):
                            avalible_tiles.append((new_i, new_j))
                    elif abs(state[new_i][new_j][1]) != abs(cur_col) and (0 <= new_i + i_koef <= 7) and (0 <= new_j + j_koef <= 7) and state[new_i + i_koef][new_j + j_koef][1] == NO_CHECKER:
                            avalible_tiles.append((new_i + i_koef, new_j + j_koef))
                            is_eating = True
                    else:
                        break
                else:
                    break
    return is_eating

def SelectChecker(i, j):
    DrawCell(i, j, col=3)
    DrawChecker(i, j, kf=CHECKER_SELECTED_KOEF)
    
    AvalibleTiles(i, j)
    for pos in avalible_tiles:
        DrawCell(*pos, col=2)
        DrawChecker(*pos)

def Move(i, j):
    if not (i, j) in avalible_tiles: return
    eaten = False
    cur_col = state[highlighted[0]][highlighted[1]][1]
    state[i][j][1] = cur_col
    if (i == 7 * (is_reversed ^ (abs(cur_col) == 2))):
        state[i][j][1] = -abs(state[i][j][1])
    ReDrawItem(i, j)
    state[highlighted[0]][highlighted[1]][1] = NO_CHECKER
    ReDrawItem(*highlighted)

    i_koef = 1 - 2 * (i < highlighted[0])
    j_koef = 1 - 2 * (j < highlighted[1])
    steps = 1
    while (highlighted[0] + i_koef * steps != i):
        if state[highlighted[0] + i_koef * steps][highlighted[1] + j_koef * steps][1] != NO_CHECKER:
            eaten = True
            state[highlighted[0] + i_koef * steps][highlighted[1] + j_koef * steps][1] = NO_CHECKER
            ReDrawItem(highlighted[0] + i_koef * steps, highlighted[1] + j_koef * steps)
        steps += 1

    PutChecker()
    
    

def ClickFunc(pos):
    j, i = pos
    i //= CELL_SIZE
    j //= CELL_SIZE
    print(i, j)
    if (state[i][j][1] != NO_CHECKER):
        SelectChecker(i, j)
    else:
        Move(i, j)

#init
ResetState()
DrawField()
#init

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ClickFunc(pygame.mouse.get_pos())
            
    
    pygame.display.flip()

pygame.quit()
