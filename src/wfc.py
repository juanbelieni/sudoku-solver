from typing import List, Optional, Tuple
from xmlrpc.client import Boolean
from helpers import range2d
from sudoku import Board, CellPosition, copy_board, is_board_solved
from random import shuffle

CellOptions = Optional[List[int]]
BoardOptions = List[List[CellOptions]]


def get_options(board: Board) -> BoardOptions:
    def get_options_for_cell(position: CellPosition) -> CellOptions:
        (i, j) = position

        if board[i][j] is not None:
            return None

        row = board[i]
        column = [board[k][j] for k in range(9)]

        square_i = (i // 3) * 3
        square_j = (j // 3) * 3
        square = [board[square_i + k][square_j + l] for (k, l) in range2d(3)]

        return [n for n in range(1, 10) if n not in row + column + square]

    options = [[get_options_for_cell((i, j)) for j in range(9)] for i in range(9)]
    return options


def get_positions_with_fewest_options(
    options: BoardOptions,
) -> Optional[List[CellPosition]]:
    options_lengths = [
        len(options[i][j]) for (i, j) in range2d(9) if options[i][j] is not None
    ]

    if 0 in options_lengths:
        return None

    fewest_options = min(options_lengths)

    return [
        (i, j)
        for (i, j) in range2d(9)
        if options[i][j] is not None and len(options[i][j]) == fewest_options
    ]


def solve_board(board: Board) -> List[Board]:
    def solve_board_rec(
        board: Board,
        history: List[Board],
        depth: int,
    ) -> Tuple[Boolean, List[Board]]:
        history = [*history, board]

        if is_board_solved(board):
            return True, history

        options = get_options(board)
        positions = get_positions_with_fewest_options(options)

        if positions is None:
            return False, history

        shuffle(positions)

        for position in positions:
            (i, j) = position
            cell_options = options[i][j]

            for possibility in cell_options:
                new_board = copy_board(board)
                new_board[i][j] = possibility

                print(f"{depth}: {position} = {possibility}", end="\r")

                solved, history = solve_board_rec(new_board, history, depth + 1)

                if solved:
                    return (True, history)

        return False, history

    return solve_board_rec(board, [], 0)[1]
