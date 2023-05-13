import random
import time

def ClickFunc(pos):
    j, i = pos
    i //= CELL_SIZE
    j //= CELL_SIZE

    ind = i * 8 + j
    if REVERSED_ORIENTATION: ind = 63 - ind
    
    if STATE[ind] == ' ':
        if Move(ind) and GAME_MODE == "MULTIPLAYER":
            try: CONNECTED_SOCKET.send(("MOVE_" + str(ind) + ' ').encode())
            except: ExitMultiplayer("Failed to send data", menu="GAME")
    else:
        if SelectChecker(ind) and GAME_MODE == "MULTIPLAYER":
            try: CONNECTED_SOCKET.send(("SELECT_" + str(ind) + ' ').encode())
            except: ExitMultiplayer("Failed to send data", menu="GAME")

def PlayerMove(): ClickFunc(pygame.mouse.get_pos())

def RobotRandomMove():
    checker = random.choice(tuple(AVALIBLE_CHECKERS[CUR_COLOR == 'B']))
    SelectChecker(checker, show=False)
    Move(random.choice(tuple(AVALIBLE_CELLS)))

HARD_BOT = False
def RobotMove():
    time.sleep(0.2 * (GAME_MODE != "BOT_VS_BOT"))
    if not IS_SELECT_LOCKED:
        time.sleep(len(AVALIBLE_CHECKERS[CUR_COLOR == 'B']) * 0.1 *
                   (GAME_MODE != "BOT_VS_BOT"))
        if HARD_BOT and not (random.randint(0, 1000) % 20 == 0):
            state_bkp = [STATE[:], PLAYER_COLOR, CUR_COLOR]
            #for checker in AVALIBLE_CHECKERS[CUR_COLOR == 'B']: 
        else:
            RobotRandomMove()
    else: Move(random.choice(tuple(AVALIBLE_CELLS)))

def CheckWinner():
    if bool(AVALIBLE_CHECKERS[CUR_COLOR == 'B']): return "NONE"
    return ("BLACK", "WHITE")[CUR_COLOR == 'B']    

def CheckWinnerPlus():
    winner = CheckWinner()
    if winner != "NONE":
        if DebOut: print(winner, "WON")
        APP_STATE = "GAME END"

def RunGameTurn():
    global APP_STATE

    if GAME_MODE == "BOT_VS_BOT":
        if PLAYER_COLOR == CUR_COLOR: ChangePlayerColor()

    if CUR_COLOR == PLAYER_COLOR:
        PlayerMove()
    else:
        if GAME_MODE == "BOT" or GAME_MODE == "BOT_VS_BOT": RobotMove()
        elif GAME_MODE == "ONE_PLAYER": ChangePlayerColor()
        elif GAME_MODE == "MULTIPLAYER": OtherPlayerHandler()

    if GAME_MODE == "BOT_VS_BOT":
        if PLAYER_COLOR == CUR_COLOR: ChangePlayerColor()

    CheckWinnerPlus()
    
    pygame.display.flip()
