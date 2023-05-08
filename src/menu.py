def NormalSizeOfButton(txt_fnt, txt_sz, txt):
    text_size = pygame.font.SysFont(txt_fnt, txt_sz).size(txt)
    return (text_size[1] * 150 // 100, text_size[0] * 110 // 100)

def NormalSizeOfButtons(buttons):
    ans = [0, 0]
    for button in buttons:
        button_size = NormalSizeOfButton(button.get("txt_fnt", def_kwargs["txt_fnt"]),
                                         button.get("txt_sz", def_kwargs["txt_sz"]),
                                         button.get("txt", "DEFAULT_TEXT"))
        ans[0] = max(buttons_max_sizes[0], button_size[0])
        ans[1] = max(buttons_max_sizes[1], button_size[1])
    return ans

class Button:

    def __init__(self, pnt=None, sz=(None, None), act="NONE", col=None, cor_col=None, pressed_col=None, c_sz=None, txt="DEFAULT_TEXT", txt_col=WHITE[:], txt_fnt=DEFAULT_FONT, txt_sz=None, mode="BASIC", center=None):
        if col is None:
            if mode == "BASIC": col = TRANSPARENT[:]
            elif mode == "SELECT": col = GREEN[:]
        if cor_col is None:
            if mode == "BASIC": cor_col = col[:]
            elif mode == "SELECT": cor_col = YELLOW[:]
        if pressed_col is None:
            if mode == "BASIC": pressed_col = col[:]
            elif mode == "SELECT": pressed_col = BLUE[:]

        if txt_sz is None and sz == (None, None): txt_sz = DEFAULT_FONT_SIZE
        if not (txt_sz is None) and (sz == (None, None)): sz = NormalSizeOfButton(txt_fnt, txt_sz, txt)
        if not txt_sz is None and ((sz[0] is None) or (sz[1] is None)):
            normal_size = NormalSizeOfButton(txt_fnt, txt_sz, txt)
            if sz[0] is None: sz = (normal_size[0], sz[1])
            if sz[1] is None: sz = (sz[0], normal_size[1])
        if txt_sz is None:
            #todo?
            #if not (sz[])
            txt_sz = DEFAULT_FONT_SIZE
            normal_size = NormalSizeOfButton(txt_fnt, txt_sz, txt)
            if sz[0] is None: sz = (normal_size[0], sz[1])
            if sz[1] is None: sz = (sz[0], normal_size[1])
            
                

        if c_sz is None:
            if mode == "BASIC": c_sz = 0
            elif mode == "SELECT": c_sz = 5

        if (pnt is None) and (center is None): center = (HEIGHT // 2, WIDTH // 2)
        if not (center is None): pnt = (center[0] - sz[0] // 2, center[1] - sz[1] // 2)

        self.mode=mode
        self.point = pnt[:]
        self.size = sz[:]
        self.action = act[:]
        self.color = col[:]
        self.corner_color = cor_col[:]
        self.corner_size = c_sz
        self.text = txt[:]
        self.text_font = txt_fnt
        self.text_color = txt_col[:]
        self.text_size = txt_sz
        self.pressed_color = pressed_col[:]

        self.unselected_color = self.color[:]
        self.pressed = False

    def GetCenter(self):
        return (self.point[0] + self.size[0] // 2, self.point[1] + self.size[1] // 2)

    def draw(self):
        if self.corner_color != TRANSPARENT:
            pygame.draw.rect(screen, self.corner_color, (self.point[1], self.point[0], self.size[1], self.size[0]))
        if self.color != TRANSPARENT:
            pygame.draw.rect(screen,
                             self.color,
                             (self.point[1] + self.corner_size,
                              self.point[0] + self.corner_size,
                              self.size[1] - self.corner_size * 2,
                              self.size[0] - self.corner_size * 2
                              )
                             )
        if self.text_color != TRANSPARENT:
            img = pygame.font.SysFont(self.text_font, self.text_size).render(self.text, True, self.text_color)
            center = self.GetCenter()
            rect = img.get_rect()
            rect.center = (center[1], center[0])
            screen.blit(img, rect.topleft)

    def check_mouse(self, pos):
        is_on_button = (self.point[0] <= pos[0] <= self.point[0] + self.size[0]) and (self.point[1] <= pos[1] <= self.point[1] + self.size[1])
        if not is_on_button: self.pressed = False
        expected_color = (self.unselected_color[:], [self.corner_color[:], self.pressed_color[:]][self.pressed])[is_on_button]
        if expected_color != self.color:
            self.color = expected_color
            self.draw()
        return is_on_button

    def blink(self, timer=0.05):
        self.draw()
        pygame.display.flip()
        time.sleep(timer)

    def press(self):
        if self.mode == "SELECT":
            self.pressed = True
            self.color = self.pressed_color[:]
            self.blink()
    
    def unpress(self):
        if self.mode == "SELECT":
            self.pressed = False
            self.color = self.unselected_color[:]
            self.draw()
            


#menu_tools
def AddButton(*args, **kwargs):
    ##doesnt work
    BUTTONS.append(Button(*args, **kwargs))
    BUTTONS[-1].draw()

def UpdateButton(ind, **kwargs):
    BUTTONS[ind] = Button(BUTTONS[ind].__dict__ | kwargs)
    BUTTONS[ind].draw()

def ClearScreen(screen_col=DEFAULT_CLEAR_SCREEN[:]):
    global BUTTONS
    screen.fill(screen_col)
    BUTTONS = []

def SetSelectMenu(buttons, SPACE=10, COVERAGE=(80, 80), **kwargs):
    def_kwargs = ({"sz":(None, None), "mode":"SELECT"}) | kwargs

    if def_kwargs["sz"][0] is None:
        to_put = (HEIGHT * COVERAGE[0]) // (len(buttons) * 100 + (len(buttons) - 1) * SPACE)
        def_kwargs["sz"] = (to_put, def_kwargs["sz"][1])
    if def_kwargs["sz"][1] is None:
        to_put = WIDTH * COVERAGE[1] // 100
        def_kwargs["sz"] = (def_kwargs["sz"][0], to_put)

    center = [(HEIGHT - (len(buttons) - 1) * def_kwargs["sz"][0] * (100 + SPACE) // 100) // 2, WIDTH // 2]
    for button in buttons:
        AddButton(**(def_kwargs | ({"center": center} | button)))
        center[0] += (def_kwargs["sz"][0] * (100 + SPACE)) // 100

GLOBAL_SURFACE = pygame.Surface((WIDTH, HEIGHT)) # I TOTALLY DONT KNOW WHY DOUBLE-CALLING SHOWTEXT (with the surface declared as local) SETS SCREEN BLACK!!!!
def ShowText(text, timer=1, **kwargs):
    GLOBAL_SURFACE.blit(screen, (0, 0))

    kwargs.setdefault("col", BLUE[:])
    kwargs.setdefault("txt_col", YELLOW[:])
    kwargs.setdefault("txt_sz", DEFAULT_FONT_SIZE)
    kwargs.setdefault("txt_fnt", DEFAULT_FONT)
    lines = text.split('\n')
    buttons_args = [{"txt":line} | kwargs for line in lines]
    req_space = [0, 0]
    for button in buttons_args:
        normal_size = NormalSizeOfButton(txt_fnt=button["txt_fnt"], txt_sz=button["txt_sz"], txt=button["txt"])
        req_space[0] += normal_size[0]
        req_space[1] = max(normal_size[1], req_space[1])

    add = 0 #in %
    req_space[0] += HEIGHT * add // 100
    #print(req_space[0])
    req_space[1] += WIDTH * add // 100
    
    corner_size = 5
    substrate_pos = (HEIGHT // 2 - req_space[0] // 2 - corner_size, WIDTH // 2 - req_space[1] // 2 - corner_size)
    pygame.draw.rect(screen, WHITE[:], (*substrate_pos[::-1], req_space[1] + 2 * corner_size, req_space[0] + 2 * corner_size))
    
    SetSelectMenu(buttons_args, SPACE=0, sz=(req_space[0] // len(lines), req_space[1]), mode="BASIC")
    pygame.display.flip()
    time.sleep(timer)

    for i in range(len(lines)): del BUTTONS[-1]
    screen.blit(GLOBAL_SURFACE, (0, 0))
    pygame.display.flip()
#menu_tools



def SetExitingGameMenu():
    SetSelectMenu(({"txt":"Save the session?", "mode":"BASIC"},
                   {"act":"SAVE_SESSION", "txt":"Yes"},
                   {"act":"DONT_SAVE_SESSION", "txt":"No"}))

def SetMainMenu():
    global SESSIONS_PAGE
    SESSIONS_PAGE = 0
    ClearScreen()
    SetSelectMenu(({"txt":"Ahahah Checkers...", "txt_col":BLUE[:], "col":DEFAULT_CLEAR_SCREEN[:], "cor_col":DEFAULT_CLEAR_SCREEN[:], "mode":"BASIC"},
                   {"act":"SHOW_SESSIONS", "txt":"Play"},
                   {"act":"SETTINGS", "txt":"Settings"},
                   {"act":"EXIT_APP", "txt":"Exit"}))

def ShowSettings():
    SetSelectMenu(({"txt":"Back to main menu", "act":"SET_MENU MAIN"}, {"txt":"Change settings", "act":"SET_MENU "}, {"txt":"Change Username", "act":"SET_MENU INPUT USERNAME"}))

#working with sessions
def RunSession(ind):
    global APP_STATE
    ClearScreen()
    SetFromSessions(ind)
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
    plus_sz = 100 #idk too
    if ind != -1:
        SetFromSessions(ind)
        DrawField(cell_sz=cell_sz, pos=point)
        sz = (corner[0], cell_sz * 4)
        center = [point[0] + cell_sz * 8 + sz[0] // 2, point[1] + sz[1] // 2]
        AddButton(center=center, sz=sz, act="PLAY " + str(ind), txt="Play " + str(ind + 1), txt_sz=txt_sz, mode="SELECT")
        center[1] += sz[1]
        AddButton(center=center, sz=sz, act="DELETE " + str(ind), txt="Delete " + str(ind + 1), txt_sz=txt_sz, col=RED[:], mode="SELECT")
    else:
        AddButton(point, (cell_sz * 8, cell_sz * 8), act="NEW_GAME", txt="+", txt_col=RED[:], txt_sz=plus_sz, mode="SELECT")
    SESSION_IND = -1
    pygame.display.flip()

def ShowSessionPage():
    global SESSIONS_PAGE
    ClearScreen()
    if not (0 <= SESSIONS_PAGE <= len(SESSIONS) // 4): SESSIONS_PAGE = 0
    for i in range(4 * SESSIONS_PAGE, min(4 * (SESSIONS_PAGE + 1), len(SESSIONS) + 1)):
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

def SelectingColour():
    SetSelectMenu(({"txt":"Choose color", "mode":"BASIC"},
                   {"act":"SELECT_WHITE", "txt":"White", "mode":"SELECT"},
                   {"act":"SELECT_BLACK", "txt":"Black", "mode":"SELECT"})
                  )
#working with sessions



def ShowTestMenu():
    ShowText("Test menu I guess...")
    ClearScreen()
    pygame.display.flip()
    ShowText("Test1\nTest2\n3\n4\n6\n8\n9\n")
    ClearScreen()
    AddButton(**{"txt":"BUTTON", "act":"SET_MENU MAIN", "mode":"SELECT"})
    pygame.display.flip()

def InitInput():
    SetSelectMenu(({"txt":"Editing " + APP_STATE[11:] + " value", "mode":"BASIC"}, {"txt":"", "mode":"BASIC", "col":BLUE[:]}, {"txt":"Apply", "act":"APPLY_VAR"}))

def SetMenu(menu, additional=None):
    global APP_STATE
    APP_STATE = "MENU " + menu
    if menu == "TEST": ShowTestMenu(); return
    ClearScreen()
    if menu.startswith("INPUT"): InitInput()
    if menu == "MAIN": SetMainMenu()
    elif menu == "EXITING_GAME": SetExitingGameMenu()
    elif menu == "SESSIONS": ShowSessionPage()
    elif menu == "SETTINGS": ShowSettings()
    elif menu == "SELECTING_COLOR": SelectingColour()
    pygame.display.update()

def PressButton(button):
    global PLAYER_COLOR
    action = button.action
    if action == "NONE": return
    if action.startswith("PLAY"): RunSession(int(action[5:]))
    elif action.startswith("SET_MENU"): SetMenu(action[9:])
    elif action == "SETTINGS": SetMenu("SETTINGS")
    elif action == "APPLY_VAR":
        var = BUTTONS[0].text[8:-6]
        exec("global " + var + "; " + var + " = " + BUTTONS[1].text)
        print(var, "WAS CHANGED TO", BUTTONS[1].text)
        print(WHITE_CHECKER)
        SetMenu("SETTINGS")
    elif action == "EXIT_APP": ExitApp()
    elif action == "SHOW_SESSIONS": SetMenu("SESSIONS")
    elif action == "NEW_GAME": ResetState(); SetMenu("SELECTING_COLOR")
    elif action == "SELECT_WHITE":
        PLAYER_COLOR = WHITE_CHECKER[:]
        RunGame()
    elif action == "SELECT_BLACK":
        PLAYER_COLOR = BLACK_CHECKER[:]
        RunGame()
    elif action.startswith("DELETE"):
        DeleteSession(int(action[6:]))
        SetMenu("SESSIONS")
    elif action.endswith("SAVE_SESSION"):
        if action == "SAVE_SESSION":
            SaveSession(SESSION_IND)
        SetMenu("SESSIONS")

def ChangeGameMode():
    global GAME_MODE
    if GAME_MODE == "BOT":
        GAME_MODE = "BOT_VS_BOT"
        if APP_STATE.startswith("GAME"):
            PutChecker()
            if PLAYER_COLOR == CUR_COLOR: ChangePlayerColor()
    elif GAME_MODE == "BOT_VS_BOT":
        GAME_MODE = "ONE_PLAYER"
    elif GAME_MODE == "ONE_PLAYER":
        GAME_MODE = "BOT"
        if APP_STATE.startswith("GAME"):
            if CUR_COLOR != PLAYER_COLOR: ChangePlayerColor()
            SyncWithPlayerColor(True)
    message = "Mode changed to " + GAME_MODE.lower()
    if (GAME_MODE == "BOT_VS_BOT"):
        message = message + "\n(click to make next move)"
    ShowText(message)

AVALIBLE_BUTTONS = {"MAIN":"G - Change game mode",
                    "SESSIONS":"Esc - Go to main menu\nG - Change game mode\nN - New session\nS - Save sessions to file\nR - Read sessions from file\nArrows < > - Change page\n[1, 2, 3, 4] - Select Game",
                    "GAME":"Esc - Session saving dialog\nG - Change game mode\nR - Rotate field\nS - Save the session\nQ - Exit to sessions (no saving)",
                    "SETTINGS":"Esc - Go to main menu",
                    "EXITING_GAME":"Esc - Back to game",
                    "SELECTING_COLOR":"Esc - Back to sessions"
                    }

def ShowAvalibleButtons(menu):
    message = AVALIBLE_BUTTONS.get(menu, "РАЗРАБОТЧИК EBLAN\nКНОПОЧКИ НЕ ПРОСТАВИЛ")
    ShowText(message, timer=message.count('\n') * 0.5 + 0.5)

