import pygame as pg
from helpers import range2d
from sudoku import Board, create_board
from wfc import BoardOptions, get_options, solve_board

BOARD_SIZE = 810
CELL_SIZE = BOARD_SIZE // 9


def create_screen() -> pg.Surface:
    pg.init()
    pg.display.set_caption("Sudoku")
    screen = pg.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    return screen


def draw_board(
    screen: pg.Surface, board: Board, options: BoardOptions
) -> None:
    screen.fill((255, 255, 255))

    for (i, j) in range2d(9):
        x = j * CELL_SIZE
        y = i * CELL_SIZE

        pg.draw.rect(screen, (128, 128, 128), (x, y, CELL_SIZE, CELL_SIZE), 1)

        if j % 3 == 0:
            pg.draw.line(screen, (0, 0, 0), (x, 0), (x, BOARD_SIZE), 2)
        if i % 3 == 0:
            pg.draw.line(screen, (0, 0, 0), (0, y), (BOARD_SIZE, y), 2)

        if board[i][j] is not None:
            font_size = CELL_SIZE // 2
            font = pg.font.SysFont("Arial", font_size)
            text = font.render(str(board[i][j]), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
            screen.blit(text, text_rect)
        else:
            for option in options[i][j]:
                poss_x = x + ((option - 1) % 3) * (CELL_SIZE // 3)
                poss_y = y + ((option - 1) // 3) * (CELL_SIZE // 3)

                font_size = CELL_SIZE // 6
                font = pg.font.SysFont("Arial", font_size)
                text = font.render(str(option), True, (0, 0, 0))

                text_rect = text.get_rect()
                text_rect.center = (poss_x + font_size, poss_y + font_size)

                screen.blit(text, text_rect)


def wait_for_space() -> None:
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return


screen = create_screen()
board = create_board()

# board[0] = [5, 3, None, None, 7, None, None, None, None]
# board[1] = [6, None, None, 1, 9, 5, None, None, None]
# board[2] = [None, 9, 8, None, None, None, None, 6, None]
# board[3] = [8, None, None, None, 6, None, None, None, 3]
# board[4] = [4, None, None, 8, None, 3, None, None, 1]
# board[5] = [7, None, None, None, 2, None, None, None, 6]
# board[6] = [None, 6, None, None, None, None, 2, 8, None]
# board[7] = [None, None, None, 4, 1, 9, None, None, 5]
# board[8] = [None, None, None, None, 8, None, None, 7, 9]

history = solve_board(board)
i = 0

print()

wait_for_space()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    if i < len(history):
        print(f"{i}/{len(history)}", end="\r")
        solved_board = history[i]
        options = get_options(solved_board)
        draw_board(screen, solved_board, options)
        i += 1
    else:
        pass
        # print("\nSolved!")
        # history = solve_board(board)
        # i = 0
        # print()

    pg.display.flip()
    # pg.time.delay(1)
    # wait_for_space()
