from dataclasses import dataclass, field
from decimal import DefaultContext
from enum import Enum
from typing import TypeAlias, override

Point: TypeAlias = tuple[int, int]


class Player(Enum):
    Empty = 0
    X = 1
    O = 2  # noqa: E741


class GameState(Enum):
    O_WIN = -1
    TIE = 0
    X_WIN = 1


@dataclass
class Board:
    # side size of board
    side: int = 3
    board: list[list[Player]] = field(default_factory=list)

    # whose turn is it?
    current_turn: Player = Player.Empty

    #
    def __post_init__(self):
        # default value or else
        self.board = (
            [[Player.Empty for _ in range(self.side)] for _ in range(self.side)]
            if self.board == []
            else self.board
        )

    # place player symbol on board
    def place(self, value: Player, tile: Point):
        self.board[tile[1]][tile[0]] = value

    def placeX(self, tile: Point):
        self.place(Player.X, tile)

    def placeY(self, tile: Point):
        self.place(Player.O, tile)

    def get_state(self) -> GameState:
        # check rows
        for row in self.board:
            # all X's
            if row.count(Player.X) == self.side:
                return GameState.X_WIN
            # all O's
            elif row.count(Player.O) == self.side:
                return GameState.O_WIN

        # check columns
        for r in range(self.side):
            x_count, o_count = 0, 0
            for c in range(self.side):
                match self.board[r][c]:
                    case Player.X:
                        x_count += 1
                    case Player.O:
                        o_count += 1
                    case _:
                        pass

            if x_count == self.side:
                return GameState.X_WIN
            elif o_count == self.side:
                return GameState.O_WIN

        i, j = 0, 0
        x_count, o_count = 0, 0
        # direction of diagonal
        increment = 1

        # run twice for 2 diagonals
        for _ in range(2):
            # check diagonals
            while i >= 0 and j >= 0 and i < self.side and j < self.side:
                match self.board[i][j]:
                    case Player.X:
                        x_count += 1
                    case Player.O:
                        o_count += 1
                    case _:
                        pass

                i += increment
                j += increment

            if x_count == self.side:
                return GameState.X_WIN
            elif o_count == self.side:
                return GameState.O_WIN

            # for second iteration (loop only runs twice)
            i, j = self.side - 1, self.side - 1
            x_count, o_count = 0, 0
            increment = -1

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
                    case Player.X:
                        board_str += "|  X  "
                    case Player.O:
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
