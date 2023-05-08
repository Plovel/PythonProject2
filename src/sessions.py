def ReadFromFile():
    global SESSIONS
    SESSIONS = []
    tmp = []
    if not os.path.isfile(WORKING_DIR + PATH_TO_SESSIONS_FILE):
        with open(WORKING_DIR + PATH_TO_SESSIONS_FILE, 'w') as file: pass
    with open(WORKING_DIR + PATH_TO_SESSIONS_FILE, 'r') as file:
        for line in file:
            if len(tmp) == 8 and len(tmp[7]) == 8:
                tmp.append(line.strip())
                SESSIONS.append(tmp)
                tmp = []
            else:
                tmp.append([])
                for i in range(8):
                    tmp[-1].append([WHITE_CELL[:], NO_CHECKER[:], False])
                    if ((len(tmp) + (i % 8)) % 2) == 0:
                        tmp[-1][i % 8][0] = BLACK_CELL[:]
                    letter = line[i]
                    if letter == ' ': continue
                    if letter.upper() == letter:
                        tmp[-1][i % 8][2] = True
                    letter = letter.lower()
                    if letter == 'w': tmp[-1][i % 8][1] = WHITE_CHECKER[:]
                    else: tmp[-1][i % 8][1] = BLACK_CHECKER[:]

def WriteToFile():
    with open(WORKING_DIR + PATH_TO_SESSIONS_FILE, 'w') as file:
        for session in SESSIONS:
            for i in range(8):
                for j in range(8):
                    letter = ' '
                    if session[i][j][1] == WHITE_CHECKER: letter = 'w'
                    if session[i][j][1] == BLACK_CHECKER: letter = 'b'
                    if session[i][j][2]: letter = letter.upper()
                    print(letter, end='', file=file)
                print(file=file)
            print(session[8], end='\n', file=file)

def SetFromSessions(ind):
    global STATE
    global PLAYER_COLOR
    global CUR_COLOR
    global IS_SELECT_LOCKED
    global SESSION_IND
    IS_SELECT_LOCKED = False
    STATE = []
    SESSION_IND = ind
    session = SESSIONS[ind]
    for i in range(8):
        STATE.append([])
        for j in range(8):
            STATE[i].append(session[i][j][:])
    st = session[8]
    if (st[0] == 'W'): PLAYER_COLOR = WHITE_CHECKER
    else: PLAYER_COLOR = BLACK_CHECKER
    if (st[1] == 'W'): CUR_COLOR = WHITE_CHECKER
    else: CUR_COLOR = BLACK_CHECKER
    SyncWithPlayerColor()
    UpdateCheckersState()

def CreateNewSession():
    global SESSIONS
    SESSIONS.append([])
    SESSIONS[-1] = [[] for i in range(9)]
    for i in range(8):
        SESSIONS[-1][i] = [[] for j in range(8)]

def DeleteSession(ind):
    if ind != -1: del SESSIONS[ind]

def SaveSession(ind):
    global SESSIONS
    if ind == -1:
        CreateNewSession()
    for i in range(8):
        for j in range(8):
            SESSIONS[ind][i][j] = STATE[i][j][:]
    st = ''
    if PLAYER_COLOR == WHITE_CHECKER: st += 'W'
    else: st += 'B'
    if CUR_COLOR == WHITE_CHECKER: st += 'W'
    else: st += 'B'
    SESSIONS[ind][8] = st
