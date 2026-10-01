import json

def read_records(path):
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                data = json.loads(line)

                if "device_id" not in data:
                    continue
                if "temperature_c" not in data:
                    continue
                if "humidity" not in data:
                    continue

                temperature = float(data["temperature_c"])
                humidity = float(data["humidity"])

                yield data["device_id"], temperature, humidity
            except:
                yield None, None, None

path = input("Enter JSONL file path: ").strip()

stats = {}
corrupted = {}

try:
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                data = json.loads(line)

                if "device_id" not in data or "temperature_c" not in data or "humidity" not in data:
                    raise ValueError

                device = data["device_id"]
                temperature = float(data["temperature_c"])
                float(data["humidity"])

                if device not in stats:
                    stats[device] = [0, temperature, temperature, 0]

                stats[device][0] += 1
                stats[device][1] = min(stats[device][1], temperature)
                stats[device][2] = max(stats[device][2], temperature)
                stats[device][3] += temperature

            except:
                device = "UNKNOWN"
                corrupted[device] = corrupted.get(device, 0) + 1

    for device in sorted(stats):
        count, minimum, maximum, total = stats[device]
        bad = corrupted.get(device, 0)
        average = total / count
        print(
            device,
            "count=" + str(count),
            "min=" + str(minimum),
            "max=" + str(maximum),
            "avg=" + f"{average:.2f}",
            "corrupted=" + str(bad)
        )

except FileNotFoundError:
    print("File not found")
