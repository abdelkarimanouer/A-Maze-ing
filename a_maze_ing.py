import random
import sys
from parsing import file_parsing, config_parsing


bin_value = {'s': 1, 'w': 2, 'n': 4, 'e': 8}
directions = ['s', 'w', 'n', 'e']
y_axis = {'s': 1, 'w': 0, 'n': -1, 'e': 0}
x_axis = {'s': 0, 'w': -1, 'n': 0, 'e': 1}
rev_directions = {'s': 'n', 'w': 'e', 'n': 's', 'e': 'w'}


class Cell:

    def __init__(self):
        self.wall = 15
        self.visited = False


class Maze:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze_struct = [
            [Cell() for w in range(width)] for h in range(height)
        ]

    def maze_generator(self, entry):
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


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("ERROR: (python3 a_maze_ing.py <config.txt>)")
        sys.exit(1)

    configuration = file_parsing(sys.argv[1])

    config = config_parsing(configuration)

    maze = Maze(config["WIDTH"], config["HEIGHT"])
    maze.maze_generator(config["ENTRY"])
    with open(config['OUTPUT_FILE'], "a") as maze_file:
        for _ in maze.maze_struct:
            for c in _:
                maze_file.write(format(c.wall, 'X'))
            maze_file.write("\n")
