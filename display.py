import curses
import sys

class Display():

	screen = None
	_prompt = None
	game   = None
	status = None

	gamesz = (0,0)

	# TODO: This
	def __init__(self):
		self.screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.screen.keypad(True)

		self._prompt = curses.newwin(1, curses.COLS, 0, 0)
		self.game   = curses.newwin(curses.LINES - 3, curses.COLS, 1, 0)
		self.status = curses.newwin(2, curses.COLS, curses.LINES - 2, 0)

		self.gamesz = (curses.LINES - 4, curses.COLS)


	def __del__(self):
		curses.nocbreak()
		self.screen.keypad(False)
		curses.echo()
		#curses.endwin()

	def draw_zone(self, zone):
		for i in range(len(zone.tiles)):
			for j in range(len(zone.tiles[i])):
				self.game.addch(i, j, zone.tiles[i][j].getsym() if zone.tiles[i][j] else ' ')
	
	def prompt(self, text):
		self._prompt.addstr(0,0,text)
		self._prompt.refresh()

