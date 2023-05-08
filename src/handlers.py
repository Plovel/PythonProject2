def InputHandler(event):
    char = event.unicode
    if event.key == pygame.K_ESCAPE:
        SetMenu("SETTINGS")
        return
    elif event.key == pygame.K_BACKSPACE:
        if len(BUTTONS[1].text) > 0:
            BUTTONS[1].text = BUTTONS[1].text[:-1]
    elif char.isascii():
        BUTTONS[1].text += char
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
        elif event.key == pygame.K_q: SetMenu("SESSIONS") #



MENU_HANDLER_MOUSE_EVENTS = set((pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION))
def MenuHandler(event):
    global APP_STATE
    menu = APP_STATE[5:]
    if event.type in MENU_HANDLER_MOUSE_EVENTS:
        pos = pygame.mouse.get_pos()
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
                        print("ACTIVATED BUTTON", button.text)
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
            elif menu == "SELECTING_COLOR": SetMenu("SESSIONS") #
        elif event.key == pygame.K_LEFT:
            if menu == "SESSIONS": TurnSessionsPage(side='L') #
        elif event.key == pygame.K_RIGHT:
            if menu == "SESSIONS": TurnSessionsPage(side='R') #
        elif event.key == pygame.K_s:
            if menu == "SESSIONS": #
                WriteToFile()
                ShowText("Sessions was saved")
                SetMenu("SESSIONS")
        elif event.key == pygame.K_r:
            if menu == "SESSIONS": #
                ReadFromFile()
                ShowText("Sessions was read")
                SetMenu("SESSIONS")
        elif event.key == pygame.K_g:
            if menu in ("MAIN", "SESSIONS"): ChangeGameMode() #
        elif event.key == pygame.K_t: SetMenu("TEST") #shouldnt be shown
        elif event.key == pygame.K_n: #
            if menu == "SESSIONS": ResetState(); SetMenu("SELECTING_COLOR")
        elif event.key == pygame.K_x: ShowAvalibleButtons(menu) #shouldnt be shown
        elif event.key in KEYS_TO_NUMBERS: #
            if menu == "SESSIONS":
                session = SESSIONS_PAGE * 4 + KEYS_TO_NUMBERS[event.key] - 1
                if 0 <= session < len(SESSIONS): RunSession(session)
                elif session == len(SESSIONS): ResetState(); SetMenu("SELECTING_COLOR")
