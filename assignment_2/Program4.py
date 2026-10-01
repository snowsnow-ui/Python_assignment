import re

allowed_columns = {
    "student.id",
    "student.name",
    "student.spi",
    "course.id",
    "course.name",
    "registration.course_id"
}

columns = input("Columns separated by comma: ").split(",")
columns = [x.strip() for x in columns]

where_text = input("Where condition, example course.id=PY101: ").strip()
order_column = input("Order column: ").strip()
direction = input("Sort direction ASC/DESC: ").strip().upper()
limit = int(input("Limit: "))

if not 1 <= limit <= 1000:
    print("INVALID LIMIT")
    raise SystemExit

if not columns or any(x not in allowed_columns for x in columns):
    print("INVALID COLUMN")
    raise SystemExit

if order_column not in allowed_columns:
    print("INVALID ORDER COLUMN")
    raise SystemExit

if direction not in ["ASC", "DESC"]:
    print("INVALID SORT DIRECTION")
    raise SystemExit

match = re.fullmatch(r"([A-Za-z]+\.[A-Za-z_]+)\s*(=|>|<|>=|<=|LIKE)\s*(.+)", where_text)

if not match:
    print("INVALID WHERE")
    raise SystemExit

where_column = match.group(1)
operator = match.group(2)
value = match.group(3).strip()

if where_column not in allowed_columns:
    print("INVALID WHERE COLUMN")
    raise SystemExit

if value.startswith("'") and value.endswith("'"):
    value = value[1:-1]

if value == "":
    print("INVALID VALUE")
    raise SystemExit

sql = """
SELECT {columns}
FROM Student student
JOIN CourseRegistration registration ON student.id = registration.student_id
JOIN Course course ON registration.course_id = course.id
WHERE {where_column} {operator} %s
ORDER BY {order_column} {direction}
LIMIT %s
""".format(
    columns=", ".join(columns),
    where_column=where_column,
    operator=operator,
    order_column=order_column,
    direction=direction
)

print("SQL_OK")
print(sql.strip())
print("Parameters:", [value, limit])
