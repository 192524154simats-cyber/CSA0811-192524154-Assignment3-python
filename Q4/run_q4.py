import random, time
from electives import *

ai = {"192311001", "192311004", "192311007", "192311009"}
iot = {"192311002", "192311004", "192311009", "192311010"}
everyone = {f"1923110{i:02d}" for i in range(1, 11)}

print("== Hand verification (small case) ==")
print("AI = {001, 004, 007, 009}   IoT = {002, 004, 009, 010}   all = 001..010")
print("by hand: both = {004, 009}; exactly one = {001, 002, 007, 010}; neither = {003, 005, 006, 008}; either = 8 students")
for k, v in analyse(ai, iot, everyone).items():
    report(k, v)
print("operators == methods:", analyse(ai, iot, everyone) == analyse_methods(ai, iot, everyone))
print("sizes: |AI|+|IoT| =", len(ai) + len(iot), " = |union| + |both| =", len(ai | iot) + len(ai & iot), "(inclusion-exclusion)")

print("\n== Duplicates removed ==")
raw = ["192311001", "192311004", "192311001", "192311004", "192311004"]
print("registrations typed:", raw, "->", sorted(set(raw)), "| order of typing lost, counts lost")

print("\n== Empty and identical electives ==")
empty = set()
print("empty & AI :", analyse(empty, ai, everyone)["both (clash)"], "| exactly one:", sorted(analyse(empty, ai, everyone)["exactly one"]))
print("empty & empty:", analyse(empty, empty, everyone)["exactly one"], "| neither =", len(analyse(empty, empty, everyone)["neither"]), "(everyone)")
same = analyse(ai, set(ai), everyone)
print("identical electives: both =", sorted(same["both (clash)"]), "| exactly one =", sorted(same["exactly one"]), "| only AI =", sorted(same["only AI"]))

print("\n== Sets: tuples allowed, lists not ==")
print("{(1, 2), (3, 4)} ok ->", {(1, 2), (3, 4)})
try:
    {[1, 2]}
except TypeError as e:
    print("{[1, 2]} ->", e)

print("\n== Membership: x in list vs x in set (worst case: value not present), 200 lookups ==")
print(f"{'n':>10} | {'list (ms per lookup)':>21} {'set (us per lookup)':>20} | ratio")
for n in (10_000, 100_000, 1_000_000):
    nums = [str(192300000 + i) for i in range(n)]
    s = set(nums)
    probes = ["missing" + str(i) for i in range(200)]
    t0 = time.perf_counter()
    for p in probes: p in nums
    t1 = time.perf_counter()
    for p in probes: p in s
    t2 = time.perf_counter()
    a, b = (t1 - t0) / 200, (t2 - t1) / 200
    print(f"{n:>10} | {a * 1000:>21.4f} {b * 1e6:>20.3f} | {a / b:>10,.0f}x")

print("\n== Common students: nested loops vs & ==")
print(f"{'n = m':>8} | {'nested loops':>13} {'comparisons':>12} | {'sorted walk':>12} | {'set &':>10} | same")
def nested(a, b):
    out, comps = [], 0
    for x in a:
        for y in b:
            comps += 1
            if x == y: out.append(x)
    return out, comps
def sorted_walk(a, b):
    a, b = sorted(a), sorted(b); i = j = 0; out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]: out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]: i += 1
        else: j += 1
    return out
rnd = random.Random(4)
for n in (500, 1000, 2000, 4000):
    A = rnd.sample(range(n * 2), n); B = rnd.sample(range(n * 2), n)
    t0 = time.perf_counter(); r1, comps = nested(A, B); t1 = time.perf_counter()
    r2 = sorted_walk(A, B); t2 = time.perf_counter()
    r3 = set(A) & set(B); t3 = time.perf_counter()
    print(f"{n:>8} | {t1 - t0:>12.4f}s {comps:>12,} | {t2 - t1:>11.4f}s | {t3 - t2:>9.5f}s | {set(r1) == set(r2) == r3}")
for n in (100_000, 1_000_000):
    A = rnd.sample(range(n * 2), n); B = rnd.sample(range(n * 2), n)
    t0 = time.perf_counter(); r2 = sorted_walk(A, B); t1 = time.perf_counter()
    r3 = set(A) & set(B); t2 = time.perf_counter()
    print(f"{n:>8} | {'(too slow: ' + format(n * n, ',') + ' comparisons)':>26} | {t1 - t0:>11.4f}s | {t2 - t1:>9.5f}s | {set(r2) == r3}")
