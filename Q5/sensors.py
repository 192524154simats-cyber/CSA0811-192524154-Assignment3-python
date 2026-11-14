"""Q5 - Cold-storage temperature monitor: clean, convert, alarms. Valid range -50..50 C; safe range 2..8 C."""
import random

LOW_ERR, HIGH_ERR = -50, 50
SAFE_LOW, SAFE_HIGH = 2, 8

def generate(n, seed=3):
    """Mostly 2-8 C, some drift outside, about 3 % sensor errors (beyond +-50)."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.random()
        if x < 0.03: out.append(round(rnd.choice([-1, 1]) * rnd.uniform(50.1, 99.9), 1))
        elif x < 0.10: out.append(round(rnd.uniform(-10, 20), 1))
        else: out.append(round(rnd.uniform(2, 8), 1))
    return out

def clean_loop(readings):
    """for-loop with append. Returns (celsius, fahrenheit)."""
    c_list, f_list = [], []
    for c in readings:
        if LOW_ERR <= c <= HIGH_ERR:
            c_list.append(c)
            f_list.append(c * 9 / 5 + 32)
    return c_list, f_list

def clean_comprehension(readings):
    c_list = [c for c in readings if LOW_ERR <= c <= HIGH_ERR]
    f_list = [c * 9 / 5 + 32 for c in c_list]          # convert only the already-valid values (one filter pass)
    return c_list, f_list

def clean_map_filter(readings):
    c_list = list(filter(lambda c: LOW_ERR <= c <= HIGH_ERR, readings))
    f_list = list(map(lambda c: c * 9 / 5 + 32, c_list))
    return c_list, f_list

def alarm_minutes(readings):
    """Minutes (0-based index in the ORIGINAL log) with a VALID reading outside 2-8 C, using enumerate()."""
    alarms = []
    for minute, c in enumerate(readings):
        if LOW_ERR <= c <= HIGH_ERR and not (SAFE_LOW <= c <= SAFE_HIGH):
            alarms.append(minute)
    return alarms

def alarm_minutes_comprehension(readings):
    return [m for m, c in enumerate(readings) if LOW_ERR <= c <= HIGH_ERR and not SAFE_LOW <= c <= SAFE_HIGH]
