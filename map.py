import pathlib
import typing as tp

Map = tp.List[tp.List[str]]
Cell = tp.Tuple[int, int]


def load_map(mapfile: pathlib.Path = pathlib.Path("default.map")) -> Map:
    map: Map = [[]]
    path = pathlib.Path(mapfile)
    with open(path, "r") as f:
        map = [
            [j for j in i] for i in str(f.read()).split("\n")
        ] 

    return map

def find_sam(map: Map) -> tp.Optional[Cell]:
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "☺":
                return (i,j)
    return None


def find_ways(map: Map, sam: Cell) -> tp.Optional[tp.List[Cell]]:
    cells = [
        (sam[0] - 1, sam[1]),
        (sam[0] + 1, sam[1]),
        (sam[0], sam[1] - 1),
        (sam[0], sam[1] + 1),
    ]
    passable_pos = [i for i in cells if (map[i[0]][i[1]] == "." or map[i[0]][i[1]] == "☼")]
    return passable_pos


def find_sonne(map: Map) -> Cell:
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "☼":
                return (i,j)
    return None

def mapmaker(map: Map, sam: Cell) -> tp.Optional[Map]:
    sun_location = find_sonne(map)
    if abs(sam[0]-sun_location[0]) + abs(sam[1]-sun_location[1]) == 1:
        return map
    for way in find_ways(map, sam):
        map[way[0]][way[1]] ="☺"
        if mapmaker(map, way):
            return map

    map[sam[0]][sam[1]] = "."
    return None

def printer(map, basic_map, sam):
    if map:
        for i in range(len(map)):
            print("".join(map[i]))
    else:
        basic_map[sam[0]][sam[1]] = "☺"
        for i in range(len(basic_map)):
            print("".join(basic_map[i]))

if __name__ == "__main__":
    map = load_map()
    sam = find_sam(map)
    result = mapmaker(map, sam)
    printer(result,map,sam)
