import re
from collections import defaultdict, deque

x, t = map(int, input().split())
n = int(input())

failed = defaultdict(deque)
suspicious = {}

pattern = re.compile(r"^(\d\d):(\d\d)\s+(\S+)\s+(\S+)\s+(FAIL|SUCCESS)$")

for _ in range(n):
    line = input().strip()
    match = pattern.match(line)

    if not match:
        continue

    hour = int(match.group(1))
    minute = int(match.group(2))
    user = match.group(3)
    ip = match.group(4)
    status = match.group(5)

    current = hour * 60 + minute

    if status == "FAIL":
        failed[user].append((current, ip))
        while failed[user] and current - failed[user][0][0] > t:
            failed[user].popleft()

    else:
        while failed[user] and current - failed[user][0][0] > t:
            failed[user].popleft()

        if len(failed[user]) >= x:
            different = False
            for _, old_ip in failed[user]:
                if old_ip != ip:
                    different = True
                    break

            if different and user not in suspicious:
                suspicious[user] = f"{hour:02d}:{minute:02d}"

for user in sorted(suspicious):
    print(user, suspicious[user])
