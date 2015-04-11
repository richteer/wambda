import display
import zone
import curses
import creature

quit = False

def end():
	global quit
	quit = True


player = creature.Creature(20,1,'@')
player._set_pos(6,6)

controls = {
	'KEY_RIGHT': player.move_right,
	'KEY_LEFT': player.move_left,
	'KEY_DOWN': player.move_down,
	'KEY_UP': player.move_up,

	'l': player.move_right,
	'h': player.move_left,
	'j': player.move_down,
	'k': player.move_up,

	'q': end
}

def main(s):
	global player

	disp = display.Display()
	z = zone.Zone(disp.gamesz[0], disp.gamesz[1])
	creature.gencreatures(z)
	player._zone = z
	z.add_creature(player)
	while not quit:
		disp.draw_zone(z)
		disp.game.refresh()

		k = disp.screen.getkey()

		func = controls.get(k)
		disp._prompt.clear()
		if func:
			func()
		else:
			disp.prompt("Invalid keypress '{}'".format(k.replace('\n','ENTER')))

if __name__ == "__main__":
	curses.wrapper(main)
	#main(1)
