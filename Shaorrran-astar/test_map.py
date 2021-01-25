from map import (
    Node,
    a_star,
    construct_path,
    fill_path,
    find_dest,
    find_sam,
    generate_neighbors,
    load_maze,
    manhattan_distance,
    reconstruct_maze,
    redefine_open_list,
    select_node,
)


def test_load_maze():
    assert load_maze() == [
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
        ["☒", "☺", ".", "☒", ".", "☼", "☒"],
        ["☒", "☒", ".", "☒", ".", "☒", "☒"],
        ["☒", ".", ".", "☒", ".", ".", "☒"],
        ["☒", ".", "☒", ".", "☒", ".", "☒"],
        ["☒", ".", ".", ".", ".", ".", "☒"],
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
    ]


def test_reconstruct_maze():
    assert (
        reconstruct_maze(load_maze())
        == "☒☒☒☒☒☒☒\n☒☺.☒.☼☒\n☒☒.☒.☒☒\n☒..☒..☒\n☒.☒.☒.☒\n☒.....☒\n☒☒☒☒☒☒☒\n"
    )


def test_find_sam():
    maze = load_maze()
    assert find_sam(maze) == (1, 1)


def test_find_dest():
    maze = load_maze()
    assert find_dest(maze) == (1, 5)


def test_manhattan_distance():
    start = Node(None, (1, 1))
    end = Node(None, (1, 2))
    assert manhattan_distance(start, end) == 1
    end = Node(None, (1, 5))
    assert manhattan_distance(start, end) == 4
    assert manhattan_distance(start, start) == 0


def test_generate_neighbors():
    maze = load_maze()
    current = Node(None, (1, 1))
    assert generate_neighbors(maze, current) == [Node(None, (1, 2))]
    current = Node(None, (5, 3))
    assert generate_neighbors(maze, current) == [
        Node(None, (5, 2)),
        Node(None, (5, 4)),
        Node(None, (4, 3)),
    ]


def test_select_node():
    start = Node(None, (1, 1))
    test = Node(None, (1, 3))  # mock node
    test.g = 1
    test.h = 2
    test.f = test.g + test.h  # mock heuristic
    assert select_node([start, test]) == (0, start)
    assert select_node([start, start]) == (0, start)
    assert select_node([test, start]) == (1, start)


def test_construct_path():
    path_construct = [
        (1, 2),
        (2, 2),
        (3, 2),
        (3, 1),
        (4, 1),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (4, 5),
        (3, 5),
        (3, 4),
        (2, 4),
        (1, 4),
        (1, 5),
    ]
    prev = Node(None, (1, 1))
    for i in range(len(path_construct)):
        end = Node(prev, path_construct[i])
        prev = end
    assert construct_path(end) == [
        (1, 2),
        (2, 2),
        (3, 2),
        (3, 1),
        (4, 1),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (4, 5),
        (3, 5),
        (3, 4),
        (2, 4),
        (1, 4),
    ]


def test_redefine_open_list():
    neighborhood = [Node(None, (5, 4)), Node(None, (4, 3))]
    print([i.pos for i in neighborhood])
    open_list = [Node(None, (5, 4))]
    closed_list = [Node(None, (5, 2))]
    current = Node(None, (5, 3))
    end = Node(None, (1, 5))
    assert set(
        [i.pos for i in redefine_open_list(neighborhood, open_list, closed_list, current, end)]
    ) == set([(5, 4), (4, 3)])


def test_a_star():
    start = (1, 1)
    dest = (1, 5)
    maze = load_maze()
    assert a_star(maze, start, dest) == [
        (1, 2),
        (2, 2),
        (3, 2),
        (3, 1),
        (4, 1),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (4, 5),
        (3, 5),
        (3, 4),
        (2, 4),
        (1, 4),
    ]


def test_fill_path():
    maze = load_maze()
    path = a_star(maze, (1, 1), (1, 5))
    assert fill_path(maze, path) == [
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
        ["☒", "☺", "☺", "☒", "☺", "☼", "☒"],
        ["☒", "☒", "☺", "☒", "☺", "☒", "☒"],
        ["☒", "☺", "☺", "☒", "☺", "☺", "☒"],
        ["☒", "☺", "☒", ".", "☒", "☺", "☒"],
        ["☒", "☺", "☺", "☺", "☺", "☺", "☒"],
        ["☒", "☒", "☒", "☒", "☒", "☒", "☒"],
    ]
