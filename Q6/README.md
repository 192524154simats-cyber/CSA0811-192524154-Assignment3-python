# Q6 – Nested Data: A Railway Timetable (K4)

**Run:** `python run_q6.py` · `python alternatives.py`  (data structure and functions in `railway.py`)

## The nested structure (5 trains built in `SAMPLE`; output of `print_timetable`)
```
timetable ─ dict ─► train number (int) ──► dict
                                           ├─ "name" : str
                                           ├─ "stops": list ─► (station, arrival, departure)   tuple, tuple, ...
                                           └─ "days" : set  ─► {"Mon", "Wed", "Fri"}
```
Example train: `12601: {"name": "Chennai Mail", "stops": [("Chennai","--","20:00"), ("Arakkonam","21:10","21:12"), ("Katpadi","22:05","22:10"), ...], "days": {"Mon","Wed","Fri"}}`

**Expression for the departure time of the third station of a train:**
`timetable[12601]["stops"][2][2]` → `'22:10'` (train → `"stops"` list → third stop at index 2 → departure at index 2 of the tuple). The station name is `…["stops"][2][0]` → `'Katpadi'`.

## Why each part uses that type
- **dict (train number → details):** direct access by a unique key in O(1); the key is not a position.
- **dict for the details (name, stops, days):** fields have names; the number of fields is small and fixed.
- **list of stops:** the **order of stops matters** (route sequence) and a list keeps it, allows indexing (`[2]`) and slicing.
- **tuple (station, arrival, departure):** one stop is a fixed record of three values that should not be changed by accident; tuples are smaller and show intent.
- **set of days:** days have no order and no duplicates; `"Sun" in days` is O(1).

## Work for one station query (no index)
`stops_at(timetable, station, day)` visits every train (T of them): checks `day in days` (O(1)); for trains that run that day it scans the stops (s per train, here 8–14) until the station is found. Work ≈ **O(T · s) = O(total stops)** in the worst case, then sorting the r matching trains: O(r log r). With 10,000 trains × ~11 stops = 109,719 stops.

## Index station → list of trains (`build_index`)
`index = {station: [train numbers]}` built once: for each train, for each stop, `index.setdefault(station, []).append(train)` – O(total stops) time, O(total stops) space. Then a query reads `index.get(station, [])` (O(1)) and only the r' trains that stop there are examined: **O(trains at the station)** + sorting.
(Even faster variant: store `(train, arrival, departure)` in the index so no stop scan is needed.)

## Tests
| Case | Result |
|---|---|
| Katpadi on Sat | 3 trains sorted by departure: 16721 (00:20), 12007 (07:37), 22651 (11:55) |
| Unknown station "Atlantis" | `[]` (index: `index.get` → `[]`, no `KeyError`) |
| Katpadi on Tue | 22651 excluded (runs only Sat/Sun) → `[16721, 12007]` |
| Salem on Wed | only 12601 (16721 and 22651 do not run on Wed) |
| Coimbatore on Sun | `[(22651, '07:15'), (16721, '--')]` – terminus has no departure, sorted last |
Both versions give identical answers on all 300 random queries at each size.
Limitation: times are text `HH:MM`, so a departure just after midnight (00:20) sorts first in the day; a real system needs a day offset.

## Experiment (300 random (station, day) queries; 300 stations; output of `run_q6.py`)
| trains | total stops | avg trains / station | no index (ms/query) | with index (ms/query) | speed-up | index memory |
|---|---|---|---|---|---|---|
| 100 | 1,091 | 3.6 | 0.0263 | 0.0025 | 11× | 35 KiB (build 0.1 ms) |
| 1,000 | 10,846 | 36.2 | 0.2827 | 0.0192 | 15× | 113 KiB (build 1.0 ms) |
| 10,000 | 109,719 | 365.7 | 3.274 | 0.416 | 8× | 933 KiB (build 9.7 ms) |
The query time without the index grows ≈ 10× per 10× trains (linear in the timetable), the indexed query grows with the number of trains **at that station** (3.6 → 36 → 366) – both grow, but the index version starts and stays about an order of magnitude cheaper. The speed-up is not larger because each indexed query still scans ~11 stops of every train it finds and sorts the results; the no-index version skips trains that do not run that day without scanning them.

## Conclusion – why an index makes queries faster, and the trade-off
An index does the searching **once in advance**: it groups the trains by station, so a query goes straight to the right list through a hash lookup instead of looking at every train. **Trade-off:** extra memory (≈ 1 MB at 10,000 trains), build time (≈ 10 ms), and the index must be **kept in step** with the timetable – when a train is added, cancelled or its stops change, the index must be updated, otherwise queries return wrong answers. Worth it when queries are far more frequent than timetable changes (an enquiry counter).

## Alternative concept: one flat list of (train, station, arrival, departure, days) tuples
```python
flat = [(no, name, station, arr, dep, days), ...]      # one row per stop
[r for r in flat if r[2] == station and day in r[5]]    # scanned for every query
```
| trains | total stops | flat scan (ms/query) | nested + index (ms/query) | ratio |
|---|---|---|---|---|
| 100 | 1,091 | 0.021 | 0.0016 | 13× |
| 1,000 | 10,846 | 0.227 | 0.0289 | 8× |
| 10,000 | 109,719 | 2.34 | 0.292 | 8× |
- **Time per query:** flat list **O(total stops)** – it always reads every row (109,719 rows at 10,000 trains); nested dictionaries + index **O(trains at the station)** plus a short scan of each of their stops.
- **Space:** flat list O(total stops) rows, with the train name and days repeated or shared in every row (the data of a train is *not* stored once); nested design O(total stops) too, plus the index O(total stops) (≈ 938 KiB here) – so the index roughly adds one reference per stop. (In the table, "flat list memory" is the memory of the extra row tuples only, because the station/time strings are shared with the nested data built first; a stand-alone flat list would hold the same strings, so the total memory of both designs is about the same apart from the index.)
- **Design:** the flat list is simplest to build and fine for a few hundred rows; nested + index is better when the timetable is large and queries are frequent, and it stores each train's name and days once.
