"""Q1 alternative: deque(maxlen=7) window, or dict keyed by date. Time and space."""
import time, tracemalloc, datetime
from collections import deque
from rainfall import generate, moving_average_running

def moving_average_deque(readings, w=7):
    """Window kept in deque(maxlen=7): appending the 8th value pushes the oldest out automatically.
    sum(window) re-adds 7 values each time (O(7n)); the running-sum variant keeps O(n)."""
    win, out = deque(maxlen=w), []
    for r in readings:
        win.append(r)
        if len(win) == w:
            out.append(sum(win) / w)             # w additions per window
    return out

def moving_average_deque_running(readings, w=7):
    win, out, total = deque(maxlen=w), [], 0.0
    for r in readings:
        if len(win) == w:
            total -= win[0]                       # value about to be pushed out
        win.append(r); total += r
        if len(win) == w:
            out.append(total / w)
    return out

def moving_average_dict(rain_by_date, start, n, w=7):
    """Readings stored in a dict {date: mm}; window found by looking up each date: 7 lookups per day."""
    out = []
    for i in range(n - w + 1):
        out.append(sum(rain_by_date[start + datetime.timedelta(days=i + j)] for j in range(w)) / w)
    return out

for n in (365, 36500, 365000):
    data = generate(n)
    start = datetime.date(2024, 1, 1)
    d = {start + datetime.timedelta(days=i): v for i, v in enumerate(data)}
    ref, _ = moving_average_running(data)
    res = {}
    for name, fn in (("deque + sum(window)  O(7n)", lambda: moving_average_deque(data)),
                     ("deque + running sum  O(n)", lambda: moving_average_deque_running(data)),
                     ("dict by date (7 lookups) ", lambda: moving_average_dict(d, start, n))):
        t0 = time.perf_counter(); out = fn(); sec = time.perf_counter() - t0
        res[name] = (sec, all(abs(a - b) < 1e-6 for a, b in zip(out, ref)))
    print(f"n = {n}")
    for k, (s, ok) in res.items():
        print(f"   {k}: {s:8.4f} s  same result: {ok}")
    tracemalloc.start(); lst = list(data); a = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    tracemalloc.start(); dd = {start + datetime.timedelta(days=i): v for i, v in enumerate(data)}; b = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    print(f"   memory: list of readings {a / 1024:9.1f} KiB | dict keyed by date {b / 1024:9.1f} KiB | deque window: 7 values (~{__import__('sys').getsizeof(deque(maxlen=7))} bytes)")
