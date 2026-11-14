# Q1 – Lists and Slicing: Daily Rainfall Records (K3)

**Run:** `python run_q1.py` · `python alternatives.py`  (functions in `rainfall.py`; readings are made with `random`, seed fixed)

## Implementation (output of `run_q1.py`, 365 readings)
- **Weekly totals** by slicing: `[sum(readings[i:i+7]) for i in range(0, n, 7)]` → 53 blocks (52 full weeks + 1 leftover day because 365 = 52×7 + 1).
- **Max/min with positions** (`max_min_with_position`): wettest full week = week 47 (278.0 mm), driest = week 4 (0.0 mm); wettest day = day 251 (78.8 mm).
- **7-day moving average:** `moving_average_naive` and `moving_average_running`.
- **Dry days** (0 mm): 231 days; `[i + 1 for i, r in enumerate(readings) if r == 0]`.

## Pseudocode – 7-day moving average (running sum)
```
START
INPUT readings, window = 7
IF length of readings < window THEN
    OUTPUT empty list
ELSE
    SET total TO sum of the first 7 readings
    SET averages TO [total / 7]
    FOR i FROM 7 TO length of readings - 1
        SET total TO total + readings[i] - readings[i - 7]
        ADD total / 7 TO averages
    ENDFOR
    OUTPUT averages
ENDIF
END
```

## What the slices return (example list of 17 values `[5,0,3,8,0,1,2,9,4,0,6,7,1,2,3,4,5]`)
- `readings[7:14]` → items at index 7 to 13 (14 not included) = the **2nd week**, days 8–14: `[9, 4, 0, 6, 7, 1, 2]`. (A slice is a new list; indexes beyond the end are silently cut.)
- `readings[-7:]` → the **last 7** readings: `[6, 7, 1, 2, 3, 4, 5]`.
- `readings[::7]` → every 7th reading starting at index 0 (one per week, the first day of each week): `[5, 9, 3]`.

## Why a list, and operation costs
A list keeps readings **in date order**, gives any day by index in O(1), supports slicing for weeks, and grows when new days arrive.
| Operation | Cost | Reason |
|---|---|---|
| `append(x)` | O(1) amortised | adds at the end (occasionally the array is re-allocated) |
| `insert(i, x)` | **O(n)** | all items after position i shift one place |
| `pop()` (last) | O(1) | remove from the end |
| `pop(i)` / `pop(0)` | O(n) | items after i shift |
| `sort()` | O(n log n) | comparison sort (Timsort; O(n) if already sorted) |
| `x in list` | O(n) | scans |

## Number of additions (derived and counted)
- **Naive** (re-add every window): windows = n − 6; each window needs 6 additions (7 values) → **6(n − 6)** = O(7n).
- **Running sum:** first window 6 additions, then every shift = 1 addition + 1 subtraction → **6 + 2(n − 7)** = O(n).
| n | naive adds (counted = derived) | running ops (counted = derived) | naive time | running time |
|---|---|---|---|---|
| 365 | 2,154 | 722 | 0.0002 s | 0.0001 s |
| 36,500 | 218,964 | 72,992 | 0.0256 s | 0.0066 s |
| 365,000 | 2,189,964 | 729,992 | 0.190 s | 0.048 s |
The counted additions match the formulas exactly; the time ratio (≈ 3.4–4×) follows the ratio of counts (≈ 3×) plus the overhead of the inner loop.

## Edge cases
Empty list → weekly `[]`, max/min `None`, averages `[]`; 3 values → one short week, no moving average (`[]`); exactly 7 values → one average. No exceptions.

## Design question: a reading that arrives late
`list.insert(i, x)` shifts every later element: **O(n)** (measured at n = 365,000: ≈ 225 µs, versus 0.07 µs for `append`). For 365 values this is nothing, so a list is still fine. Better: because the position is the day number, pre-fill a year list with `None` (or `0.0`) and **assign** `readings[day] = value` – O(1), no shifting, no insertion at all. A dictionary keyed by date is the choice if days can be missing or the data is not a continuous year.

## Alternative concept: `deque(maxlen=7)` or dict keyed by date (output of `alternatives.py`)
```python
win = deque(maxlen=7)          # appending the 8th value drops the oldest automatically
```
| Approach | Time for n days | Measured n = 365,000 | Space |
|---|---|---|---|
| list + slicing + `sum(readings[i:i+7])` | O(7n) | – | O(n) list (2.8 MiB) + a 7-item temporary list per window |
| `deque(maxlen=7)` + `sum(window)` | O(7n) | 0.055 s | O(n) readings + **O(7)** window (about 0.7 KB) |
| `deque` + running sum | **O(n)** | 0.036 s | O(7) window |
| dict `{date: mm}` + 7 lookups per day | O(7n) (each lookup O(1) average) | 1.13 s | **~11× more** (31.9 MiB vs 2.9 MiB: hash table + date objects) |
The deque makes the window code simple (no index arithmetic, memory O(7)); the running sum is what changes the time from O(7n) to O(n). The dictionary is only worth its memory when dates, not positions, are the natural key (missing days, random access by date).
