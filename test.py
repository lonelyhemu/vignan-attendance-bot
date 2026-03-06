from attendance_selenium import get_attendance

data = get_attendance("23L31A04E1", "17122005")

subjects = []
total_held = 0
total_attended = 0

for row in data:
    if len(row) >= 5 and row[0].isdigit():
        subject = row[1]
        held = int(row[2])
        attend = int(row[3])
        percent = row[4]

        subjects.append((subject, held, attend, percent))

        total_held += held
        total_attended += attend

print("\nSUBJECT WISE ATTENDANCE\n")

for s in subjects:
    print(f"{s[0]} : {s[2]}/{s[1]} ({s[3]}%)")

overall = (total_attended / total_held) * 100

print("\nTOTAL")
print(total_attended, "/", total_held)
print("Percentage:", round(overall,2), "%")

required = 0.75

max_bunk = int((total_attended - required * total_held) / required)

print("\nYou can bunk", max_bunk, "classes and stay above 75%")