import csv
import os
import matplotlib.pyplot as plt

input_file = input("Enter marks CSV path: ").strip()
output_folder = input("Enter output folder: ").strip()

os.makedirs(output_folder, exist_ok=True)

try:
    with open(input_file, "r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("No data")
        raise SystemExit

    fields = list(rows[0].keys())
    subjects = fields[2:]

    for row in rows:
        for subject in subjects:
            value = row[subject].strip()
            if value == "":
                row[subject] = "0"
            else:
                mark = float(value)
                if mark < 0 or mark > 100:
                    row[subject] = "0"

    cleaned_file = os.path.join(output_folder, "cleaned_marks.csv")
    summary_file = os.path.join(output_folder, "summary.csv")

    with open(cleaned_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    averages = []
    for subject in subjects:
        total = 0
        for row in rows:
            total += float(row[subject])
        averages.append(total / len(rows))

    with open(summary_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Subject", "Average"])
        for subject, average in zip(subjects, averages):
            writer.writerow([subject, f"{average:.2f}"])

    grade_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for row in rows:
        total = 0
        for subject in subjects:
            total += float(row[subject])
        average = total / len(subjects)

        if average >= 80:
            grade_count["A"] += 1
        elif average >= 70:
            grade_count["B"] += 1
        elif average >= 60:
            grade_count["C"] += 1
        elif average >= 50:
            grade_count["D"] += 1
        else:
            grade_count["F"] += 1

    plt.figure()
    plt.bar(grade_count.keys(), grade_count.values())
    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Students")
    plt.savefig(os.path.join(output_folder, "grade_distribution.png"))
    plt.close()

    plt.figure()
    plt.bar(subjects, averages)
    plt.title("Subject Average")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.savefig(os.path.join(output_folder, "subject_average.png"))
    plt.close()

    student_scores = []
    for row in rows:
        total = 0
        for subject in subjects:
            total += float(row[subject])
        student_scores.append((row["name"], total / len(subjects)))

    student_scores.sort(key=lambda x: x[1], reverse=True)
    top = student_scores[:5]

    names = [x[0] for x in top]
    scores = [x[1] for x in top]

    plt.figure()
    plt.bar(names, scores)
    plt.title("Top Performers")
    plt.xlabel("Student")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=30)
    plt.savefig(os.path.join(output_folder, "top_performers.png"))
    plt.close()

    print("cleaned_marks.csv")
    print("summary.csv")
    print("grade_distribution.png")
    print("subject_average.png")
    print("top_performers.png")

except FileNotFoundError:
    print("File not found")
