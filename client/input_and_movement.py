from sys import exit
from time import time
import curses

from common.constants import *

from client.communication import debug_msg

"""
We load and use the keyboard module only if either we're root
or we're on Windows.
After we do, we keep a reference to it in keyboard.
"""
keyboard = None

"""
Else, we read keyboard input through standard input with curses.
(Note that this results in much less smooth steering.)
In that case, we keep a reference to the game's main window object in screen.
"""
screen = None

time_of_last_tick = 0


def _should_use_keyboard():
    from platform import system

    if system() == "Windows":
        return True
        
    if system() == "Linux":
        from os import getuid
        # if we're the root user
        if getuid() == 0:
            return True

    else:
        return False


def init(player_car, screen_window):
    player_car.velocity = INITIAL_VELOCITY

    if _should_use_keyboard():
        from importlib import import_module
        global keyboard
        try:
            keyboard = import_module("keyboard")
        except ImportError:
            exit("Please install the keyboard module as root:\n"
                 "\tsudo python3 -m pip install keyboard")
    else:
        exit("run with sudo pls")     # TODO: make curses support decent, then remove this line
        global screen
        screen = screen_window
        screen.nodelay(True)


def read_input_and_update_player(player_car):
    global time_of_last_tick

    current_time = time()
    time_since_last_tick = current_time - time_of_last_tick
    time_of_last_tick = current_time

    player_car.latitude += player_car.velocity * time_since_last_tick

    if keyboard:
        if   keyboard.is_pressed("left"):  player_car.longitude += -1
        elif keyboard.is_pressed("right"): player_car.longitude += +1

        """TODO: the stuff below could probably be significantly simplified with a variable like intended_directon=(1 if keyboard.is_pressed("up") else -1) and then some multiplications"""

        # If the player is trying to increase their vertical speed.
        if keyboard.is_pressed("up")     and player_car.velocity >= 0:
            player_car.velocity += + PEDAL_ACCELERATION * time_since_last_tick
        elif keyboard.is_pressed("down") and player_car.velocity <= 0:
            player_car.velocity += - PEDAL_ACCELERATION * time_since_last_tick

        # If the player is braking.
        elif keyboard.is_pressed("up")   and player_car.velocity < 0:
            player_car.velocity += + BRAKE_DECELERATION * time_since_last_tick
        elif keyboard.is_pressed("down") and player_car.velocity > 0:
            player_car.velocity += - BRAKE_DECELERATION * time_since_last_tick

        # If the player is sleeping.
        else:
            speed_decrement = IDLE_DECELERATION * time_since_last_tick

            if abs(player_car.velocity) < speed_decrement:
                player_car.velocity = 0
            elif player_car.velocity > 0:
                player_car.velocity += - speed_decrement
            else:
                player_car.velocity += + speed_decrement
    
    else:
        input = screen.getch()

        """Flush the input buffer because, in the next call to this function,
        we'll want only input that has been entered since now. We don't
        want to accumulate input.
        """
        curses.flushinp()

        if input == curses.KEY_LEFT:
            player_car.longitude += -1
        elif input == curses.KEY_RIGHT:
            player_car.longitude +=  1
    
    debug_msg("velocity: " + str(player_car.velocity))
