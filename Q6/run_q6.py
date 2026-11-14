import time, random, sys, tracemalloc
from railway import *

print("== The nested structure (5 trains) ==")
print_timetable(SAMPLE)
print("\nDeparture time of the third station of train 12601: SAMPLE[12601]['stops'][2][2] =", SAMPLE[12601]["stops"][2][2])
print("Name of that station: SAMPLE[12601]['stops'][2][0] =", SAMPLE[12601]["stops"][2][0])
print("Does 12635 run on Sun? ->", "Sun" in SAMPLE[12635]["days"])

print("\n== Query: trains at Katpadi on Sat, sorted by departure (key=lambda) ==")
for row in stops_at(SAMPLE, "Katpadi", "Sat"): print("  ", row)
idx = build_index(SAMPLE)
print("index:", {k: v for k, v in idx.items()})
print("indexed query gives same answer:", stops_at(SAMPLE, "Katpadi", "Sat") == stops_at_indexed(SAMPLE, idx, "Katpadi", "Sat"))

print("\n== Tests ==")
print("unknown station   ->", stops_at(SAMPLE, "Atlantis", "Mon"), "| indexed:", stops_at_indexed(SAMPLE, idx, "Atlantis", "Mon"))
print("Katpadi on Tue    ->", [r[0] for r in stops_at(SAMPLE, "Katpadi", "Tue")], "(22651 runs only Sat/Sun, so it is excluded)")
print("Salem on Wed      ->", [r[0] for r in stops_at(SAMPLE, "Salem", "Wed")], "(16721 runs Tue/Thu/Sat/Sun, 22651 Sat/Sun: only 12601)")
print("Coimbatore Sun    ->", [(r[0], r[3]) for r in stops_at(SAMPLE, "Coimbatore", "Sun")], "('--' departure = terminus, sorted last)")

print("\n== Experiment: 100 / 1,000 / 10,000 trains; 300 queries per size ==")
print(f"{'trains':>7} {'total stops':>12} {'avg trains/station':>19} | {'no index (ms/query)':>20} {'with index (ms/query)':>22} {'speed-up':>9} | same answers | {'index memory':>13}")
for n in (100, 1_000, 10_000):
    tt = generate(n)
    total_stops = sum(len(v["stops"]) for v in tt.values())
    tracemalloc.start(); index = build_index(tt); mem = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    t0 = time.perf_counter(); index = build_index(tt); build = time.perf_counter() - t0
    rnd = random.Random(1)
    queries = [(f"Station{rnd.randrange(300):03d}", rnd.choice(ALL_DAYS)) for _ in range(300)]
    t0 = time.perf_counter(); r1 = [stops_at(tt, s, d) for s, d in queries]; t1 = time.perf_counter()
    r2 = [stops_at_indexed(tt, index, s, d) for s, d in queries]; t2 = time.perf_counter()
    a, b = (t1 - t0) / len(queries) * 1000, (t2 - t1) / len(queries) * 1000
    print(f"{n:>7} {total_stops:>12,} {total_stops / 300:>19.1f} | {a:>20.4f} {b:>22.4f} {a / b:>8.0f}x | {r1 == r2!s:>12} | {mem / 1024:>9.0f} KiB (build {build * 1000:.1f} ms)")
