REVERSED_ORIENTATION = False

def DrawCell(ind, col=None, sz=CELL_SIZE, offset=(0, 0)):
    i, j = ind // 8, ind % 8
    if REVERSED_ORIENTATION: i, j = 7 - i, 7 - j
    if col is None: col = (WHITE_CELL, BLACK_CELL)[(i + j) % 2]
    pygame.draw.rect(screen, col,
                     (j * sz + offset[1], i * sz + offset[0], sz, sz))


from pygame import gfxdraw
def draw_coolest(color1, color2, center, radius1, radius2):
    gfxdraw.aacircle(screen, *center, radius2, color1)
    gfxdraw.filled_circle(screen, *center, radius2, color1)

    gfxdraw.aacircle(screen, *center, radius2 - radius1, color2)
    gfxdraw.filled_circle(screen, *center, radius2 - radius1, color2)

def draw_cool_circle(color, center, radius, cor_sz=None):
    if cor_sz is None: cor_sz = radius // 10;
    draw_coolest(ALMOST_BLACK, color, center, cor_sz, radius)
    
    center = (center[0], center[1])
    draw_coolest(ALMOST_BLACK, color, center, cor_sz, radius)
    
    

def DrawChecker(ind, rad=None, col=None, is_king=None, cell_sz=CELL_SIZE,
                is_selected=False, offset=(0, 0)):
    state = STATE[ind]
    if col is None:
        if state == ' ': col = TRANSPARENT
        elif state.lower() == 'w': col = WHITE_CHECKER
        else: col = BLACK_CHECKER
    if col == TRANSPARENT: return
    if is_king is None: is_king = state.isupper()
    if rad is None: rad = cell_sz * CHECKER_SIZE_KOEF // 100 // 2
    if is_selected: rad = rad * CHECKER_SELECTED_KOEF // 100

    i, j = ind // 8, ind % 8
    if REVERSED_ORIENTATION: i, j = 7 - i, 7 - j
    center_coord = (j * cell_sz + cell_sz // 2 + offset[1],
                    i * cell_sz + cell_sz // 2 + offset[0])
    
    offset = max(1, rad // 5)
    draw_cool_circle(col, center_coord , rad)
    center_coord = (center_coord[0], center_coord[1] - offset)
    draw_cool_circle(col, center_coord , rad)
    
    if is_king: draw_cool_circle(KING_CROWN_COLOR, center_coord,
                                 rad * CHECKER_CROWN_KOEF // 100, 0)

def ReDrawItem(ind, pos=(0, 0), cell_sz=CELL_SIZE):
    DrawCell(ind, sz=cell_sz, offset=pos)
    DrawChecker(ind, offset=pos, cell_sz=cell_sz)

def DrawField(pos=(0, 0), cell_sz=CELL_SIZE):
    for i in range(64): ReDrawItem(i, pos=pos, cell_sz=cell_sz)
