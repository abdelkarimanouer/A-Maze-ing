import sys


def file_parsing(file_name: str) -> dict:
    configuration = {}

    try:
        with open(file_name, 'r') as file:
            for line in file:
                line = line.rstrip()

                if line.startswith("#"):
                    continue

                if "=" not in line or line.count('=') > 1:
                    print(f"ERROR: invalid line ({line})")
                    sys.exit(1)

                key, value = line.split("=")
                configuration[key] = value

    except FileNotFoundError as error:
        print(f"ERROR: {error}")
        sys.exit(1)
    return configuration


def check_values(width: int, height: int, entry: tuple, exit: tuple) -> None:

    if width <= 0 or height <= 0:
        print("ERROR: invalid maze size")
        sys.exit(1)

    if (
        entry[0] > width or entry[0] < 0 or
        entry[1] > height or entry[1] < 0
    ):
        print("ERROR: the ENTRY point is out of the maze")
        sys.exit(1)

    if (
        exit[0] > width or exit[0] < 0 or
        exit[1] > height or exit[1] < 0
    ):
        print("ERROR: the EXIT point is out of the maze")
        sys.exit(1)

    if entry == exit:
        print("ERROR: ENTRY and EXIT is the same")
        sys.exit(1)


def config_parsing(configuration: dict):
    try:
        width = int(configuration["WIDTH"])
        height = int(configuration["HEIGHT"])

        entry = tuple(map(int, configuration["ENTRY"].split(",")))
        exit = tuple(map(int, configuration["EXIT"].split(",")))

        output_file = configuration["OUTPUT_FILE"]
        perfect = configuration["PERFECT"].upper() == "TRUE"

    except ValueError as error:
        print(f"ERROR: {error}")
        sys.exit(1)
    except KeyError as error:
        print(f"ERROR: Key {error} not found")
        sys.exit(1)

    check_values(width, height, entry, exit)

    return width, height, entry, exit, output_file, perfect
