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
			self._disp.screen.getkey()

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

		self._disp.blank_prompt()
		self._disp.screen.refresh()	
		if k >= 0 and k < len(things):
			foo = getattr(self, things[k])
			self._invoke(foo)
		

	def _tick(self):
		k = self._disp.screen.getkey()

		self._disp.blank_prompt()
		func = self._controls.get(k)
		if func:
			func(self)
		else:
			self._disp.prompt("Invalid keypress '{}'".format(k.replace('\n','ENTER')))

	def _fffff(self):
		self._disp.prompt("You fall on your sword")
		self._disp.screen.getkey()
		self._health = 0


	def _command(self):
		i = 1
		self._disp._prompt.addch(0,0,':')
		self._disp._prompt.refresh()
		string = ""
		k = None
		while True:
			k = self._disp.screen.getkey()
			if k == "KEY_BACKSPACE":
				string = string[:-1]
				self._disp._prompt.addch(0,i,' ')
				self._disp._prompt.refresh()
				continue
			elif k == '\n':
				break
			self._disp._prompt.addch(0,i,k)
			self._disp._prompt.refresh()
			string += k
			i += 1
	
		try:
			g = getattr(self, string)
			if g:
				self._invoke(g)
			self._disp.blank_prompt()
		except Exception as e:
			self._disp.prompt("There was an error with your command: " + str(e))
	

	_controls = {
		'KEY_RIGHT': lambda s: Player._invoke(s,Player.move_right),
		'KEY_LEFT': lambda s: Player._invoke(s,Player.move_left),
		'KEY_DOWN': lambda s: Player._invoke(s,Player.move_down),
		'KEY_UP': lambda s: Player._invoke(s,Player.move_up),

		'l': lambda s: Player._invoke(s,Player.move_right),
		'h': lambda s: Player._invoke(s,Player.move_left),
		'j': lambda s: Player._invoke(s,Player.move_down),
		'k': lambda s: Player._invoke(s,Player.move_up),

		'd': lambda s: Player._takedamage(s,1),
		'f': lambda s: Player._invoke(s,Player._fffff),
		'q': lambda s: Player._invoke(s,Player._fffff),
		'i': lambda s: Player._invoke(s,Player.show_inv),
		',': lambda s: Player._invoke(s,Player.pickup),

		'.': lambda s: None,
		':': lambda s: Player._invoke(s,Player._command)
}
