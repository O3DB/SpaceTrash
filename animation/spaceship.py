import asyncio
import curses

from .curses_tools import (
    upload_sprite,
    draw_frame,
    read_controls,
    get_frame_size,
    adjust_sprite_position,
)
from .physics import update_speed
from .fire import fire
from . import COROUTINES

PHYSICS = {
    'row_speed': 0,
    'column_speed': 0,
}

SPACESHIP_FRAMES = upload_sprite('rocket')
# SPACESHIP_FRAME = '12'

async def animate_spaceship(canvas, start_row, start_column):
    """Display animation of spaceship"""
    row, column = start_row, start_column
    max_row, max_column = canvas.getmaxyx()
        
    while True:
        global SPACESHIP_FRAMES
        global PHYSICS
        spaceship_frame = SPACESHIP_FRAMES[0]
        update_spaceship_frame()
        sprite_hight, sprite_width = get_frame_size(spaceship_frame)
        
        #readcontrols
        d_row, d_column, space_pressed = read_controls(canvas)
        row_speed, column_speed = update_speed(PHYSICS['row_speed'], 
                                               PHYSICS['column_speed'], 
                                               d_row, 
                                               d_column)
        PHYSICS['row_speed'] = row_speed
        PHYSICS['column_speed'] = column_speed
        row += row_speed
        column += column_speed
        #validate position and make corrections
        row, column = adjust_sprite_position(
            max_row, max_column,
            sprite_hight, sprite_width,
            row, column
        )
        #draw frames
        draw_frame(canvas, round(row), round(column), spaceship_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, round(row), round(column), spaceship_frame, negative=True)

        if space_pressed:
            shot = fire(canvas, row, column + 2)
            COROUTINES.append(shot)



def update_spaceship_frame():
    """
    Modify global variable SHPACESHIP_FRAMES:
    moves frames inside list as carousel
    """
    global SPACESHIP_FRAMES
    frame = SPACESHIP_FRAMES.pop(0)
    SPACESHIP_FRAMES.append(frame)


# async def animate_spaceship(canvas, start_row, start_column, speed=5):
#     while True:
#         await run_spaceship(canvas, start_row, start_column, speed)
#         await update_spaceship_frame()



    
