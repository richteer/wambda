import curses

class Display():

	screen = None
	prompt = None
	game   = None
	status = None


	# TODO: This
	def __init__(self):
		self.screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.screen.keypad(True)

		self.prompt = curses.newwin(1, curses.COLS, 0, 0)
		self.game   = curses.newwin(curses.LINES - 3, curses.COLS, 1, 0)
		self.status = curses.newwin(2, curses.COLS, curses.LINES - 2, 0)


	def __del__(self):
		curses.nocbreak()
		self.screen.keypad(False)
		curses.echo()

	def draw_creatures(self, ls):
		for l in ls:
			self.game.addch(l.x, l.y, l.ch)
		self.game.refresh()

	def draw_zone(self, zone):
		i = 0
		for z in zone:
			self.game.addstr(i, 0, ''.join([zl.ch for zl in z]))
			i += 1
		self.game.refresh()

if __name__ == "__main__":
	
	d = Display()

	d.prompt.refresh()
	d.game.refresh()
	d.status.refresh()

	del d
