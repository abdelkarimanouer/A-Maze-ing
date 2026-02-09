*This project has been created as part of the 42 curriculum by aanouer, achouaf.*

# A-Maze-ing

## Description
A-Maze-ing is a Python project focused on generating and visualizing mazes.  
The goal is to explore algorithmic maze generation, parsing configuration files, and rendering the maze in a clear, reproducible way.  
It demonstrates modular design with separate components for generation, drawing, and parsing.

## Instructions
### Requirements
- Python 3.10 or later

### Execution
*This project must be executed from a terminal, not via an IDE “Run” button.*

```bash
make run
```

## Resources
### Learning Resources
[PlayList On Youtube To Learn Curses](https://www.youtube.com/watch?v=Db4oc8qc9RU&list=PLzMcBGfZo4-n2TONAOImWL4sgZsmyMBc8)

### AI Usage
AI was used as a **primary learning and assistance resource** throughout the project.

It was used to:
- Learn and understand the `curses` library and terminal-based rendering
- Clarify programming concepts related to maze generation and pathfinding
- Help diagnose and fix unexpected or non-obvious runtime errors
- Optimize certain parts of the code

## Features
- Terminal-based maze visualization using curses
- Animated maze generation
- Animated shortest path display
- Show / hide solution
- Maze regeneration
- Wall color changing
- Player mode
- Perfect and non-perfect maze support

## Configuration File Structure
The configuration file is a plain text file where each line follows the format:

```txt
KEY=VALUE
```

Lines starting with # are treated as comments and ignored.
### Mandatory keys
```txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Optional keys
```txt
SEED=(put number as VALUE)
```

- SEED enables reproducibility.
- If the SEED key is present, the same configuration will always generate the same maze.
- If the SEED key is removed, the maze is generated randomly at each execution.

## Maze Generation Algorithm
The maze is generated using **recursive backtracking**

## Why This Algorithm
Recursive backtracking was chosen because it is simple to implement and guarantees the generation of a perfect maze with a single valid path between the entry and the exit.

## Reusable Code
The maze generation and pathfinding logic is implemented in the `Maze` class located in the `generate_maze.py` module.  
This code is independent from the terminal display and can be reused in other projects without modification.

## Team and Project Management
### Team roles
- **aanouer**: visual representation, terminal display, animations, and user interaction
- **achouaf**: maze generation logic, configuration parsing, and solver implementation

### Planning and evolution
The project started with implementing the maze generation logic, then configuration parsing, followed by terminal visualization, animation, and additional interaction features.

### What worked well and what could be improved
**What worked well**
- Clear separation between maze generation, parsing, and display
- Stable maze generation with animation and user interaction
- Correct pathfinding and visualization

**What could be improved**
- Add more maze generation algorithms
- Provide additional display modes beyond the terminal

### Tools used
- Python 3
- curses library
- Git
- Terminal (command-line execution)