"""Q5 alternative: generator expression instead of list comprehension - time and memory for sum, max, any."""
import time, tracemalloc
from sensors import generate, LOW_ERR, HIGH_ERR

def measure(fn):
    tracemalloc.start(); t0 = time.perf_counter(); r = fn(); sec = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop(); return r, sec, peak

print(f"{'n':>10} | {'sum(list)':>10} {'peak KiB':>10} | {'sum(generator)':>15} {'peak KiB':>10} | same")
for n in (10_000, 100_000, 1_000_000):
    data = generate(n)
    a, ta, ma = measure(lambda: sum([c for c in data if LOW_ERR <= c <= HIGH_ERR]))
    b, tb, mb = measure(lambda: sum(c for c in data if LOW_ERR <= c <= HIGH_ERR))
    print(f"{n:>10} | {ta:>9.4f}s {ma / 1024:>10.1f} | {tb:>14.4f}s {mb / 1024:>10.2f} | {abs(a - b) < 1e-6}")

print("\nEarly exit: 'is there any reading above 90?' (generator stops at the first hit)")
data = generate(1_000_000)
r1, t1, m1 = measure(lambda: any([c > 90 for c in data]))
r2, t2, m2 = measure(lambda: any(c > 90 for c in data))
print(f"any([list comprehension]) {t1:.4f} s, peak {m1 / 1024:9.1f} KiB   |   any(generator) {t2:.6f} s, peak {m2 / 1024:.2f} KiB   same answer: {r1 == r2}")
