import asyncio
import random

from .curses_tools import (
    draw_frame,
    get_frame_size,
)


GAMEOVER_FRAME = \
r'''
   _____                         ____                 
  / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
'''

async def show_gameover(canvas):
    max_row, max_column = canvas.getmaxyx()
    frame_hight, frame_width = get_frame_size(GAMEOVER_FRAME)
    row = max_row // 2 - frame_hight // 2
    column = max_column // 2 - frame_width // 2
    while True:
        draw_frame(canvas, row, column, GAMEOVER_FRAME)
        await asyncio.sleep(0)