SESSIONS = []
SESSION_IND = -1
SESSIONS_PAGE = 0

PATH_TO_SESSIONS = "checkers_sessions.txt"

#doesnt use buttons
def ReadFromFile():
    global SESSIONS
    SESSIONS = []
    cur_state = ""
    if not os.path.isfile(WD + PATH_TO_SESSIONS):
        with open(WD + PATH_TO_SESSIONS, 'w', encoding="utf-8") as file: pass
    with open(WD + PATH_TO_SESSIONS, 'r', encoding="utf-8") as file:
        for line in file:
            line = line.rstrip('\n')
            cur_state += line
            if len(cur_state) == 66:
                SESSIONS.append(cur_state)
                cur_state = ""

def WriteToFile():
    with open(WD + PATH_TO_SESSIONS, 'w', encoding="utf-8") as file:
        for session in SESSIONS:
            for i in range(8): print(session[i * 8 : (i + 1) * 8], file=file)
            print(session[64:], file=file)

def SetFromSessions(ind):
    global STATE
    global PLAYER_COLOR
    global CUR_COLOR
    global IS_SELECT_LOCKED
    global SESSION_IND
    
    IS_SELECT_LOCKED = False
    SESSION_IND = ind
    session = SESSIONS[ind]
    STATE = session[:64]
    PLAYER_COLOR = session[64]
    CUR_COLOR = session[65]
    SyncWithPlayerColor()
    UpdateCheckersState()

def DeleteSession(ind):
    if ind != -1: del SESSIONS[ind]

def SaveGameAsNewSession():
    SESSIONS.append(STATE[:] + PLAYER_COLOR + CUR_COLOR)

def SaveSession(ind):
    if ind == -1: SESSIONS.append("")
    SESSIONS[ind] = STATE[:] + PLAYER_COLOR + CUR_COLOR
#doesnt use buttons

def RunSession(ind):
    global APP_STATE
    ClearScreen()
    if ind == -1: ResetGame(PLAYER_COLOR == 'B'); RunGame()
    else: SetFromSessions(ind)
    DrawField()
    APP_STATE = "GAME"
    pygame.display.flip()

def DrawSession(num, ind):
    global SESSION_IND
    i_diff = HEIGHT // 2
    j_diff = WIDTH // 2
    corner = (HEIGHT // 20, WIDTH // 20)
    cell_sz = (i_diff - corner[0] * 2) // 8
    point = (corner[0] + i_diff * (num // 2), corner[1] + j_diff * (num % 2))
    txt_sz = 30 #idk
    plus_sz = 45 #idk too
    if ind != -1:
        SetFromSessions(ind)
        DrawField(cell_sz=cell_sz, pos=point)
        sz = (corner[0], cell_sz * 4)
        center = [point[0] + cell_sz * 8 + sz[0] // 2,
                  point[1] + sz[1] // 2]
        AddButton(center=center, sz=sz, act="PLAY " + str(ind),
                  txt="Play " + str(ind + 1), txt_sz=txt_sz, mode="SELECT")
        center[1] += sz[1]
        AddButton(center=center, sz=sz, act="DELETE " + str(ind),
                  txt="Delete " + str(ind + 1), txt_sz=txt_sz,
                  col=RED[:], mode="SELECT")
    else:
        AddButton(point, (cell_sz * 8, cell_sz * 8), act="NEW_GAME",
                  txt="New session", txt_col=RED[:], txt_sz=plus_sz,
                  mode="SELECT")
    SESSION_IND = -1
    pygame.display.flip()

def ShowSessionPage():
    global SESSIONS_PAGE
    ClearScreen()
    if not (0 <= SESSIONS_PAGE <= len(SESSIONS) // 4): SESSIONS_PAGE = 0
    for i in range(4 * SESSIONS_PAGE,
                   min(4 * (SESSIONS_PAGE + 1), len(SESSIONS) + 1)):
        if i == len(SESSIONS):
            DrawSession(i % 4, -1)
            break
        DrawSession(i % 4, i)

def TurnSessionsPage(side):
    global SESSIONS_PAGE
    if side == 'L':
        if SESSIONS_PAGE - 1 >= 0:
            SESSIONS_PAGE -= 1
            ShowSessionPage()
    elif side == 'R':
        if (SESSIONS_PAGE + 1) * 4 <= len(SESSIONS):
            SESSIONS_PAGE += 1
            ShowSessionPage()
