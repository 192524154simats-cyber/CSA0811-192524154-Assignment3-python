import random, time
from contacts import *

def show(people):
    for p in sorted(people, key=lambda p: sorted(p["numbers"] | p["emails"])):
        print(f"   {display_name(p):<14} names={sorted(p['names'])} numbers={sorted(p['numbers'])} emails={sorted(p['emails'])}")

print("== Stage 3a: small list merged by hand ==")
phone1 = [{"name": "Dr. Ravi", "numbers": ["+91 98400 12345"], "emails": ["ravi@mail.com"]},
          {"name": "Meena", "numbers": ["98411-22334"]},
          {"name": "Ravi Kumar (office)", "numbers": ["09876543210"]}]
phone2 = [{"name": "ravi kumar", "numbers": ["9840012345", "9876543210"]},     # links Ravi's two numbers
          {"name": "Meena S", "numbers": ["+91-9841122334"], "emails": ["MEENA@mail.com "]},
          {"name": "Arun", "numbers": []},                                       # no number, no e-mail
          {"name": "Arun", "emails": ["arun@mail.com"]}]
sim = [{"name": "Raja", "numbers": ["9000011111"]}, {"name": "Raja", "numbers": ["9000022222"]},  # same name, different people
       {"name": "mr. ravi", "numbers": ["98400 12345"]}]
contacts = phone1 + phone2 + sim
print("10 contacts typed.  By hand: Ravi (4 entries incl. the link) -> ONE person with numbers 9840012345 and 9876543210, e-mail ravi@mail.com;")
print("Meena (2 entries) -> ONE person, 1 number, 2 e-mails merged into 1 ('meena@mail.com'); Arun (no number) -> kept apart as 2 entries;")
print("Raja x2 -> TWO different people (different numbers); expected total = 1 + 1 + 2 + 2 = 6 people")
people = merge(contacts)
show(people)
print("observed people:", len(people), "| expected 6 ->", "OK" if len(people) == 6 else "MISMATCH")

print("\n== Normalisation tests ==")
for raw in ("+91 98400 12345", "9840012345", "09840012345", "98400-12345", "+91-9840012345", "1234", "", "98400 1234a5"):
    print(f"   number {raw!r:<20} -> {normalise_number(raw)}")
for raw in ("Dr. Ravi", "ravi kumar", "  MR.  RAVI   KUMAR ", "o'brien", ""):
    print(f"   name   {raw!r:<24} -> {normalise_name(raw)!r}")
for raw in ("MEENA@mail.com ", "no-at-sign", "@x"):
    print(f"   email  {raw!r:<20} -> {normalise_email(raw)}")

print("\n== Missing fields and duplicates ==")
print("   empty list ->", merge([]))
print("   contact with no keys ->", merge([{"name": "Zed"}]))
print("   exact duplicate twice ->", len(merge([{"name": "A", "numbers": ["9000000001"]}] * 2)), "person")
print("   same name, different numbers ->", len(merge([{"name": "Raja", "numbers": ["9000011111"]}, {"name": "Raja", "numbers": ["9000022222"]}])), "people")
print("   chain: A has n1, B has n1 and n2, C has n2 ->", len(merge([{"numbers": ["9000000001"]}, {"numbers": ["9000000001", "9000000002"]}, {"numbers": ["9000000002"]}])), "person (B links A and C)")

from run_q7_data import formats, make_contacts

print("\n== Stage 3b: time for 1,000 and 100,000 contacts (dictionary design) ==")
print(f"{'contacts':>9} | {'time':>9} {'per contact':>12} | people found | lookups ~ numbers")
for n in (1_000, 10_000, 100_000):
    data = make_contacts(n)
    t0 = time.perf_counter(); res = merge(data); sec = time.perf_counter() - t0
    print(f"{n:>9} | {sec:>8.4f}s {sec / n * 1e6:>9.2f} us | {len(res):>12} | {sum(len(c['numbers']) for c in data):,}")

print("\n== Check: pairwise comparison gives the same grouping (n = 1,000 and 2,000) ==")
for n in (1_000, 2_000):
    data = make_contacts(n, seed=1)
    people = merge(data)
    groups, comps = merge_pairwise(data)
    sig_dict = sorted(tuple(sorted(p["numbers"])) for p in people)
    sig_pair = []
    for idxs in groups.values():
        s = set()
        for i in idxs:
            s |= {normalise_number(x) for x in data[i]["numbers"]}
        sig_pair.append(tuple(sorted(s)))
    print(f"   n = {n}: dictionary {len(people)} people, pairwise {len(groups)} people, same grouping: {sorted(sig_pair) == sig_dict}, pair comparisons = {comps:,} (= n(n-1)/2 = {n * (n - 1) // 2:,})")
