from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias, override

Point: TypeAlias = tuple[int, int]


class Value(Enum):
    Empty = 0
    X = 1
    O = 2  # noqa: E741


class GameState(Enum):
    TIE = 0
    X_WIN = 1
    O_WIN = 2


@dataclass
class Board:
    side: int = field(default=3)
    board: list[list[Value]] = field(default_factory=list)

    def __init__(self):
        self.board = [[Value.Empty for _ in range(self.side)] for _ in range(self.side)]

    def place(self, value: Value, tile: Point):
        self.board[tile[1]][tile[0]] = value

    def placeX(self, tile: Point):
        self.place(Value.X, tile)

    def placeY(self, tile: Point):
        self.place(Value.O, tile)

    def get_state(self) -> GameState:
        # check rows
        for row in self.board:
            # all X's
            if row.count(Value.X) == self.side:
                return GameState.X_WIN
            # all O's
            elif row.count(Value.O) == self.side:
                return GameState.O_WIN

        # check columns
        for r in range(self.side):
            x_count, o_count = 0, 0
            for c in range(self.side):
                match self.board[r][c]:
                    case Value.X:
                        x_count += 1
                    case Value.O:
                        o_count += 1
                    case _:
                        pass

            if x_count == self.side:
                return GameState.X_WIN
            elif o_count == self.side:
                return GameState.O_WIN

        # check diagnols

        # no wins found
        return GameState.TIE

    @override
    def __repr__(self) -> str:
        board_str = ""

        s = self.side
        # formula that works to figure out number of dashes ig
        row_vertical_border = "-" * (s * 6 + 1)

        for i in range(s):
            # switch between printing vertical and horizontal bars
            board_str += row_vertical_border + "\n"

            for j in range(s):
                match self.board[i][j]:
                    case Value.X:
                        board_str += "|  X  "
                    case Value.O:
                        board_str += "|  O  "
                    case _:
                        board_str += "|     "

            # don't forget to start a new line after each row using "\n"
            board_str += "|\n"

        return board_str + row_vertical_border


board = Board()

board.placeX((0, 1))
board.placeY((2, 1))

print(board)
