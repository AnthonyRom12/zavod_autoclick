import random


def random_delay(min_val, max_val):
    return random.uniform(min_val, max_val)


def generate_device_params():
    delay_min = random.randint(2, 5)
    delay_max = random.randint(5, 10)
    start_delay_min = random.randint(10, 15)
    start_delay_max = random.randint(15, 20)
    work_start = "09:00"
    work_end = "23:50"

    return {
        "delay_min": delay_min,
        "delay_max": delay_max,
        "start_delay_min": start_delay_min,
        "start_delay_max": start_delay_max,
        "work_start": work_start,
        "work_end": work_end
    }
