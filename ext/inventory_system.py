import csv
from typing import List

from sl import SL_Node
from sl_hashtable import SL_HashTable


class Property:
    def __init__(self, value):
        self.value = value
        self.links: List[SL_Node] = list()

    def __repr__(self) -> str:
        return f"Property({self.value!r}, {self.links})"

    def __lt__(self, other) -> bool:
        return self.value < other

    def __gt__(self, other) -> bool:
        return self.value > other


class PropertyBank:
    def __init__(self):
        self.bank: List[Property] = list()

    def _search(self, value, force: bool = False) -> int:
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

    def get(self, value) -> List[SL_Node]:
        if (index := self._search(value)) != -1:
            return self.bank[index].links
        return list()

    def get_by_slice(self, _from, _to) -> List[SL_Node]:
        index_from = self._search(_from, force=True)
        index_to = self._search(_to, force=True)

        products = list()
        for i in range(index_from, index_to + 1):
            links = [
                l
                for l in self.bank[i].links
                if l not in products and _from <= l.price <= _to
            ]
            products.extend(links)
        return products

    def put(self, value, link: SL_Node) -> Property:
        # Возвращаем Property, чтобы можно было установить двойную связь
        index = self._search(value, force=True)

        if index >= len(self.bank) or self.bank[index] != value:
            self.bank.insert(index, Property(value))
        self.bank[index].links.append(link)

        return self.bank[index]

    def delete(self, value, link: SL_Node):
        if (index := self._search(value)) == -1:
            raise ValueError(f"property {value!r} not in bank")

        self.bank[index].links.remove(link)
        if len(self.bank[index].links) == 0:
            self.bank.pop(index)


class Product:
    __slots__ = "name", "category", "quantity", "price", "min_quantity"

    def __repr__(self) -> str:
        return "Product(%s)" % ", ".join(
            str(getattr(self, attr).value) for attr in self.__slots__
        )


class InventorySystem:
    FIELDS = "Id", "Name", "Category", "Quantity", "Price", "Min_Allowed_Quantity"

    def __init__(self, size=100):
        self.name_bank = PropertyBank()
        self.category_bank = PropertyBank()
        self.quantity_bank = PropertyBank()
        self.price_bank = PropertyBank()
        self.min_quantity_bank = PropertyBank()

        self.table = SL_HashTable(size)

    def load_from_csv(self, filename):
        with open(filename, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                _id, *props = [row[f] for f in self.FIELDS]
                self.add_product(_id, *props)

    def save_to_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            for i in range(self.table.size):
                current = self.table.table[i].head
                while current:
                    _id, product = current.value
                    props = [getattr(product, p).value for p in product.__slots__]
                    writer.writerow(dict(zip(self.FIELDS, [_id] + props)))
                    current = current.next

    def add_product(self, _id, name, category, quantity, price, min_quantity):
        # todo что если пользователь выставит отрицательные цену или кол-во?
        product = Product()
        product.name = self.name_bank.put(str(name), product)
        product.category = self.category_bank.put(str(category), product)
        product.quantity = self.quantity_bank.put(int(quantity), product)
        product.price = self.price_bank.put(float(price), product)
        product.min_quantity = self.min_quantity_bank.put(int(min_quantity), product)

        self.table.put(int(_id), product)

    def delete_product(self, _id):
        product = self.table.get(_id)
        if product is None:
            return None

        self.name_bank.delete(product.name, product)
        self.category_bank.delete(product.category, product)
        self.quantity_bank.delete(product.quantity, product)
        self.price_bank.delete(product.price, product)
        self.min_quantity_bank.delete(product.min_quantity, product)

        return self.table.delkey(_id)

    def update_quantity(self, _id, new_quantity):
        if new_quantity < 0:
            raise ValueError("quantity can't be negative")

        node = self.table.get(_id)
        if node is None:
            return False
        product = node.value[1]

        self.quantity_bank.delete(product.quantity, product)
        product.quantity = self.quantity_bank.put(new_quantity, product)
        return True

    def find_by_name(self, name):
        return self.name_bank.get(name)

    def find_by_category(self, category):
        return self.category_bank.get(category)

    def find_by_price_range(self, min_price, max_price):
        return self.price_bank.get_by_slice(min_price, max_price)

    def generate_stock_report(self):
        print("Товары ниже минимального запаса:")
        for bucket in self.table.table:
            current = bucket.head
            while current:
                product = current.value[1]
                if product.quantity < product.min_quantity:
                    print(
                        f"{product.name.value} (Остаток: {product.quantity.value}, Минимум: {product.min_quantity.value})"
                    )
                current = current.next
