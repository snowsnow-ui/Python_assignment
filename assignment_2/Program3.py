import csv

try:
    import mysql.connector
except ImportError:
    print("Install mysql-connector-python first")
    raise SystemExit

host = input("Host: ").strip()
user = input("User: ").strip()
password = input("Password: ").strip()
database = input("Database name: ").strip()

student_file = input("Student CSV path: ").strip()
registration_file = input("Registration CSV path: ").strip()
course_id = input("Course ID: ").strip()
threshold = float(input("SPI threshold: "))

try:
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Student(
        student_id VARCHAR(30) PRIMARY KEY,
        name VARCHAR(100),
        spi FLOAT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS CourseRegistration(
        student_id VARCHAR(30),
        course_id VARCHAR(30),
        FOREIGN KEY(student_id) REFERENCES Student(student_id)
    )
    """)

    with open(student_file, newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        for row in rows:
            cur.execute(
                "INSERT IGNORE INTO Student(student_id,name,spi) VALUES(%s,%s,%s)",
                (row["student_id"], row["name"], float(row["spi"]))
            )

    with open(registration_file, newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        for row in rows:
            cur.execute(
                "INSERT INTO CourseRegistration(student_id,course_id) VALUES(%s,%s)",
                (row["student_id"], row["course_id"])
            )

    db.commit()

    query = """
    SELECT s.student_id, s.name, s.spi, r.course_id
    FROM Student s
    JOIN CourseRegistration r ON s.student_id = r.student_id
    WHERE r.course_id = %s AND s.spi > %s
    ORDER BY s.spi DESC, s.student_id ASC
    """

    cur.execute(query, (course_id, threshold))

    for row in cur.fetchall():
        print(row[0], row[1], row[2], row[3])

    cur.close()
    db.close()

except Exception as e:
    print("Database error:", e)
