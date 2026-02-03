import random
import sys
from parsing import file_parsing, config_parsing
from draw_maze import display_maze
from collections import deque


bin_value = {'n': 1, 'e': 2, 's': 4, 'w': 8}
directions = ['s', 'w', 'n', 'e']
y_axis = {'s': 1, 'w': 0, 'n': -1, 'e': 0}
x_axis = {'s': 0, 'w': -1, 'n': 0, 'e': 1}
rev_directions = {'s': 'n', 'w': 'e', 'n': 's', 'e': 'w'}


class Cell:
    """
    Represents a single cell in the maze.
    Each cell has walls and a visited status.
    """

    def __init__(self):
        """
        Creates a new cell.
        Sets all 4 walls and marks cell as not visited.
        """
        self.wall = 15
        self.visited = False


class Maze:
    """
    Represents the maze grid.
    Contains cells and methods to generate the maze.
    """

    def __init__(self, width, height):
        """
        Creates a new maze with given size.
        Fills the maze with cell objects.
        """
        self.width = width
        self.height = height
        self.maze_struct = [
            [Cell() for w in range(width)] for h in range(height)
        ]

        if width >= 15 and height >= 15:
            s_x, s_y = int(width / 2), int(height / 2)

            self.maze_struct[s_y][s_x + 1].visited = True
            self.maze_struct[s_y][s_x + 2].visited = True
            self.maze_struct[s_y][s_x + 3].visited = True
            self.maze_struct[s_y][s_x - 1].visited = True
            self.maze_struct[s_y][s_x - 2].visited = True
            self.maze_struct[s_y][s_x - 3].visited = True
            self.maze_struct[s_y + 1][s_x + 1].visited = True
            self.maze_struct[s_y + 2][s_x + 1].visited = True
            self.maze_struct[s_y + 2][s_x + 2].visited = True
            self.maze_struct[s_y + 2][s_x + 3].visited = True
            self.maze_struct[s_y + -1][s_x + 3].visited = True
            self.maze_struct[s_y - 2][s_x + 1].visited = True
            self.maze_struct[s_y - 2][s_x + 2].visited = True
            self.maze_struct[s_y - 2][s_x + 3].visited = True
            self.maze_struct[s_y - 1][s_x - 3].visited = True
            self.maze_struct[s_y - 2][s_x - 3].visited = True
            self.maze_struct[s_y + 1][s_x - 1].visited = True
            self.maze_struct[s_y + 2][s_x - 1].visited = True

    def maze_generator(self, entry):
        """
        Generates the maze using recursive backtracking.
        Starts from entry point and carves paths randomly.
        """
        x, y = entry
        curent = self.maze_struct[y][x]
        curent.visited = True

        random.shuffle(directions)

        for direction in directions:
            next_x = x + x_axis[direction]
            next_y = y + y_axis[direction]

            if (
                next_x < 0 or next_x >= self.width or
                next_y < 0 or next_y >= self.height
            ):
                continue

            if self.maze_struct[next_y][next_x].visited is False:

                neighbor = self.maze_struct[next_y][next_x]

                curent.wall = curent.wall ^ bin_value[direction]
                neighbor.wall = neighbor.wall ^ bin_value[
                    rev_directions[direction]
                ]
                self.maze_generator([next_x, next_y])

    def maze_solver(self, entry, exit):
        frontier = deque([entry])
        came_from = {entry: None}
        while frontier:
            x, y = frontier.popleft()

            if (x, y) == exit:
                break

            cell = self.maze_struct[y][x]

            for d, dx, dy, move in [
                ('n', 0, -1, 'N'),
                ('s', 0, 1, 'S'),
                ('e', 1, 0, 'E'),
                ('w', -1, 0, 'W')
            ]:
                if not (cell.wall & bin_value[d]):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in came_from:
                        frontier.append((nx, ny))
                        came_from[(nx, ny)] = ((x, y), move)

        path = ""
        curent = exit

        while came_from[curent] is not None:
            curent, move = came_from[curent]
            path = move + path

        return path


def main():
    """
    Main program entry point.
    Reads config, generates mazes in loop, displays them until user exits.
    """

    if len(sys.argv) != 2:
        print("ERROR: (python3 a_maze_ing.py <config.txt>)")
        sys.exit(1)

    configuration = file_parsing(sys.argv[1])
    config = config_parsing(configuration)

    while True:
        maze = Maze(config["WIDTH"], config["HEIGHT"])
        maze.maze_generator(config["ENTRY"])
        maze_lines = []

        open(config['OUTPUT_FILE'], "w").close()
        with open(config['OUTPUT_FILE'], "a+") as maze_file:
            for _ in maze.maze_struct:
                for c in _:
                    maze_file.write(format(c.wall, 'X'))
                maze_file.write("\n")

            maze_file.write("\n")
            maze_file.write(str(config["ENTRY"]).strip("()"))
            maze_file.write("\n")
            maze_file.write(str(config["EXIT"]).strip("()"))
            maze_file.write("\n")
            maze_file.write(maze.maze_solver(config["ENTRY"], config["EXIT"]))

            maze_file.seek(0)
            maze_lines = maze_file.readlines(config["WIDTH"] *
                                             config["HEIGHT"])

        result = display_maze(maze_lines, config)
        if result == "regenerate":
            continue
        elif result == "exit":
            break
    exit()


if __name__ == "__main__":
    main()
