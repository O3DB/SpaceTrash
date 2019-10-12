import asyncio
import curses

from .curses_tools import sleep, draw_frame

from . import GARBAGE_DELAY, COROUTINES

PHRASES = {
    # Только на английском, Repl.it ломается на кириллице
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


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


def draw_year(canvas, year):
    text = f'{year} {PHRASES.get(year) or ""}'


    max_row, max_column = canvas.getmaxyx()
    row = 0
    column = max_column // 2 - len(text) // 2

    sub_canvas = canvas.derwin(1, max_column, max_row - 2, 0)
    sub_canvas.erase()

    sub_canvas.addstr(row, column, text)


async def change_year(canvas):
    year = 1957
    while True:
        draw_year(canvas, year)
        await sleep(29) # change year for evey 3 seconds
                        # 1 turn missed during draw_year execution
        year += 1 
        GARBAGE_DELAY = get_garbage_delay_tics(year)


def run_scenario(canvas):
    COROUTINES.append(change_year(canvas))
    
