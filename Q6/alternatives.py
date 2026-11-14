"""Q6 alternative: ONE flat list of (train, station, arrival, departure, days) tuples scanned for every query,
versus nested dictionaries with a station index. Time per query and memory."""
import time, random, tracemalloc
from railway import generate, build_index, stops_at_indexed, ALL_DAYS

def flatten(tt):
    flat = []
    for no, info in tt.items():
        days = frozenset(info["days"])               # one days-object per train, shared by its rows
        for st, arr, dep in info["stops"]:
            flat.append((no, info["name"], st, arr, dep, days))
    return flat

def query_flat(flat, station, day):
    """Scans EVERY stop of the whole timetable: O(total stops)."""
    out = [(no, name, arr, dep) for no, name, st, arr, dep, days in flat if st == station and day in days]
    return sorted(out, key=lambda t: t[3] if t[3] != "--" else "99:99")

def mem(fn):
    tracemalloc.start(); r = fn(); m = tracemalloc.get_traced_memory()[0]; tracemalloc.stop(); return r, m

print(f"{'trains':>7} {'total stops':>12} | {'flat scan (ms/query)':>21} {'nested+index (ms/query)':>24} {'ratio':>6} | {'flat list memory':>17} {'nested dict':>12} {'index':>9}")
for n in (100, 1_000, 10_000):
    tt, m_nested = mem(lambda: generate(n))
    flat, m_flat = mem(lambda: flatten(tt))
    index, m_index = mem(lambda: build_index(tt))
    rnd = random.Random(2)
    queries = [(f"Station{rnd.randrange(300):03d}", rnd.choice(ALL_DAYS)) for _ in range(100)]
    t0 = time.perf_counter(); r1 = [query_flat(flat, s, d) for s, d in queries]; t1 = time.perf_counter()
    r2 = [stops_at_indexed(tt, index, s, d) for s, d in queries]; t2 = time.perf_counter()
    assert r1 == r2
    a, b = (t1 - t0) / 100 * 1000, (t2 - t1) / 100 * 1000
    stops = len(flat)
    print(f"{n:>7} {stops:>12,} | {a:>21.3f} {b:>24.4f} {a / b:>5.0f}x | {m_flat / 1024:>13.0f} KiB {m_nested / 1024:>8.0f} KiB {m_index / 1024:>5.0f} KiB")
