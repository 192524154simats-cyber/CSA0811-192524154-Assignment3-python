# Q5 – List Comprehension: Cleaning Sensor Readings (K3)

**Run:** `python run_q5.py` · `python alternatives.py`  (functions in `sensors.py`)
Rules used: valid reading = `-50 <= c <= 50` (above 50 or below −50 is a sensor error); safe range 2–8 °C inclusive; Fahrenheit = C × 9/5 + 32.

## Implementations (all three give identical results – checked at 10,000 / 100,000 / 1,000,000 readings)
```python
# 1. for loop with append
for c in readings:
    if -50 <= c <= 50: c_list.append(c); f_list.append(c * 9 / 5 + 32)
# 2. list comprehensions with conditions
c_list = [c for c in readings if -50 <= c <= 50]
f_list = [c * 9 / 5 + 32 for c in c_list]
# 3. map() and filter() with lambda
c_list = list(filter(lambda c: -50 <= c <= 50, readings))
f_list = list(map(lambda c: c * 9 / 5 + 32, c_list))
# alarm minutes with enumerate()
alarms = [m for m, c in enumerate(readings) if -50 <= c <= 50 and not 2 <= c <= 8]
```
Example `[5.0, 70.5, 3.2, -60.0, 9.1, 1.5, 8.0, 2.0]` → valid `[5.0, 3.2, 9.1, 1.5, 8.0, 2.0]`; alarm minutes `[4, 5]` (9.1 and 1.5). 70.5 and −60.0 are **errors, not alarms**; 8.0 and 2.0 are inside the safe range. `enumerate` gives the minute number of the *original* log, so removing bad readings first would give wrong minutes – that is why alarms are computed from the raw list.

## General form of a list comprehension with a condition
`[expression for item in iterable if condition]` – read as "for each item, if the condition is true, include expression(item)". With if/else inside the expression: `[a if cond else b for item in iterable]`.

## When a comprehension is harder to read than a loop
When it has several nested `for`s, several conditions, side effects, or needs a long expression or intermediate variables (e.g. `[f(x) for row in grid for x in row if x and g(x) > 2]`). Then a plain loop with names and comments is clearer. Rule of thumb: if it does not fit in one readable line, use a loop.

## Dictionary and set comprehensions
- `{m: round(c * 9 / 5 + 32, 1) for m, c in enumerate(r) if -50 <= c <= 50}` → minute → Fahrenheit: `{0: 41.0, 2: 37.8, 4: 48.4, 5: 34.7, 6: 46.4, 7: 35.6}`.
- `{int(c) for c in valid}` → distinct whole-degree values: `{1, 2, 3, 5, 8, 9}`.

## List comprehension vs generator expression
`[x for …]` builds the **whole list** in memory now. `(x for …)` builds nothing: it produces one item at a time **when asked** (lazy), takes constant memory and can be used **only once** (`sum(g), sum(g)` → `6 0`). Use a generator when you only need to loop/aggregate once (`sum`, `max`, `any`, writing to a file); use a list when you need the data again, its length, indexing or slicing.

## Experiment – time (seconds; the three versions on the same data)
| readings | valid | for + append | comprehension | map + filter |
|---|---|---|---|---|
| 10,000 | 9,689 | 0.0010 | 0.0010 | 0.0013 |
| 100,000 | 97,048 | 0.0105 | 0.0099 | 0.0129 |
| 1,000,000 | 969,838 | 0.1086 | 0.1035 | 0.1326 |
The comprehension is about 5 % faster than the loop (no repeated `append` method lookup); `map`/`filter` with a `lambda` is about 25 % **slower** because each element calls a Python-level lambda function. (An earlier version of my comprehension filtered twice and was slower than the loop – the filter must run once; this is the corrected version.)

## Memory (1,000,000 readings, 969,838 valid)
| | `sys.getsizeof` | tracemalloc peak for `sum(...)` |
|---|---|---|
| list comprehension | 8,448,728 bytes | 8,250 KiB |
| generator expression | **208 bytes** | **0.41 KiB** |
`getsizeof` of the list counts only the pointers, but the peak shows the real cost: ~8 MB versus nothing.

## Tests
All valid → 5 of 5 kept; all invalid `[99, -75, 51, -50.1]` → 0 kept, no alarms; empty list → `[]`; boundaries `50.0, -50.0` are valid (and alarm minutes 0 and 1, being outside 2–8), `50.1, -50.1` are errors. All three versions equal in every case.

## Conclusion – is a comprehension always the best choice?
No. (1) Compared with a plain loop it is only ~5 % faster – readability decides. (2) `map`/`filter` + lambda was the slowest (25 % slower here). (3) When the result is used once (a sum, a max, `any`) a **generator expression** is better: same time, 8,250 KiB → 0.4 KiB, and `any(c > 90 for c in data)` stops at the first hit (0.000011 s versus 0.0221 s for building the whole list first). (4) Complex logic is clearer in a loop.

## Alternative concept: `sum(c for c in readings if -50 <= c <= 50)`
| n | `sum([list comp])` time / peak | `sum(generator)` time / peak |
|---|---|---|
| 10,000 | 0.0005 s / 83 KiB | 0.0005 s / 0.41 KiB |
| 100,000 | 0.0055 s / 782 KiB | 0.0047 s / 0.41 KiB |
| 1,000,000 | 0.0543 s / 8,251 KiB | 0.0476 s / 0.41 KiB |
**Time O(n) in both** (every reading is tested once; the generator is even a little faster since no list is built). **Memory: O(n) for the list, O(1) for the generator** – the peak stays 0.41 KiB however many readings there are.
