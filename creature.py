
class Creature():

	_health = 1
	_speed = 1
	_ch = '='
	_zone = None

	_x = 0
	_y = 0

	def __init__(self, hp, speed, ch):
		self._health = hp
		self._speed = speed
		self._ch = ch

	def _set_pos(self, y,x):
		self._x = x
		self._y = y

	def _move(self, y, x):	
		self._zone.tiles[self._y][self._x].creature = None
		self._x += x
		self._y += y
		self._zone.tiles[self._y][self._x].creature = self

	def _trymove(self, y, x):
		return not self._zone.tiles[y][x].solid

	def move_left(self):
		if self._trymove(self._y, self._x-1):
			self._move(0,-1)

	def move_right(self):
		if self._trymove(self._y, self._x+1):
			self._move(0,1)

	def move_up(self):
		if self._trymove(self._y-1, self._x):
			self._move(-1,0)

	def move_down(self):
		if self._trymove(self._y+1, self._x):
			self._move(1,0)



# TODO: This
def gencreatures(zone):
	pass
