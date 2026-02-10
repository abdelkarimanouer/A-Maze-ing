import sys


def file_parsing(file_name: str) -> dict:
    """
    Reads a config file and returns its content as dictionary.
    Skips comment lines that start with #.
    Exits if file not found or line is invalid.
    """
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
                key = key.upper()

                if key == "" or value == "":
                    print(f"ERROR: invalid line ({line})")
                    sys.exit(1)

                config[key.strip()] = value.strip()

    except FileNotFoundError as error:
        print(f"ERROR: {error}")
        sys.exit(1)
    return config


def config_parsing(config: dict) -> dict:
    """
    Validates and converts config values to correct types.
    Checks if maze size, entry and exit points are valid.
    Exits if any value is wrong or missing.
    """
    try:
        config["SEED"] = config["SEED"]
        config["SEED_EXIST"] = True
    except Exception:
        config["SEED_EXIST"] = False

    try:
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])

        config["ENTRY"] = tuple(map(int, config["ENTRY"].split(",")))
        config["EXIT"] = tuple(map(int, config["EXIT"].split(",")))

        config["OUTPUT_FILE"] = config["OUTPUT_FILE"]

        value = config["PERFECT"].upper()
        if value == "TRUE":
            config["PERFECT"] = True
        elif value == "FALSE":
            config["PERFECT"] = False
        else:
            print("ERROR: PERFECT must be TRUE or FALSE")
            sys.exit(1)

    except ValueError as error:
        print(f"ERROR: {error}")
        sys.exit(1)
    except KeyError as error:
        print(f"ERROR: Key {error} not found")
        sys.exit(1)
    except Exception as error:
        print(f"ERROR: {error}")
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

    return config
