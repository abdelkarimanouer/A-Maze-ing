import curses

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "╔")
    stdscr.addstr(0, 1, "═")
    stdscr.addstr(0, 2, "╗")
    stdscr.addstr(1, 0, "╠")
    stdscr.addstr(1, 1, "═")
    stdscr.addstr(1, 2, "╣")
    stdscr.addstr(2, 0, "╚")
    stdscr.addstr(2, 1, "═")
    stdscr.addstr(2, 2, "╝")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)