import display
import zone
import curses
import creature
import player
import item

quit = False

def end():
	global quit
	quit = True


disp = display.Display()
player = player.Player(disp)

def command():
	global disp
	i = 1
	disp._prompt.addch(0,0,':')
	disp._prompt.refresh()
	string = ""
	k = None
	while True:
		k = disp.screen.getkey()
		if k == "KEY_BACKSPACE":
			string = string[:-1]
			disp._prompt.addch(0,i,' ')
			disp._prompt.refresh()
			continue
		elif k == '\n':
			break
		disp._prompt.addch(0,i,k)
		disp._prompt.refresh()
		string += k
		i += 1

	try:
		g = getattr(player, string)
		if g:
			player._invoke(g)
		disp.blank_prompt()
	except Exception as e:
		disp.prompt("There was an error with your command: " + str(e))

def noop():
	pass


controls = {
	'KEY_RIGHT': lambda: player._invoke(player.move_right),
	'KEY_LEFT': lambda: player._invoke(player.move_left),
	'KEY_DOWN': lambda: player._invoke(player.move_down),
	'KEY_UP': lambda: player._invoke(player.move_up),

	'l': lambda: player._invoke(player.move_right),
	'h': lambda: player._invoke(player.move_left),
	'j': lambda: player._invoke(player.move_down),
	'k': lambda: player._invoke(player.move_up),
	
	'd': lambda: player._takedamage(1),
	'f': lambda: player._invoke(player._fffff),
	'i': lambda: player._invoke(player.show_inv),
	',': lambda: player._invoke(player.pickup),

	'.': noop,

	':': command,
	'q': end
}



def main(s):
	global player
	global disp
	global quit

	z = zone.Zone(disp.gamesz[0], disp.gamesz[1])
	creature.gencreatures(z)
	item.genitems(z)
	player._zone = z
	z.add_creature(player)
	while not quit:
		disp.draw_zone(z)
		disp.game.refresh()
		disp.draw_status(player)


		for c in z.creatures:
			if c._initiative == 0:
				break
			else:
				c._tick()

		k = disp.screen.getkey()

		for c in z.creatures:
			if c._initiative <= 0:
				continue
			else:
				c._tick()

		disp.blank_prompt()
		func = controls.get(k)
		if func:
			func()
		else:
			disp.prompt("Invalid keypress '{}'".format(k.replace('\n','ENTER')))
		if player._health == 0:
			disp.blank_prompt()
			disp.prompt("Oh noes \o/")
			quit = True
			disp.screen.getkey()

if __name__ == "__main__":
	curses.wrapper(main)
	#main(1)
