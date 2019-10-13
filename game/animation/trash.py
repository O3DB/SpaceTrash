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
from ..global_variables import coroutines, obstacles, obstacles_in_last_collision, globals
from .explosion import explode


async def fly_trash(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1
    obstacle = Obstacle(row, column, *get_frame_size(garbage_frame))
    obstacles.append(obstacle)

    while row < rows_number:
        if obstacle in obstacles_in_last_collision:
            obstacles_in_last_collision.remove(obstacle)
            await explode(canvas, *obstacle.get_center())
            return

        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)

        row += speed
        obstacle.row = row
    
    obstacles.remove(obstacle)



async def fill_orbit_with_trash(canvas):
    """Generate trash flow"""
    trash_sprites = upload_sprite('trash')
    max_row, max_column = canvas.getmaxyx()
   
    while True:
        sprite = random.choice(trash_sprites)
        _, sprite_width = get_frame_size(sprite)
        start_column = random.randint(1, max_column - 1 - sprite_width)

        coroutine = fly_trash(canvas, start_column, sprite)
        coroutines.append(coroutine)

        await sleep(globals['garbage_delay'])