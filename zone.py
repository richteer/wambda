# TODO: Make this better

class Tile():
	ch = '~'
	solid = False
	creature = None
	item = None

	def __init__(self, ch, solid):
		self.ch = ch
		self.solid = solid

	def getsym(self):
		return self.creature._ch if self.creature else self.item.ch if self.item else self.ch

class Zone():

	tiles = []


	# TODO: Better zone generation here
	def __init__(self, y, x):
		wall = Tile(' ', True)
		self.tiles = [[wall for j in range(x)] for i in range(y)]

		for i in range(5,15):
			for j in range(5,15):
				self.tiles[i][j] = Tile('.', False)

	def add_creature(self, creature):
		if self.tiles[creature._y][creature._x].solid:
			return None # Invalid drop spot
		self.tiles[creature._y][creature._x].creature = creature
