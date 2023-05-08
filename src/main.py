#init
if C_LOAD_SESSIONS_ON_STARTUP: ReadFromFile()
SetMenu("MAIN")
RUNNUNG = True
pygame.display.flip()
print("initialized")
#init

ToHandle = set((pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP))
while RUNNUNG:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ExitApp()
            break
        if event.type in ToHandle:
            if APP_STATE.startswith("GAME"): GameHandler(event)
            elif APP_STATE.startswith("MENU"): MenuHandler(event)

    if APP_STATE.startswith("GAME"):
        if APP_STATE.endswith("END"):
            ShowText(CheckWinner() + " WON", col=GREEN[:])
            if C_DELETE_AFTER_END and SESSION_IND != -1:
                DeleteSession(SESSION_IND)
                SESSION_IND = -1
            SetMenu("SESSIONS")
        elif PLAYER_COLOR != CUR_COLOR and GAME_MODE != "BOT_VS_BOT": RunGameTurn()
    #pygame.display.update()

#exiting
if C_SAVE_SESSIONS_ON_EXIT: WriteToFile()
pygame.quit()
#exiting
