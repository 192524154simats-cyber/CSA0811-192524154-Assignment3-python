# Q4 – Sets: Elective Registration Clash Detection (K4)

**Run:** `python complete_code.py` · `python run_q4.py`  (functions in `electives.py`; the alternative-concept experiment is the last section of `run_q4.py`)

## Complete the Code (set operators only)
```python
both        = ai_elective & iot_elective                    # intersection
exactly_one = ai_elective ^ iot_elective                    # symmetric difference
neither     = all_students - (ai_elective | iot_elective)   # difference of the union
```
Output equals the expected output: clash `['192311004', '192311009']`; exactly one `['192311001', '192311002', '192311007', '192311010']`; neither `['192311003', '192311005', '192311006', '192311008']`.
**Rewritten with set methods** (`intersection`, `symmetric_difference`, `difference`, `union`): the program prints `True True True` – identical results. (Methods also accept any iterable such as a list; the operators need two sets.)

## Hand verification
AI = {001, 004, 007, 009}, IoT = {002, 004, 009, 010}. Common to both: 004, 009. In exactly one: AI-only {001, 007} + IoT-only {002, 010}. Union = 6 students; everyone = 10, so neither = 10 − 6 = {003, 005, 006, 008}. Check by inclusion–exclusion: |AI| + |IoT| = 8 = |union| + |both| = 6 + 2.

## Venn diagrams (numbers are the last three digits of the register numbers)
```
          AI                IoT
     ┌──────────┐     ┌──────────┐
     │  001 007 ┌─────┴──┐ 002 010│
     │          │004 009 │        │
     └──────────┴────────┴────────┘
          only AI    both     only IoT
 a & b     (intersection)       :        ████ middle only      {004, 009}
 a | b     (union)              :        ████ all of both circles {001,002,004,007,009,010}
 a - b     (difference)         :        AI circle without the middle {001, 007}
 a ^ b     (symmetric difference):       both circles without the middle {001, 002, 007, 010}
 all - (a | b) (neither)        :        the area OUTSIDE both circles {003, 005, 006, 008}
```

## Why sets remove duplicates
A set stores each element once in a hash table. Adding an element that is already there (equal hash and equal value) finds the existing slot and changes nothing, so `set(["001","004","001"])` → `{'001','004'}`. What is lost: the order of typing and the number of times a value occurred.

## Why `x in set` is faster than `x in list`
A list must compare `x` with items one by one: O(n). A set computes `hash(x)` and goes straight to one slot: O(1) on average.
| n | list lookup (value absent) | set lookup | ratio |
|---|---|---|---|
| 10,000 | 0.056 ms | 0.22 µs | 256× |
| 100,000 | 0.57 ms | 0.24 µs | 2,405× |
| 1,000,000 | 8.0 ms | 0.40 µs | 20,224× |
The list time grows ~10× for each 10× in n; the set time stays about the same.

## Why sets cannot contain lists but can contain tuples
Set members must be hashable (fixed hash). A list can change, so `{[1, 2]}` → `TypeError: unhashable type: 'list'`; a tuple of hashable items cannot change, so `{(1, 2), (3, 4)}` works (use a tuple to put a pair such as (register no, elective) in a set). 

## Tests (output of `run_q4.py`)
| Case | Result |
|---|---|
| empty elective & AI | clash `set()`, exactly one = all 4 AI students |
| empty & empty | exactly one `set()`, neither = all 10 |
| identical electives | clash = all 4, exactly one = `[]`, only-AI = `[]` |
| duplicates typed `001, 004, 001, 004, 004` | `{001, 004}` |

## Alternative concept: lists + nested loops, or sorted lists walked together
| n = m | nested loops (comparisons) | sorted walk | set `&` |
|---|---|---|---|
| 500 | 0.0056 s (250,000) | 0.0002 s | 0.00005 s |
| 1,000 | 0.0219 s (1,000,000) | 0.0003 s | 0.00008 s |
| 2,000 | 0.0777 s (4,000,000) | 0.0006 s | 0.00018 s |
| 4,000 | 0.3025 s (16,000,000) | 0.0012 s | 0.00031 s |
| 100,000 | not run (10¹⁰ comparisons) | 0.043 s | 0.015 s |
| 1,000,000 | not run (10¹² comparisons) | 0.87 s | 0.29 s |
All approaches gave the same common students.
- **Nested loops:** time **O(n·m)** (the comparison count equals n × m exactly: 16,000,000 for 4,000 × 4,000); space O(1) extra (plus the result).
- **Sort both, walk with two pointers:** sorting costs O(n log n + m log m), the walk O(n + m); space O(n + m) if sorted copies are made (O(1) extra if sorted in place). Needs items that can be ordered.
- **Sets:** building `set(A)` and `set(B)` is O(n + m); `&` is O(min(n, m)) on average; total **O(n + m)** average time, **O(n + m)** space for the two hash tables (a set uses several times the memory of a list of the same items).
Sets are fastest and simplest; the sorted walk is the fallback when memory is tight or order is needed.

## Conclusion – when to convert a list to a set
Convert when you will do many membership tests (`x in …`), remove duplicates, or compute union/intersection/difference – cost O(n) once, then O(1) per test. What is lost: **order**, **duplicates/counts**, and **indexing/slicing**; also the items must be hashable. Keep the list (or sort it) when order or counts matter.
