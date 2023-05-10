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
def ShowText(text, timer=None, **kwargs):
    global GLOBAL_SURFACE, screen
    GLOBAL_SURFACE.blit(screen, (0, 0))

    kwargs.setdefault("col", BLUE[:])
    kwargs.setdefault("txt_col", YELLOW[:])
    kwargs.setdefault("txt_sz", DEFAULT_FONT_SIZE)
    kwargs.setdefault("txt_fnt", DEFAULT_FONT)
    lines = text.split('\n')
    if timer is None: timer = len(lines) * 0.2 + 1
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
    #wtf stuff
    if APP_STATE.startswith("GAME"): DrawField(); SelectChecker(SELECTED_CHECKER)
    if APP_STATE.endswith("SESSIONS"): ShowSessionPage()
    #wtf stuff
    pygame.display.flip()
