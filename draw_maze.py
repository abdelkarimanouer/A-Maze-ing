import curses as cs


def draw_board(window: cs.window, width: int, height: int):

    window.addch(1, 0, '┏')
    window.addch(0, width, '┓')
    window.addch(height, 1, '┗')
    window.addch(height, width, '┛')

    for c in range(2, width):
        window.addch(1, c, '━')
        window.addch(height, c, '━')

    for r in range(2, height):
        window.addch(r, 1, '┃')
        window.addch(r, width, '┃')


def draw_waze(maze_lines: list[str], config: dict):
    def draw(window: cs.window):
        cs.curs_set(0)
        window.clear()

        width = config['WIDTH'] * 3
        height = config['HEIGHT'] * 3

        draw_board(window, width, height)

        window.refresh()
        window.getch()

    try:
        cs.wrapper(draw)
    except Exception as e:
        print("Error While Drawing Maze:", e)
