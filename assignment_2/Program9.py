class Product:
    def __init__(self, pid, name, stock, purchase, selling):
        self.pid = pid
        self.name = name
        self.stock = stock
        self.purchase = purchase
        self.selling = selling

class Inventory:
    def __init__(self):
        self.products = {}

    def add(self, product):
        self.products[product.pid] = product

    def delete(self, pid):
        if pid in self.products:
            del self.products[pid]
            return True
        return False

    def update(self, pid, stock):
        if pid in self.products:
            self.products[pid].stock = stock
            return True
        return False

    def total_value(self):
        total = 0
        for product in self.products.values():
            total += product.stock * product.purchase
        return total

    def __lt__(self, other):
        return self.total_value() < other.total_value()

    def __add__(self, other):
        result = Inventory()

        for pid, product in self.products.items():
            result.add(Product(
                pid,
                product.name,
                product.stock,
                product.purchase,
                product.selling
            ))

        for pid, product in other.products.items():
            if pid not in result.products:
                result.add(Product(
                    pid,
                    product.name,
                    product.stock,
                    product.purchase,
                    product.selling
                ))
            else:
                old = result.products[pid]
                old.stock += product.stock
                old.purchase = min(old.purchase, product.purchase)
                old.selling = max(old.selling, product.selling)

        return result

def read_inventory():
    inventory = Inventory()
    n = int(input())
    for _ in range(n):
        pid, name, stock, purchase, selling = input().split()
        inventory.add(Product(
            pid,
            name,
            int(stock),
            float(purchase),
            float(selling)
        ))
    return inventory

print("Enter Inventory A")
a = read_inventory()

print("Enter Inventory B")
b = read_inventory()

operation = input("Operation: ").strip().upper()

if operation == "MERGE":
    result = a + b
    for pid in sorted(result.products):
        p = result.products[pid]
        print(
            p.pid,
            p.name,
            "stock=" + str(p.stock),
            "purchase=" + str(int(p.purchase) if p.purchase.is_integer() else p.purchase),
            "selling=" + str(int(p.selling) if p.selling.is_integer() else p.selling)
        )
    print("TOTAL", result.total_value())

elif operation == "COMPARE":
    if a < b:
        print("Inventory A has lower value")
    elif b < a:
        print("Inventory B has lower value")
    else:
        print("Both inventories have equal value")
else:
    print("Invalid operation")
