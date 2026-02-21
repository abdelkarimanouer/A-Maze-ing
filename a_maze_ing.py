import sys
from src.mazegen import file_parsing, config_parsing
from src.mazegen import display_maze
import src.mazegen.generate_maze as generate_maze
import random


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
    sys.setrecursionlimit(3000)
    try:
        while True:
            if config["SEED_EXIST"] is False:
                config["SEED"] = random.randint(1, 100)
            maze = generate_maze.Maze(
                config["WIDTH"], config["HEIGHT"], config["SEED"]
            )

            maze.pattern_42()

            result = display_maze(maze, config)
            if result == "done":
                with open(config['OUTPUT_FILE'], "w") as maze_file:
                    for _ in maze.maze_struct:
                        for c in _:
                            maze_file.write(format(c.wall, 'X'))
                        maze_file.write("\n")

                    maze_file.write("\n")
                    maze_file.write(str(config["ENTRY"]).strip("()"))
                    maze_file.write("\n")
                    maze_file.write(str(config["EXIT"]).strip("()"))
                    maze_file.write("\n")
                    maze_file.write(maze.maze_solver(config["ENTRY"],
                                                     config["EXIT"]))
                continue
            elif result == "exit":
                break
        exit()
    except KeyboardInterrupt:
        print("You pressed Ctrl + C and the program Stopping safely")


if __name__ == "__main__":
    main()
