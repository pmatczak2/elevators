import random
from loguru import logger
import pandas as pd

# logger.remove()
logger.add("./sim_{time}.log", level="TRACE", rotation="100 MB")


def clock_to_ordinal_days(clock_time):
    return 1 + ((clock_time + 1) // 24)


def time_current_day(clock_time):
    return (clock_time + 1) - (clock_to_ordinal_days(clock_time) * 24)


def is_busy(current_time, busy_times):
    if current_time in busy_times:
        return True
    return False


def run_sim(simulation):  # clock works in hours (an int that represents hours)
    logger.info(">>>> RUN START\n")
    results = {}
    for current_time in range(simulation['duration_hours']):
        if current_time < simulation['working_day'][0] or \
                current_time >= simulation['working_day'][1]:
            continue

        # code goes in here that happens each tick of duration

        # show how time progresses...
        logger.info("Day: {}:{}", str(clock_to_ordinal_days(current_time)
                                      + 100)[1:], str(time_current_day(current_time) + 100)[1:])



        total_occupants = simulation['number_of_floors'] * simulation['occupancy_per_floor']
        working_day_duration = simulation['working_day'][1] - simulation['working_day'][0]
        hourly_movement_load = 2 * (total_occupants / working_day_duration)
        busy = is_busy(current_time, simulation['busy_periods'])
        if busy:
            hourly_movement_load *= simulation['busy_weight']
        results[current_time] = {
            'hourly_movement_load': hourly_movement_load,
            'elevator_trips_per_hour': hourly_movement_load / simulation['max_people_per_elevator'],
            'elevator_use_per_hour': (hourly_movement_load / simulation['max_people_per_elevator'] / (
                        60 / simulation['elevator_move_time_mins']))

        }

    results = pd.DataFrame(results)
    print(results)
    logger.info("\n\n>>>> RUN END")


def simulate():
    # set up
    simulation = {}
    simulation['duration_days'] = 3
    simulation['duration_hours'] = simulation['duration_days'] * 24
    simulation['working_day'] = (6, 18)
    simulation['busy_periods'] = [7, 8, 11, 16, 17]
    simulation['busy_weight'] = 1.5
    simulation['number_of_floors'] = 10
    simulation['occupancy_per_floor'] = 100
    # simulation['arrivals'] = simulation['number_of_floors']
    simulation['use_stairs'] = 0.05
    simulation['max_people_per_elevator'] = 8
    simulation['elevator_move_time_mins'] = 2

    # start sim
    run_sim(simulation)


if __name__ == "__main__":
    simulate()
