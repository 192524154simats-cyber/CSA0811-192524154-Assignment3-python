# Q7 – Design a Contact-Merging Program from First Principles (K5)

**Run:** `python run_q7.py` (hand-checked example, normalisation tests, timings for 1,000 / 10,000 / 100,000 contacts, check against pairwise) · `python alternatives.py` (pairwise comparison experiment)
Files: `contacts.py` (design), `run_q7_data.py` (synthetic contact generator, seeded).

## Stage 1 – Interpret the problem
**Input:** contact lists from phone 1, phone 2 and the SIM: each contact has an optional name, zero or more phone numbers (any format) and zero or more e-mail addresses.
**Output:** one record per person: all their (normalised) numbers, all e-mails, and a display name.
**Rule: two contacts are the same person if they share at least one normalised phone number** (a person's number identifies them). A contact with no number but an e-mail is matched by e-mail. **The name is never a key**, because spellings differ ("Dr. Ravi", "ravi kumar") and different people can share a name.
**Data structures:**
| Need | Structure | Why |
|---|---|---|
| a contact | `dict` with optional keys | missing fields are simply absent (`c.get("numbers", [])`) |
| numbers / e-mails / names of one person | `set` | no duplicates; merging is `\|=` |
| find the person that owns a number | `dict` number → person id | O(1) average lookup |
| all people | `dict` id → person (`{"names","numbers","emails"}`) | removing a person after a merge is O(1) |

## Stage 2 – Design
**Normalising numbers (`normalise_number`):** keep only digits; if 12 digits starting with `91` drop `91`; if 11 digits starting with `0` drop the `0`; accept only exactly 10 digits, else `None`. So `+91 98400 12345`, `09840012345`, `98400-12345`, `9840012345` all become `9840012345`.
**Normalising e-mail:** strip spaces, lower-case, must contain `@` (not at either end).
**Normalising names (`normalise_name`):** remove punctuation (apostrophe kept), lower-case, split into words, drop titles (`dr, mr, mrs, ms, prof, shri, smt, sri`), capitalise → `"Dr. Ravi"` → `Ravi`, `"  MR.  RAVI   KUMAR "` → `Ravi Kumar`. Names are only collected for display; the longest spelling is shown.
**Merging:** dictionary `key_to_person` keyed by the normalised number (set of numbers and e-mails inside each person).
```
ALGORITHM MergeContacts
START
SET people TO empty dictionary            // person id -> {names, numbers, emails} (sets)
SET key_to_person TO empty dictionary     // normalised number (or e-mail) -> person id
FOR each contact IN all contacts
    SET nums TO set of valid normalised numbers of the contact
    SET mails TO set of valid normalised e-mails of the contact
    SET keys TO nums IF nums is not empty ELSE mails
    IF keys is empty THEN
        ADD the contact as a separate person (cannot be matched)
    ELSE
        SET owners TO set of key_to_person[k] for every k IN keys that is already known
        IF owners is empty THEN
            CREATE a new person
        ELSE
            SET person TO the smallest id IN owners
            FOR each other IN owners except person
                MERGE other's names, numbers and e-mails into person
                REPOINT every key of other to person
            ENDFOR
        ENDIF
        ADD the name, nums, mails to person
        SET key_to_person[k] TO person for every k IN nums and mails
    ENDIF
ENDFOR
OUTPUT all people
END
```
A contact holding two numbers that belong to two earlier people **links them** (they are merged): see the "chain" test.

## Stage 3 – Implement, test, measure (output of `run_q7.py`)
**Hand check:** 10 typed contacts (3 lists). By hand: Ravi appears 4 times (`+91 98400 12345`, `9840012345`, `98400 12345`, and one entry holding both `9840012345` and `9876543210`, plus `09876543210` office) → 1 person with 2 numbers and 1 e-mail; Meena 2 entries → 1 person (e-mails `MEENA@mail.com ` and others normalised); Arun with no number → kept as separate entries (2); Raja twice with different numbers → 2 people. Expected **6 people**; program output **6 – OK**.
**Tests:** formats (`+91 …`, `0…`, hyphen, spaces) → same 10 digits; too short `1234` → `None`; missing fields (no name, no number, empty list) → no crash; exact duplicate → 1 person; same name, different numbers → 2 people; chain A(n1), B(n1,n2), C(n2) → 1 person.
**Time (dictionary design, generated contacts: ≈ 1.6 contacts per person, some with 2 numbers, mixed formats):**
| contacts | time | per contact | people found |
|---|---|---|---|
| 1,000 | 0.0052 s | 5.2 µs | 515 |
| 10,000 | 0.0543 s | 5.4 µs | 5,114 |
| 100,000 | 0.86 s | 8.6 µs | 51,077 |
Time grows about in proportion to n (the per-contact cost rises a little at 100,000 because of cache effects of the large dictionaries).
**Cross-check:** at n = 1,000 and 2,000 the pairwise method finds exactly the same grouping (509 and 1,028 people).

## Stage 4 – Defend the design
**Why a dictionary beats comparing every pair:** to know whether a number was seen before, the dictionary answers in one hash lookup (O(1) average). Comparing pairs asks the question of n(n − 1)/2 pairs: for 100,000 contacts that is 4,999,950,000 comparisons. The dictionary does ≈ 1.2 lookups per contact.
**Two different people with the same name:** the name is not part of the key, so "Raja" (9000011111) and "Raja" (9000022222) stay two records (tested). Only a shared number merges records.
**Limitations (one is enough; several noted):**
1. People who share a number (a family landline or an office number) are wrongly merged, and one person with two numbers who never appears with both in the same contact stays split in two.
2. Contacts with no number or e-mail cannot be matched (kept separate; "Arun" stays two entries).
3. Digit-only normalisation ignores letters inside numbers (`98400 1234a5` → `9840012345`) and handles only Indian 10-digit mobile numbers.
4. Names are not compared at all, so "Ravi" and "Ravi Kumar" with different numbers are two people – merging them would need fuzzy matching (and risks wrong merges).

## Alternative concept: compare every pair of contacts (`alternatives.py`)
```python
for i in range(n):
    for j in range(i + 1, n):
        if keys[i] & keys[j]: union(i, j)      # n(n-1)/2 comparisons, joined with union-find
```
| n | dictionary | pairwise | pair comparisons | slowdown |
|---|---|---|---|---|
| 1,000 | 0.008 s | 0.062 s | 499,500 | 8× |
| 2,000 | 0.010 s | 0.160 s | 1,999,000 | 16× |
| 4,000 | 0.021 s | 0.633 s | 7,998,000 | 30× |
| 8,000 | 0.044 s | 2.70 s | 31,996,000 | 62× |
| **100,000** | **0.80 s (measured)** | **≈ 420–450 s ≈ 7–8 min (estimated: 4,999,950,000 comparisons × measured ≈ 84–90 ns per pair; not run)** | 4,999,950,000 | ≈ 500× |
- **Time:** pairwise **O(n²)** – doubling n multiplies the time by about 4 (0.062 → 0.160 → 0.633 → 2.70 s, comparisons exactly n(n − 1)/2); dictionary **O(n)** average – doubling n doubles the time (0.0079 → 0.0103 → 0.0211 → 0.0438 s).
- **Space:** dictionary O(n) (the key→person map plus the merged people: 4,618 KiB at n = 8,000); pairwise O(n) as well (the key sets and union-find array: 3,208 KiB at n = 8,000) – the difference is time, not memory. The pairwise estimate for 100,000 contacts is a lower bound (the cost per pair rose with n in the table), and it gives the same grouping, so correctness is not the issue – scalability is.
