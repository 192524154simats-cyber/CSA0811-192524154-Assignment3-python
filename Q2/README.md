# Q2 – Tuples, Mutability and Copying (K4)

**Run:** `python complete_code.py` · `python tuples_demo.py` · `python alternatives.py`

## Complete the Code (TODO 1 done in `complete_code.py`)
`good = [[0] * cols for _ in range(rows)]` – the comprehension runs `[0] * cols` **once per row**, so each row is a new list. Output equals the expected output:
```
bad: [[0, 7, 0, 0], [0, 7, 0, 0], [0, 7, 0, 0]]
good: [[0, 7, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
True False
T. Nagar
```
A list as a dictionary key: `TypeError: unhashable type: 'list'`.

## Why tuples can be dictionary keys but lists cannot
A dictionary finds a key by its **hash value**, and the key must keep the same hash for its whole life. A tuple of numbers cannot change, so its hash is fixed (`hash((13.0, 80.0))` works). A list can change (`append`, item assignment), so its hash could change after it was stored and the dictionary would no longer find it – therefore Python refuses: `hash([..])` → `TypeError: unhashable type: 'list'`. (A tuple is hashable only if everything inside it is hashable: `([1], 2)` cannot be a key.)

## Memory diagrams
`bad = [[0] * 3] * 3` – three references to **one** inner list:
```
bad ──► [ ●, ●, ● ]         ids of rows: 140322692320064 (all three the same)
          │  │  │
          └──┴──┴──────►  [0, 0, 0]      <- ONE list object
```
`good = [[0] * 3 for _ in range(3)]` – three separate inner lists:
```
good ──► [ ●, ●, ● ]
          │  │  └───────►  [0, 0, 0]     (id …152)
          │  └──────────►  [0, 0, 0]     (id …088)
          └─────────────►  [0, 0, 0]     (id …896)
```
Evidence: `bad[0] is bad[1]` → `True`, `good[0] is good[1]` → `False`; after `[0][1] += 5`, `bad` shows 5 in every row, `good` only in row 0.

## Aliasing, shallow copy, deep copy (output of `tuples_demo.py`)
| Statement | New outer list? | Inner lists shared? | Effect of `orig[0][0] = 99` and `orig.append(...)` |
|---|---|---|---|
| `alias = orig` | no – same object | – | sees both changes |
| `copy.copy(orig)` / `orig[:]` | yes | **yes** | sees the inner change (99), not the new row |
| `copy.deepcopy(orig)` | yes | no | sees neither |
**Shallow copy is enough** when the elements are immutable (numbers, strings, tuples) – a flat list of numbers. **Deep copy is needed** when the elements are mutable and you will change them independently (a grid, a list of lists/dicts). 

## Why a function that changes a list argument changes the caller's list
Python passes a **reference** to the object. `zones.append("Z9")` changes that single object, which the caller also references: after `add_zone(mine)` the caller's list is `['Z1', 'Z9']`. To avoid it: copy first (`zones = list(zones)`), or return a new list (`zones + ["Z9"]`, shown in `add_zone_safe`).

## A list stored inside a tuple
`t = ([1, 2], 3)`: `t[0].append(99)` **works** – the tuple still holds the same list object; the list was changed, not the tuple. `t[0] += [100]` raises `TypeError: 'tuple' object does not support item assignment` **but the list is extended anyway** (`+=` first extends the list in place, then tries to store the result back into the tuple and fails). Immutability of a tuple is only one level deep: it fixes *which objects* it holds, not their contents.

## Memory and time (1,000,000 values)
| | list | tuple |
|---|---|---|
| `sys.getsizeof` | 8,000,056 bytes | 8,000,040 bytes |
| small (2 items) | 72 bytes | 56 bytes |
| create from `range` | 18.6 ms | 16.8 ms |
| create a literal of 5 constants | 48 ns | 23 ns (the constant tuple is built once at compile time) |
| 1,000,000 index operations | 14.7 ms | 16.0 ms (same, O(1) each) |
`getsizeof` counts only the container (8 bytes per pointer), not the ints. A list built by `append` is larger than one built from `range` because of spare capacity kept for growth; a tuple has no spare slots.

## Conclusion
Use a **tuple** for a fixed group of related values that belongs together (a (latitude, longitude) pair, a record) and for dictionary keys or set members. Immutability protects you from accidental changes by other code (including functions you pass the data to), from aliasing bugs where one change shows up elsewhere, and from broken dictionary keys. Use a **list** when the number or the content of items must change.

## Alternative concept: dictionary keyed by (row, col) holding only non-empty zones
```python
sparse = {}
sparse[(r, c)] = sparse.get((r, c), 0) + 1       # only zones with passengers exist
```
| grid | cells | busy zones | list of lists | dict | access list / dict |
|---|---|---|---|---|---|
| 100×100 | 10,000 | 494 | 84 KiB | 18 KiB | 43 / 44 ns |
| 1000×1000 | 1,000,000 | 4,990 | 7,876 KiB | 144 KiB | 61 / 51 ns |
| 3000×3000 | 9,000,000 | 4,999 | 70,498 KiB | 144 KiB | 61 / 51 ns |
Access is O(1) in both (index arithmetic vs hash lookup – measured about the same). **Space:** list of lists O(rows × cols) regardless of use; dictionary O(number of non-empty zones) (about 30 bytes ×… per entry, so the dictionary wins when fewer than roughly 1 zone in 10 is busy; when most zones are busy the list is smaller and faster). The dictionary also needs `.get(key, 0)` for empty zones and does not give row-wise slices.
