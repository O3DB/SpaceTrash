import asyncio
import curses

from .animation.curses_tools import sleep, draw_frame

from .global_variables import coroutines, globals, PHRASES
from .settings import GameConfig




def get_garbage_delay_tics(year):
    if year < 1961:
        return 40
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2


def draw_info_bar(canvas, year):
    # chose a suitable comment for the current year
    for date, comment in PHRASES.items():
        if year < date:
            break
    year_info = f'{year}: {comment}'

    game_speed_repr = round(1 / GameConfig.game_speed, 1)
    speed_info = f'Speed: {game_speed_repr}'

    text = f'{year_info} | {speed_info}'

    max_row, max_column = canvas.getmaxyx()
    row = 1
    column = max_column // 2 - len(text) // 2

    canvas.clear()
    canvas.box()
    canvas.addstr(row, column, text)


async def change_year(canvas):
    year = 1957
    while True:
        draw_info_bar(canvas, year)
        await sleep(GameConfig.years_changing_speed)
        year += 1 

        globals['garbage_delay'] = get_garbage_delay_tics(year)
        globals['shotgun_exists'] = year >= GameConfig.shotgun_appeared_at
        GameConfig.increase_game_speed()


def run_scenario(canvas):
    coroutines.append(change_year(canvas))
    
