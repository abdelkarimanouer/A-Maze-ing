import curses as cs
import time
from . import generate_maze
from typing import Any, Literal, Callable, List, Dict, Tuple
import random


class DrawMaze:

    """
    Collection of static helper methods for drawing and interacting
    with the maze using curses.
    """

    @staticmethod
    def get_cell_walls_from_struct(row: int, col: int,
                                   maze_struct: List[List[generate_maze.Cell]]
                                   ) -> Dict[str, bool]:
        """
        Same idea as get_cell_walls(), but reads from maze_struct (Cell.wall).
        """
        if row < 0 or col < 0:
            return {'east': False, 'north': False, 'west': False,
                    'south': False}

        if row >= len(maze_struct):
            return {'east': False, 'north': False, 'west': False,
                    'south': False}

        if col >= len(maze_struct[0]):
            return {'east': False, 'north': False, 'west': False,
                    'south': False}

        v = maze_struct[row][col].wall

        return {
            'north': bool(v & 1),
            'east': bool(v & 2),
            'south': bool(v & 4),
            'west': bool(v & 8),
        }

    @staticmethod
    def get_corner_walls(cy: int, cx: int,
                         maze_struct: List[List[generate_maze.Cell]]
                         ) -> Dict[str, bool]:
        """
        Same idea as get_corner_walls(), but reads from maze_struct.
        """
        top_left = DrawMaze.get_cell_walls_from_struct(cy - 1, cx - 1,
                                                       maze_struct)
        top_right = DrawMaze.get_cell_walls_from_struct(cy - 1, cx,
                                                        maze_struct)
        bottom_left = DrawMaze.get_cell_walls_from_struct(cy, cx - 1,
                                                          maze_struct)
        bottom_right = DrawMaze.get_cell_walls_from_struct(cy, cx,
                                                           maze_struct)

        up = top_left['east'] or top_right['west']
        down = bottom_left['east'] or bottom_right['west']
        left = top_left['south'] or bottom_left['north']
        right = top_right['south'] or bottom_right['north']

        return {'up': up, 'down': down, 'left': left, 'right': right}

    @staticmethod
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

    @staticmethod
    def fill_cells(window: cs.window,
                   maze_struct: List[List[generate_maze.Cell]],
                   width: int, height: int, *,
                   use_visited: bool) -> None:

        """ this method to fill cells with white or black"""

        for y in range(height):
            for x in range(width):
                if use_visited and maze_struct[y][x].visited:
                    attr = cs.color_pair(2)
                else:
                    attr = cs.color_pair(1)

                sy = y * 2 + 1
                sx = x * 3 + 1

                window.addstr(sy,     sx,     "  ", attr)
                window.addstr(sy + 1, sx,     "  ", attr)

    @staticmethod
    def draw_the_maze(window: cs.window,
                      maze_struct: List[List[generate_maze.Cell]],
                      width: int, height: int,
                      color_walls: int = 5,
                      use_visited: bool = True) -> None:
        """
        Draw maze using maze_struct (live walls), not maze_lines.
        """
        DrawMaze.fill_cells(window, maze_struct, width, height,
                            use_visited=use_visited)
        corner_rows = height + 1
        corner_cols = width + 1

        for cy in range(corner_rows):
            for cx in range(corner_cols):
                walls = DrawMaze.get_corner_walls(cy, cx, maze_struct)
                char = DrawMaze.get_corner_char(walls['up'], walls['down'],
                                                walls['left'], walls['right'])

                screen_y = cy * 2
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

    @staticmethod
    def draw_entry_exit(window: cs.window, entry: Tuple[int, int],
                        exit: Tuple[int, int]) -> None:
        """
        Places entry and exit markers on the maze.
        Entry is marked with flag emoji 🏁.
        Exit is marked with flag emoji 🚩.
        """
        entry_x, entry_y = entry
        entry_screen_y = (entry_y * 2) + 1
        entry_screen_x = (entry_x * 3) + 1
        window.addstr(entry_screen_y, entry_screen_x, '🏁')

        exit_x, exit_y = exit
        exit_screen_y = (exit_y * 2) + 1
        exit_screen_x = (exit_x * 3) + 1
        window.addstr(exit_screen_y, exit_screen_x, '🚩')

    @staticmethod
    def display_menu_with_header(window: cs.window, perfect: bool) -> None:
        """
        Shows menu options centered on screen.
        """
        menu = [
            "1. Generate Maze",
            f"2. Perfect Maze: {perfect}",
            "X. Exit"
        ]

        max_y, max_x = window.getmaxyx()

        menu_width = max(len(line) for line in menu)

        start_x = (max_x - menu_width) // 2
        start_y = 16

        for i, line in enumerate(menu):
            window.addstr(start_y + i, start_x, line, cs.A_BOLD)

        window.refresh()

    @staticmethod
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
                window.addstr(menu_y + i, menu_x, line,
                              cs.A_BOLD | cs.A_UNDERLINE)
            elif line:
                window.addstr(menu_y + i, menu_x, line, cs.A_BOLD)

    @staticmethod
    def draw_a_maze_ing_header(window: cs.window, perfect: bool) -> str:

        """ this method for show the header A-Maze-Ing """

        header = """
██████████████████████████████████████████████████████████████████████████████┓
█                                                                            █┃
█                                                                            █┃
█     █████┓       ███┓   ███┓ █████┓ ███████┓███████┓      ██┓███┓   ██┓    █┃
█    ██┏━━██┓      ████┓ ████┃██┏━━██┓┗━━███┏┛██┏━━━━┛      ██┃████┓  ██┃    █┃
█    ███████┃█████┓██┏████┏██┃███████┃  ███┏┛ █████┓  █████┓██┃██┏██┓ ██┃    █┃
█    ██┏━━██┃┗━━━━┛██┃┗██┏┛██┃██┏━━██┃ ███┏┛  ██┏━━┛  ┗━━━━┛██┃██┃┗██┓██┃    █┃
█    ██┃  ██┃      ██┃ ┗━┛ ██┃██┃  ██┃███████┓███████┓      ██┃██┃ ┗████┃    █┃
█    ┗━┛  ┗━┛      ┗━┛     ┗━┛┗━┛  ┗━┛┗━━━━━━┛┗━━━━━━┛      ┗━┛┗━┛  ┗━━━┛    █┃
█                                                                            █┃
█                            By: aanouer & achouaf                           █┃
█                                                                            █┃
██████████████████████████████████████████████████████████████████████████████┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
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
            DrawMaze.display_menu_with_header(window, perfect)
            for i, line in enumerate(lines):
                if line.strip():
                    window.addstr(start_y + i, start_x, line, cs.A_BOLD)
            window.refresh()
            try:
                key = window.getkey()
                if (
                    key == '1' or key == '2' or key == 'x'
                    or key == 'X' or key == '\x1b'
                ):
                    window.nodelay(False)
                    return key
            except Exception:
                key = None

    @staticmethod
    def draw_congratulations(window: cs.window) -> None:

        """ this method for show the congratulation
        header after player win """

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

    @staticmethod
    def player_mode(window: cs.window, entry: Tuple[int, int],
                    exit: Tuple[int, int],
                    maze_struct: List[List[generate_maze.Cell]], width: int,
                    height: int) -> bool:

        """ this method showed player mode so the user
        can move the player to the exit by arrows """

        x, y = entry

        while True:
            key = window.getkey()
            if key == "x" or key == "X" or key == '\x1b':
                return False

            window.addstr((y * 2) + 1, (x * 3) + 1, "  ", cs.color_pair(2))

            walls = DrawMaze.get_cell_walls_from_struct(y, x, maze_struct)

            if key == "KEY_UP" and not walls['north']:
                y -= 1
            elif key == "KEY_DOWN" and not walls['south']:
                y += 1
            elif key == "KEY_LEFT" and not walls['west']:
                x -= 1
            elif key == "KEY_RIGHT" and not walls['east']:
                x += 1
            elif key == "1" or key == "2" or key == "4" or key in ("R", "r"):
                return False

            window.addstr((y * 2) + 1, (x * 3) + 1, "👤", cs.color_pair(2))
            window.refresh()

            if (x, y) == exit:
                time.sleep(0.1)
                return True

    @staticmethod
    def animate_path(window: cs.window, entry: Tuple[int, int],
                     path: Any | Literal[''],
                     delay: float = 0.08) -> None:

        """ this method for draw path with animation """
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
                gy = old_y * 2 + 1
                window.addstr(gy,     gx, " ", cs.color_pair(3))
            else:  # N or S
                gy = min(old_y, y) * 2 + 2
                gx = old_x * 3 + 1
                window.addstr(gy, gx, "  ", cs.color_pair(3))

            # paint new cell (FULL interior 2x2)
            sy = y * 2 + 1
            sx = x * 3 + 1
            window.addstr(sy,     sx, "  ", cs.color_pair(3))

            window.refresh()
            time.sleep(delay)

    @staticmethod
    def set_colors() -> None:

        """ this method for set colors to use them later in the maze"""

        cs.start_color()
        cs.use_default_colors()

        cs.init_pair(1, cs.COLOR_BLACK, cs.COLOR_WHITE)
        cs.init_pair(2, cs.COLOR_BLACK, cs.COLOR_BLACK)
        cs.init_pair(3, cs.COLOR_BLACK, cs.COLOR_GREEN)
        cs.init_pair(4, cs.COLOR_BLUE, cs.COLOR_BLACK)
        cs.init_pair(5, cs.COLOR_WHITE, cs.COLOR_BLACK)
        cs.init_pair(6, cs.COLOR_RED, cs.COLOR_BLACK)
        cs.init_pair(10, -1, cs.COLOR_BLACK)

    @staticmethod
    def first_generate_maze(window: cs.window, maze: generate_maze.Maze,
                            maze_entry: Tuple[int, int], maze_width: int,
                            maze_height: int, color_walls: int,
                            perfect: bool,
                            maze_exit: Tuple[int, int],
                            step: Callable[[], None]) -> None:

        """ this method for generate method for the first time"""

        window.erase()
        maze.maze_generator(maze_entry, step, perfect)
        DrawMaze.draw_the_maze(window, maze.maze_struct,
                               maze_width, maze_height, color_walls)
        DrawMaze.draw_entry_exit(window, maze_entry, maze_exit)
        DrawMaze.draw_maze_menu(window, maze_width, maze_height)
        window.refresh()

        cs.flushinp()

    @staticmethod
    def handle_maze_menu(window: cs.window, maze: generate_maze.Maze,
                         maze_width: int, maze_height: int,
                         maze_entry: Tuple[int, int],
                         maze_exit: Tuple[int, int],
                         color_walls: int, perfect: bool,
                         maze_box: Dict[str, generate_maze.Maze],
                         step: Callable[[], None],
                         seed: int, seed_exist: bool
                         ) -> Tuple[str, generate_maze.Maze]:

        """ this method to handle and show the correct
        thing that user choose """

        visible_path = False
        path = None
        key = None
        result = "exit"

        while True:
            key = window.getkey()
            if key in ('R', 'r'):
                if seed_exist is False:
                    seed = random.randint(1, 100)
                n_maze = generate_maze.Maze(maze_width, maze_height, seed)
                maze_box["maze"] = n_maze

                maze = n_maze
                visible_path = False
                path = None
                color_walls = 5

                window.erase()
                maze_box["maze"].maze_generator(maze_entry, step, perfect)

                window.erase()
                DrawMaze.draw_the_maze(window, maze_box["maze"].maze_struct,
                                       maze_width, maze_height,
                                       color_walls)
                DrawMaze.draw_entry_exit(window, maze_entry, maze_exit)
                DrawMaze.draw_maze_menu(window, maze_width, maze_height)
                window.refresh()
                cs.flushinp()

            if key == '1':
                if path is None:
                    path = maze.maze_solver(maze_entry, maze_exit)
                DrawMaze.animate_path(window, maze_entry, path)
                cs.flushinp()
                visible_path = True
            elif key == '2':
                if path is None:
                    continue
                if visible_path is False:
                    DrawMaze.animate_path(window, maze_entry, path, 0)
                    cs.flushinp()
                    DrawMaze.draw_entry_exit(window, maze_entry, maze_exit)
                    visible_path = True
                else:
                    window.erase()
                    DrawMaze.draw_the_maze(window, maze.maze_struct,
                                           maze_width, maze_height,
                                           color_walls)
                    DrawMaze.draw_entry_exit(window, maze_entry, maze_exit)
                    DrawMaze.draw_maze_menu(window, maze_width, maze_height)
                    window.refresh()
                    visible_path = False
            elif key == '3':
                if visible_path:
                    window.erase()
                    DrawMaze.draw_the_maze(window, maze.maze_struct,
                                           maze_width, maze_height,
                                           color_walls)
                    DrawMaze.draw_entry_exit(window, maze_entry, maze_exit)
                    DrawMaze.draw_maze_menu(window, maze_width, maze_height)
                    window.refresh()
                    visible_path = False
                rs = DrawMaze.player_mode(window, maze_entry, maze_exit,
                                          maze.maze_struct, maze_width,
                                          maze_height)
                if rs:
                    DrawMaze.draw_congratulations(window)
                    time.sleep(3)
                    break
                elif rs is False:
                    window.erase()
                    DrawMaze.draw_the_maze(window,
                                           maze_box["maze"].maze_struct,
                                           maze_width, maze_height,
                                           color_walls)
                    DrawMaze.draw_entry_exit(window, maze_entry, maze_exit)
                    DrawMaze.draw_maze_menu(window, maze_width, maze_height)
                    window.refresh()
                    cs.flushinp()
            elif key == "4":
                if color_walls == 4:
                    color_walls = 5
                elif color_walls == 5:
                    color_walls = 6
                elif color_walls == 6:
                    color_walls = 4
                window.erase()
                DrawMaze.draw_the_maze(window, maze_box["maze"].maze_struct,
                                       maze_width, maze_height,
                                       color_walls)
                DrawMaze.draw_entry_exit(window, maze_entry, maze_exit)
                DrawMaze.draw_maze_menu(window, maze_width, maze_height)
                if path is not None:
                    DrawMaze.animate_path(window, maze_entry, path, 0)
                    DrawMaze.draw_entry_exit(window, maze_entry, maze_exit)
                    visible_path = True
                else:
                    visible_path = False

                window.refresh()
                cs.flushinp()
            elif key == "x" or key == "X" or key == '\x1b':
                result = "done"
                break
        return result, maze_box["maze"]

    @staticmethod
    def update_perfect_in_config(filename: str, value: bool) -> None:

        """ this method for update the config file """
        with open(filename, "r") as f:
            lines = f.readlines()

        with open(filename, "w") as f:
            for line in lines:
                if line.startswith("PERFECT="):
                    f.write(f"PERFECT={value}\n")
                else:
                    f.write(line)


def display_maze(maze: generate_maze.Maze, config: Dict["str", Any]) -> str:
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

        DrawMaze.set_colors()
        window.bkgd(' ', cs.color_pair(10))

        window.erase()

        maze_box = {"maze": maze}

        def step() -> None:
            window.erase()
            DrawMaze.draw_the_maze(
                window,
                maze_box["maze"].maze_struct,
                config["WIDTH"],
                config["HEIGHT"],
            )
            DrawMaze.draw_entry_exit(window, config["ENTRY"], config["EXIT"])
            window.noutrefresh()
            cs.doupdate()
            time.sleep(0.01)

        maze_width = config['WIDTH']
        maze_height = config['HEIGHT']
        maze_entry = config['ENTRY']
        maze_exit = config['EXIT']
        perfect = config['PERFECT']
        color_walls = 5  # this number for white to draw walls

        key = DrawMaze.draw_a_maze_ing_header(window, perfect)
        window.erase()

        if key == "2":
            while key not in ("1", "x", "X"):
                perfect = not perfect
                DrawMaze.update_perfect_in_config("config.txt", perfect)
                window.clear()
                key = DrawMaze.draw_a_maze_ing_header(window, perfect)
                window.erase()
        if key == "1" or key in ('\n', 'KEY_ENTER'):
            DrawMaze.first_generate_maze(window, maze, maze_entry, maze_width,
                                         maze_height, color_walls, perfect,
                                         maze_exit, step)
            result, maze = DrawMaze.handle_maze_menu(window, maze, maze_width,
                                                     maze_height, maze_entry,
                                                     maze_exit, color_walls,
                                                     perfect, maze_box, step,
                                                     config["SEED"],
                                                     config["SEED_EXIST"])

    try:
        cs.wrapper(draw)
        return result
    except Exception as e:
        print("Error While Drawing Maze:", e)
        return "exit"
