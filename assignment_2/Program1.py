import re

file_path = input("Enter text file path: ").strip()

pattern = r"[A-Za-z0-9+._-]+@[A-Za-z0-9.-]+\.(?:com|edu|org)\b"
data = {}

try:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            emails = re.findall(pattern, line)
            for email in emails:
                email = email.lower()
                domain = email.split("@")[1]
                if domain not in data:
                    data[domain] = set()
                data[domain].add(email)

    for domain in sorted(data):
        emails = sorted(data[domain])
        print(domain, len(emails), emails[0])
except FileNotFoundError:
    print("File not found")
