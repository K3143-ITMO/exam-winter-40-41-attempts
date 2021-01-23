from map import find_passable, find_path, find_sam, load_map, reconstruct_map


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


def test_find_passable():
    map = load_map()
    pos = find_sam(map)
    assert find_passable(map, pos) == (1, 2)
    map[5][2] = "☺"
    assert find_passable(map, (5, 3), (4, 3)) == (5, 4)


def test_find_sam():
    map = load_map()
    assert find_sam(map) == (1, 1)


def test_find_path():
    map = load_map()
    sam = find_sam(map)
    assert find_path(map, sam) == [
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
        ["☒", "☺", "☺", "☒", "☺", "☼", "☒"],
        ["☒", "☒", "☺", "☒", "☺", "☒", "☒"],
        ["☒", "☺", "☺", "☒", "☺", "☺", "☒"],
        ["☒", "☺", "☒", ".", "☒", "☺", "☒"],
        ["☒", "☺", "☺", "☺", "☺", "☺", "☒"],
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
    ]


def test_reconstruct_map():
    map = load_map()
    assert reconstruct_map(map) == "☒☒☒☒☒☒☒\n☒☺.☒.☼☒\n☒☒.☒.☒☒\n☒..☒..☒\n☒.☒.☒.☒\n☒.....☒\n☒☒☒☒☒☒☒\n"
