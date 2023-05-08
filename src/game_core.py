def ChangeTurn():
    global CUR_COLOR
    if CUR_COLOR == WHITE_CHECKER:
        CUR_COLOR = BLACK_CHECKER[:]
    else:
        CUR_COLOR = WHITE_CHECKER[:]

def ChangePlayerColor():
    global PLAYER_COLOR
    if PLAYER_COLOR == WHITE_CHECKER:
        PLAYER_COLOR = BLACK_CHECKER
    else:
        PLAYER_COLOR = WHITE_CHECKER

def UpdateExistingCheckers():
    global EXISTING_CHECKERS
    EXISTING_CHECKERS = [[], []]
    for i in range(8):
        for j in range(8):
            if STATE[i][j][1] != NO_CHECKER:
                if STATE[i][j][1] == WHITE_CHECKER:
                    EXISTING_CHECKERS[0].append((i, j))
                if STATE[i][j][1] == BLACK_CHECKER:
                    EXISTING_CHECKERS[1].append((i, j))

def ResetState(is_black=False):
    global STATE
    global PLAYER_COLOR
    global CUR_COLOR
    global SELECTED_CHECKER
    global AVALIBLE_CELLS
    global IS_EATEN
    global IS_SELECT_LOCKED
    STATE = []
    SELECTED_CHECKER = DEFAULT_SELECTED_CHECKER[:]
    AVALIBLE_CELLS = []
    IS_EATEN = False
    IS_SELECT_LOCKED = False
    PLAYER_COLOR = WHITE_CHECKER[:]
    CUR_COLOR = WHITE_CHECKER[:]
    for i in range(8):
        STATE.append([])
        for j in range(8):
            STATE[i].append([WHITE_CELL[:], NO_CHECKER[:], False])
            if ((i + j) % 2):
                STATE[i][j][0] = BLACK_CELL[:]

    for i in range(24):
        if (((i // 8) + (i % 8)) % 2):
            STATE[i // 8][i % 8][1] = BLACK_CHECKER[:]
            STATE[(63 - i) // 8][(63 - i) % 8][1] = WHITE_CHECKER[:]

    if (is_black): ChangePlayerColor()

def PutChecker():
    global SELECTED_CHECKER
    global AVALIBLE_CELLS
    global IS_EATEN
    if IS_SELECT_LOCKED:
        print("Selection locked, cant put checker")
        return
    ReDrawItem(*SELECTED_CHECKER)
    for pos in AVALIBLE_CELLS:
        ReDrawItem(*pos)
    
    SELECTED_CHECKER = DEFAULT_SELECTED_CHECKER[:]
    AVALIBLE_CELLS = []
    IS_EATEN = False
    

def AvalibleTiles(i, j, eating_required=False, forbidden_koef=(0, 0)):
    global AVALIBLE_CELLS
    global IS_EATEN

    #PutChecker() SELECTED_CHECKER = (i, j)

    cur_col = STATE[i][j][1]
    simple_move_i_koef = -1 + 2 * (cur_col == BLACK_CHECKER)
    avalible_length = 1 + 6 * (STATE[i][j][2])
    AVALIBLE_CELLS = []
    IS_EATEN = False
    for i_koef in (-1, 1):
        for j_koef in (-1, 1):
            if (i_koef, j_koef) == forbidden_koef: continue
            eaten = False
            for length in range(1, avalible_length + 1):
                new_i = i + i_koef * length
                new_j = j + j_koef * length
                if (0 <= new_i <= 7) and (0 <= new_j <= 7):
                    if STATE[new_i][new_j][1] == NO_CHECKER:
                        if (eating_required <= eaten) and ((STATE[i][j][2]) or (i_koef == simple_move_i_koef)):
                            AVALIBLE_CELLS.append((new_i, new_j))
                    elif STATE[new_i][new_j][1] != cur_col and (0 <= new_i + i_koef <= 7) and (0 <= new_j + j_koef <= 7) and STATE[new_i + i_koef][new_j + j_koef][1] == NO_CHECKER:
                        AVALIBLE_CELLS.append((new_i + i_koef, new_j + j_koef))
                        eaten = True
                        IS_EATEN = True
                    else: break
                else: break

def SelectChecker(i, j, forbidden_koef=(0, 0), show=True):
    global SELECTED_CHECKER
    if IS_SELECT_LOCKED and (i, j) != SELECTED_CHECKER: print("LOCKED, YOU CANT SELECT ANOTHER"); return
    if CUR_COLOR != STATE[i][j][1]: print("IT ISNT YOUR COLOR"); return

    PutChecker()

    SELECTED_CHECKER = (i, j)
    if show:
        DrawCell(i, j, col=SELECTED_CELL)
        DrawChecker(i, j, kf=CHECKER_SELECTED_KOEF)
    
    if not (i, j) in AVALIBLE_CHECKERS[CUR_COLOR == BLACK_CHECKER]: print("THIS CHECKER CANT MOVE", (i, j), AVALIBLE_CHECKERS[CUR_COLOR == BLACK_CHECKER]); return

    AvalibleTiles(i, j, forbidden_koef=forbidden_koef)
    if IS_EATEN: AvalibleTiles(i, j, eating_required=True, forbidden_koef=forbidden_koef)
    if show:
        for pos in AVALIBLE_CELLS:
            DrawCell(*pos, col=HIGHLIGHTED_CELL)
            DrawChecker(*pos)

def UpdateAvalibleCheckers():
    global AVALIBLE_CHECKERS
    global AVALIBLE_CELLS
    global IS_EATEN
    bkp = (AVALIBLE_CELLS[:], IS_EATEN)
    AVALIBLE_CHECKERS = [[], []]
    for i in range(2):
        eaten = False
        for checker in EXISTING_CHECKERS[i]:
            AvalibleTiles(*checker)
            if eaten:
                if IS_EATEN:
                    AVALIBLE_CHECKERS[i].append(checker[:])
            elif len(AVALIBLE_CELLS) != 0:
                if IS_EATEN:
                    eaten = True
                    AVALIBLE_CHECKERS[i] = []
                AVALIBLE_CHECKERS[i].append(checker[:])
    AVALIBLE_CELLS, IS_EATEN = bkp
                
def UpdateCheckersState():
    UpdateExistingCheckers()
    UpdateAvalibleCheckers()

def Move(i, j):
    global STATE
    global IS_SELECT_LOCKED
    if not (i, j) in AVALIBLE_CELLS: print("Why did you press here?"); return
    IS_SELECT_LOCKED = False
    pygame.mixer.Sound.play(random.choice(CHESS_SOUNDS))
    s_i, s_j = SELECTED_CHECKER
    cur_col = STATE[s_i][s_j][1]
    is_king = STATE[s_i][s_j][2]
    STATE[i][j][1] = cur_col
    STATE[i][j][2] = is_king
    ReDrawItem(i, j)
    STATE[s_i][s_j][1] = NO_CHECKER
    ReDrawItem(s_i, s_j)
    if i == 7 * (cur_col == BLACK_CHECKER):
        STATE[i][j][2] = True

    i_koef = 1 - 2 * (i < s_i)
    j_koef = 1 - 2 * (j < s_j)
    steps = 1
    while (s_i + i_koef * steps != i):
        STATE[s_i + i_koef * steps][s_j + j_koef * steps][1] = NO_CHECKER
        ReDrawItem(s_i + i_koef * steps, s_j + j_koef * steps)
        steps += 1

    UpdateCheckersState()
    
    if IS_EATEN:
        SelectChecker(i, j, forbidden_koef=(-i_koef, -j_koef), show=(PLAYER_COLOR == CUR_COLOR))
        if IS_EATEN:
            IS_SELECT_LOCKED = True
            print("I locked you")
        else:
            ChangeTurn()
            PutChecker()
    else:
        ChangeTurn()
        PutChecker()

def ReverseOrientation(is_redraw_needed=True):
    global REVERSED_ORIENTATION
    REVERSED_ORIENTATION = not REVERSED_ORIENTATION
    if is_redraw_needed:
        DrawField()
        SelectChecker(*SELECTED_CHECKER)

def SyncWithPlayerColor(is_redraw_needed=False):
    if (PLAYER_COLOR == WHITE_CHECKER) == REVERSED_ORIENTATION:
        ReverseOrientation(is_redraw_needed)

def RunGame():
    global APP_STATE
    APP_STATE = "GAME"
    SyncWithPlayerColor()
    UpdateCheckersState()
    DrawField()
    pygame.display.flip()
    
def SetDefaultState():
    ResetState()
    RunGame()
