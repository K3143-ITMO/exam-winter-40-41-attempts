"""
Sam Bridges task solution
"""
import argparse
import pathlib
import typing as tp

Maze = tp.List[tp.List[str]]
Cell = tp.Tuple[int, int]


class Node:
    def __init__(self, parent=None, pos = None):
        self.parent = parent
        self.pos = pos

        self.g = 0  # distance from start
        self.h = 0  # heuristic (distance to dest)
        self.f = 0  # total cost

    def __eq__(self, other) -> bool:
        return self.pos == other.pos


def load_maze(mazefile: pathlib.Path = pathlib.Path("default.map")) -> Maze:
    """
    Load map from a file as a list of lists of strings
    """
    maze: Maze = [[]]
    path = pathlib.Path(mazefile)
    with open(path, "r") as f:
        maze = [
            [j for j in i] for i in str(f.read()).split("\n")
        ]  # split f.read() into strings, then into characters

    return maze


def reconstruct_maze(maze: Maze) -> str:
    return "".join(["".join(i) + "\n" for i in maze])

def find_sam(maze: Maze) -> Cell:
    for i, _ in enumerate(maze):
        for j, e in enumerate(maze[i]):
            if e == "☺":
                return (i, j)

def find_dest(maze: Maze) -> Cell:
    for i, _ in enumerate(maze):
        for j, e in enumerate(maze[i]):
            if e == "☼":
                return (i, j)

def a_star(maze: Maze, start: Node, end: Node) -> tp.Optional[tp.List[Cell]]:
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    See https://en.wikipedia.org/wiki/A*_search_algorithm for info on the algorithm
    """

    # Init start and end nodes
    start_node = Node(None, start)
    start_node.f = start_node.g = start_node.h = 0
    end_node = Node(None, end)
    end_node.f = end_node.g = end_node.h = 0

    # Init open and closed lists
    open_list: tp.List[Node] = []
    closed_list: tp.List[Node] = []

    # Add start
    open_list.append(start_node)

    # Main loop
    while len(open_list) > 0:
        # Get current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Exit condition (found dest)
        if current_node == end_node:
            path = []
            current = current_node
            while current:
                path.append(current.pos)
                current = current.parent
            return path[::-1]  # Path should be reversed

        # Generate children
        children = []
        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Von Neumann neighborhood
            # Get node pos
            node_pos = (current_node.pos[0] + new_pos[0], current_node.pos[1] + new_pos[1])

            # Check range
            if (
                node_pos[0] > (len(maze) - 1)
                or node_pos[0] < 0
                or node_pos[1] > (len(maze[len(maze) - 1]) - 1)
                or node_pos[1] < 0
            ):
                continue

            # Check walkability
            if maze[node_pos[0]][node_pos[1]] == "☒":
                continue

            # Create new node and append
            new_node = Node(current_node, node_pos)
            children.append(new_node)

        for child in children:
            # Child closed
            for closed in closed_list:
                if child == closed:
                    continue

            # Create heuristic values
            child.g = current_node.g + 1
            child.h = abs(child.pos[0] - end_node.pos[0]) + abs(
                child.pos[1] - end_node.pos[1]
            )  # Manhattan distance
            child.f = child.g + child.h

            # Child open
            for open in open_list:
                if child == open and child.g > open.g:
                    continue

            open_list.append(child)

    return None

def fill_path(maze: Maze, path: tp.List[Cell]) -> Maze:
    for pos in path:
        maze[pos[0]][pos[1]] = "☺"

    return maze

def main():
    maze = load_maze()
    start = find_sam(maze)
    end = find_dest(maze)
    path = a_star(maze, start, end)[1:-1] # cut start and end nodes
    print(reconstruct_maze(fill_path(maze, path)))

if __name__ == "__main__":
    main()
