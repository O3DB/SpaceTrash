import time
import asyncio
import curses

from animation.fire import fire
from animation.spaceship import animate_spaceship
from animation.stars import animate_stars
from animation.trash import fill_orbit_with_trash
from animation.curses_tools import upload_sprite
from animation.game_scenario import run_scenario

from animation import COROUTINES

def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)

    run_scenario(canvas)
    stars = animate_stars(canvas)
    spaceship = animate_spaceship(canvas, 20, 20)
    trash_generator = fill_orbit_with_trash(canvas)
  
    COROUTINES.extend([*stars, spaceship, trash_generator])

    while True:
        for coroutine in COROUTINES:
            
            try:
                coroutine.send(None)
                canvas.border('|', '|')
                canvas.refresh()

            except StopIteration:
                COROUTINES.remove(coroutine)

        if len(COROUTINES) == 0:
            break

        time.sleep(.1)
            

def start_game():
    curses.update_lines_cols()
    curses.wrapper(draw)