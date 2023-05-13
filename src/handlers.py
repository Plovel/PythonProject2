AVALIBLE_BUTTONS = {
"MAIN":
'''G - Change game mode
X - shows hotkeys of menus
Tab/Enter navigation avalible
T - Dev/Fun Menu''',
 
"SESSIONS":
'''Esc - Go to main menu
G - Change game mode
N - New session
S - Save sessions to file
R - Read sessions from file
Arrows < > - Change page
[1, 2, 3, 4] - Select Game
O - connect to another player''',
 
"GAME":
'''Esc - Session saving dialog
G - Change game mode
R - Rotate field
S - Save the session
N - save game as new session
Q - Exit to sessions (no saving)
O - accept connection''',

"SETTINGS":
'''Esc - Go to main menu''',
 
"EXITING_GAME":
'''Esc - Back to game''',

"SELECTING_COLOR":
'''Esc - Back to sessions''',

"CONFIG":
'''Esc - back to settings
v or ^ - change value
< or > - change variable
S - save config to file
R - read config from file
D - set default config
E - Manual editing (dangerous)'''
}

def ApplyVar():
    var = BUTTONS[0].text[8:]
    var = GetVar(var)
    var_type = VARS_INFO[var][0]

    val = BUTTONS[1].text.replace('|', '')
    if var_type == "IP":
        if not type(val) == str: ShowText("Unable convert to IP"); return
        try: socket.inet_aton(val)
        except socket.error: ShowText("Not correct IP address"); return
        SetConfig({var:val})
        SetMenu(InitInput.MENU_BKP)
        return
    
    elif var == "COMMAND_TO_EXECUTE":
        SetConfig({var:val})
        if not RUN_COMMAND(COMMAND_TO_EXECUTE):
            ShowText("Something\nbad happened....",
                     **{"col":RED, "txt_col":BLUE})
        return
    elif var_type == "TEXT": SetConfig({var:val})
    
    else:
        try: val = eval(val)
        except: ShowText("Not correct value"); return
        if var_type == "COLORS":
            try: ShowText("Test text", col=BLACK, txt_col=val, timer=0)
            except:
                ShowText("Not correct color")
                SetMenu("CONFIG")
            SetConfig({var:val})
        elif var_type == "NUMBER":
            if int(val) != val or val < 0:
                ShowText("Invalid integer"); return
            SetConfig({var:val})
        else: ShowText("Failed to define variable type"); return
    SetMenu(InitInput.MENU_BKP)


def ShowAvalibleButtons(menu):
    message = AVALIBLE_BUTTONS.get(menu, "DEV DID NOT TELL\nWHAT TO SHOW HERE")
    ShowText(message)

def EmulateButtonPressSound():
    pygame.mixer.Sound.play(random.choice(BUTTON_DOWN_SOUNDS))
    pygame.time.wait(100)
    pygame.mixer.Sound.play(random.choice(BUTTON_UP_SOUNDS))

def PressButton(button):
    action = button.action
    if DebOut: print("ACTIVATED BUTTON", button.text)
    if action == "NONE": return
    if action.startswith("PLAY"): RunSession(int(action[5:]))
    elif action.startswith("SET_MENU"): SetMenu(action[9:])
    elif action.startswith("SET_GAME"): ClearScreen(); RunGame(False)
    elif action == "SETTINGS": SetMenu("SETTINGS")
    elif action == "APPLY_VAR": ApplyVar()
    elif action == "EXIT_APP": ExitApp()
    elif action == "EXIT_APP+": ExitApp()
    elif action == "SHOW_SESSIONS": SetMenu("SESSIONS")
    elif action == "NEW_GAME": ResetGame(); SetMenu("SELECTING_COLOR")
    elif action == "SELECT_WHITE":
        if PLAYER_COLOR != 'W': ChangePlayerColor()
        RunSession(SESSION_IND)
    elif action == "SELECT_BLACK":
        if PLAYER_COLOR != 'B': ChangePlayerColor()
        RunSession(SESSION_IND)
    elif action.startswith("DELETE"):
        DeleteSession(int(action[6:]))
        SetMenu("SESSIONS")
    elif action.endswith("SAVE_SESSION"):
        if GAME_MODE == "MULTIPLAYER": Disconnect()
        if action == "SAVE_SESSION":
            SaveSession(SESSION_IND)
        SetMenu("SESSIONS")

def InputHandler(event):
    char = event.unicode
    if event.key == pygame.K_ESCAPE: SetMenu(InitInput.MENU_BKP); return
    left, right = BUTTONS[1].text.split('|')
    if event.key == pygame.K_BACKSPACE:
        if left: EmulateButtonPressSound(); left = left[:-1]
    elif event.key == pygame.K_LEFT:
        if left:
            EmulateButtonPressSound()
            right = left[-1] + right
            left = left[:-1]
    elif event.key == pygame.K_RIGHT:
        if right:
            EmulateButtonPressSound()
            left += right[0]
            right = right[1:]
    elif char != '|' and char.isascii():
        EmulateButtonPressSound()
        left += char
    BUTTONS[1].text = left + '|' + right
    BUTTONS[1].draw()
    pygame.display.flip()

