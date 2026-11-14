import time
from collections import Counter
from complaints import *

print("== Tests: empty text, upper/lower case, punctuation ==")
print("tokenize('')                   ->", tokenize(""))
print("tokenize('   ')                ->", tokenize("   "))
print("tokenize('Seeds, SEEDS! seeds.') ->", tokenize("Seeds, SEEDS! seeds."))
print("frequencies([], STOP)          ->", frequencies([], STOP_DEFAULT))
print("frequencies(['Seeds, SEEDS! seeds.'], STOP) ->", frequencies(["Seeds, SEEDS! seeds."], STOP_DEFAULT))
print("setdefault version equal:", frequencies_setdefault(["Seeds, SEEDS! seeds. Price price"], STOP_DEFAULT) == frequencies(["Seeds, SEEDS! seeds. Price price"], STOP_DEFAULT))
print("top ties alphabetical:", top({"b": 2, "a": 2, "c": 5}, 3))

print("\n== Grouping (dict of lists) on 8 sample complaints ==")
recs = make_complaints(8)
by_d = group_by(recs, 0); by_c = group_by(recs, 1)
print("complaints per district:", {d: len(v) for d, v in by_d.items()})
print("complaints per crop    :", {c: len(v) for c, v in by_c.items()})
print("one crop's complaints  :", next(iter(by_c.items())))

print("\n== Dictionary views ==")
c = {"seeds": 3, "price": 2}
ks, vs, its = c.keys(), c.values(), c.items()
print("keys():", ks, "values():", vs, "items():", its)
c["rain"] = 1
print("views are LIVE (after adding 'rain'):", ks, vs)
print("insertion order kept (Python 3.7+):", list(c))

print("\n== Experiment: 1,000 / 10,000 / 100,000 complaints ==")
def with_count_method(texts, stop):
    words = [w for t in texts for w in tokenize(t) if w not in stop]
    return {w: words.count(w) for w in set(words)}          # list.count for every DISTINCT word
def with_counter(texts, stop):
    return Counter(w for t in texts for w in tokenize(t) if w not in stop)
print(f"{'complaints':>10} {'words':>9} {'distinct':>9} | {'dict get()':>11} {'setdefault':>11} {'list.count':>11} {'Counter':>9} | same result")
for n in (1_000, 10_000, 100_000):
    texts = [r[2] for r in make_complaints(n)]
    t0 = time.perf_counter(); a = frequencies(texts, STOP_DEFAULT); t1 = time.perf_counter()
    b = frequencies_setdefault(texts, STOP_DEFAULT); t2 = time.perf_counter()
    cc = with_count_method(texts, STOP_DEFAULT); t3 = time.perf_counter()
    d = with_counter(texts, STOP_DEFAULT); t4 = time.perf_counter()
    nwords = sum(a.values())
    print(f"{n:>10} {nwords:>9} {len(a):>9} | {t1 - t0:>10.4f}s {t2 - t1:>10.4f}s {t3 - t2:>10.4f}s {t4 - t3:>8.4f}s | {a == b == cc == dict(d)}")
print("top 5 words (100,000 complaints):", top(a, 5))
