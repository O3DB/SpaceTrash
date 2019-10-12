import asyncio
import curses

from .obstacles import Obstacle
from . import OBSTACLES, OBSTACLES_IN_LAST_COLLISION


async def fire(canvas, start_row, start_column, rows_speed=-1, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        # check for collision
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        for obstacle in OBSTACLES:
            if obstacle.has_collision(row, column):
                OBSTACLES_IN_LAST_COLLISION.append(obstacle)
                return    
        row += rows_speed
        column += columns_speed

def fill_orbit_with_trash():
    pass