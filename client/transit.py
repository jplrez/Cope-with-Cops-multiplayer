from common.constants import *

from sys import exit   # temp

"""
Our transit is a linked list of cars.
_transit_back maintains a reference to the car that has the lowest latitude.
Each car has a reference to the car that has the lowest latitude
that is greater than its own.
"""
_transit_back  = None
_transit_front = None



def update_transit(new_events):
    """Take new transit cars from an events object.

    Takes an object that has a list new_transit containing references
    to the back and to the front of linked list of cars.
    and the 
    The received list of cars is simply appended to the end of our transit.
    Thus, the cars in it are all expected to have latitudes higher
    than those of the cars we already have, and to be correctly ordered.
    """
    global _transit_back, _transit_front

    if new_events.new_transit:
        if not _transit_front:
            _transit_back  = new_events.new_transit[0]
            _transit_front = new_events.new_transit[1]
            return

        _transit_front.next_car = new_events.new_transit[0]
        _transit_front          = new_events.new_transit[1]


"""
get_visible_cars creates an iterator that feeds the cars that are to be
drawn on the screen.
"""
def get_visible_cars(maximum_visible_latitude):
    class Iterator():
        def __iter__(self):
            return self
        def __init__(self, transit_back, maximum_visible_latitude):
            self.current_car = transit_back
            self.maximum_visible_latitude = maximum_visible_latitude
        def __next__(self):
            current_car = self.current_car
            if not current_car or (current_car.latitude - (CAR_HEIGHT - 1) >
                                   maximum_visible_latitude):
                raise StopIteration
            self.current_car = current_car.next_car
            return current_car
    return Iterator(_transit_back, maximum_visible_latitude)


def check_for_collision(player_car):
    for other_car in get_visible_cars(player_car.latitude):
        Ay, Ax = player_car.latitude, player_car.longitude
        By, Bx =  other_car.latitude,  other_car.longitude

        if (((Ax <= Bx and Ax + CAR_WIDTH > Bx) or (Bx <= Ax and Bx + CAR_WIDTH > Ax)) and
            ((Ay <= By and Ay + CAR_HEIGHT > By) or (By <= Ay and By + CAR_HEIGHT > Ay))):
            pass # debug_msg("i crashed :(")
