import curses as cs
import time
import generate_maze


def get_cell_walls_from_struct(row: int, col: int,
                               maze_struct: list[list]) -> dict:
    """
    Same idea as get_cell_walls(), but reads from maze_struct (Cell.wall).
    """
    if row < 0 or col < 0:
        return {'east': False, 'north': False, 'west': False, 'south': False}

    if row >= len(maze_struct):
        return {'east': False, 'north': False, 'west': False, 'south': False}

    if col >= len(maze_struct[0]):
        return {'east': False, 'north': False, 'west': False, 'south': False}

    v = maze_struct[row][col].wall

    return {
        'north': bool(v & 1),
        'east': bool(v & 2),
        'south': bool(v & 4),
        'west': bool(v & 8),
    }


def get_corner_walls_from_struct(cy: int, cx: int,
                                 maze_struct: list[list]) -> dict:
    """
    Same idea as get_corner_walls(), but reads from maze_struct.
    """
    top_left = get_cell_walls_from_struct(cy - 1, cx - 1, maze_struct)
    top_right = get_cell_walls_from_struct(cy - 1, cx, maze_struct)
    bottom_left = get_cell_walls_from_struct(cy, cx - 1, maze_struct)
    bottom_right = get_cell_walls_from_struct(cy, cx, maze_struct)

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


def fill_cells(window: cs.window, maze_struct: list[list],
               width: int, height: int, *, use_visited: bool) -> None:
    for y in range(height):
        for x in range(width):
            if use_visited and maze_struct[y][x].visited:
                attr = cs.color_pair(2)
            else:
                attr = cs.color_pair(1)

            sy = y * 3 + 1
            sx = x * 3 + 1

            window.addstr(sy,     sx,     "  ", attr)
            window.addstr(sy + 1, sx,     "  ", attr)


def draw_the_maze_from_struct(window: cs.window, maze_struct: list[list],
                              width: int, height: int,
                              color_walls: int = 5,
                              use_visited: bool = True) -> None:
    """
    Draw maze using maze_struct (live walls), not maze_lines.
    """
    fill_cells(window, maze_struct, width, height, use_visited=use_visited)
    corner_rows = height + 1
    corner_cols = width + 1

    for cy in range(corner_rows):
        for cx in range(corner_cols):
            walls = get_corner_walls_from_struct(cy, cx, maze_struct)
            char = get_corner_char(walls['up'], walls['down'],
                                   walls['left'], walls['right'])

            screen_y = cy * 3
            screen_x = cx * 3
            window.addstr(screen_y, screen_x, char,
                          cs.color_pair(color_walls) | cs.A_BOLD)

            if walls['right'] and cx < width:
                window.addstr(screen_y, screen_x + 1, '━',
                              cs.color_pair(color_walls) | cs.A_BOLD)
                window.addstr(screen_y, screen_x + 2, '━',
                              cs.color_pair(color_walls) | cs.A_BOLD)

            if walls['down'] and cy < height:
                window.addstr(screen_y + 1, screen_x, '┃',
                              cs.color_pair(color_walls) | cs.A_BOLD)
                window.addstr(screen_y + 2, screen_x, '┃',
                              cs.color_pair(color_walls) | cs.A_BOLD)


def draw_entry_exit(window: cs.window, entry: tuple, exit: tuple) -> None:
    """
    Places entry and exit markers on the maze.
    Entry is marked with flag emoji 🏁.
    Exit is marked with flag emoji 🚩.
    """
    entry_x, entry_y = entry
    entry_screen_y = (entry_y * 3) + 1
    entry_screen_x = (entry_x * 3) + 1
    window.addstr(entry_screen_y, entry_screen_x, '🏁')

    exit_x, exit_y = exit
    exit_screen_y = (exit_y * 3) + 1
    exit_screen_x = (exit_x * 3) + 1
    window.addstr(exit_screen_y, exit_screen_x, '🚩')


def display_menu_with_header(window: cs.window) -> None:
    """
    Shows menu options centered on screen.
    """

    menu = [
        "1. Generate Maze",
        "X. Exit"
    ]

    max_y, max_x = window.getmaxyx()

    menu_width = max(len(line) for line in menu)

    start_x = (max_x - menu_width) // 2
    start_y = 16

    for i, line in enumerate(menu):
        window.addstr(start_y + i, start_x, line, cs.A_BOLD)

    window.refresh()


