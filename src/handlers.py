AVALIBLE_BUTTONS = {"MAIN":"G - Change game mode\nM - Go here from any menu\nT - Dev/Fun Menu",
                    "SESSIONS":"Esc - Go to main menu\nG - Change game mode\nN - New session\nS - Save sessions to file\nR - Read sessions from file\nArrows < > - Change page\n[1, 2, 3, 4] - Select Game\nO - connect to another player",
                    "GAME":"Esc - Session saving dialog\nG - Change game mode\nR - Rotate field\nS - Save the session\nN - save game as new session\nQ - Exit to sessions (no saving)\nO - accept connection",
                    "SETTINGS":"Esc - Go to main menu",
                    "EXITING_GAME":"Esc - Back to game",
                    "SELECTING_COLOR":"Esc - Back to sessions",
                    "CONFIG":"Esc - back to settings\nv or ^ - change value\n< or > - change variable\nS - save config to file\nR - read config from file\nD - set default config\nE - Manual editing (dangerous)"
                    }

def ShowAvalibleButtons(menu):
    message = AVALIBLE_BUTTONS.get(menu, "DEV DID NOT TELL\nWHAT TO SHOW HERE")
    ShowText(message)

def EmulateButtonPressSound():
    pygame.mixer.Sound.play(random.choice(BUTTON_DOWN_SOUNDS))
    pygame.time.wait(100)
    pygame.mixer.Sound.play(random.choice(BUTTON_UP_SOUNDS))

def PressButton(button):
    global PLAYER_COLOR
    action = button.action
    #print("ACTIVATED BUTTON", button.text)
    if action == "NONE": return
    if action.startswith("PLAY"): RunSession(int(action[5:]))
    elif action.startswith("SET_MENU"): SetMenu(action[9:])
    elif action.startswith("SET_GAME"): ClearScreen(); RunGame(False)
    elif action == "SETTINGS": SetMenu("SETTINGS")
    elif action == "APPLY_VAR":
        var = BUTTONS[0].text[8:]
        try: val = eval(BUTTONS[1].text.replace('|', ''))
        except: ShowText("Trash value..."); return;
        if var == "COMMAND_TO_EXECUTE":
            globals()[var] = val
            if not RUN_COMMAND(COMMAND_TO_EXECUTE): ShowText("Ahahaahahahh something\nbad happened....", **{"col":RED, "txt_col":BLUE})
        else:
            try: SetConfig({var:val})
            except: ShowText("Something went wrong")
        SetMenu(InitInput.MENU_BKP)
    elif action == "EXIT_APP": ExitApp()
    elif action == "EXIT_APP+": ExitApp()
    elif action == "SHOW_SESSIONS": SetMenu("SESSIONS")
    elif action == "NEW_GAME": ResetGame(); SetMenu("SELECTING_COLOR")
    elif action == "SELECT_WHITE":
        PLAYER_COLOR = 'W'
        RunSession(SESSION_IND)
    elif action == "SELECT_BLACK":
        PLAYER_COLOR = 'B'
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
        if left: EmulateButtonPressSound(); right = left[-1] + right; left = left[:-1]
    elif event.key == pygame.K_RIGHT:
        if right: EmulateButtonPressSound(); left += right[0]; right = right[1:]
    elif char != '|' and char.isascii(): EmulateButtonPressSound(); left += char
    BUTTONS[1].text = left + '|' + right
    BUTTONS[1].draw()
    pygame.display.flip()

def GameHandler(event):
    if APP_STATE.endswith("END"): return
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            RunGameTurn()

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE: SetMenu("EXITING_GAME") #
        elif event.key == pygame.K_g: ChangeGameMode() #
        elif event.key == pygame.K_r: ReverseOrientation(True); ShowText("Orientation was changed") #
        elif event.key == pygame.K_s: #
            global SESSION_IND
            SaveSession(SESSION_IND)
            if SESSION_IND == -1: SESSION_IND = len(SESSIONS) - 1
            ShowText("Session Saved", timer=0.3)
        elif event.key == pygame.K_x: ShowAvalibleButtons("GAME") #
        elif event.key == pygame.K_q:
            if GAME_MODE == "MULTIPLAYER": Disconnect()
            SetMenu("SESSIONS") #
        elif event.key == pygame.K_o: SetMenu("WAITING_FOR_PLAYER True") #
        elif event.key == pygame.K_c: SaveGameAsNewSession(); ShowText("Game saved into new session") #
            