def GameHandler(event):
    if APP_STATE.endswith("END"): return
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            RunGameTurn()

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE: SetMenu("EXITING_GAME")
        elif event.key == pygame.K_g: ChangeGameMode()
        elif event.key == pygame.K_r:
            ReverseOrientation(True)
            ShowText("Orientation was changed")
        elif event.key == pygame.K_s:
            global SESSION_IND
            SaveSession(SESSION_IND)
            if SESSION_IND == -1: SESSION_IND = len(SESSIONS) - 1
            ShowText("Session Saved", timer=0.3)
        elif event.key == pygame.K_x: ShowAvalibleButtons("GAME")
        elif event.key == pygame.K_q:
            if GAME_MODE == "MULTIPLAYER": Disconnect()
            SetMenu("SESSIONS")
        elif event.key == pygame.K_o:
            if GAME_MODE == "MULTIPLAYER": ShowText("You are connected")
            else: SetMenu("WAITING_FOR_PLAYER True")
        elif event.key == pygame.K_c:
            SaveGameAsNewSession()
            ShowText("Game saved into new session")
            

MENU_HANDLER_BUTTONS_EVENTS = set((pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
                                   pygame.MOUSEMOTION))
def MenuHandler(event):
    global APP_STATE, VAR_IND
    menu = APP_STATE[5:]
    if event.type in MENU_HANDLER_BUTTONS_EVENTS:
        pos = event.pos
        pos = (pos[1], pos[0])
        for button in BUTTONS:
            if button.check_mouse(pos):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    button.press()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    was_pressed = button.pressed
                    if was_pressed:
                        button.unpress()
                        if button.action == "NONE": continue
                        PressButton(button)
                
        pygame.display.flip()
    elif event.type == pygame.KEYDOWN:
        if menu.startswith("INPUT"): InputHandler(event); return
        elif event.key == pygame.K_ESCAPE:
            if menu == "EXITING_GAME": #
                DrawField()
                APP_STATE = "GAME"
                pygame.display.flip()
            elif menu == "SESSIONS": SetMenu("MAIN") #
            elif menu == "SETTINGS": SetMenu("MAIN") #
            elif menu == "CONFIG": SetMenu("SETTINGS") 
            elif menu == "SELECTING_COLOR": SetMenu("SESSIONS") #
            elif menu == "TEST": SetMenu("MAIN") #??
            elif menu == "BIG_BUTTON": SetMenu("TEST") #??
            elif menu.startswith("WAITING_FOR_PLAYER"):
                Disconnect()
                SetMenu(["SESSIONS", "GAME"][IS_OPENING_GAME])
        elif event.key == pygame.K_LEFT:
            if menu == "SESSIONS":
                EmulateButtonPressSound()
                TurnSessionsPage(side='L') #
            elif menu == "CONFIG":
                EmulateButtonPressSound()
                VAR_IND -= 1
                VAR_IND %= len(AVALIBLE_CONFIG_NAMES)
                SetConfigMenu(VAR_IND)
        elif event.key == pygame.K_RIGHT:
            if menu == "SESSIONS":
                EmulateButtonPressSound()
                TurnSessionsPage(side='R') #
            elif menu == "CONFIG":
                EmulateButtonPressSound()
                VAR_IND += 1
                VAR_IND %= len(AVALIBLE_CONFIG_NAMES)
                SetConfigMenu(VAR_IND)
        elif event.key == pygame.K_DOWN:
            if menu == "CONFIG":
                ChangeVal(BUTTONS[0].text, False)
                EmulateButtonPressSound()
                SetConfigMenu(VAR_IND)
        elif event.key == pygame.K_UP:
            if menu == "CONFIG":
                ChangeVal(BUTTONS[0].text, True)
                EmulateButtonPressSound()
                SetConfigMenu(VAR_IND)
        elif event.key == pygame.K_s:
            if menu == "SESSIONS":
                WriteToFile()
                ShowText("Sessions was saved")
                SetMenu("SESSIONS")
            elif menu == "CONFIG":
                res = WriteConfigToFile()
                if not res: ShowText("Config saved")
                else: ShowText("Failed to save config\nReason: " + res)
        elif event.key == pygame.K_r:
            if menu == "SESSIONS":
                ReadFromFile()
                ShowText("Sessions was read")
                SetMenu("SESSIONS")
            elif menu == "CONFIG":
                res = ReadConfigFromFile()
                if not res:
                    SetConfigMenu(VAR_IND)
                    pygame.display.flip()
                    ShowText("Config was read")
                else: ShowText("Failed to read config\nReason: " + res)
        elif event.key == pygame.K_d:
            if menu == "CONFIG":
                SetConfig(DEFAULT_CONFIG)
                SetMenu("CONFIG")
                ShowText("Setted default config")
        elif event.key == pygame.K_g:
            if menu in ("MAIN", "SESSIONS"): ChangeGameMode()
        elif event.key == pygame.K_t:
            if menu == "MAIN":
                SetMenu("TEST")
                #I know it's long string; just leave it
                ShowText("This menu was created\nfor joy of programming\nIt can brake the game", timer=3)
        elif event.key == pygame.K_n:
            if menu == "SESSIONS":
                EmulateButtonPressSound()
                ResetGame()
                SetMenu("SELECTING_COLOR")
        elif event.key == pygame.K_o:
            if menu == "SESSIONS": SetMenu("WAITING_FOR_PLAYER False")
        elif event.key == pygame.K_x:
            ShowAvalibleButtons(menu) #shouldnt be shown in shortcuts
        #elif event.key == pygame.K_b: PressButton(Button(act="EXIT_APP+"))
        elif event.key in KEYS_TO_NUMBERS:
            if menu == "SESSIONS":
                session = SESSIONS_PAGE * 4 + KEYS_TO_NUMBERS[event.key] - 1
                if 0 <= session < len(SESSIONS): RunSession(session)
                elif session == len(SESSIONS):
                    ResetGame()
                    SetMenu("SELECTING_COLOR")
        elif event.key == pygame.K_e:
            if menu == "CONFIG":
                EmulateButtonPressSound()
                SetMenu("INPUT " + BUTTONS[0].text)



