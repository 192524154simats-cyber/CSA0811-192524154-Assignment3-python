"""Q3 alternative: list.count() for every distinct word versus dict loop versus Counter.
Pre-tokenised words, so only the COUNTING step is timed. n words, d distinct words."""
import random, time, tracemalloc
from collections import Counter

def count_dict(words):
    c = {}
    for w in words: c[w] = c.get(w, 0) + 1
    return c

def count_list_count(words):
    return {w: words.count(w) for w in set(words)}        # one full pass of the list for EVERY distinct word

def count_counter(words):
    return Counter(words)

n = 100_000
print(f"n = {n} words")
print(f"{'distinct d':>10} | {'dict loop':>10} {'list.count':>11} {'Counter':>9} | list.count / dict | comparisons n*d")
for d in (10, 100, 1000, 3000):
    rnd = random.Random(d)
    vocab = [f"word{i}" for i in range(d)]
    words = [rnd.choice(vocab) for _ in range(n)]
    t0 = time.perf_counter(); a = count_dict(words); t1 = time.perf_counter()
    b = count_list_count(words); t2 = time.perf_counter()
    c = count_counter(words); t3 = time.perf_counter()
    assert a == b == dict(c)
    print(f"{d:>10} | {t1 - t0:>9.4f}s {t2 - t1:>10.4f}s {t3 - t2:>8.4f}s | {(t2 - t1) / (t1 - t0):>16.1f}x | {n * len(a):>14,}")

print("\nSpace (distinct d = 1000, n = 100,000):")
rnd = random.Random(1); vocab = [f"word{i}" for i in range(1000)]; words = [rnd.choice(vocab) for _ in range(n)]
for name, fn in (("dict loop", count_dict), ("list.count", count_list_count), ("Counter", count_counter)):
    tracemalloc.start(); r = fn(words); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"  {name:11} peak extra memory {peak / 1024:8.1f} KiB (result holds {len(r)} entries)")
