"""Q3 - Kisan call centre: word counts with dict, grouping, top-k, stop words."""
import random, string

STOP_DEFAULT = {"the", "a", "is", "and", "not", "to", "of", "in", "my", "for", "has", "have", "are", "no", "very", "high"}

def tokenize(text):
    """Lower-case, remove punctuation, split into words. Empty text -> []."""
    return text.lower().translate(str.maketrans("", "", string.punctuation)).split()

def frequencies(texts, stop):
    """Dictionary word -> count for every word not in stop, using dict.get()."""
    counts = {}
    for text in texts:
        for word in tokenize(text):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts

def frequencies_setdefault(texts, stop):
    """Same result with setdefault (counts stored in a one-item list, to show the other idiom)."""
    box = {}
    for text in texts:
        for word in tokenize(text):
            if word not in stop:
                box.setdefault(word, [0])[0] += 1
    return {w: c[0] for w, c in box.items()}

def top(counts, k):
    """k most frequent (word, count) pairs: highest count first, alphabetical for ties."""
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]

def group_by(records, key_index):
    """records: list of (district, crop, text). Dictionary key -> list of complaint texts (setdefault)."""
    groups = {}
    for rec in records:
        groups.setdefault(rec[key_index], []).append(rec[2])
    return groups

# ---------- data generation ----------
VOCAB = ["seeds", "fertiliser", "price", "subsidy", "received", "delayed", "water", "pump", "loan", "insurance", "rain",
         "pest", "disease", "leaf", "yellow", "market", "payment", "credit", "tractor", "electricity", "canal", "soil", "test",
         "report", "officer", "visit", "scheme", "registration", "mobile", "app", "error", "bank", "account", "link", "aadhaar",
         "harvest", "storage", "godown", "transport", "rate"]
VOCAB += [f"item{i}" for i in range(80)]          # long tail: about 120 distinct words in all
DISTRICTS = ["Salem", "Erode", "Madurai", "Theni", "Thanjavur", "Cuddalore", "Vellore", "Tiruppur"]
CROPS = ["paddy", "cotton", "sugarcane", "banana", "groundnut", "turmeric"]

def make_complaints(n, seed=7):
    rnd = random.Random(seed)
    recs = []
    for _ in range(n):
        words = [rnd.choice(VOCAB[:40]) if rnd.random() < 0.7 else rnd.choice(VOCAB) for _ in range(rnd.randint(3, 9))]
        words += [rnd.choice(["not", "the", "is", "very", "high"]) for _ in range(rnd.randint(0, 2))]
        text = " ".join(words).capitalize() + rnd.choice([".", "!", ""])
        recs.append((rnd.choice(DISTRICTS), rnd.choice(CROPS), text))
    return recs
