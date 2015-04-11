
class Creature():

	_maxhealth = 1
	_health = 1
	_speed = 1
	_ch = '='
	_zone = None
	_gold = 0
	_name = "wat"
	_initiative = 0
	_x = 0
	_y = 0

	def __init__(self, hp, speed, ch, name):
		self._health = hp
		self._maxhealth = hp
		self._speed = speed
		self._ch = ch
		self._name = name

	def _set_pos(self, y,x):
		self._x = x
		self._y = y

	def _tick(self):
		for c in self._zone.creatures:
			if c.__class__.__name__ == "Player":
				p = c
		if not p:
			return None
	
		dx = self._x - p._x
		dy = self._y - p._y

		if (dx == 0 and abs(dy) == 1) or (abs(dx) == 1 and dy == 0):
			p._takedamage(1, source=self)
			

		elif abs(dx) > abs(dy):
			if dx < 0:
				self.move_right()
			else:
				self.move_left()
		elif abs(dx) < abs(dy):
			if dy < 0:
				self.move_down()
			else:
				self.move_up()


	def _move(self, y, x):	
		self._zone.tiles[self._y][self._x].creature = None
		self._x += x
		self._y += y
		self._zone.tiles[self._y][self._x].creature = self

	def _trymove(self, y, x):
		return not (self._zone.tiles[y][x].solid or self._zone.tiles[y][x].creature)

	def _takedamage(self, amount, source=None):
		self._health -= amount
		if self._health == 0:
			self._zone.tiles[self._y][self._x].creature = None
			return True
		return False

	def move_left(self):
		if self._trymove(self._y, self._x-self._speed):
			self._move(0,-self._speed)

	def move_right(self):
		if self._trymove(self._y, self._x+self._speed):
			self._move(0,self._speed)

	def move_up(self):
		if self._trymove(self._y-self._speed, self._x):
			self._move(-self._speed,0)

	def move_down(self):
		if self._trymove(self._y+self._speed, self._x):
			self._move(self._speed,0)

	def pickup(self):
		it = self._zone.tiles[self._y][self._x].item
		self._zone.tiles[self._y][self._x].item = None
		if it:
			if hasattr(it, "gold"):
				self._gold += it.gold
			else:
				setattr(self, it.func.__name__, it.func)
		else:
			pass

	

# TODO: This
def gencreatures(zone):
	c = Creature(2,1,'E',"Emu")
	c._initiative = 1
	c._set_pos(13,7)
	zone.add_creature(c)

