"""
Sam Bridges task solution
"""
import argparse
import pathlib

# All of this would have been easier if he had tried to build a FUCKING BRIDGE first!
import typing as tp
from os import name

Map = tp.List[tp.List[str]]
Cell = tp.Tuple[int, int]


def load_map(mapfile: pathlib.Path = pathlib.Path("default.map")) -> Map:
    """
    Load map from a file as a list of lists of strings
    """
    map: Map = [[]]
    path = pathlib.Path(mapfile)
    with open(path, "r") as f:
        map = [
            [j for j in i] for i in str(f.read()).split("\n")
        ]  # split f.read() into strings, then into characters

    return map


def find_passable(map: Map, pos: Cell, cut: tp.Optional[Cell] = None) -> tp.Optional[Cell]:
    """
    Finds cells that can be traversed, returns coordinates or None is the path is blocked
    """
    cells = [
        (pos[0] - 1, pos[1]),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0], pos[1] + 1),
    ]  # down, up, left, right
    passable_pos = [
        i for i in cells if (map[i[0]][i[1]] == "." or map[i[0]][i[1]] == "☼") and i != cut
    ]
    # passes if the position is either traversable or is a destination
    # Also disregards cut paths (those already traversed but going into a dead end)
    if not passable_pos:  # no passable paths found
        return None
    return passable_pos[0]  # return only one possible value


def find_sam(map: Map) -> tp.Optional[Cell]:
    """
    Find Sam's starting position
    """
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "☺":
                return (i, j)

    return None  # what the fuck


def find_path(map: Map, sam: Cell) -> Map:
    old = sam
    cut = None
    empty_pos = find_passable(map, sam, cut)
    while not map[sam[0]][sam[1]] == "☼":
        if empty_pos:
            map[empty_pos[0]][empty_pos[1]] = "☺"
            empty_pos = find_passable(map, empty_pos, cut)
        if not empty_pos:  # dead end
            map[sam[0]][sam[1]] = "."  # revert traversal
            cut = sam  # cut the path
            sam = old  # revert position
            empty_pos = find_passable(map, sam, cut)  # find new path
            map[sam[0]][sam[1]] = "☺"  # go there
            if empty_pos:
                sam = empty_pos  # update position
        else:
            old = sam  # save previous position in case we fuck up
            sam = empty_pos  # update position

    return map


def reconstruct_map(map: Map) -> str:
    list_map = []
    for i in map:
        list_map.append("".join(i) + "\n")
    return "".join(list_map)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Samuel Porter Bridges")
    argparser.add_argument(
        "path",
        metavar="file",
        type=pathlib.Path,
        nargs="?",
        default=pathlib.Path("default.map"),
        help="Path to map file",
    )
    namespace = argparser.parse_args()
    map = load_map(namespace.path)
    sam = find_sam(map)
    if not sam:
        raise ValueError("Where is Mr. Bridges?")
    solution = find_path(map, sam)
    print(reconstruct_map(solution))
