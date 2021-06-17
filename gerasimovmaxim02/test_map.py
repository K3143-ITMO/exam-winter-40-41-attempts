from map import find_sam, find_sonne, find_ways, load_map, mapmaker


def test_load_map():
    assert load_map() == [
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
        ["☒", "☺", ".", "☒", ".", "☼", "☒"],
        ["☒", "☒", ".", "☒", ".", "☒", "☒"],
        ["☒", ".", ".", "☒", ".", ".", "☒"],
        ["☒", ".", "☒", ".", "☒", ".", "☒"],
        ["☒", ".", ".", ".", ".", ".", "☒"],
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
    ]


def test_find_sam():
    map = load_map()
    assert find_sam(map) == (1, 1)


def test_find_ways():
    map = load_map()
    pos = find_sam(map)
    assert find_ways(map, pos) == [(1, 2)]
    map[5][2] = "☺"
    assert find_ways(map, (5, 3)) == [(4, 3), (5, 4)]


def test_find_sonne():
    map = load_map()
    assert find_sonne(map) == (1, 5)


def test_mapmaker():
    map = load_map()
    sam = find_sam(map)
    assert mapmaker(map, sam) == [
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
        ["☒", "☺", "☺", "☒", "☺", "☼", "☒"],
        ["☒", "☒", "☺", "☒", "☺", "☒", "☒"],
        ["☒", "☺", "☺", "☒", "☺", "☺", "☒"],
        ["☒", "☺", "☒", ".", "☒", "☺", "☒"],
        ["☒", "☺", "☺", "☺", "☺", "☺", "☒"],
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
    ]