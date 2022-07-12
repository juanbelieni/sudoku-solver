from typing import List, Optional, Tuple

from helpers import range2d

Cell = Optional[int]
Board = List[List[Cell]]
CellPosition = Tuple[int, int]


def create_board() -> Board:
    return [[None] * 9 for _ in range(9)]


def copy_board(board: Board) -> Board:
    return [[board[i][j] for j in range(9)] for i in range(9)]

def is_board_solved(board: Board) -> bool:
    for (i, j) in range2d(9):
        if board[i][j] is None:
            return False

    return True
