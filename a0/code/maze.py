import sys
from dataclasses import dataclass


@dataclass
class Node:
    state: list["Node"]
    parent: "Node | None"
    action: list[int]


@dataclass
class StackFrontier:
    frontier: list[Node]


print(Node(state=[], parent=None, action=[]))
