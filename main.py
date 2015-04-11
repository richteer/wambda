import display
import zone
import curses
import creature
import player
import item

quit = False

disp = display.Display()
player = player.Player(disp)

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
			c._tick()

		if player._health <= 0:
			disp.blank_prompt()
			disp.prompt("Oh noes \o/")
			quit = True
			disp.screen.getkey()


if __name__ == "__main__":
	curses.wrapper(main)
	#main(1)
