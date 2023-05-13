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

class Button:

    def __init__(self, pnt=None, sz=(None, None), act="NONE", col=None,
                 cor_col=None, pressed_col=None, c_sz=None, txt="DEFAULT_TEXT",
                 txt_col=WHITE[:], txt_fnt=DEFAULT_FONT, txt_sz=None,
                 mode="BASIC", center=None):
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
            if mode == "BASIC": c_sz = 5
            elif mode == "SELECT": c_sz = 5

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

        self.unselected_color = self.color[:]
        self.pressed = False

    def GetCenter(self):
        return (self.point[0] + self.size[0] // 2,
                self.point[1] + self.size[1] // 2)

    def draw(self):
        TEST_VFX = True and self.pressed
        if self.corner_color != TRANSPARENT:
            pygame.draw.rect(screen, self.corner_color,
                             (self.point[1], self.point[0],
                              self.size[1], self.size[0]))
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
            font = pygame.font.SysFont(self.text_font,
                                       self.text_size - TEST_VFX * 3)
            img = font.render(self.text, True, self.text_color)
            center = self.GetCenter()
            if TEST_VFX: center = (center[0] + 2, center[1])
            rect = img.get_rect()
            rect.center = (center[1], center[0])
            screen.blit(img, rect.topleft)

    def check_mouse(self, pos):
        is_on_button = (True and
        (self.point[0] <= pos[0] <= self.point[0] + self.size[0]) and
        (self.point[1] <= pos[1] <= self.point[1] + self.size[1]))
        if self.pressed and not is_on_button:
            self.pressed = False
            pygame.mixer.Sound.play(random.choice(BUTTON_UP_SOUNDS))
        expected_color = self.unselected_color
        if self.pressed: expected_color = self.pressed_color
        elif is_on_button:
            if self.mode == "SELECT": expected_color = self.corner_color
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
        if self.mode == "SELECT":
            self.pressed = True
            pygame.mixer.Sound.play(random.choice(BUTTON_DOWN_SOUNDS))
            self.color = self.pressed_color[:]
            self.blink()
    
    def unpress(self):
        if self.mode == "SELECT":
            pygame.mixer.Sound.play(random.choice(BUTTON_UP_SOUNDS))
            self.pressed = False
            self.color = self.unselected_color[:]
            self.draw()

def AddButton(*args, **kwargs):
    BUTTONS.append(Button(*args, **kwargs))
    BUTTONS[-1].draw()
