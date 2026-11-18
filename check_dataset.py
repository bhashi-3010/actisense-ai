
from pathlib import Path
from collections import Counter

data_folder = Path(__file__).parent / "data"

print("\n========== COMPLETE mHealth DATASET ==========\n")

total_records = 0
total_missing = 0
combined_activities = Counter()

for subject in range(1, 11):

    file_path = data_folder / f"mHealth_subject{subject}.log"

    if not file_path.exists():
        print(f"Subject {subject}: FILE NOT FOUND")
        continue

    records = 0
    activity_counts = Counter()
    missing = 0
    column_counts = Counter()

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            values = line.split()

            if not values:
                continue

            records += 1
            column_counts[len(values)] += 1

            missing += sum(
                1 for value in values
                if value.lower() in ["nan", "null", "none"]
            )

            activity_counts[values[-1]] += 1

    total_records += records
    total_missing += missing
    combined_activities.update(activity_counts)

    print(f"SUBJECT {subject}")
    print("Records:", records)
    print("Columns:", dict(column_counts))
    print("Missing values:", missing)
    print("Activity classes:", len(activity_counts))
    print("-" * 40)

print("\n========== FINAL DATASET SUMMARY ==========")

print("Total subjects: 10")
print("Total records:", total_records)
print("Total missing values:", total_missing)

print("\nCOMBINED ACTIVITY DISTRIBUTION")

for activity, count in sorted(
    combined_activities.items(),
    key=lambda x: float(x[0])
):
    print(f"Activity {activity}: {count}")

print("\n========== COMPLETED ==========")