MENU_HANDLER_BUTTONS_EVENTS = set((pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION))
def MenuHandler(event):
    global APP_STATE
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
        elif event.key == pygame.K_m: SetMenu("MAIN") #??
        elif event.key == pygame.K_LEFT:
            if menu == "SESSIONS":
                EmulateButtonPressSound()
                TurnSessionsPage(side='L') #
            elif menu == "CONFIG":
                EmulateButtonPressSound()
                SetConfigMenu((AVALIBLE_CONFIG_NAMES.index(BUTTONS[0].text) - 1) % len(AVALIBLE_CONFIG_NAMES))
        elif event.key == pygame.K_RIGHT:
            if menu == "SESSIONS":
                EmulateButtonPressSound()
                TurnSessionsPage(side='R') #
            elif menu == "CONFIG":
                EmulateButtonPressSound()
                SetConfigMenu((AVALIBLE_CONFIG_NAMES.index(BUTTONS[0].text) + 1) % len(AVALIBLE_CONFIG_NAMES))
        elif event.key == pygame.K_DOWN:
            if menu == "CONFIG":
                ind = AVALIBLE_CONFIG_NAMES.index(BUTTONS[0].text)
                VarPrevVal(ind)
                EmulateButtonPressSound()
                SetConfigMenu(ind)
        elif event.key == pygame.K_UP:
            if menu == "CONFIG":
                ind = AVALIBLE_CONFIG_NAMES.index(BUTTONS[0].text)
                VarNextVal(ind)
                EmulateButtonPressSound()
                SetConfigMenu(ind)
        elif event.key == pygame.K_s:
            if menu == "SESSIONS": #
                WriteToFile()
                ShowText("Sessions was saved")
                SetMenu("SESSIONS")
            elif menu == "CONFIG": #
                res = WriteConfigToFile()
                if not res: ShowText("Config saved")
                else: ShowText("Failed to save config\nReason: " + res)
        elif event.key == pygame.K_r:
            if menu == "SESSIONS": #
                ReadFromFile()
                ShowText("Sessions was read")
                SetMenu("SESSIONS")
            elif menu == "CONFIG": #
                res = ReadConfigFromFile()
                if not res: ShowText("Config was read")
                else: ShowText("Failed to read config\nReason: " + res)
        elif event.key == pygame.K_d:
            if menu == "CONFIG": SetConfig(DEFAULT_CONFIG); SetMenu("CONFIG"); ShowText("Setted default config")
        elif event.key == pygame.K_g:
            if menu in ("MAIN", "SESSIONS"): ChangeGameMode() #
        elif event.key == pygame.K_t:
            SetMenu("TEST") #
            ShowText("This menu was created\nfor joy of programming\nIt can brake the game", timer=3)
        elif event.key == pygame.K_n: #
            if menu == "SESSIONS": EmulateButtonPressSound(); ResetGame(); SetMenu("SELECTING_COLOR")
        elif event.key == pygame.K_o:
            if menu == "SESSIONS": SetMenu("WAITING_FOR_PLAYER False")
        elif event.key == pygame.K_x: ShowAvalibleButtons(menu) #shouldnt be shown in shortcuts
        elif event.key == pygame.K_b: PressButton(Button(act="EXIT_APP"))
        elif event.key in KEYS_TO_NUMBERS: #
            if menu == "SESSIONS":
                session = SESSIONS_PAGE * 4 + KEYS_TO_NUMBERS[event.key] - 1
                if 0 <= session < len(SESSIONS): RunSession(session)
                elif session == len(SESSIONS): ResetState(); SetMenu("SELECTING_COLOR")
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
        elif event.type == pygame.KEYUP: EmulateMouseUp(SELECT_INDEXES[CUR_KEY_IND])

    pygame.display.update()

