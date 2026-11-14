"""Q4 - Elective clash detection with sets."""
def analyse(ai, iot, everyone):
    """Returns dictionary of the five set results (set operators)."""
    return {"both (clash)": ai & iot,
            "exactly one": ai ^ iot,
            "only AI": ai - iot,
            "only IoT": iot - ai,
            "either": ai | iot,
            "neither": everyone - (ai | iot)}

def analyse_methods(ai, iot, everyone):
    """Same with set METHODS."""
    return {"both (clash)": ai.intersection(iot),
            "exactly one": ai.symmetric_difference(iot),
            "only AI": ai.difference(iot),
            "only IoT": iot.difference(ai),
            "either": ai.union(iot),
            "neither": everyone.difference(ai.union(iot))}

def report(title, result):
    print(f"{title:14} ({len(result)}): {sorted(result)}")
