import asyncio
import curses
import random

from .curses_tools import (
    upload_sprite,
    sleep,
    draw_frame,
)

async def fly_trash(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 1

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed



async def fill_orbit_with_trash(canvas, coroutines, speed=20):
    """Generate trash flow"""
    trash_sprites = upload_sprite('trash')
    max_row, max_column = canvas.getmaxyx()

    while True:
        sprite = random.choice(trash_sprites)
        start_column = random.randint(1, max_column - 1)

        coroutine = fly_trash(canvas, start_column, sprite)
        coroutines.append(coroutine)

        await sleep(speed)