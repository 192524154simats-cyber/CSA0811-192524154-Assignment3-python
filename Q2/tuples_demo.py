"""Q2 - tuples, aliasing, shallow/deep copy, the grid bug. Complete-the-Code program is in complete_code.py."""
import copy, sys, time

print("== 1. Tuples as dictionary keys, lists cannot ==")
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
for (lat, lon), name in stops.items():                       # unpacking in a for loop
    print(f"  {name:16} lat={lat:8.4f} lon={lon:8.4f}")
try:
    bad_key = {[13.0418, 80.2341]: "T. Nagar"}
except TypeError as e:
    print("  list as key ->", type(e).__name__ + ":", e)
print("  hash((13.0, 80.0)) =", hash((13.0, 80.0)))
try:
    hash([13.0, 80.0])
except TypeError as e:
    print("  hash([13.0, 80.0]) ->", e)

print("\n== 2. The grid bug: [[0] * cols] * rows ==")
rows, cols = 3, 3
bad = [[0] * cols] * rows
good = [[0] * cols for _ in range(rows)]
print("  ids of rows, bad :", [id(r) for r in bad])
print("  ids of rows, good:", [id(r) for r in good])
print("  bad[0] is bad[1] ->", bad[0] is bad[1], "| good[0] is good[1] ->", good[0] is good[1])
bad[0][1] += 5; good[0][1] += 5
print("  after [0][1] += 5   bad :", bad)
print("  after [0][1] += 5   good:", good)

print("\n== 3. Aliasing, shallow copy, deep copy ==")
orig = [[1, 2], [3, 4]]
alias = orig
shallow1 = copy.copy(orig)
shallow2 = orig[:]
deep = copy.deepcopy(orig)
print("  alias is orig:", alias is orig, "| shallow is orig:", shallow1 is orig, "| shallow rows are the same objects:", shallow1[0] is orig[0], "| deep rows same objects:", deep[0] is orig[0])
orig[0][0] = 99          # change a NESTED list
orig.append([5, 6])      # change the OUTER list
print("  orig    :", orig)
print("  alias   :", alias, " <- sees everything (same object)")
print("  copy.copy:", shallow1, " <- no new row, but the inner list changed (shared)")
print("  [:]     :", shallow2, " <- same as copy.copy")
print("  deepcopy:", deep, " <- completely independent")

print("\n== 4. A function that changes a list argument changes the caller's list ==")
def add_zone(zones):
    zones.append("Z9")           # mutates the object the caller also references
def add_zone_safe(zones):
    return zones + ["Z9"]        # builds a new list
mine = ["Z1"]; add_zone(mine); print("  after add_zone(mine):", mine)
mine2 = ["Z1"]; new = add_zone_safe(mine2); print("  after add_zone_safe: original", mine2, "new", new)

print("\n== 5. A list stored inside a tuple ==")
t = ([1, 2], 3)
t[0].append(99)
print("  t[0].append(99) works ->", t, "(the tuple still holds the SAME list object; only the list changed)")
try:
    t[0] += [100]
except TypeError as e:
    print("  t[0] += [100] ->", type(e).__name__ + ":", e)
print("  but the list WAS extended before the error:", t)
try:
    t[1] = 5
except TypeError as e:
    print("  t[1] = 5 ->", type(e).__name__ + ":", e)

print("\n== 6. Memory and time: list vs tuple of 1,000,000 values ==")
N = 1_000_000
lst = list(range(N)); tup = tuple(range(N))
print(f"  sys.getsizeof(list)  = {sys.getsizeof(lst):>10,} bytes")
print(f"  sys.getsizeof(tuple) = {sys.getsizeof(tup):>10,} bytes   (container only; the int objects are shared by both)")
print("  small ones: getsizeof((1,2)) =", sys.getsizeof((1, 2)), "| getsizeof([1,2]) =", sys.getsizeof([1, 2]))
def timeit(fn, number):
    t0 = time.perf_counter()
    for _ in range(number): fn()
    return (time.perf_counter() - t0) / number
print(f"  create from range: list {timeit(lambda: list(range(N)), 5) * 1000:7.2f} ms | tuple {timeit(lambda: tuple(range(N)), 5) * 1000:7.2f} ms")
print(f"  create literal of 5: list {timeit(lambda: [1, 2, 3, 4, 5], 1_000_000) * 1e9:6.0f} ns | tuple {timeit(lambda: (1, 2, 3, 4, 5), 1_000_000) * 1e9:6.0f} ns (tuple of constants is built once at compile time)")
def idx(seq):
    for _ in range(1_000_000): seq[500_000]
print(f"  1,000,000 indexings: list {timeit(lambda: idx(lst), 3) * 1000:7.2f} ms | tuple {timeit(lambda: idx(tup), 3) * 1000:7.2f} ms")