###Tab-Enter navigation
class Evnt:
    def __init__(self):
        self.type = pygame.MOUSEMOTION

MM = Evnt()
MBD = Evnt()
MBU = Evnt()

def InitEvents():
    MM.type = pygame.MOUSEMOTION
    MBD.type = pygame.MOUSEBUTTONDOWN
    MBD.button = 1
    MBU.type = pygame.MOUSEBUTTONUP
    MBU.button = 1
InitEvents()

CUR_KEY_IND = 0
SAVED_BUTTONS = []
SELECT_INDEXES = []

EVENTS_TO_ADD = []
def EmulateSelect(ind):
    point = BUTTONS[ind].point[:]
    sz = BUTTONS[ind].size[:]
    center = (point[0] + sz[0] // 2, point[1] + sz[1] // 2)

    new_event = MM
    new_event.pos = center[::-1]
    EVENTS_TO_ADD.append(new_event)

def EmulateMouseDown(ind):
    point = BUTTONS[ind].point[:]
    sz = BUTTONS[ind].size[:]
    center = (point[0] + sz[0] // 2, point[1] + sz[1] // 2)

    new_event = MBD
    new_event.pos = center[::-1]
    EVENTS_TO_ADD.append(new_event)

def EmulateMouseUp(ind):
    point = BUTTONS[ind].point[:]
    sz = BUTTONS[ind].size[:]
    center = (point[0] + sz[0] // 2, point[1] + sz[1] // 2)

    new_event = MBU
    new_event.pos = center[::-1]
    EVENTS_TO_ADD.append(new_event)

def TabNavHandler(event):
    global CUR_KEY_IND
    global SAVED_BUTTONS
    global SELECT_INDEXES
    if len(BUTTONS) == 0: return
    if SAVED_BUTTONS != BUTTONS:
        SAVED_BUTTONS = BUTTONS
        SELECT_INDEXES = []
        for i in range(len(BUTTONS)):
            if BUTTONS[i].mode == "SELECT": SELECT_INDEXES.append(i)
        CUR_KEY_IND = -1
    if len(SELECT_INDEXES) == 0: return
    if event.key == pygame.K_TAB:
        if event.type == pygame.KEYDOWN:
            CUR_KEY_IND += 1
            CUR_KEY_IND %= len(SELECT_INDEXES)
            EmulateSelect(SELECT_INDEXES[CUR_KEY_IND])
    elif event.key == pygame.K_RETURN:
        if event.type == pygame.KEYDOWN:
            if CUR_KEY_IND == -1: CUR_KEY_IND = 0; EmulateSelect(CUR_KEY_IND)
            else: EmulateMouseDown(SELECT_INDEXES[CUR_KEY_IND])
        elif event.type == pygame.KEYUP:
            EmulateMouseUp(SELECT_INDEXES[CUR_KEY_IND])
            if BUTTONS == SAVED_BUTTONS:
                EmulateSelect(SELECT_INDEXES[CUR_KEY_IND])

    pygame.display.update()

