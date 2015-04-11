import curses

class Item():
	ch = '~'
	func = None

	def __init__(self, ch, func):
		self.ch = ch
		if ch == "*":
			self.gold = func
		else:
			self.func = func

def attack(self):
	if self.__class__.__name__ != "Player":
		# TODO: Bounds check this
		potential = [self._zone.tiles[self._y-1][self._x].creature,
						self._zone.tiles[self._y+1][self._x].creature,
						self._zone.tiles[self._y][self._x-1].creature,
						self._zone.tiles[self._y][self._x+1].creature]
		for p in potential:
			if p.__class__.__name__ == "Player":
				p._takedamage(1, source=self)
		
		return
	
	y,x = self._disp.promptdir()
	c = self._zone.tiles[self._y + y][self._x + x].creature
	if c:
		r = c._takedamage(1, source=self)
		self._disp.prompt("You attack the {} for {} damage".format(c._name, 1))
		if r:
			self._disp.screen.getkey()
			self._disp.blank_prompt()
			self._disp.prompt("You have slain the {}".format(c._name))
	else:
		self._disp.prompt("You attack the air")


def bind(self):
	if self.__class__.__name__ != "Player":
		return

	self._disp.prompt("What key to bind?")
	key = self._disp.screen.getkey()
	self._disp.blank_prompt()
	self._disp.prompt("Which lambda to bind? (any key for list)")
	self._disp.screen.getkey()
	
	things = [d for d in dir(self) if not d.startswith('_')]
	win = curses.newwin(len(things), curses.COLS, 0,0)

	for i in range(len(things)):
		win.addstr(i,0,"{}.) {}".format(chr(i + ord('a')), things[i]))

	win.refresh()
	k = ord(self._disp.screen.getkey()) - ord('a')


	win.erase()
	del win
	self._disp.blank_prompt()

	if k >= 0 and k < len(things):
		foo = getattr(self, things[k])
		self._controls[key] = lambda s: foo(s)

	self._disp.blank_prompt()
	self._disp.screen.refresh()	
	self._disp.prompt("Bound key '{}' to lambda '{}'".format(key, things[k]))


def genitems(zone):
	zone.tiles[5][5].item = Item('b', bind)
	zone.tiles[10][10].item = Item('y', attack)
	zone.tiles[8][8].item = Item('*', 17)
