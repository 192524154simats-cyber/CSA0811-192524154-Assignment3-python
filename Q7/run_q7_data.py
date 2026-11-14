"""Synthetic contact generator for Q7."""
import random

# ---------- data generator ----------
def formats(num, rnd):
    return rnd.choice([num, f"+91 {num[:5]} {num[5:]}", f"0{num}", f"{num[:5]}-{num[5:]}", f"+91-{num}"])

def make_contacts(n, seed=0):
    rnd = random.Random(seed)
    people_count = max(1, int(n / 1.6))
    nums = rnd.sample(range(6_000_000_000, 9_999_999_999), people_count * 2)
    out = []
    first = ["Ravi", "Meena", "Arun", "Raja", "Kavya", "Suresh", "Divya", "Karthik"]
    for i in range(n):
        p = rnd.randrange(people_count)
        mine = [str(nums[2 * p])] + ([str(nums[2 * p + 1])] if rnd.random() < 0.3 else [])
        shown = [formats(x, rnd) for x in mine if rnd.random() < 0.9] or [formats(mine[0], rnd)]
        c = {"name": rnd.choice(["Dr. ", "", "mr ", ""]) + rnd.choice(first) + rnd.choice(["", " Kumar", " S"]), "numbers": shown}
        if rnd.random() < 0.3: c["emails"] = [f"p{p}@mail.com"]
        out.append(c)
    return out

