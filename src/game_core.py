SELECTED_CHECKER = -1
AVALIBLE_CELLS = set()
IS_EATEN = False
IS_SELECT_LOCKED = False

EXISTING_CHECKERS = [set(), set()]
AVALIBLE_CHECKERS = [set(), set()]

def ChangeTurn():
    global CUR_COLOR
    if CUR_COLOR == 'W': CUR_COLOR = 'B'
    else: CUR_COLOR = 'W'

def ChangePlayerColor():
    global PLAYER_COLOR
    if PLAYER_COLOR == 'W': PLAYER_COLOR = 'B'
    else: PLAYER_COLOR = 'W'

def UpdateExistingCheckers():
    global EXISTING_CHECKERS
    EXISTING_CHECKERS = [set(), set()]
    for ind in range(64):
        state = STATE[ind]
        if state != ' ': EXISTING_CHECKERS[state.upper() == 'B'].add(ind)

def ResetGame(is_black=False):
    global STATE
    STATE = " b b b bb b b b  b b b b                w w w w  w w w ww w w w "
    
    global PLAYER_COLOR
    global CUR_COLOR
    PLAYER_COLOR = 'W'
    CUR_COLOR = 'W'
    if is_black: PLAYER_COLOR = 'B'
    
    global SELECTED_CHECKER
    global AVALIBLE_CELLS
    global IS_EATEN
    global IS_SELECT_LOCKED
    SELECTED_CHECKER = -1
    AVALIBLE_CELLS = set()
    IS_EATEN = False
    IS_SELECT_LOCKED = False

    global EXISTING_CHECKERS
    global AVALIBLE_CHECKERS
    EXISTING_CHECKERS = [set(), set()]
    AVALIBLE_CHECKERS = [set(), set()]

def PutChecker():
    global SELECTED_CHECKER
    global AVALIBLE_CELLS
    global IS_EATEN
    if IS_SELECT_LOCKED:
        if DebOut: print("Selection locked, cant put checker")
        return
    if SELECTED_CHECKER == -1: return
    
    ReDrawItem(SELECTED_CHECKER)
    for pos in AVALIBLE_CELLS: ReDrawItem(pos)
    
    SELECTED_CHECKER = -1
    AVALIBLE_CELLS = set()
    IS_EATEN = False

def CI(i, j): return (0 <= i <= 7) and (0 <= j <= 7) #CheckIndexes
def AvalibleTiles(ind, eating_required=False, forbidden_koef=(0, 0)):
    global AVALIBLE_CELLS
    global IS_EATEN
    AVALIBLE_CELLS = set()
    IS_EATEN = False

    checker = STATE[ind]
    i, j = ind // 8, ind % 8
    if checker == ' ':
        if DebOut: print("AVALIBLE FOR VOID?")
        return
    simple_move_i_koef = -1 + 2 * (checker.upper() == "B")
    avalible_length = 1 + 6 * (checker.isupper())
    for i_koef in (-1, 1):
        for j_koef in (-1, 1):
            if (i_koef, j_koef) == forbidden_koef: continue
            eaten = False
            for length in range(1, avalible_length + 1):
                new_i, new_j = i + i_koef * length, j + j_koef * length
                if CI(new_i, new_j):
                    new_ind = new_i * 8 + new_j
                    if STATE[new_ind] == ' ':
                        if ((eating_required <= eaten) and
                        (checker.isupper() or (i_koef == simple_move_i_koef))):
                            AVALIBLE_CELLS.add(new_ind)
                    elif STATE[new_ind].upper() != checker.upper():
                        if (CI(new_i + i_koef, new_j + j_koef) and
                        STATE[new_ind + i_koef * 8 + j_koef] == ' '):
                            IS_EATEN = True
                            eaten = True
                            if eating_required:
                                AVALIBLE_CELLS.add(new_ind +
                                                   i_koef * 8 + j_koef)
                            else:
                                AvalibleTiles(ind, eating_required=True,
                                              forbidden_koef=forbidden_koef)
                                return
                        else: break
                    elif STATE[new_ind].upper() == checker.upper(): break
                else: break

