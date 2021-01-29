import pathlib
import typing as tp
import argparse

Map = tp.List[tp.List[str]]
Cell = tp.Tuple[int, int]


def load_map(mapfile: str = "1.map") -> Map:
    map: Map = [[]]
    path = pathlib.Path(mapfile)
    with open(path, "r", encoding="utf-8") as f:
        map = [[j for j in i] for i in str(f.read()).split("\n")]
    return map


def find_element(map: Map, element: str) -> tp.Optional[Cell]:
    for i, _ in enumerate(map):
        for j, cell in enumerate(map[i]):
            if cell == element:
                return (i, j)
    return None


def find_ways(map: Map, sam: Cell) -> tp.Optional[tp.List[Cell]]:
    cells = []
    for step in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        cells.append((sam[0] + step[0], sam[1] + step[1]))
    return [i for i in cells if map[i[0]][i[1]] == "."]


def find_path(map: Map, sam: Cell) -> tp.Optional[Map]:
    sun = find_element(map, "☼")
    if abs(sam[0] - sun[0]) + abs(sam[1] - sun[1]) == 1:
        return map
    for way in find_ways(map, sam):
        map[way[0]][way[1]] = "☺"
        if find_path(map, way):
            return map

    map[sam[0]][sam[1]] = "."
    return None


def print_solution(map: Map):
    for i, _ in enumerate(map):
        print("".join(map[i]))


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("mapfile", type=str)
    args = argparser.parse_args()
    map = load_map(args.mapfile)
    sam = find_element(map, "☺")
    result = find_path(map, sam)
    if result:
        print_solution(result)
    else:
        map[sam[0]][sam[1]] = "☺"
        print_solution(map)
