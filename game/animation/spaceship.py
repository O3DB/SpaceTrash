import asyncio
import curses

from .curses_tools import (
    load_sprite,
    draw_frame,
    read_controls,
    get_frame_size,
    adjust_sprite_position,
)
from .physics import update_speed
from .fire import fire
from ..global_variables import coroutines, obstacles, globals
from .gameover import show_gameover


future_spaceship_frames = load_sprite('rocket')


async def animate_spaceship(canvas, start_row, start_column):
    """Display animation of spaceship"""
    row, column = start_row, start_column
    max_row, max_column = canvas.getmaxyx()
    
    row_speed, column_speed = 0, 0

    while True:
        spaceship_frame = future_spaceship_frames[0]
        rotate_spaceship_frame()

        rocket_hight, rocket_width = get_frame_size(spaceship_frame)
        
        # readcontrols
        d_row, d_column, space_pressed = read_controls(canvas)
        row_speed, column_speed = update_speed(row_speed, 
                                               column_speed, 
                                               d_row, 
                                               d_column)
        row += row_speed
        column += column_speed

        # validate position and make corrections
        row, column = adjust_sprite_position(
            max_row, max_column,
            rocket_hight, rocket_width,
            row, column
        )

        # draw frames
        draw_frame(canvas, round(row), round(column), spaceship_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, round(row), round(column), spaceship_frame, negative=True)

        # make a shot
        if space_pressed and globals['shotgun_exists']:
            shot = fire(canvas, row, column + 2)
            coroutines.append(shot)

        # check collison
        for obstacle in obstacles:
            if obstacle.has_collision(row, column, rocket_hight, rocket_width):
                coroutines.append(show_gameover(canvas))
                return   


def rotate_spaceship_frame():
    """
    Modify list future_spaceship_frames:
    moves frames inside list as carousel
    """
    frame = future_spaceship_frames.pop(0)
    future_spaceship_frames.append(frame)



    
