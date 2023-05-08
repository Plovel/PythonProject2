import random
import time

def ClickFunc(pos):
    j, i = pos
    i //= CELL_SIZE
    j //= CELL_SIZE
    if REVERSED_ORIENTATION:
        i = 7 - i
        j = 7 - j
    if STATE[i][j][1] != NO_CHECKER:
        SelectChecker(i, j)
    else:
        Move(i, j)

def PlayerMove():
    ClickFunc(pygame.mouse.get_pos())

def RobotMove():
    time.sleep(0.2 * (GAME_MODE != "BOT_VS_BOT"))
    if not IS_SELECT_LOCKED:
        time.sleep(len(AVALIBLE_CHECKERS[CUR_COLOR == BLACK_CHECKER]) * 0.1 * (GAME_MODE != "BOT_VS_BOT"))
        checker = random.choice(AVALIBLE_CHECKERS[CUR_COLOR == BLACK_CHECKER])
        SelectChecker(*checker)
    Move(*random.choice(AVALIBLE_CELLS))

def CheckWinner():
    if CUR_COLOR == WHITE_CHECKER:
        if len(AVALIBLE_CHECKERS[0]) == 0:
            return "BLACK"
    if CUR_COLOR == BLACK_CHECKER:
        if len(AVALIBLE_CHECKERS[1]) == 0:
            return "WHITE"
    return "NONE"    

def RunGameTurn():
    global APP_STATE

    if GAME_MODE == "BOT_VS_BOT":
        if PLAYER_COLOR == CUR_COLOR: ChangePlayerColor()

    if CUR_COLOR == PLAYER_COLOR:
        PlayerMove()
    else:
        if GAME_MODE == "BOT" or GAME_MODE == "BOT_VS_BOT": RobotMove()
        elif GAME_MODE == "ONE_PLAYER": ChangePlayerColor()

    if GAME_MODE == "BOT_VS_BOT":
        if PLAYER_COLOR == CUR_COLOR: ChangePlayerColor()

    winner = CheckWinner()
    if winner != "NONE":
        print(winner, "WON")
        APP_STATE = "GAME END"
    
    pygame.display.flip()
