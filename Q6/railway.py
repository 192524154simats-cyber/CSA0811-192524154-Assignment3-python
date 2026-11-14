"""Q6 - Railway timetable as nested data.
timetable = { train_no: {"name": str, "stops": [(station, arrival, departure), ...], "days": {"Mon", ...}} }
Times are 'HH:MM' strings (24 h) so they sort correctly as text."""
import random

ALL_DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

SAMPLE = {
    12601: {"name": "Chennai Mail", "stops": [("Chennai", "--", "20:00"), ("Arakkonam", "21:10", "21:12"), ("Katpadi", "22:05", "22:10"), ("Salem", "00:30", "00:35"), ("Coimbatore", "03:00", "--")],
            "days": {"Mon", "Wed", "Fri"}},
    12635: {"name": "Vaigai Express", "stops": [("Chennai", "--", "06:40"), ("Villupuram", "09:00", "09:02"), ("Trichy", "11:15", "11:20"), ("Madurai", "13:35", "--")],
            "days": set(ALL_DAYS)},
    16721: {"name": "Cheran Express", "stops": [("Chennai", "--", "22:10"), ("Katpadi", "00:15", "00:20"), ("Salem", "02:50", "02:55"), ("Erode", "03:50", "03:55"), ("Coimbatore", "06:10", "--")],
            "days": {"Tue", "Thu", "Sat", "Sun"}},
    12007: {"name": "Shatabdi", "stops": [("Chennai", "--", "06:00"), ("Katpadi", "07:35", "07:37"), ("Bengaluru", "11:00", "--")],
            "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat"}},
    22651: {"name": "Salem Intercity", "stops": [("Coimbatore", "--", "07:15"), ("Erode", "08:30", "08:35"), ("Salem", "09:25", "09:30"), ("Katpadi", "11:50", "11:55")],
            "days": {"Sat", "Sun"}},
}

def stops_at(timetable, station, day):
    """Trains that stop at `station` and run on `day`, sorted by departure time from the station.
    Scans EVERY train and EVERY stop (no index). Returns list of (train_no, name, arrival, departure)."""
    found = []
    for no, info in timetable.items():
        if day not in info["days"]:
            continue
        for st, arr, dep in info["stops"]:
            if st == station:
                found.append((no, info["name"], arr, dep))
                break
    return sorted(found, key=lambda t: t[3] if t[3] != "--" else "99:99")

def build_index(timetable):
    """station -> list of train numbers that stop there."""
    index = {}
    for no, info in timetable.items():
        for st, _, _ in info["stops"]:
            index.setdefault(st, []).append(no)
    return index

def stops_at_indexed(timetable, index, station, day):
    """Same answer using the index: only the trains that stop at the station are examined."""
    found = []
    for no in index.get(station, []):
        info = timetable[no]
        if day not in info["days"]:
            continue
        for st, arr, dep in info["stops"]:                 # short scan of this train's ~10 stops
            if st == station:
                found.append((no, info["name"], arr, dep))
                break
    return sorted(found, key=lambda t: t[3] if t[3] != "--" else "99:99")

def print_timetable(timetable, only=None):
    print(f"{'Train':<6} {'Name':<16} {'Days':<28} Stops (station arr/dep)")
    for no in sorted(timetable):
        if only and no not in only: continue
        info = timetable[no]
        days = ",".join(d for d in ALL_DAYS if d in info["days"])
        stops = " > ".join(f"{s} {a}/{d}" for s, a, d in info["stops"])
        print(f"{no:<6} {info['name']:<16} {days:<28} {stops}")

def generate(n_trains, n_stations=300, seed=9):
    """Random timetable: each train has 8-14 stops from n_stations stations, runs on 3-7 days."""
    rnd = random.Random(seed)
    stations = [f"Station{i:03d}" for i in range(n_stations)]
    tt = {}
    for i in range(n_trains):
        k = rnd.randint(8, 14)
        route = rnd.sample(stations, k)
        minute = rnd.randint(0, 1439)
        stops = []
        for j, st in enumerate(route):
            arr = "--" if j == 0 else f"{(minute % 1440) // 60:02d}:{minute % 60:02d}"
            minute += rnd.randint(1, 3)
            dep = "--" if j == k - 1 else f"{(minute % 1440) // 60:02d}:{minute % 60:02d}"
            minute += rnd.randint(30, 90)
            stops.append((st, arr, dep))
        tt[10000 + i] = {"name": f"Train {10000 + i}", "stops": stops, "days": set(rnd.sample(ALL_DAYS, rnd.randint(3, 7)))}
    return tt
