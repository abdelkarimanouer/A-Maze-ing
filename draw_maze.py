import curses as cs


def get_cell_walls(row: int, col: int, maze_lines: list[str]) -> dict:
    """
    Checks which walls exist for a cell at given position.
    Returns dictionary with 4 directions (north, east, south, west).
    Each direction is True if wall exists, False if not.
    """
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
    """
    Checks walls around a corner point where 4 cells meet.
    Looks at all 4 cells around the corner.
    Returns which walls connect to this corner point.
    """
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
    """
    Returns the correct box drawing character for a corner.
    Chooses character based on which walls connect to it.
    Uses special Unicode characters to draw smooth lines.
    """
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
    """
    Draws the maze walls on the screen using box characters.
    Each cell takes 3x3 spaces on screen for better visibility.
    Connects all corners and walls to make complete maze.
    """
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


def draw_entry_exit(window: cs.window, entry: tuple, exit: tuple) -> None:
    """
    Places entry and exit markers on the maze.
    Entry is marked with flag emoji 🏁.
    Exit is marked with flag emoji 🚩.
    """
    entry_x, entry_y = entry
    entry_screen_y = (entry_y * 3) + 1
    entry_screen_x = (entry_x * 3) + 1
    window.addch(entry_screen_y, entry_screen_x, '🏁')

    exit_x, exit_y = exit
    exit_screen_y = (exit_y * 3) + 1
    exit_screen_x = (exit_x * 3) + 1
    window.addch(exit_screen_y, exit_screen_x, '🚩')


def display_menu(window: cs.window) -> int:
    pass


def draw_a_maze_ing_header(window: cs.window) -> None:

    header = """
******************************************************************\
********************************************
*                                                                 \
                                           *
*                                                                 \
                                           *
*           _          ____    ____       _       ________  ______\
__       _____  ____  _____   ______       *
*          / \\        |_   \\  /   _|     / \\     |  __   _||_\
   __\
  |     |_   _||_   \\|_   _|.' ___  |      *
*         / _ \\  ______ |   \\/   |      / _ \\    |_/  / /    | |_\
 \\_|______ | |    |   \\ | | / .'   \\_|      *
*        / ___ \\|______|| |\\  /| |     / ___ \\      .'.' _   |  _\
| _|______|| |    | |\\ \\| | | |   ____      *
*      _/ /   \\ \\_     _| |_\\/_| |_  _/ /   \\ \\_  _/ /__/ | _|\
 |_\
_/ |      _| |_  _| |_\\   |_\\ `.___]  |     *
*     |____| |____|   |_____||_____||____| |____||________||______\
__|     |_____||_____|\\____|`._____.'      *
*                                                                 \
                                           *
*                                                                 \
                                           *
*                                     Developed by:\
 aanouer and achouaf                                      *
*                                                                 \
                                           *
******************************************************************\
****************************************** *
"""
    window.timeout(200)

    max_y, max_x = window.getmaxyx()
    lines = header.split('\n')
    header_width = max(len(line) for line in lines)
    start_x = (max_x - header_width) // 2
    start_y = 0
    show = True

    while True:
        window.clear()
        if show:
            for i, line in enumerate(lines):
                if line.strip():
                    window.addstr(start_y + i, start_x, line, cs.A_BOLD)
        window.refresh()
        cs.napms(500)
        if window.getch() != -1:
            break
        show = not show

    window.timeout(-1)


def display_maze(maze_lines: list[str], config: dict) -> None:
    """
    Main function to display the complete maze on terminal.
    Uses curses library to draw header and the maze with walls and markers.
    Waits for key press before closing.
    """
    def draw(window: cs.window) -> None:
        cs.curs_set(0)
        window.clear()

        draw_a_maze_ing_header(window)
        display_menu(window)

        window.clear()
        maze_width = config['WIDTH']
        maze_height = config['HEIGHT']
        maze_entry = config['ENTRY']
        maze_exit = config['EXIT']

        draw_the_maze(window, maze_lines, maze_width, maze_height)
        draw_entry_exit(window, maze_entry, maze_exit)

        window.refresh()
        window.getch()

    try:
        cs.wrapper(draw)
    except Exception as e:
        print("Error While Drawing Maze:", e)
