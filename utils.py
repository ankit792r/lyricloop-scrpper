import random, time

SLEEP_INTERVALS = [1, 0, 2, 3, 4, 5, 0, 1, 3, 2, 5, 1, 3]
def random_tread_sleep():
    interval = random.choice(SLEEP_INTERVALS)
    time.sleep(interval)