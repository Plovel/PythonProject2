def DrawCell(ind, col=None, sz=CELL_SIZE, offset=(0, 0)):
    if col is None:
        if (ind // 8 + ind % 8) % 2: col = BLACK_CELL
        else: col = WHITE_CELL
    if REVERSED_ORIENTATION: ind = 63 - ind
    pygame.draw.rect(screen, col, ((ind % 8) * sz + offset[1], (ind // 8) * sz + offset[0], sz, sz))

from pygame import gfxdraw
def draw_cool_circle(color, center, radius):
    if True:
        gfxdraw.aacircle(screen, *center, radius, color)
        gfxdraw.filled_circle(screen, *center, radius, color)
        if False:
            clr = WHITE
            gfxdraw.aacircle(screen, *center, radius, clr)
            gfxdraw.aacircle(screen, *center, radius * 80 // 100, clr)
    else:
        pygame.draw.circle(screen, color, center, radius); return
    #gfxdraw.circle(screen, *center, radius, color); #return
    #gfxdraw.filled_circle(screen, *center, radius, color); return
    

def DrawChecker(ind, rad=None, col=None, is_king=None, cell_sz=CELL_SIZE, is_selected=False, offset=(0, 0)):
    state = STATE[ind]
    if col is None:
        if state == ' ': col = TRANSPARENT
        elif state.lower() == 'w': col = WHITE_CHECKER
        else: col = BLACK_CHECKER
    if col == TRANSPARENT: return
    if is_king is None: is_king = state.isupper()
    if rad is None: rad = cell_sz * CHECKER_SIZE_KOEF // 100 // 2
    if is_selected: rad = rad * CHECKER_SELECTED_KOEF // 100
    if REVERSED_ORIENTATION: ind = 63 - ind

    center_coord = ((ind % 8) * cell_sz + cell_sz // 2 + offset[1], (ind // 8) * cell_sz + cell_sz // 2 + offset[0])
    draw_cool_circle(col, center_coord , rad)
    if is_king: draw_cool_circle(KING_CROWN_COLOR, center_coord, rad * CHECKER_CROWN_KOEF // 100)

def ReDrawItem(ind, pos=(0, 0), cell_sz=CELL_SIZE):
    DrawCell(ind, sz=cell_sz, offset=pos)
    DrawChecker(ind, offset=pos, cell_sz=cell_sz)

def DrawField(pos=(0, 0), cell_sz=CELL_SIZE):
    for i in range(64): ReDrawItem(i, pos=pos, cell_sz=cell_sz)
