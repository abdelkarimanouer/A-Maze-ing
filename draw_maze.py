import curses as cs


def draw_waze():
    def draw(window: cs.window):
        cs.curs_set(0)
        window.clear()

        window.addstr(0, 0, "=====")

        window.refresh()
        window.getch()

    try:
        cs.wrapper(draw)
    except Exception as e:
        print("Error While Drawing Maze:", e)