def SelectChecker(ind, forbidden_koef=(0, 0), show=True):
    global SELECTED_CHECKER
    if ind == -1: return
    if IS_SELECT_LOCKED and ind != SELECTED_CHECKER:
        if DebOut: print("LOCKED, YOU CANT SELECT ANOTHER")
        return False
    if CUR_COLOR != STATE[ind].upper():
        if DebOut: print("IT ISNT YOUR COLOR")
        return False

    PutChecker()
    SELECTED_CHECKER = ind
    
    if show:
        DrawCell(ind, col=SELECTED_CELL)
        DrawChecker(ind, is_selected=True)
    
    if not ind in AVALIBLE_CHECKERS[CUR_COLOR == 'B']:
        if DebOut: print("THIS CHECKER CANT MOVE")
        return False

    AvalibleTiles(ind, forbidden_koef=forbidden_koef)
    if show:
        for pos in AVALIBLE_CELLS:
            DrawCell(pos, col=HIGHLIGHTED_CELL)
            DrawChecker(pos)
    return True

def UpdateAvalibleCheckers():
    global AVALIBLE_CHECKERS
    global AVALIBLE_CELLS
    global IS_EATEN
    bkp = (set() | AVALIBLE_CELLS, IS_EATEN)
    AVALIBLE_CHECKERS = [set(), set()]
    for i in range(2):
        eaten_req = False
        for checker in EXISTING_CHECKERS[i]:
            AvalibleTiles(checker)
            if eaten_req:
                if IS_EATEN: AVALIBLE_CHECKERS[i].add(checker)
            elif len(AVALIBLE_CELLS) != 0:
                if IS_EATEN:
                    eaten_req = True
                    AVALIBLE_CHECKERS[i] = set()
                AVALIBLE_CHECKERS[i].add(checker)
    AVALIBLE_CELLS, IS_EATEN = bkp
                
def UpdateCheckersState():
    UpdateExistingCheckers()
    UpdateAvalibleCheckers()

def ChangeChecker(ind, checker):
    global STATE
    STATE = STATE[:ind] + checker + STATE[ind + 1:]

def Move(ind, sound=True):
    global IS_SELECT_LOCKED
    if not ind in AVALIBLE_CELLS:
        if DebOut: print("Why did you press here?")
        return False
    IS_SELECT_LOCKED = False

    if sound: pygame.mixer.Sound.play(random.choice(CHESS_SOUNDS))
    checker = STATE[SELECTED_CHECKER]
    if (ind // 8) == 7 * (checker.upper() == 'B'): checker = checker.upper()
    ChangeChecker(ind, checker)
    ReDrawItem(ind)
    ChangeChecker(SELECTED_CHECKER, ' ')
    ReDrawItem(SELECTED_CHECKER)
    

    i_koef = 1 - 2 * (ind // 8 < SELECTED_CHECKER // 8)
    j_koef = 1 - 2 * (ind % 8 < SELECTED_CHECKER % 8)
    cur_pos = SELECTED_CHECKER
    was_eaten = IS_EATEN
    PutChecker()
    while (cur_pos != ind):
        if STATE[cur_pos] != ' ':
            ChangeChecker(cur_pos, ' ')
            ReDrawItem(cur_pos)
        cur_pos += i_koef * 8 + j_koef
    
    UpdateCheckersState()
    
    if was_eaten:
        SelectChecker(ind, forbidden_koef=(-i_koef, -j_koef),
                      show=(PLAYER_COLOR == CUR_COLOR))
        if IS_EATEN:
            IS_SELECT_LOCKED = True
            if DebOut: print("I locked you")
        else:
            ChangeTurn()
            PutChecker()
    else:
        ChangeTurn()
    return True

def ReverseOrientation(is_redraw_needed=True):
    global REVERSED_ORIENTATION
    REVERSED_ORIENTATION = not REVERSED_ORIENTATION
    if is_redraw_needed:
        DrawField()
        SelectChecker(SELECTED_CHECKER)

def SyncWithPlayerColor(is_redraw_needed=False):
    if (PLAYER_COLOR == 'W') == REVERSED_ORIENTATION:
        ReverseOrientation(is_redraw_needed)

def RunGame(sync=True):
    global APP_STATE
    APP_STATE = "GAME"
    UpdateCheckersState()
    if sync: SyncWithPlayerColor(True)
    DrawField()
    SelectChecker(SELECTED_CHECKER)
    pygame.display.flip()
