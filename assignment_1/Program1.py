def main():
    try:
        n, k, m = map(int, input().split())
        students = []
        semesters = {}
        subjects = [[] for _ in range(m)]

        for _ in range(n):
            data = input().split()
            enrollment = data[0]
            name = data[1]
            semester = int(data[2])
            cpi = float(data[3])
            marks = list(map(int, data[4:]))

            student = (enrollment, name, semester, cpi, tuple(marks))
            students.append(student)

            if semester not in semesters:
                semesters[semester] = []
            semesters[semester].append(student)

            for i in range(m):
                subjects[i].append((marks[i], enrollment))

        for semester in sorted(semesters):
            group = semesters[semester]
            group.sort(key=lambda x: (-x[3], -sum(x[4]) / m, x[0]))
            result = [student[0] for student in group[:k]]
            print(f"Semester {semester}:", *result)

        for i in range(m):
            highest = max(mark for mark, enrollment in subjects[i])
            toppers = []
            for mark, enrollment in subjects[i]:
                if mark == highest:
                    toppers.append(enrollment)
            toppers.sort()
            print(f"S{i + 1}:", *toppers)

    except (ValueError, IndexError):
        print("INVALID INPUT")


if __name__ == "__main__":
    main()