def draw_maze_menu(window: cs.window, maze_width: int,
                   maze_height: int) -> None:
    """
    Draws menu on the right side of maze.
    """

    menu = [
        "R. ReGenerate The Maze",
        "1. Find Path",
        "2. Show/Hide Path",
        "3. Player Mode",
        "4. Change Color of Maze",
        "X. Exit"
    ]

    max_y, max_x = window.getmaxyx()

    menu_x = (maze_width + 1) * 3 + 5

    maze_total_height = (maze_height + 1) * 3
    menu_total_height = len(menu)
    menu_y = (maze_total_height - menu_total_height) // 2

    for i, line in enumerate(menu):
        if line.startswith("==="):
            window.addstr(menu_y + i, menu_x, line, cs.A_BOLD | cs.A_UNDERLINE)
        elif line:
            window.addstr(menu_y + i, menu_x, line, cs.A_BOLD)


def draw_a_maze_ing_header(window: cs.window) -> str:

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

    max_y, max_x = window.getmaxyx()
    lines = header.split('\n')
    header_width = max(len(line) for line in lines)
    start_x = (max_x - header_width) // 2
    start_y = 0
    key = None

    window.erase()
    window.nodelay(True)
    while True:
        display_menu_with_header(window)
        for i, line in enumerate(lines):
            if line.strip():
                window.addstr(start_y + i, start_x, line, cs.A_BOLD)
        window.refresh()
        try:
            key = window.getkey()
            if key == '1' or key == 'x' or key == 'X' or key == '\x1b':
                window.nodelay(False)
                return key
        except Exception:
            key = None


