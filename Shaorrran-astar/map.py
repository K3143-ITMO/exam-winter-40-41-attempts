"""
Sam Bridges task solution using A-star
"""
import argparse
import pathlib
import typing as tp

Maze = tp.List[tp.List[str]]
Cell = tp.Tuple[int, int]


class Node:
    """
    Node class for A-star algo. Stores parent (previous node), position and heuristic values (f, g, h)
    """

    def __init__(self, parent=None, pos=None):
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
    """
    Convert map as list of lists back to a string
    """
    return "".join(["".join(i) + "\n" for i in maze])


def find_sam(maze: Maze) -> tp.Optional[Cell]:
    """
    Find starting position
    """
    for i, _ in enumerate(maze):
        for j, e in enumerate(maze[i]):
            if e == "☺":
                return (i, j)

    return None


def find_dest(maze: Maze) -> tp.Optional[Cell]:
    """
    Find destination position
    """
    for i, _ in enumerate(maze):
        for j, e in enumerate(maze[i]):
            if e == "☼":
                return (i, j)

    return None


def manhattan_distance(start: Node, end: Node) -> int:
    """
    Calculate Manhattan distance (see https://en.wikipedia.org/wiki/Taxicab_geometry)
    """
    return abs(start.pos[0] - end.pos[0]) + abs(start.pos[1] - end.pos[1])


def generate_neighbors(maze: Maze, current: Node) -> tp.Optional[tp.List[Node]]:
    """
    Select passable neighbors in a maze using range-1 Von Neumann neighborhood (see https://en.wikipedia.org/wiki/Von_Neumann_neighborhood)
    """
    neighborhood = []
    for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Von Neumann neighborhood
        node_pos = (current.pos[0] + new_pos[0], current.pos[1] + new_pos[1])
        if (
            node_pos[0] > (len(maze) - 1)
            or node_pos[0] < 0
            or node_pos[1] > (len(maze[len(maze) - 1]) - 1)
            or node_pos[1] < 0
        ):
            continue

        if maze[node_pos[0]][node_pos[1]] == "☒":
            continue

        neighborhood.append(Node(current, node_pos))

    return neighborhood


def select_node(open_list: tp.List[Node]) -> tp.Tuple[int, Node]:
    """
    Next node selection function for A-star algo
    """
    current_node = open_list[0]
    current_index = 0
    for index, item in enumerate(open_list):
        if item.f < current_node.f:
            current_node = item
            current_index = index

    return (current_index, current_node)


def construct_path(current_node: Node) -> tp.List[Cell]:
    """
    Construct a path as a list of coordinate tuples (excluding start and dest returned by A-star)
    """
    path: tp.List[Cell] = []
    current = current_node
    while current:
        path.insert(0, current.pos)
        current = current.parent
    return path[1:-1]  # cut start and end nodes


def redefine_open_list(
    neighborhood: tp.List[Node],
    open_list: tp.List[Node],
    closed_list: tp.List[Node],
    current: Node,
    end: Node,
) -> tp.List[Node]:
    """
    Reinitialize open_list of nodes to continue A-star
    """
    for neighbor in neighborhood:
        for closed in closed_list:
            if neighbor == closed:
                continue

        # Create heuristic values
        neighbor.g = current.g + 1
        neighbor.h = manhattan_distance(neighbor, end)
        neighbor.f = neighbor.g + neighbor.h

        for open_node in open_list:
            if neighbor == open_node and neighbor.g > open_node.g:
                continue

        open_list.append(neighbor)

    return open_list


def a_star(maze: Maze, start: Node, end: Node) -> tp.Optional[tp.List[Cell]]:
    """
    See https://en.wikipedia.org/wiki/A*_search_algorithm for info on the algorithm
    """
    # Init start and end nodes
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Init open and closed lists
    open_list: tp.List[Node] = []
    closed_list: tp.List[Node] = []

    # Add start
    open_list.append(start_node)

    # Main loop
    while len(open_list) > 0:
        # Get current node
        current_index, current_node = select_node(open_list)

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Exit condition (found dest)
        if current_node == end_node:
            return construct_path(current_node)

        # Create neighborhood
        neighborhood = generate_neighbors(maze, current_node)
        if not neighborhood:
            raise ValueError("No possible path.")

        open_list = redefine_open_list(neighborhood, open_list, closed_list, current_node, end_node)

    return None


def fill_path(maze: Maze, path: tp.List[Cell]) -> Maze:
    """
    Fill the path (as a list of coordinate tuples) with Sam symbols
    """
    for pos in path:
        maze[pos[0]][pos[1]] = "☺"

    return maze


def main():
    maze = load_maze()
    start = find_sam(maze)
    end = find_dest(maze)
    path = a_star(maze, start, end)
    print(reconstruct_maze(fill_path(maze, path)))


if __name__ == "__main__":
    main()
