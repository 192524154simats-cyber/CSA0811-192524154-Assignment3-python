"""Q2 alternative: sparse grid {(row, col): count} instead of list of lists. Access time and space."""
import sys, time, random, tracemalloc

def build_dense(rows, cols, events):
    g = [[0] * cols for _ in range(rows)]
    for r, c in events: g[r][c] += 1
    return g

def build_sparse(rows, cols, events):
    g = {}
    for rc in events: g[rc] = g.get(rc, 0) + 1
    return g

random.seed(5)
print(f"{'grid':>12} {'cells':>10} {'busy zones':>11} | {'list of lists':>14} {'dict (tuple keys)':>18} | {'access list':>12} {'access dict':>12}")
for rows, cols, busy in ((100, 100, 500), (1000, 1000, 5000), (3000, 3000, 5000)):
    busy_cells = {(random.randrange(rows), random.randrange(cols)) for _ in range(busy)}
    events = list(busy_cells) * 2
    tracemalloc.start(); dense = build_dense(rows, cols, events); a = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    tracemalloc.start(); sparse = build_sparse(rows, cols, events); b = tracemalloc.get_traced_memory()[0]; tracemalloc.stop()
    assert all(dense[r][c] == v for (r, c), v in sparse.items())
    keys = list(busy_cells) * 20
    t0 = time.perf_counter()
    for r, c in keys: dense[r][c]
    t1 = time.perf_counter()
    for k in keys: sparse.get(k, 0)
    t2 = time.perf_counter()
    print(f"{rows:>5}x{cols:<6} {rows * cols:>10,} {len(busy_cells):>11,} | {a / 1024:>11.0f} KiB {b / 1024:>15.0f} KiB | {(t1 - t0) / len(keys) * 1e9:>9.0f} ns {(t2 - t1) / len(keys) * 1e9:>9.0f} ns")
