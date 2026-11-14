"""Q1 - Daily rainfall records: weekly totals (slicing), max/min with positions, 7-day moving average, dry days."""
import random

def generate(n, seed=1):
    """n daily readings (mm): about 60 % dry days, otherwise 0.1-80.0 mm."""
    rnd = random.Random(seed)
    return [0.0 if rnd.random() < 0.6 else round(rnd.uniform(0.1, 80.0), 1) for _ in range(n)]

def weekly_totals(readings):
    """Totals of consecutive 7-day blocks using slicing; the last block may be shorter."""
    return [round(sum(readings[i:i + 7]), 1) for i in range(0, len(readings), 7)]

def max_min_with_position(values):
    """Returns (max, index of max, min, index of min); None for an empty list."""
    if not values:
        return None
    hi = lo = 0
    for i, v in enumerate(values):
        if v > values[hi]: hi = i
        if v < values[lo]: lo = i
    return values[hi], hi, values[lo], lo

def moving_average_naive(readings, w=7):
    """Re-adds the whole window every time. Returns (averages, number_of_additions)."""
    out, adds = [], 0
    for i in range(len(readings) - w + 1):
        total = readings[i]
        for j in range(i + 1, i + w):
            total += readings[j]; adds += 1          # w-1 additions per window
        out.append(total / w)
    return out, adds

def moving_average_running(readings, w=7):
    """Running sum: add the new reading, subtract the one leaving. Returns (averages, additions+subtractions)."""
    if len(readings) < w:
        return [], 0
    ops = 0
    total = readings[0]
    for j in range(1, w):
        total += readings[j]; ops += 1                # first window: w-1 additions
    out = [total / w]
    for i in range(w, len(readings)):
        total += readings[i] - readings[i - w]; ops += 2   # one addition and one subtraction per move
        out.append(total / w)
    return out, ops

def dry_days(readings):
    """Day numbers (1-based) with 0 mm."""
    return [i + 1 for i, r in enumerate(readings) if r == 0]
