MOD = 1000000007

n, m = map(int, input().split())
matrix = []

for _ in range(n):
    matrix.append(input().split())

score = [[None] * m for _ in range(n)]
ways = [[0] * m for _ in range(n)]

if matrix[0][0] != "X":
    score[0][0] = int(matrix[0][0])
    ways[0][0] = 1

for i in range(n):
    for j in range(m):
        if matrix[i][j] == "X":
            continue

        if i == 0 and j == 0:
            continue

        value = int(matrix[i][j])
        best = None
        count = 0

        previous = []

        if i > 0:
            previous.append((score[i - 1][j], ways[i - 1][j]))

        if j > 0:
            previous.append((score[i][j - 1], ways[i][j - 1]))

        if i > 0 and j > 0:
            previous.append((score[i - 1][j - 1], ways[i - 1][j - 1]))

        for old_score, old_count in previous:
            if old_score is None or old_count == 0:
                continue

            if best is None or old_score > best:
                best = old_score
                count = old_count
            elif old_score == best:
                count = (count + old_count) % MOD

        if best is not None:
            score[i][j] = best + value
            ways[i][j] = count

if score[n - 1][m - 1] is None:
    print("IMPOSSIBLE")
else:
    print(score[n - 1][m - 1], ways[n - 1][m - 1])
