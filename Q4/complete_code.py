ai_elective = {"192311001", "192311004", "192311007", "192311009"}
iot_elective = {"192311002", "192311004", "192311009", "192311010"}
all_students = {f"1923110{i:02d}" for i in range(1, 11)}

# TODO 1 (done): set OPERATORS only
both = ai_elective & iot_elective                        # intersection
exactly_one = ai_elective ^ iot_elective                 # symmetric difference
neither = all_students - (ai_elective | iot_elective)    # difference of the union

print("clash:", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither:", sorted(neither))

# ---- Same with set METHODS ----
both_m = ai_elective.intersection(iot_elective)
exactly_one_m = ai_elective.symmetric_difference(iot_elective)
neither_m = all_students.difference(ai_elective.union(iot_elective))
print("\nmethods give the same results:", both == both_m, exactly_one == exactly_one_m, neither == neither_m)
