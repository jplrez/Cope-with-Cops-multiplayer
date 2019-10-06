from common.constants import *
from common.car import Car
import client.start_screen       as start_screen
import client.tick_rate_control  as tick_rate_control
import client.rendering          as rendering
import client.input_and_movement as input_and_movement
import client.communication      as communication
import client.transit            as transit

def main(screen):
    rendering.init(screen)
    start_screen.request_resize(screen, MIN_SCREEN_HEIGHT, MIN_SCREEN_WIDTH)

    player_car = Car(CAR_HEIGHT + PLAYER_DISTANCE_FROM_BOTTOM,
                     ROAD_WIDTH // 2, 7, is_cop_car = True)
    input_and_movement.init(player_car, screen)

    communication.init()
    
    while True:
        input_and_movement.read_input_and_update_player(player_car)
        new_events = communication.get_new_events()
        transit.update_transit(new_events)
        visible_transit_cars = transit.get_visible_cars(rendering.get_maximum_visible_latitude(player_car))
        rendering.draw_scene(player_car, visible_transit_cars)
        transit.check_for_collision(player_car)

        tick_rate_control.sleep_until_next_tick()