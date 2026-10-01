import os
import pickle
import re
import zipfile


def make_index(folder):
    index = {}
    files_count = 0
    lines_count = 0
    log_files = []

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith((".txt", ".log")):
            continue

        path = os.path.join(folder, filename)
        if not os.path.isfile(path):
            continue

        log_files.append(path)
        files_count += 1

        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            for line_number, line in enumerate(file, 1):
                lines_count += 1
                words = re.findall(r"[A-Za-z0-9_]+", line.lower())

                for word in set(words):
                    if word not in index:
                        index[word] = []
                    index[word].append((filename, line_number))

    return index, files_count, lines_count, log_files


def build(folder, archive_name):
    index, files_count, lines_count, log_files = make_index(folder)
    pickle_path = os.path.join(folder, "index.pkl")

    with open(pickle_path, "wb") as file:
        pickle.dump(index, file)

    with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in log_files:
            archive.write(path, os.path.basename(path))
        archive.write(pickle_path, "index.pkl")

    print("FILES", files_count)
    print("LINES", lines_count)
    print("TOKENS", len(index))


def search(pickle_path, queries):
    with open(pickle_path, "rb") as file:
        index = pickle.load(file)

    for word in queries:
        print(word + ":")
        matches = index.get(word.lower(), [])
        for filename, line_number in matches:
            print(filename + ":" + str(line_number))


def main():
    try:
        data = input().split()
        mode = data[0].upper()

        if mode == "BUILD":
            folder = data[1]
            archive = data[2]
            build(folder, archive)

        elif mode == "SEARCH":
            pickle_path = data[1]
            q = int(data[2])
            queries = data[3:3 + q]
            search(pickle_path, queries)

        else:
            print("INVALID INPUT")

    except (IndexError, ValueError, OSError, pickle.PickleError):
        print("INVALID INPUT")


if __name__ == "__main__":
    main()
