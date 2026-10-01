import re

first = input("Enter number of HTML files and K: ").split()
p = int(first[0])
k = int(first[1])

files = []
for i in range(p):
    files.append(input().strip())

products = {}

pattern = re.compile(
    r'<div[^>]*class=["\']product["\'][^>]*>.*?'
    r'<[^>]*class=["\']name["\'][^>]*>(.*?)</[^>]+>.*?'
    r'<[^>]*class=["\']price["\'][^>]*>(.*?)</[^>]+>.*?'
    r'<[^>]*class=["\']rating["\'][^>]*>(.*?)</[^>]+>.*?</div>',
    re.I | re.S
)

try:
    for path in files:
        with open(path, "r", encoding="utf-8") as file:
            html = file.read()

        for name, price, rating in pattern.findall(html):
            name = re.sub(r"<.*?>", "", name).strip()
            price = re.sub(r"[^0-9.]", "", price)
            rating = re.sub(r"[^0-9.]", "", rating)

            if not price or not rating:
                continue

            price = float(price)
            rating = float(rating)

            if name not in products or rating > products[name][1] or (
                rating == products[name][1] and price < products[name][0]
            ):
                products[name] = (price, rating)

    result = list(products.items())
    result.sort(key=lambda x: (-x[1][1], x[1][0], x[0]))

    for name, value in result[:k]:
        price, rating = value
        print(name, int(price) if price.is_integer() else price, rating)
except FileNotFoundError:
    print("HTML file not found")
