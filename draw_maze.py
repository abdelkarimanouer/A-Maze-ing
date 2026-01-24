import curses as cs


def get_cell_walls(row: int, col: int, maze_lines: list[str]) -> dict:
    directions = dict()
    if row < 0 or col < 0:
        return {'east': False, 'north': False, 'west': False, 'south': False}
    if row >= len(maze_lines):
        return {'east': False, 'north': False, 'west': False, 'south': False}
    line = maze_lines[row].strip()
    if col >= len(line):
        return {'east': False, 'north': False, 'west': False, 'south': False}
    else:
        line = maze_lines[row].strip()
        char_h = line[col]
        v = int(char_h, 16)
        directions['north'] = bool(v & 1)
        directions['east'] = bool(v & 2)
        directions['south'] = bool(v & 4)
        directions['west'] = bool(v & 8)
        return directions


def get_corner_walls(cy: int, cx: int, maze_lines: list[str]) -> dict:
    top_left = get_cell_walls(cy - 1, cx - 1, maze_lines)
    top_right = get_cell_walls(cy - 1, cx, maze_lines)
    bottom_left = get_cell_walls(cy, cx - 1, maze_lines)
    bottom_right = get_cell_walls(cy, cx, maze_lines)

    up = top_left['east'] or top_right['west']
    down = bottom_left['east'] or bottom_right['west']
    left = top_left['south'] or bottom_left['north']
    right = top_right['south'] or bottom_right['north']

    return {'up': up, 'down': down, 'left': left, 'right': right}


def get_corner_char(up: bool, down: bool, left: bool, right: bool) -> str:
    char_map = {
        (True, True, True, True): '╋',
        (True, True, True, False): '┫',
        (True, True, False, True): '┣',
        (False, True, True, True): '┳',
        (True, False, True, True): '┻',
        (True, True, False, False): '┃',
        (False, False, True, True): '━',
        (True, False, True, False): '┛',
        (True, False, False, True): '┗',
        (False, True, True, False): '┓',
        (False, True, False, True): '┏',
        (True, False, False, False): '┃',
        (False, True, False, False): '┃',
        (False, False, True, False): '━',
        (False, False, False, True): '━',
        (False, False, False, False): ' '
    }
    return char_map.get((up, down, left, right), ' ')


def draw_the_maze(window: cs.window, maze_lines: list[str], width: int,
                  height: int) -> None:

    corner_rows = height + 1
    corner_cols = width + 1

    for cy in range(corner_rows):
        for cx in range(corner_cols):
            walls = get_corner_walls(cy, cx, maze_lines)
            char = get_corner_char(walls['up'], walls['down'],
                                   walls['left'], walls['right'])
            screen_y = cy * 3
            screen_x = cx * 3
            window.addch(screen_y, screen_x, char)

            if walls['right'] and cx < width:
                window.addch(screen_y, screen_x + 1, '━')
                window.addch(screen_y, screen_x + 2, '━')

            if walls['down'] and cy < height:
                window.addch(screen_y + 1, screen_x, '┃')
                window.addch(screen_y + 2, screen_x, '┃')


def display_maze(maze_lines: list[str], config: dict) -> None:
    def draw(window: cs.window) -> None:
        cs.curs_set(0)
        window.clear()

        maze_width = config['WIDTH']
        maze_height = config['HEIGHT']

        draw_the_maze(window, maze_lines, maze_width, maze_height)

        window.refresh()
        window.getch()

    try:
        cs.wrapper(draw)
    except Exception as e:
        print("Error While Drawing Maze:", e)
