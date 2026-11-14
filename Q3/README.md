# Q3 – Dictionaries: Farmer Helpline Complaint Analysis (K4)

**Run:** `python complete_code.py` · `python run_q3.py` · `python alternatives.py`  (functions in `complaints.py`)

## Complete the Code (done in `complete_code.py`)
Output: `[('seeds', 3), ('price', 2), ('received', 2)]` – exactly as expected.
- `frequencies`: `counts[word] = counts.get(word, 0) + 1` for each word not in `STOP`.
- `top`: `sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]` – the key is a tuple: first the **negative count** (so larger counts come first), then the word (alphabetical).
- **Why `price` comes before `received`:** both have count 2, so the first part of the key ties; the second part compares the words, and `"price" < "received"` because `p` comes before `r` in the alphabet.

## Implementation (`complaints.py`)
- `tokenize` – lower-case, remove punctuation (`str.translate`), `split()`. `""` → `[]`.
- `frequencies` (with `get()`) and `frequencies_setdefault` (with `setdefault()`, `box.setdefault(word, [0])[0] += 1`) give identical results.
- `group_by(records, i)` – `groups.setdefault(key, []).append(text)`: dictionary of lists, used for complaints per district (index 0) and per crop (index 1).
- `top(counts, k)` – top k by count then alphabetically. Stop words are a **set** (`word not in stop` is O(1)).
Tests (from `run_q3.py`): empty text → `[]` / `{}`; `'Seeds, SEEDS! seeds.'` → `{'seeds': 3}` (case and punctuation handled); ties sorted alphabetically.

## How a dictionary finds a key, and why lookup cost does not depend on size
`d[key]`: Python computes `hash(key)`, uses it to pick a slot in an array (hash table); if the slot holds an equal key, the value is returned; if the slot is taken by another key (a collision) it probes the next slot(s) in a fixed pattern. The table is kept less than about 2/3 full (it is resized as it grows), so on average only a **constant number of slots** is examined, whatever the number of keys: O(1) average. (Worst case O(n) if many keys collide – unlikely with good hashes.)

## Dictionary vs `list.count()` for every distinct word
`words.count(w)` scans the whole list for **each** distinct word: n × d comparisons = O(n·d). The dictionary loop touches each word once: O(n).

## Order of keys (Python 3.7+)
Keys keep **insertion order** (guaranteed by the language): `list(c)` returned `['seeds', 'price', 'rain']` in the order they were added. Updating an existing key does not move it; deleting and re-adding puts it at the end. (It is *not* sorted order.)

## Views
`keys()`, `values()`, `items()` return **view objects**: they show the dictionary's current content without copying it. They are *live* – after `c["rain"] = 1` the views created earlier show `rain` too – and cannot be changed while iterating the dictionary (adding keys during a loop raises `RuntimeError`). `items()` gives `(key, value)` pairs, used for `for word, count in d.items()`.

## Experiment (output of `run_q3.py`; complaint text with ≈ 6 words each, 120 distinct words)
| complaints | words | dict `get()` | `setdefault` | `list.count` | `Counter` | same result |
|---|---|---|---|---|---|---|
| 1,000 | 5,997 | 0.0031 s | 0.0034 s | 0.0083 s | 0.0029 s | yes |
| 10,000 | 60,184 | 0.0299 s | 0.0313 s | 0.0874 s | 0.0301 s | yes |
| 100,000 | 600,651 | 0.313 s | 0.319 s | 0.876 s | 0.295 s | yes |
(The times include tokenising. Dict, `setdefault` and `Counter` are the same speed because `Counter` is the same dictionary idea in C; `list.count` is only ~3× slower here because d is just 120 and the scanning runs in C.)

**The n·d growth shows when d grows** (`alternatives.py`, 100,000 words, counting only):
| distinct d | dict loop | `list.count` | `list.count` ÷ dict | comparisons n·d |
|---|---|---|---|---|
| 10 | 0.0048 s | 0.0081 s | 1.7× | 1,000,000 |
| 100 | 0.0039 s | 0.0732 s | 18.9× | 10,000,000 |
| 1,000 | 0.0035 s | 0.729 s | 210× | 100,000,000 |
| 3,000 | 0.0034 s | 2.84 s | 828× | 300,000,000 |
The dictionary time stays flat (O(n)); `list.count` time grows in proportion to d (O(n·d)).

## Engineering decision for 100,000 complaints a day
Deploy **`collections.Counter`** (or the plain dictionary loop – same speed). Reasons: O(n) time independent of the number of distinct words (real complaints have thousands of distinct words, where `list.count` becomes hundreds of times slower), memory O(d) (not extra O(n) list), shorter code (`Counter(words).most_common(k)`; note `most_common` orders ties by first appearance, so for the required "count, then alphabetical" order I still use my `top()` with the sorted key). 100,000 complaints take ≈ 0.3 s.

## Alternative concept: `list.count()` per distinct word, or `Counter`
```python
{w: words.count(w) for w in set(words)}     # O(n·d), n words, d distinct
Counter(words)                              # O(n)
```
- **Time:** `list.count` O(n·d) (measured above: 0.73 s vs 0.0035 s at d = 1,000); dictionary loop and Counter O(n).
- **Space:** dictionary / Counter O(d) (38 KiB for d = 1,000); the `list.count` version needs the `set(words)` plus the result, O(d) too (70 KiB), plus the list of all n words that every approach needs in the first place – so the difference is time, not memory.
