import time, sys, tracemalloc
from sensors import *

print("== Small example ==")
r = [5.0, 70.5, 3.2, -60.0, 9.1, 1.5, 8.0, 2.0]
print("readings:", r)
print("loop          :", clean_loop(r))
print("comprehension :", clean_comprehension(r))
print("map/filter    :", clean_map_filter(r))
print("alarm minutes (valid but outside 2-8):", alarm_minutes(r), " <- 70.5 and -60.0 are sensor errors, NOT alarms; 2.0 and 8.0 are safe")

print("\n== Dictionary and set comprehension for this problem ==")
valid = clean_loop(r)[0]
print("dict {minute: Fahrenheit} for valid readings:", {m: round(c * 9 / 5 + 32, 1) for m, c in enumerate(r) if LOW_ERR <= c <= HIGH_ERR})
print("set of distinct valid whole-degree readings :", {int(c) for c in valid})
print("generator expression:", (c for c in r if LOW_ERR <= c <= HIGH_ERR))

print("\n== Tests: all valid and all invalid ==")
allv = [4.0] * 5; alli = [99.0, -75.0, 51.0, -50.1]
for label, data in (("all valid", allv), ("all invalid", alli), ("empty", []), ("boundaries +-50", [50.0, -50.0, 50.1, -50.1])):
    a, b, c = clean_loop(data), clean_comprehension(data), clean_map_filter(data)
    print(f"{label:16} loop == comprehension == map/filter: {a == b == c}   valid count {len(a[0])}   alarms {alarm_minutes(data)}")

print("\n== Experiment: time of the three versions ==")
print(f"{'readings':>10} {'valid':>9} | {'for + append':>13} {'comprehension':>14} {'map + filter':>13} | identical results")
for n in (10_000, 100_000, 1_000_000):
    data = generate(n)
    t0 = time.perf_counter(); a = clean_loop(data); t1 = time.perf_counter()
    b = clean_comprehension(data); t2 = time.perf_counter()
    c = clean_map_filter(data); t3 = time.perf_counter()
    print(f"{n:>10} {len(a[0]):>9} | {t1 - t0:>12.4f}s {t2 - t1:>13.4f}s {t3 - t2:>12.4f}s | {a == b == c}")

print("\n== Memory: list comprehension vs generator expression (1,000,000 readings) ==")
data = generate(1_000_000)
lc = [c for c in data if LOW_ERR <= c <= HIGH_ERR]
ge = (c for c in data if LOW_ERR <= c <= HIGH_ERR)
print(f"sys.getsizeof(list comprehension) = {sys.getsizeof(lc):>10,} bytes ({len(lc):,} items)")
print(f"sys.getsizeof(generator)          = {sys.getsizeof(ge):>10,} bytes (items are produced one at a time)")
tracemalloc.start(); total = sum(c for c in data if LOW_ERR <= c <= HIGH_ERR); peak_g = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
tracemalloc.start(); total2 = sum([c for c in data if LOW_ERR <= c <= HIGH_ERR]); peak_l = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
print(f"tracemalloc peak: sum(list comprehension) {peak_l / 1024:9.1f} KiB | sum(generator) {peak_g / 1024:6.2f} KiB | same total: {abs(total - total2) < 1e-6}")
print("A generator can be used ONCE:", end=" ")
g = (c for c in [1, 2, 3]); print(sum(g), sum(g), "(second sum is 0: already exhausted)")
