import asyncio
import curses
import random

from .curses_tools import sleep

async def blink(canvas, row, column, symbol='*', delay=0):
    await sleep(delay)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(tics=20)

        canvas.addstr(row, column, symbol)
        await sleep(tics=3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(tics=5)

        canvas.addstr(row, column, symbol)
        await sleep(tics=3)


def animate_stars(canvas, stars_num=100):
    symbols = '+*.:'
    max_row, max_column = canvas.getmaxyx()
    max_delay = 30
    
    coroutines = []
    for _ in range(stars_num):
        row = random.randint(2, max_row - 1)
        column = random.randint(2, max_column - 1)
        symbol = random.choice(symbols)
        delay = random.randint(0, max_delay)
        coroutine = blink(canvas, row, column, symbol, delay)
        coroutines.append(coroutine)
    
    return coroutines