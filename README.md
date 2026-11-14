# CSA08-<RegisterNumber>-Assignment3 – Data Structures (Lists, Tuples, Dictionaries, Sets)

| | |
|---|---|
| Name | `<your name>` |
| Register number | `<your register number>` |
| Python version | 3.12 |
| Libraries | none to install – standard library only (see `requirements.txt`) |
| GitHub link | `<paste your repository link here>` |

> Replace the `<...>` parts and rename the folder to `CSA08-<RegisterNumber>-Assignment3` before pushing.

## How to use
1. Open this folder in VS Code (File → Open Folder). 2. Open the terminal, `cd` into a question folder, run the commands below and screenshot every output. 3. Upload the screenshots into the matching folder on GitHub. 4. Commit one question at a time (`git add Q1`, `git commit -m "Q1: rainfall lists"`) – the commit history is checked.
Each folder's `README.md` has the written answers (explanations, diagrams, tables of counts and timings, the *Alternative Concept and Complexity Analysis*). Random data uses fixed seeds, so counts and results repeat on every computer; **timings** will differ a little – use your own numbers in your screenshots. Optional: `python run_all.py` runs everything (about 3–4 minutes in total, Q7 `alternatives.py` is the longest).

| Q | Topic | Run (inside the folder) | Main evidence |
|---|---|---|---|
| Q1 | Lists, slicing, moving average | `python run_q1.py` · `python alternatives.py` | counted additions = derived 6(n−6) and 6+2(n−7); deque and dict alternatives |
| Q2 | Tuples, copying, grid bug | `python complete_code.py` · `python tuples_demo.py` · `python alternatives.py` | expected output, id()/is proof, shallow vs deep copy, sparse dict grid |
| Q3 | Dictionaries, word counts | `python complete_code.py` · `python run_q3.py` · `python alternatives.py` | `[('seeds', 3), ('price', 2), ('received', 2)]`; list.count n·d growth |
| Q4 | Sets, clash detection | `python complete_code.py` · `python run_q4.py` | expected output; in-list vs in-set up to 1,000,000; nested loops vs `&` |
| Q5 | List comprehension | `python run_q5.py` · `python alternatives.py` | loop vs comprehension vs map/filter; list vs generator memory |
| Q6 | Nested timetable + index | `python run_q6.py` · `python alternatives.py` | 100 / 1,000 / 10,000 trains, with and without index, flat list |
| Q7 | Contact merging | `python run_q7.py` · `python alternatives.py` | hand-checked 6 people; 1,000 and 100,000 contacts; pairwise O(n²) |

## Complete-the-Code locations
Q2: `Q2/complete_code.py` · Q3: `Q3/complete_code.py` · Q4: `Q4/complete_code.py` (operators and methods).

## Short result note per question
1. Counted additions equal the derived formulas (naive 6(n−6), running sum 6+2(n−7)); running sum ≈ 4× faster at 365,000 readings; `list.insert` is O(n).
2. `[[0]*c]*r` makes one shared row (`is` → True); the comprehension makes separate rows; a tuple holding a list can still change the list.
3. Dictionary counting is O(n); `list.count` per distinct word grows with d (828× slower at d = 3,000).
4. `&`, `^`, `-` give the expected clash / exactly-one / neither sets; set lookup is 20,000× faster than list at 1,000,000 items.
5. Comprehension ≈ 5 % faster than the loop, map+filter ≈ 25 % slower; a generator uses 0.41 KiB instead of 8.2 MB.
6. A station index makes queries 8–15× faster for ~1 MB extra memory; the price is keeping it up to date.
7. Dictionary keyed by normalised number: 0.86 s for 100,000 contacts; pairwise is O(n²) (≈ 7–8 minutes estimated).
