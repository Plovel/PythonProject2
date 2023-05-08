def DrawCell(i, j, col=None, sz=CELL_SIZE, offset=(0, 0)):
    if col is None: col = STATE[i][j][0]
    if REVERSED_ORIENTATION:
        i = 7 - i
        j = 7 - j
    pygame.draw.rect(screen, col, (j * sz + offset[1], i * sz + offset[0], sz, sz))

def DrawChecker(i, j, col=None, is_king=False, cell_sz=CELL_SIZE, sz=None, king_sz=None, kf=1, offset=(0, 0)):
    if col is None:
        col = STATE[i][j][1]
        is_king = STATE[i][j][2]
    if col == NO_CHECKER: return
    if sz is None: sz = cell_sz / 16 * 5
    if king_sz is None: king_sz = cell_sz / 16 * 1
    if REVERSED_ORIENTATION:
        i = 7 - i
        j = 7 - j
    pygame.draw.circle(screen, col, ((j + 0.5) * cell_sz + offset[1], (i + 0.5) * cell_sz + offset[0]), sz * kf)
    if is_king:
        pygame.draw.circle(screen, KING_CROWN_COLOR, ((j + 0.5) * cell_sz + offset[1], (i + 0.5) * cell_sz + offset[0]), king_sz * kf)

def ReDrawItem(i, j, pos=(0, 0), cell_sz=CELL_SIZE):
    DrawCell(i, j, sz=cell_sz, offset=pos)
    DrawChecker(i, j, offset=pos, cell_sz=cell_sz)

def DrawField(pos=(0, 0), cell_sz=CELL_SIZE):
    for i in range(64):
        ReDrawItem(i // 8, i % 8, pos=pos, cell_sz=cell_sz)
        
