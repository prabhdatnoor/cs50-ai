import sys
from dataclasses import dataclass


@dataclass
class Node:
    state: str
    parent: "Node | None"
    action: list[int]


@dataclass
class StackFrontier:
    frontier: list[Node]

    def add(self, n: Node):
        self.frontier.append(n)

    def empty(self):
        return len(self.frontier) == 0

    def exists(self, n: Node):
        return any(node.state == n.state for node in self.frontier)

    def peek(self):
        return self.frontier[-1]

    def pop(self):
        if self.empty():
            raise Exception("Frontier empty!")

        return self.frontier.pop()


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Frontier empty!")

        return self.frontier.pop(0)
