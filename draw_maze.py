import curses as cs


def draw_waze(maze_lines: list[str], config: dict):
    def draw(window: cs.window):
        cs.curs_set(0)
        window.clear()


        width = config['WIDTH'] * 3
        height = config['HEIGHT'] * 3

        window.addch(0, 0, '┏')
        window.addch(0, width, '┓')
        window.addch(height, 0, '┗')
        window.addch(height, width, '┛')

        for c in range(1, width):
            window.addch(0, c, '━')
            window.addch(height, c, '━')

        for r in range(1, height):
            window.addch(r, 0, '┃')
            window.addch(r, width, '┃')

        window.refresh()
        window.getch()

    try:
        cs.wrapper(draw)
    except Exception as e:
        print("Error While Drawing Maze:", e)
