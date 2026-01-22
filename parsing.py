import sys


def file_parsing(file_name: str) -> dict:
    config = {}

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
                config[key.strip()] = value.strip()

    except FileNotFoundError as error:
        print(f"ERROR: {error}")
        sys.exit(1)
    return config


def config_parsing(config: dict):
    try:
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])

        config["ENTRY"] = tuple(map(int, config["ENTRY"].split(",")))
        config["EXIT"] = tuple(map(int, config["EXIT"].split(",")))

        config["PERFECT"] = config["PERFECT"].upper() == "TRUE"

    except ValueError as error:
        print(f"ERROR: {error}")
        sys.exit(1)
    except KeyError as error:
        print(f"ERROR: Key {error} not found")
        sys.exit(1)

    if config["WIDTH"] <= 0 or config["HEIGHT"] <= 0:
        print("ERROR: invalid maze size")
        sys.exit(1)

    if len(config["ENTRY"]) != 2:
        print("ERROR: invalid ENTRY")
        sys.exit(1)

    if len(config["EXIT"]) != 2:
        print("ERROR: invalid EXIT")
        sys.exit(1)

    e_x, e_y = config["ENTRY"]
    x_x, x_y = config["EXIT"]

    if (
        e_x >= config["WIDTH"] or e_x < 0 or
        e_y >= config["HEIGHT"] or e_y < 0
    ):
        print("ERROR: the ENTRY point is out of the maze")
        sys.exit(1)

    if (
        x_x >= config["WIDTH"] or x_x < 0 or
        x_y >= config["HEIGHT"] or x_y < 0
    ):
        print("ERROR: the EXIT point is out of the maze")
        sys.exit(1)

    if config["ENTRY"] == config["EXIT"]:
        print("ERROR: ENTRY and EXIT is the same")
        sys.exit(1)
    
    # if 

    return config
