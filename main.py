from loguru import logger


logger.remove()
logger.add("./sim_{time}.log", level="TRACE", rotation="100 MB")

def clock_to_original_days(clock_time):
    return (clock_time + 1) // 24

def time_current_day(clock_time):
    return (clock_time + 1) - (clock_to_original_days(clock_time) * 24)



def run_sim(simulation):
    logger.info(">>> RUN START\n")
    for current_time in range(simulation['duration_hours']):
        logger.info("Day: {}:{}", str(clock_to_original_days(current_time) + 100)[1:],
                    str(time_current_day(current_time) + 100)[1:])


def simulate():
    simulation = {}
    simulation['duration_days'] = 3
    simulation['duration_hours'] = simulation['duration_days'] * 24
    simulation['busy_periods'] = [7, 8, 11, 4, 5]
    simulation["busy_weight"] = 1.5
    simulation["number_of_floors"] = 10
    simulation['occupancy_per_floor'] = 100
    simulation['arrivals'] = simulation['number_of_floors']


    run_sim(simulation)


if __name__ == "__main__":
    simulate()