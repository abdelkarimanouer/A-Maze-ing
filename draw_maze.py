import curses as cs


def draw_board(window: cs.window, width: int, height: int) -> None:

    window.addch(0, 0, '┏')
    window.addch(0, width, '┓')
    window.addch(height, 0, '┗')
    window.addch(height, width, '┛')

    for c in range(1, width):
        window.addch(0, c, '━')
        window.addch(height, c, '━')

    for r in range(1, height):
        window.addch(r, 0, '┃')
        window.addch(r, width, '┃')


def get_cell_walls(row: int, col: int, maze_lines: list[str]) -> dict:
    directions = dict()
    if row < 0 or col < 0:
        return {'east': False, 'north': False, 'west': False, 'south': False}
    if row >= len(maze_lines):
        return {'east': False, 'north': False, 'west': False, 'south': False}
    if col >= len(maze_lines[row]):
        return {'east': False, 'north': False, 'west': False, 'south': False}
    else:
        line = maze_lines[row].strip()
        hex = line[col]
        v = int(hex, 16)
        directions['east'] = bool(v & 8)
        directions['north'] = bool(v & 4)
        directions['west'] = bool(v & 2)
        directions['south'] = bool(v & 1)
        return directions


def draw_the_maze(window: cs.window, maze_lines: list[str], width: int,
                  height: int) -> None:

    for y, line in enumerate(maze_lines):
        line = line.strip()
        for x, char in enumerate(line):
            v = int(char, 16)
            east = v & 8
            north = v & 4
            west = v & 2
            south = v & 1

            start_y = (y * 3) + 1
            start_x = (x * 3) + 1
            if east:
                window.addch(start_y + 1, start_x + 2, '┃')
            if west:
                window.addch(start_y + 1, start_x, '┃')
            if north:
                window.addch(start_y, start_x + 1, '━')
            if south:
                window.addch(start_y + 2, start_x + 1, '━')

            if north and west:
                window.addch(start_y, start_x, '┏')
            if north and east:
                window.addch(start_y, start_x + 2, '┓')
            if south and west:
                window.addch(start_y + 2, start_x, '┗')
            if south and east:
                window.addch(start_y + 2, start_x + 2, '┛')


def display_maze(maze_lines: list[str], config: dict) -> None:
    def draw(window: cs.window) -> None:
        cs.curs_set(0)
        window.clear()

        width = config['WIDTH'] * 3 + 1
        height = config['HEIGHT'] * 3 + 1

        draw_board(window, width, height)

        draw_the_maze(window, maze_lines, width, height)

        window.refresh()
        window.getch()

    try:
        cs.wrapper(draw)
    except Exception as e:
        print("Error While Drawing Maze:", e)
