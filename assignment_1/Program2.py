import re


def is_banned(password, banned_words):
    password = password.lower()
    for word in banned_words:
        if word.lower() in password:
            return True
    return False


def check_password(password, banned_words):
    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    if is_banned(password, banned_words):
        return "COMPROMISED"

    if not re.search(r"[a-z]", password):
        return "WEAK_PATTERN"
    if not re.search(r"[A-Z]", password):
        return "WEAK_PATTERN"
    if not re.search(r"[0-9]", password):
        return "WEAK_PATTERN"
    if not re.search(r"[$#@]", password):
        return "WEAK_PATTERN"
    if re.search(r"(.)\1{3,}", password):
        return "WEAK_PATTERN"

    return "STRONG"


def main():
    try:
        b = int(input())
        banned_words = []

        for _ in range(b):
            banned_words.append(input().strip())

        n = int(input())

        for i in range(1, n + 1):
            password = input().rstrip("\n")
            result = check_password(password, banned_words)
            print(f"{i}: {result}")

    except (ValueError, EOFError):
        print("INVALID INPUT")


if __name__ == "__main__":
    main()
