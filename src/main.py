#init
if LOAD_SESSIONS_ON_STARTUP: ReadFromFile()

events = pygame.event.get()
SetConfig(CONFIG)
SetMenu("MAIN")
if READ_CONFIG_ON_STARTUP:
    res = ReadConfigFromFile()
    if res: ShowText("Failed to set contig from file\nReason: " + res + "\nSetting default config")
    else: SetMenu("MAIN")#; ShowText("Config was read and setted\nsuccsessfully")

RUNNUNG = True
pygame.display.flip()
print("initialized")
#init

ToHandle = set((pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.KEYUP))
HandleToTab = set((pygame.K_TAB, pygame.K_RETURN))
while RUNNUNG:
    clock.tick(FPS)
    events = pygame.event.get() + EVENTS_TO_ADD
    EVENTS_TO_ADD = []
    
    for event in events:
        if event.type == pygame.QUIT:
            REBUILD_AND_RUN_ON_EXITING = False
            ExitApp()
            break
        if event.type in ToHandle:
            if event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key in HandleToTab: TabNavHandler(event)
            elif APP_STATE.startswith("GAME"): GameHandler(event)
            elif APP_STATE.startswith("MENU"): MenuHandler(event)

    if APP_STATE.startswith("GAME"):
        if APP_STATE.endswith("END"):
            winner = CheckWinner()
            txt_col = (BLACK_CHECKER[:], WHITE_CHECKER)[winner == "WHITE"]
            ShowText(winner + " WON", col=BLACK_CELL[:], txt_col=txt_col)
            if DELETE_SESSION_AFTER_END and SESSION_IND != -1:
                DeleteSession(SESSION_IND)
                SESSION_IND = -1
            SetMenu("SESSIONS")
        elif PLAYER_COLOR != CUR_COLOR and GAME_MODE != "BOT_VS_BOT": RunGameTurn()
    if APP_STATE == "MENU WAITING_FOR_PLAYER":
        CheckPlayer()
        pass
    pygame.display.update() #can be removed

#exiting
if SAVE_SESSIONS_ON_EXIT: WriteToFile()
if SAVE_CONFIG_ON_EXIT:
    res = WriteConfigToFile()
    if res: ShowText(res)
    #else: ShowText("Config was saved")
SOCKET_R.close()
SOCKET_S.close()
pygame.quit()
#exiting
