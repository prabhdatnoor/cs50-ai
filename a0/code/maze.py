import sys
from dataclasses import dataclass, field
from typing import TypeAlias, override

Point: TypeAlias = tuple[int, int]


@dataclass
class Node:
    state: Point
    parent: "Node | None"
    action: str


@dataclass
class StackFrontier:
    frontier: list[Node] = field(default_factory=list)

    def add(self, n: Node):
        self.frontier.append(n)

    def empty(self):
        return len(self.frontier) == 0

    def exists(self, p: Point):
        return any(node.state == p for node in self.frontier)

    def peek(self):
        return self.frontier[-1] if not self.empty() else None

    def pop(self):
        if self.empty():
            raise Exception("Frontier empty!")

        return self.frontier.pop()


class QueueFrontier(StackFrontier):
    @override
    def pop(self):
        if self.empty():
            raise Exception("Frontier empty!")

        return self.frontier.pop(0)

    @override
    def peek(self):
        return self.frontier[0] if not self.empty() else None


SimplifiedNodeRepr: TypeAlias = tuple[str, tuple[int, int]]


@dataclass
class Maze:
    height: int
    width: int
    walls: list[list[bool]]
    solution: tuple[list[str], list[Point]] | None
    start: Point
    goal: Point

    explored: set[Point]
    num_explored: int

    def __init__(self, filename: str):
        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row: list[bool] = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state: Point) -> list[SimplifiedNodeRepr]:
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result: list[SimplifiedNodeRepr] = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""

        # keep track of number of states explored
        self.num_explored = 0

        # initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action="")
        frontier = StackFrontier()
        frontier.add(start)

        # empty explored set
        self.explored = set()

        while not frontier.empty():
            # remove node from frontier
            node = frontier.pop()

            # if node contains goal state
            if node.state == self.goal:
                actions: list[str] = []
                cells: list[Point] = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()

                self.solution = (actions, cells)
                return

            # add node to explored set
            self.explored.add(node.state)
            self.num_explored += 1

            for action, state in self.neighbors(node.state):
                # if not already in the frontier or the explored set, add to frontier
                if not frontier.exists(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

        else:
            raise Exception("No solution!")

    def output_image(
        self, filename: str, show_solution: bool = True, show_explored: bool = False
    ):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA", (self.width * cell_size, self.height * cell_size), "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    (
                        [
                            (j * cell_size + cell_border, i * cell_size + cell_border),
                            (
                                (j + 1) * cell_size - cell_border,
                                (i + 1) * cell_size - cell_border,
                            ),
                        ]
                    ),
                    fill=fill,
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
