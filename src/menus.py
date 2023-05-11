def SelectingColour():
    SetSelectMenu(({"txt":"Choose color", "mode":"BASIC"},
                   {"act":"SELECT_WHITE", "txt":"White", "txt_col":WHITE_CHECKER[:], "col":BLACK_CELL[:], "mode":"SELECT"},
                   {"act":"SELECT_BLACK", "txt":"Black", "txt_col":BLACK_CHECKER[:], "col":BLACK_CELL[:], "mode":"SELECT"})
                  )

def SetExitingGameMenu():
    message = ["Save", "Rewrite"][SESSION_IND != -1] + " the session?"
    SetSelectMenu(({"txt":message, "mode":"BASIC"},
                   {"act":"SAVE_SESSION", "txt":"Yes"},
                   {"act":"DONT_SAVE_SESSION", "txt":"No", "col":RED}))

def SetMainMenu():
    globals()['SESSIONS_PAGE'] = 0
    ClearScreen()
    SetSelectMenu(({"txt":"CheckersOS...", "txt_col":RED, "col":DEFAULT_CLEAR_SCREEN[:], "cor_col":DEFAULT_CLEAR_SCREEN[:], "mode":"BASIC"},
                   {"txt":"Play", "act":"SHOW_SESSIONS"},
                   {"txt":"Settings", "act":"SETTINGS", "col":WHITE[:], "txt_col":ORANGE[:]},
                   {"txt":"Exit" + "+Rebuild+Relaunch" * REBUILD_AND_RUN_ON_EXITING, "act":"EXIT_APP", "col":RED[:], "txt_col":BLACK[:]}))

def ShowSettings():
    SetSelectMenu(({"txt":"Edit config", "act":"SET_MENU CONFIG", "col":WHITE, "txt_col":ORANGE},
                   {"txt":"Change username", "act":"SET_MENU INPUT USERNAME", "col":GREY, "txt_col":ORANGE},
                   {"txt":"Set my ip", "act":"SET_MENU INPUT HOST", "col":GREY, "txt_col":ORANGE},
                   {"txt":"Set other player ip", "act":"SET_MENU INPUT IP_TO_CONNECT", "col":GREY, "txt_col":ORANGE},
                   {"txt":"Back to main menu", "act":"SET_MENU MAIN"}))

def ChangeGameMode():
    global GAME_MODE
    if GAME_MODE == "MULTIPLAYER": ShowText("Unable to change mode"); return
    message = 'Game mode was changed to\n'
    if GAME_MODE == "BOT":
        GAME_MODE = "BOT_VS_BOT"
        message += "Bot vs Bot (click to make a move)"
        if APP_STATE.startswith("GAME"):
            PutChecker()
            if PLAYER_COLOR == CUR_COLOR: ChangePlayerColor()
    elif GAME_MODE == "BOT_VS_BOT":
        GAME_MODE = "ONE_PLAYER"
        message += "Manual"
    elif GAME_MODE == "ONE_PLAYER":
        GAME_MODE = "BOT"
        message += "Player vs Bot"
        if APP_STATE.startswith("GAME"):
            if CUR_COLOR != PLAYER_COLOR: ChangePlayerColor()
            SyncWithPlayerColor(True)
    ShowText(message, timer=3)

def ShowPlayerWaiting(is_opening):
    global IS_OPENING_GAME, timer_for_opening
    IS_OPENING_GAME = is_opening
    timer_for_opening = time.time()
    if is_opening: DrawField()
    SetSelectMenu(({"txt":["Trying to connect", "Waiting for player"][is_opening], "col":BLUE, "cor_col":GREEN , "mode":"BASIC"}, {"txt":"???", "col":BLUE, "cor_col":RED, "mode":"BASIC"}), SPACE=10, COVERAGE=(20, 60))

COMMAND_TO_EXECUTE = "echo ahaha"
changing_variable = "WHITE_CHECKER"
def ShowTestMenu():
    ClearScreen()
    SetSelectMenu(({"txt":"Change " + changing_variable, "act":"SET_MENU INPUT " + changing_variable, "col":WHITE, "txt_col":RED},
                   {"txt":"Enter changing variable", "act":"SET_MENU INPUT changing_variable", "col":WHITE, "txt_col":RED},
                   {"txt":"Ahah execute command...", "act":"SET_MENU INPUT COMMAND_TO_EXECUTE", "col":RED, "txt_col":BLACK},
                   {"txt":"Back to main menu", "act":"SET_MENU MAIN", "col":GREEN, "txt_col":WHITE},))
    pygame.display.flip()

