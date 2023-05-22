def NormalSizeOfButton(txt_fnt, txt_sz, txt):
    text_size = pygame.font.SysFont(txt_fnt, txt_sz).size(txt)
    return (text_size[1] * 150 // 100, text_size[0] * 110 // 100)

def NormalSizeOfButtons(buttons):
    ans = [0, 0]
    for button in buttons:
        sz = NormalSizeOfButton(button.get("txt_fnt", def_kwargs["txt_fnt"]),
                                button.get("txt_sz", def_kwargs["txt_sz"]),
                                button.get("txt", "DEFAULT_TEXT"))
        ans[0] = max(buttons_max_sizes[0], sz[0])
        ans[1] = max(buttons_max_sizes[1], sz[1])
    return ans

TEST_VFX = True
BUTTON_SOUND_IND = 0
class Button:

    def __init__(self, pnt=None, sz=(None, None), act="NONE", col=None,
                 cor_col=None, pressed_col=None, c_sz=None, txt="DEFAULT_TEXT",
                 txt_col=WHITE[:], txt_fnt=DEFAULT_FONT, txt_sz=None,
                 mode="BASIC", center=None, offset=None):
        if col is None:
            if mode == "BASIC": col = TRANSPARENT[:]
            elif mode == "SELECT": col = GREEN[:]
        unselected_color = col[:]
        if cor_col is None:
            if mode == "BASIC": cor_col = col[:]
            elif mode == "SELECT": cor_col = YELLOW[:]
        if pressed_col is None:
            if TEST_VFX:
                if mode == "BASIC": pressed_col = col[:]
                elif mode == "SELECT":
                    res = tuple([val + 20 for val in unselected_color])
                    pressed_col = (tuple([min(255, val) for val in res]))
            else:
                if mode == "BASIC": pressed_col = col[:]
                elif mode == "SELECT": pressed_col = BLUE[:]

        if txt_sz is None and sz == (None, None): txt_sz = DEFAULT_FONT_SIZE
        if not (txt_sz is None) and (sz == (None, None)):
            sz = NormalSizeOfButton(txt_fnt, txt_sz, txt)
        if not txt_sz is None and ((sz[0] is None) or (sz[1] is None)):
            normal_size = NormalSizeOfButton(txt_fnt, txt_sz, txt)
            if sz[0] is None: sz = (normal_size[0], sz[1])
            if sz[1] is None: sz = (sz[0], normal_size[1])
        if txt_sz is None:
            #todo
            txt_sz = DEFAULT_FONT_SIZE
            normal_size = NormalSizeOfButton(txt_fnt, txt_sz, txt)
            if sz[0] is None: sz = (normal_size[0], sz[1])
            if sz[1] is None: sz = (sz[0], normal_size[1])
            
                

        if c_sz is None:
            common = 2 + min(sz) // 400
            if mode == "BASIC": c_sz = common
            elif mode == "SELECT": c_sz = common

        if (pnt is None) and (center is None):
            center = (HEIGHT // 2, WIDTH // 2)
        if not (center is None):
            pnt = (center[0] - sz[0] // 2, center[1] - sz[1] // 2)

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
        
        self.pressed = False
        self.selected = False
        if offset is None:
            if mode == "SELECT": offset = (max(sz[1] * 1 // 100, 4),
                                           2)
            elif mode == "BASIC": offset = (0, 0)
        self.offset = offset[:]
        
        #self.img_bkp = pygame.screen.Screen()

    def GetCenter(self, pos=None, sz=None):
        if pos is None: pos = self.point[:]
        if sz is None: sz = self.size[:]
        return (pos[0] + sz[0] // 2,
                pos[1] + sz[1] // 2)
    
    def draw(self, check=True):
        line_sz = 2
        c_sz = self.corner_size
        pos = self.point[:]
        sz = self.size[:]
        col = self.color[:]

        #prep
        pygame.draw.rect(screen, DEFAULT_CLEAR_SCREEN,
                         (pos[1], pos[0] - max(self.offset) + c_sz,
                          sz[1], sz[0] + max(self.offset) - c_sz))
        #prep
        
        #ind = BUTTONS.index(self)
        #if check and ind != 0: BUTTONS[ind - 1].draw(check=False)
        
        if self.corner_color != TRANSPARENT:
            pygame.draw.rect(screen, self.corner_color,
                             (*pos[::-1], *sz[::-1]))

        sz = (sz[0] - c_sz * 2, sz[1] - c_sz * 2)
        pos = (pos[0] + c_sz, pos[1] + c_sz)
        
        if col != TRANSPARENT:
            if self.mode == "SELECT":
                if self.pressed:
                    col = tuple([min(255, val + 25) for val in col])
                elif self.selected:
                    col = tuple([min(255, val + 15) for val in col])

                offset = self.offset[self.pressed]
                pos = (pos[0] - offset, pos[1])
                pygame.draw.rect(screen, col, (pos[1], pos[0],
                                               sz[1], sz[0] + offset))
                
                points = ((pos[1], pos[0] + sz[0] + offset), pos[::-1],
                          (pos[1] + sz[1], pos[0]),
                          (pos[1] + sz[1], pos[0] + sz[0] + offset))
                ln_col = ALMOST_BLACK
                for i in range(len(points) - 1):
                    pygame.draw.aaline(screen, ln_col,
                                       points[i], points[i + 1])
                pygame.draw.aaline(screen, ln_col,
                                   (pos[1], pos[0] + sz[0]),
                                   (pos[1] + sz[1], pos[0] + sz[0]))
            elif self.mode == "BASIC":
                pygame.draw.rect(screen, col, (*pos[::-1], *sz[::-1]))
        
        if self.text_color != TRANSPARENT:
            font = pygame.font.SysFont(self.text_font,
                                       self.text_size)
            img = font.render(self.text, True, self.text_color)
            center = self.GetCenter(pos, sz)
            rect = img.get_rect()
            rect.center = (center[1], center[0])
            screen.blit(img, rect.topleft)
        
        #if check and ind < len(BUTTONS) - 1: BUTTONS[ind + 1].draw(check=False)
        #if check: pygame.display.flip()

    def check_mouse(self, pos):
        is_on_button = (True and
        (self.point[0] <= pos[0] <= self.point[0] + self.size[0]) and
        (self.point[1] <= pos[1] <= self.point[1] + self.size[1]))
        if self.pressed and not is_on_button: self.unpress(); return
        if is_on_button != self.selected:
            self.selected = is_on_button
            self.draw()
        return self.selected

    def blink(self, timer=0.05):
        self.draw()
        pygame.display.flip()
        time.sleep(timer)

    def press(self):
        global BUTTON_SOUND_IND
        if self.mode == "SELECT":
            self.pressed = True
            BUTTON_SOUND_IND = random.randint(0, len(BUTTON_DOWN_SOUNDS) - 1)
            BUTTON_DOWN_SOUNDS[BUTTON_SOUND_IND].play()
            self.draw()
    
    def unpress(self):
        if self.mode == "SELECT":
            BUTTON_UP_SOUNDS[BUTTON_SOUND_IND].play()
            self.pressed = False
            self.draw()

def AddButton(*args, **kwargs):
    BUTTONS.append(Button(*args, **kwargs))
    BUTTONS[-1].draw()
