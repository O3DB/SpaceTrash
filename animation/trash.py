import asyncio
import curses
import random

from .curses_tools import (
    upload_sprite,
    sleep,
    draw_frame,
    get_frame_size,
)
from .obstacles import Obstacle, show_obstacles
from . import COROUTINES, OBSTACLES, OBSTACLES_IN_LAST_COLLISION, GARBAGE_DELAY
from .explosion import explode


async def fly_trash(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        obstacle = Obstacle(row, column, *get_frame_size(garbage_frame))
        OBSTACLES.append(obstacle)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        OBSTACLES.pop(0)
        if obstacle in OBSTACLES_IN_LAST_COLLISION:
            OBSTACLES_IN_LAST_COLLISION.remove(obstacle)
            COROUTINES.append(explode(canvas, *obstacle.get_center()))
            return




async def fill_orbit_with_trash(canvas):
    """Generate trash flow"""
    trash_sprites = upload_sprite('trash')
    max_row, max_column = canvas.getmaxyx()
    global GARBAGE_DELAY
    #remove then
    COROUTINES.append(show_obstacles(canvas, OBSTACLES))
    while True:
        sprite = random.choice(trash_sprites)
        start_column = random.randint(1, max_column - 1)

        coroutine = fly_trash(canvas, start_column, sprite)
        COROUTINES.append(coroutine)

        await sleep(GARBAGE_DELAY)