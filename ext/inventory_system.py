import csv
from typing import List

from sl import SL_Node
from sl_hashtable import SL_HashTable


class Property:
    def __init__(self, value: int | str):
        self.value = value
        self.links: List[SL_Node] = list()

    def __repr__(self) -> str:
        return f"Property({self.value!r}, {self.links})"

    def __lt__(self, other: int | str) -> bool:
        return self.value < other

    def __le__(self, other: int | str) -> bool:
        return self.value <= other

    def __eq__(self, other: int | str) -> bool:
        return self.value == other

    def __ne__(self, other: int | str) -> bool:
        return self.value != other

    def __ge__(self, other: int | str) -> bool:
        return self.value >= other

    def __gt__(self, other: int | str) -> bool:
        return self.value > other


class PropertyBank:
    def __init__(self):
        self.bank: List[Property] = list()

    def b_search(self, value: int | str, force: bool = False) -> int:
        # Бинарный поиск. С флагом `force` всегда возвращает индекс
        west, east = 0, len(self.bank) - 1
        while west <= east:
            center = (west + east) >> 1
            if self.bank[center] < value:
                west = center + 1
            elif self.bank[center] > value:
                east = center - 1
            else:
                return center
        return west if force else -1

    def get(self, value: int | str) -> List[SL_Node] | None:
        if (index := self.b_search(value)) != -1:
            return self.bank[index].links
        return None

    def put(self, value: int | str, link: SL_Node) -> Property:
        # Возвращаем Property, чтобы можно было установить двойную связь
        index = self.b_search(value, force=True)

        if self.bank[index] != value:
            self.bank.insert(index, Property(value))
        self.bank[index].links.append(link)

        return self.bank[index]

    def delete(self, value: int | str):
        if (index := self.b_search(value)) != -1:
            self.bank.pop(index)
        raise ValueError(f"property {value!r} not in bank")


class InventorySystem:
    def __init__(self, size=100):
        self.table = SL_HashTable(size)

    def load_from_csv(self, filename):
        with open(filename, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = int(row["Id"])
                data = {
                    "Name": row["Name"],
                    "Category": row["Category"],
                    "Quantity": int(row["Quantity"]),
                    "Price": float(row["Price"]),
                    "Min_Allowed_Quantity": int(row["Min_Allowed_Quantity"]),
                }
                self.table.put(key, data)

    def save_to_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            fieldnames = [
                "Id",
                "Name",
                "Category",
                "Quantity",
                "Price",
                "Min_Allowed_Quantity",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(self.table.size):
                current = self.table.table[i].head
                while current:
                    key, data = current.value
                    writer.writerow(
                        {
                            "Id": key,
                            "Name": data["Name"],
                            "Category": data["Category"],
                            "Quantity": data["Quantity"],
                            "Price": data["Price"],
                            "Min_Allowed_Quantity": data["Min_Allowed_Quantity"],
                        }
                    )
                    current = current.next

    def add_product(self, id, name, category, quantity, price, min_quantity):
        data = {
            "Name": name,
            "Category": category,
            "Quantity": quantity,
            "Price": price,
            "Min_Allowed_Quantity": min_quantity,
        }
        self.table.put(id, data)

    def delete_product(self, id):
        return self.table.delkey(id)

    def update_quantity(self, id, new_quantity):
        node = self.table.get(id)
        if node:
            node.value[1]["Quantity"] = new_quantity
            return True
        return False

    def find_by_name(self, name):
        results = []
        for bucket in self.table.table:
            current = bucket.head
            while current:
                if name.lower() in current.value[1]["Name"].lower():
                    results.append(current.value)
                current = current.next
        return results

    def find_by_category(self, category):
        results = []
        for bucket in self.table.table:
            current = bucket.head
            while current:
                if category.lower() == current.value[1]["Category"].lower():
                    results.append(current.value)
                current = current.next
        return results

    def find_by_price_range(self, min_price, max_price):
        results = []
        for bucket in self.table.table:
            current = bucket.head
            while current:
                price = current.value[1]["Price"]
                if min_price <= price <= max_price:
                    results.append(current.value)
                current = current.next
        return results

    def generate_stock_report(self):
        print("Товары ниже минимального запаса:")
        for bucket in self.table.table:
            current = bucket.head
            while current:
                product = current.value[1]
                if product["Quantity"] < product["Min_Allowed_Quantity"]:
                    print(
                        f'{product["Name"]} (Остаток: {product["Quantity"]}, Минимум: {product["Min_Allowed_Quantity"]})'
                    )
                current = current.next
