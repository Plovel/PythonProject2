def DrawCell(i, j, col=-1):
    if (col == -1): col = state[i][j][0]
    pygame.draw.rect(
                screen,
                FIELD_COLORS[col],
                (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

def DrawChecker(i, j, col=NO_CHECKER, is_king=False, sz=CHECKER_SIZE, king_sz=CHECKER_KING_SIZE, kf=1):
    if col == NO_CHECKER:
        col = abs(state[i][j][1])
        is_king = (state[i][j][1] < 0)
    if col == NO_CHECKER: return
    pygame.draw.circle(
                screen,
                PLAYER_COLORS[col],
                ((j + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE),
                sz * kf
            )
    if is_king:
        pygame.draw.circle(
                screen,
                YELLOW,
                ((j + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE),
                king_sz * kf
            )

def ReDrawItem(i, j):
    DrawCell(i, j)
    DrawChecker(i, j)

def DrawField():
    for i in range(64):
        ReDrawItem(i // 8, i % 8)
