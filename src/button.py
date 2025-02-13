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
                 mode="BASIC", center=None):
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
                    coef = 70
                    tmp = unselected_color[:]
                    pressed_col = (tmp[0] * coef // 100,
                                   tmp[1] * coef // 100,
                                   tmp[2] * coef // 100)
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

        self.unselected_color = unselected_color[:]
        self.pressed = False

    def GetCenter(self):
        return (self.point[0] + self.size[0] // 2,
                self.point[1] + self.size[1] // 2)

    def draw(self):
        #VFX
        VFX = TEST_VFX and self.pressed
        c_sz = self.corner_size
        if VFX and c_sz != 0:
            add = 1 + min(self.size) // 400
            c_sz += add
        #if TEST_VFX and 
        #VFX
        if self.corner_color != TRANSPARENT:
            pygame.draw.rect(screen, self.corner_color,
                             (self.point[1], self.point[0],
                              self.size[1], self.size[0]))
        if self.color != TRANSPARENT:
            pygame.draw.rect(screen,
                             self.color,
                             (self.point[1] + c_sz,
                              self.point[0] + c_sz,
                              self.size[1] - c_sz * 2,
                              self.size[0] - c_sz * 2
                              )
                             )
        if self.text_color != TRANSPARENT:
            font = pygame.font.SysFont(self.text_font,
                                       self.text_size - VFX * 1)
            img = font.render(self.text, True, self.text_color)
            center = self.GetCenter()
            if TEST_VFX and self.pressed:
                center = (center[0] + self.size[0] * 1 // 100, center[1])
            rect = img.get_rect()
            rect.center = (center[1], center[0])
            screen.blit(img, rect.topleft)
        pygame.display.flip()

    def check_mouse(self, pos):
        is_on_button = (True and
        (self.point[0] <= pos[0] <= self.point[0] + self.size[0]) and
        (self.point[1] <= pos[1] <= self.point[1] + self.size[1]))
        if self.pressed and not is_on_button: self.unpress()
        expected_color = self.unselected_color
        if self.pressed: expected_color = self.pressed_color
        elif is_on_button:
            if self.mode == "SELECT":
                if TEST_VFX:
                    coef = 90
                    tmp = self.unselected_color[:]
                    expected_color = (tmp[0] * coef // 100,
                                      tmp[1] * coef // 100,
                                      tmp[2] * coef // 100)
                else: expected_color = self.corner_color
            elif self.mode == "BASIC": expected_color = self.color
        if expected_color != self.color:
            self.color = expected_color
            self.draw()
        return is_on_button

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
            self.color = self.pressed_color[:]
            self.blink()
    
    def unpress(self):
        if self.mode == "SELECT":
            BUTTON_UP_SOUNDS[BUTTON_SOUND_IND].play()
            self.pressed = False
            self.color = self.unselected_color[:]
            self.draw()

def AddButton(*args, **kwargs):
    BUTTONS.append(Button(*args, **kwargs))
    BUTTONS[-1].draw()
