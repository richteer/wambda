from creature import Creature
import curses

class Player(Creature):
	_disp = None

	def __init__(self, disp):
		self._disp = disp
		self._health = 20
		self._maxhealth = 20
		self._speed = 1
		self._ch = '@'
		self._set_pos(6,6)
		self._name = "Igor the Idiot"

	def _invoke(self, f):
		if f.__class__.__name__ == "method":
			f()
		elif f.__class__.__name__ == "function":
			f(self)
		else:
			self._disp("Something went wrong on the invoke, yo")


	def _takedamage(self, amount, source=None):
		self._health -= amount
		if source:
			self._disp.prompt("You take {} damage from the {}".format(amount, source._name))

	def pickup(self):
		it = self._zone.tiles[self._y][self._x].item
		self._zone.tiles[self._y][self._x].item = None
		if it:
			if hasattr(it, "gold"):
				self._gold += it.gold
				self._disp.prompt("You picked up {} gold!".format(it.gold))
			else:
				setattr(self, it.func.__name__, it.func)
				self._disp.prompt("You assimilated the '{}' lambda".format(it.func.__name__))
		else:
			self._disp.prompt("There is nothing to pick up!")

	def show_inv(self):
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
			self._invoke(foo)	

	def _fffff(self):
		self._disp.prompt("You fall on your sword")
		self._disp.screen.getkey()
		self._health = 0

