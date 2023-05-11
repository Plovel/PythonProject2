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
            try: SOCKET_S.send(("MOVE_" + str(ind) + ' ').encode())
            except: Disconnect()
    else:
        if SelectChecker(ind) and GAME_MODE == "MULTIPLAYER":
            try: SOCKET_S.send(("SELECT_" + str(ind) + ' ').encode())
            except: Disconnect()

def PlayerMove(): ClickFunc(pygame.mouse.get_pos())

def RobotMove():
    time.sleep(0.2 * (GAME_MODE != "BOT_VS_BOT"))
    if not IS_SELECT_LOCKED:
        time.sleep(len(AVALIBLE_CHECKERS[CUR_COLOR == 'B']) * 0.1 * (GAME_MODE != "BOT_VS_BOT"))
        checker = random.choice(tuple(AVALIBLE_CHECKERS[CUR_COLOR == 'B']))
        SelectChecker(checker, show=False)
    Move(random.choice(tuple(AVALIBLE_CELLS)))

def CheckWinner():
    if bool(AVALIBLE_CHECKERS[CUR_COLOR == 'B']): return "NONE"
    return ("BLACK", "WHITE")[CUR_COLOR == 'B']    

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

    winner = CheckWinner()
    if winner != "NONE":
        print(winner, "WON")
        APP_STATE = "GAME END"
    
    pygame.display.flip()
