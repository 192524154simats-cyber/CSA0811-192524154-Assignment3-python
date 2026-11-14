"""Q7 alternative: compare every pair of contacts (O(n^2)) versus the dictionary design (O(n)).
Measured at 1,000 / 2,000 / 4,000 / 8,000 contacts; 100,000 is ESTIMATED (not run) from the measured cost per pair."""
import time, tracemalloc
from contacts import merge, merge_pairwise
from run_q7_data import make_contacts

print(f"{'n':>8} | {'dictionary':>11} | {'pairwise':>10} {'pair comparisons':>17} | slowdown   (timed WITHOUT tracemalloc)")
cost_per_pair = None
for n in (1_000, 2_000, 4_000, 8_000):
    data = make_contacts(n, seed=2)
    t0 = time.perf_counter(); merge(data); a = time.perf_counter() - t0
    t0 = time.perf_counter(); _, comps = merge_pairwise(data); b = time.perf_counter() - t0
    cost_per_pair = b / comps
    print(f"{n:>8} | {a:>10.4f}s | {b:>9.3f}s {comps:>17,} | {b / a:>7.0f}x")

print("\nMemory (tracemalloc peak) at n = 2,000 and 8,000:")
for n in (2_000, 8_000):
    data = make_contacts(n, seed=2)
    tracemalloc.start(); merge(data); ma = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    tracemalloc.start(); merge_pairwise(data); mb = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"   n = {n:>5}: dictionary {ma / 1024:7.0f} KiB   pairwise {mb / 1024:7.0f} KiB")

n = 100_000
pairs = n * (n - 1) // 2
data = make_contacts(n, seed=2)
t0 = time.perf_counter(); merge(data); a = time.perf_counter() - t0
est = pairs * cost_per_pair
print(f"\nn = 100,000: dictionary measured {a:.3f} s.")
print(f"             pairwise would need {pairs:,} comparisons; at {cost_per_pair * 1e9:.0f} ns per pair ~ {est:,.0f} s = {est / 60:.0f} minutes (estimated, NOT run; the cost per pair tends to rise with n).")
print("Doubling n: dictionary time x2, pairwise time x4 (check the table: 1000 -> 2000 -> 4000 -> 8000).")
