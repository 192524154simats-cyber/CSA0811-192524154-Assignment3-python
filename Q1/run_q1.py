import time
from rainfall import *

r = generate(365)
print("== 1. Weekly totals, wettest and driest week (365 days) ==")
wk = weekly_totals(r)
print("weeks:", len(wk), "(52 full weeks + a last block of", len(r[364:]), "day)")
print("first 5 weekly totals:", wk[:5])
mx, imx, mn, imn = max_min_with_position(wk[:52])
print(f"wettest full week: week {imx + 1} (days {imx * 7 + 1}-{imx * 7 + 7}) = {mx} mm; driest full week: week {imn + 1} = {mn} mm")
d_max, i_max, d_min, i_min = max_min_with_position(r)
print(f"wettest day: day {i_max + 1} = {d_max} mm; driest day (first minimum): day {i_min + 1} = {d_min} mm")
dd = dry_days(r)
print(f"dry days: {len(dd)} ; first ten: {dd[:10]}")

print("\n== 2. What the slices return ==")
small = [5, 0, 3, 8, 0, 1, 2, 9, 4, 0, 6, 7, 1, 2, 3, 4, 5]
print("readings (17 values):", small)
print("readings[7:14]  ->", small[7:14], " (days 8-14, the 2nd week: index 7 up to but not including 14)")
print("readings[-7:]   ->", small[-7:], " (the last 7 readings)")
print("readings[::7]   ->", small[::7], " (every 7th reading starting at index 0)")

print("\n== 3. Moving average ==")
a, ops1 = moving_average_naive(small); b, ops2 = moving_average_running(small)
print("17 values, window 7 -> 11 windows; first three averages:", [round(x, 3) for x in a[:3]])
print("naive additions:", ops1, "(= 11 windows x 6)  running-sum operations:", ops2, "(= 6 + 2 x 10)  same results:", all(abs(x - y) < 1e-9 for x, y in zip(a, b)))

print("\n== 4. Edge cases ==")
for label, data in (("empty list", []), ("3 values (< 7)", [1.0, 2.0, 3.0]), ("exactly 7 values", [1.0] * 7)):
    print(f"{label:18} weekly={weekly_totals(data)} max/min={max_min_with_position(data)} naive={moving_average_naive(data)} running={moving_average_running(data)} dry={dry_days(data)}")

print("\n== 5. Experiment: counts vs derived formulas and times ==")
print("Derived: naive additions = (n-6) x 6 ; running = 6 + 2 x (n-7)")
print(f"{'n':>8} {'naive adds':>12} {'derived':>12} {'running ops':>12} {'derived':>10} {'naive time':>11} {'running time':>13} {'ratio':>6}")
for n in (365, 36500, 365000):
    data = generate(n)
    t0 = time.perf_counter(); _, a1 = moving_average_naive(data); t1 = time.perf_counter()
    _, a2 = moving_average_running(data); t2 = time.perf_counter()
    print(f"{n:>8} {a1:>12} {(n - 6) * 6:>12} {a2:>12} {6 + 2 * (n - 7):>10} {t1 - t0:>10.4f}s {t2 - t1:>12.4f}s {(t1 - t0) / (t2 - t1):>5.1f}x")

print("\n== 6. Late reading: list.insert cost ==")
for n in (365, 36500, 365000):
    data = generate(n)
    t0 = time.perf_counter()
    for _ in range(100): data.insert(0, 1.0)
    t1 = time.perf_counter()
    for _ in range(100): data.append(1.0)
    t2 = time.perf_counter()
    print(f"n={n:>7}: insert at front {(t1 - t0) / 100 * 1e6:9.2f} us, append {(t2 - t1) / 100 * 1e6:7.3f} us")