def draw_congratulations(window: cs.window) -> None:

    header = """
 ██████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗  █████╗ ████████╗██╗   ██╗██╗\
      █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██╔══██╗\
╚══██╔══╝██║   ██║██║     ██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝███████║   ██║   \
██║   ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║
██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║   ██║   \
██║   ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║  ██║   ██║   \
╚██████╔╝███████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    \
╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""
    max_y, max_x = window.getmaxyx()
    lines = header.split('\n')
    header_width = max(len(line) for line in lines)
    header_height = len(lines)
    start_x = (max_x - header_width) // 2
    start_y = (max_y - header_height) // 2

    window.erase()
    for i, line in enumerate(lines):
        if line.strip():
            window.addstr(start_y + i, start_x, line, cs.A_BOLD)
    window.refresh()


def player_mode(window: cs.window, entry: tuple, exit: tuple,
                maze_struct: list[list], width: int, height: int) -> bool:

    x, y = entry

    while True:
        key = window.getkey()
        if key == "x" or key == "X" or key == '\x1b':
            return False

        window.addstr((y * 3) + 1, (x * 3) + 1, "  ", cs.color_pair(2))

        walls = get_cell_walls_from_struct(y, x, maze_struct)

        if key == "KEY_UP" and not walls['north']:
            y -= 1
        elif key == "KEY_DOWN" and not walls['south']:
            y += 1
        elif key == "KEY_LEFT" and not walls['west']:
            x -= 1
        elif key == "KEY_RIGHT" and not walls['east']:
            x += 1

        window.addstr((y * 3) + 1, (x * 3) + 1, "👤", cs.color_pair(2))
        window.refresh()

        if (x, y) == exit:
            time.sleep(0.1)
            return True


def animate_path(window, entry, path, delay=0.08):
    x, y = entry

    for move in path:
        old_x, old_y = x, y  # save old cell

        # move path
        if move == "N":
            y -= 1
        elif move == "S":
            y += 1
        elif move == "E":
            x += 1
        elif move == "W":
            x -= 1

        # paint corridor between old and new (THE GAP)
        if move in ("E", "W"):
            gx = min(old_x, x) * 3 + 3
            gy = old_y * 3 + 1
            window.addstr(gy,     gx, " ", cs.color_pair(3))
            window.addstr(gy + 1, gx, " ", cs.color_pair(3))
        else:  # N or S
            gy = min(old_y, y) * 3 + 3
            gx = old_x * 3 + 1
            window.addstr(gy, gx, "  ", cs.color_pair(3))

        # paint new cell (FULL interior 2x2)
        sy = y * 3 + 1
        sx = x * 3 + 1
        window.addstr(sy,     sx, "  ", cs.color_pair(3))
        window.addstr(sy + 1, sx, "  ", cs.color_pair(3))

        window.refresh()
        time.sleep(delay)


def display_maze(maze: generate_maze.Maze, config: dict) -> str:
    """
    Main function to display the complete maze on terminal.
    Uses curses library to draw header and the maze with walls and markers.
    Waits for key press before closing.
    """

    result = "exit"

    def draw(window: cs.window) -> None:
        nonlocal result
        nonlocal maze
        cs.curs_set(0)
        cs.noecho()
        window.keypad(True)
        cs.start_color()
        cs.use_default_colors()

        # for cells white background
        cs.init_pair(1, cs.COLOR_BLACK, cs.COLOR_WHITE)

        # for cells black background
        cs.init_pair(2, cs.COLOR_BLACK, cs.COLOR_BLACK)

        # Green Color For Path
        cs.init_pair(3, cs.COLOR_BLACK, cs.COLOR_GREEN)

        cs.init_pair(4, cs.COLOR_BLUE, cs.COLOR_BLACK)
        cs.init_pair(5, cs.COLOR_WHITE, cs.COLOR_BLACK)

        # Foreground default, background black
        cs.init_pair(10, -1, cs.COLOR_BLACK)
        window.bkgd(' ', cs.color_pair(10))

        window.erase()

        def step() -> None:
            window.erase()
            draw_the_maze_from_struct(
                window,
                maze.maze_struct,
                config["WIDTH"],
                config["HEIGHT"],
            )
            draw_entry_exit(window, config["ENTRY"], config["EXIT"])
            window.noutrefresh()
            cs.doupdate()
            time.sleep(0.01)

        key = draw_a_maze_ing_header(window)

        window.erase()
        maze_width = config['WIDTH']
        maze_height = config['HEIGHT']
        maze_entry = config['ENTRY']
        maze_exit = config['EXIT']
        perfect = config['PERFECT']
        visible_path = False
        path = None
        color_walls = 5  # this number for white to draw walls
        if key == "1" or key in ('\n', 'KEY_ENTER'):
            window.erase()
            maze.maze_generator(maze_entry, step, perfect)
            draw_the_maze_from_struct(window, maze.maze_struct, maze_width,
                                      maze_height, color_walls)
            draw_entry_exit(window, maze_entry, maze_exit)
            draw_maze_menu(window, maze_width, maze_height)
            window.refresh()

            cs.flushinp()
            while True:
                key = window.getkey()
                if key in ('R', 'r'):
                    n_maze = generate_maze.Maze(maze_width, maze_height)

                    maze = n_maze
                    visible_path = False
                    path = None
                    color_walls = 5

                    window.erase()
                    maze.maze_generator(maze_entry, step, perfect)

                    window.erase()
                    draw_the_maze_from_struct(window, maze.maze_struct,
                                              maze_width, maze_height,
                                              color_walls)
                    draw_entry_exit(window, maze_entry, maze_exit)
                    draw_maze_menu(window, maze_width, maze_height)
                    window.refresh()
                    cs.flushinp()

                if key == '1':
                    if path is None:
                        path = maze.maze_solver(maze_entry, maze_exit)
                    animate_path(window, maze_entry, path)
                    cs.flushinp()
                    visible_path = True
                elif key == '2':
                    if path is None:
                        continue
                    if visible_path is False:
                        animate_path(window, maze_entry, path, 0)
                        cs.flushinp()
                        draw_entry_exit(window, maze_entry, maze_exit)
                        visible_path = True
                    else:
                        window.erase()
                        draw_the_maze_from_struct(window, maze.maze_struct,
                                                  maze_width, maze_height,
                                                  color_walls)
                        draw_entry_exit(window, maze_entry, maze_exit)
                        draw_maze_menu(window, maze_width, maze_height)
                        window.refresh()
                        visible_path = False
                elif key == '3':
                    if player_mode(window, maze_entry, maze_exit,
                                   maze.maze_struct, maze_width, maze_height):
                        draw_congratulations(window)
                        time.sleep(3)
                        break
                elif key == "4":
                    if color_walls == 5:
                        color_walls = 4
                    elif color_walls == 4:
                        color_walls = 5
                    window.erase()
                    maze.maze_generator(maze_entry, step, perfect)
                    draw_the_maze_from_struct(window, maze.maze_struct,
                                              maze_width, maze_height,
                                              color_walls)
                    draw_entry_exit(window, maze_entry, maze_exit)
                    draw_maze_menu(window, maze_width, maze_height)
                    animate_path(window, maze_entry, path, 0)
                    draw_entry_exit(window, maze_entry, maze_exit)
                    visible_path = True

                    window.refresh()
                    cs.flushinp()
                elif key == "x" or key == "X" or key == '\x1b':
                    result = "done"
                    break
        elif key == "x" or key == "X" or key == '\x1b':
            result = "exit"

    try:
        cs.wrapper(draw)
        return result
    except Exception as e:
        print("Error While Drawing Maze:", e)
        return "exit"