def InitInput(var, menu):
    InitInput.MENU_BKP = menu
    try: str(globals()[var])
    except: ShowText("Variable does not exist"); SetMenu("TEST"); return
    to_show = str(globals()[var])
    if to_show == globals()[var]:
        to_show = '"' + to_show + '"'
    SetSelectMenu(({"txt":"Editing " + var, "mode":"BASIC"}, {"txt":to_show + "|", "mode":"BASIC", "col":BLUE[:], "cor_col":WHITE}, {"txt":"Apply", "act":"APPLY_VAR"}))

def VarPrevVal(ind):
    value_type = AVALIBLE_CONFIG_INFO[ind][0]
    var = BUTTONS[0].text
    if value_type == "COLORS":
        new_ind = 0
        if globals()[var] in COLORS: new_ind = (COLORS.index(globals()[var]) - 1) % len(COLORS)
        globals()[var] = COLORS[new_ind]
    elif value_type == "NUMBER": globals()[var] = max(0, globals()[var] - 1)
    elif value_type == "FLAG": globals()[var] = not globals()[var]
    SetConfig({var:globals()[var]})
def VarNextVal(ind):
    value_type = AVALIBLE_CONFIG_INFO[ind][0]
    var = BUTTONS[0].text
    if value_type == "COLORS":
        new_ind = 0
        if globals()[var] in COLORS: new_ind = (COLORS.index(globals()[var]) + 1) % len(COLORS)
        globals()[var] = COLORS[new_ind]
    elif value_type == "NUMBER": globals()[var] = max(0, globals()[var] + 1)
    elif value_type == "FLAG": globals()[var] = not globals()[var]
    SetConfig({var:globals()[var]})

def VarToButtonArgs(ind):
    if AVALIBLE_CONFIG_INFO[ind][0] == "COLORS":
        cur_color = CONFIG[AVALIBLE_CONFIG_NAMES[ind]]
        return {"txt":COLORS_TO_TEXT.get(cur_color, "Unknown color"), "mode":"BASIC", "col":[BLACK, WHITE][cur_color == BLACK], "cor_col":WHITE, "txt_col":CONFIG[AVALIBLE_CONFIG_NAMES[ind]]}
    elif AVALIBLE_CONFIG_INFO[ind][0] == "NUMBER": return {"txt":str(CONFIG[AVALIBLE_CONFIG_NAMES[ind]]), "mode":"BASIC", "col":BLACK[:], "cor_col":WHITE[:], "txt_col":WHITE[:]}
    elif AVALIBLE_CONFIG_INFO[ind][0] == "FLAG":
        flag = CONFIG[AVALIBLE_CONFIG_NAMES[ind]]
        return {"txt":("NO", "YES")[flag], "txt_col":WHITE, "col":(RED, GREEN)[flag]}

def SetConfigMenu(ind):
    ClearScreen()
    SetSelectMenu(({"txt":AVALIBLE_CONFIG_NAMES[ind], "mode":"BASIC"}, VarToButtonArgs(ind)))
    pygame.display.update()

def SetMenu(menu):
    global APP_STATE
    app_state_bkp = APP_STATE
    APP_STATE = "MENU " + menu
    if menu == "TEST": ShowTestMenu(); return
    ClearScreen()
    if menu.startswith("INPUT"): InitInput(APP_STATE[11:], app_state_bkp[5:])
    elif menu == "MAIN": SetMainMenu()
    elif menu == "EXITING_GAME": SetExitingGameMenu()
    elif menu == "SESSIONS": ShowSessionPage()
    elif menu == "SETTINGS": ShowSettings()
    elif menu == "CONFIG": SetConfigMenu(0)
    elif menu == "SELECTING_COLOR": SelectingColour()
    elif menu.startswith("WAITING_FOR_PLAYER"): ShowPlayerWaiting(APP_STATE[24:] == "True")
    pygame.display.update()


