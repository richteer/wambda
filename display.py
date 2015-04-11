import curses
import sys
from termcolor import colored

dirs = {
	'h' : (0,-1),
	'j' : (1,0),
	'k' : (-1,0),
	'l' : (0,1),

	'KEY_RIGHT': (0,1),
	'KEY_LEFT' : (0,-1),
	'KEY_DOWN' : (1,0),
	'KEY_UP'   : (-1,0)
}


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
		curses.curs_set(0)
		curses.start_color()
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)


	def __del__(self):
		curses.nocbreak()
		self.screen.keypad(False)
		curses.echo()
		#curses.endwin()

	def draw_zone(self, zone):
		for i in range(len(zone.tiles)):
			for j in range(len(zone.tiles[i])):
				self.game.addch(i, j, zone.tiles[i][j].getsym() if zone.tiles[i][j] else ' ')
	
	def draw_status(self, player):
		char = "#"
		a = "Health: ({:2d}/{}) ".format(player._health, player._maxhealth)
		b = "{}{}".format("".join([char for i in range(int(player._health/player._maxhealth * 20))]), "".join([' ' for i in range(20 - int(player._health/player._maxhealth * 20))]))
		c = 1
		if player._health/player._maxhealth <= .5:
			c = 2
		if player._health/player._maxhealth <= .25:
			c = 3

		self.status.addstr(0,0,a + "[")
		self.status.addstr(0,len(a) + 1,b, curses.color_pair(c))
		self.status.addstr(0,len(a)+len(b)+1,"]")
		self.status.addstr(1,0,"  Gold: {0: <}".format(player._gold))
		self.status.refresh()


	def prompt(self, text):
		self._prompt.addstr(0,0,text)
		self._prompt.refresh()

	def promptdir(self):
		d = None
		while not d:
			self.blank_prompt()
			self._prompt.addstr(0,0, "Which Direction?")
			self._prompt.refresh()
			k = self.screen.getkey()
			d = dirs.get(k)	
		return d	

	def blank_prompt(self):
		self._prompt.addstr(0,0,''.join([" " for i in range(self.gamesz[1]-1)]))
		self._prompt.refresh()
