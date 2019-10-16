import time
import asyncio
import curses

from .animation.fire import fire
from .animation.spaceship import animate_spaceship
from .animation.stars import animate_stars
from .animation.trash import fill_orbit_with_trash
from .animation.curses_tools import load_sprite
from .game_scenario import run_scenario
from .global_variables import coroutines
from .settings import GameConfig


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)

    max_row, max_column = canvas.getmaxyx()

    info_bar_window = canvas.derwin(3, max_column, 0, 0)
    info_bar_window.box()

    # initialize coroutines   
    run_scenario(info_bar_window)
    stars = animate_stars(canvas)
    spaceship = animate_spaceship(canvas, max_row // 2, max_column // 2)
    trash_generator = fill_orbit_with_trash(canvas)
  
    coroutines.extend([*stars, spaceship, trash_generator])

    while coroutines:
        for coroutine in coroutines:
            
            try:
                coroutine.send(None)
                canvas.refresh()
                canvas.border('|', '|')

            except StopIteration:
                coroutines.remove(coroutine)

        time.sleep(GameConfig.game_speed)
            

def start_game():
    curses.update_lines_cols()
    curses.wrapper(draw)