import csv
from typing import List


class Property:
    def __init__(self, value):
        self.value = value
        self.links: List[Product] = list()

    def __repr__(self) -> str:
        return f"Property({self.value!r})"

    def __lt__(self, other) -> bool:
        return self.value < other

    def __gt__(self, other) -> bool:
        return self.value > other


class Product:
    PROTO = {
        "id": {
            "type": int,
            "width": 4,
        },
        "name": {
            "type": str,
            "width": 32,
        },
        "category": {
            "type": str,
            "width": 32,
        },
        "quantity": {
            "type": int,
            "width": 4,
        },
        "price": {
            "type": int,
            "width": 4,
        },
        "min_quantity": {
            "type": int,
            "width": 4,
        },
    }
    __slots__ = tuple(PROTO.keys())

    def __repr__(self) -> str:
        return "Product(%s)" % ", ".join(
            str(getattr(self, attr).value) for attr in self.__slots__
        )


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

    def get(self, value) -> List[Product]:
        if (index := self._search(value)) != -1:
            return self.bank[index].links
        return list()

    def get_by_slice(self, _from, _to) -> List[Product]:
        index_from = self._search(_from, force=True)
        index_to = self._search(_to, force=True)

        products = list()
        for i in range(index_from, index_to + 1):
            for link in self.bank[i].links:
                if link in products:
                    continue
                if link.price < _from or link.price > _to:
                    continue
                products.append(link)
        return products

    def put(self, value, link: Product) -> Property:
        # Возвращаем Property, чтобы можно было установить двойную связь
        index = self._search(value, force=True)

        if index >= len(self.bank) or self.bank[index] != value:
            self.bank.insert(index, Property(value))
        self.bank[index].links.append(link)

        return self.bank[index]

    def delete(self, value, link: Product):
        if (index := self._search(value)) == -1:
            raise ValueError(f"property {value!r} not in bank")

        self.bank[index].links.remove(link)
        if len(self.bank[index].links) == 0:
            self.bank.pop(index)


class Product:
    PROTO = {
        "id": {
            "type": int,
            "width": 4,
        },
        "name": {
            "type": str,
            "width": 32,
        },
        "category": {
            "type": str,
            "width": 32,
        },
        "quantity": {
            "type": int,
            "width": 4,
        },
        "price": {
            "type": int,
            "width": 4,
        },
        "min_quantity": {
            "type": int,
            "width": 4,
        },
    }
    __slots__ = tuple(PROTO.keys())

    def __repr__(self) -> str:
        return "Product(%s)" % ", ".join(
            str(getattr(self, attr).value) for attr in self.__slots__
        )


class InventorySystem:
    def __init__(self):
        self.id_bank = PropertyBank()
        self.name_bank = PropertyBank()
        self.category_bank = PropertyBank()
        self.quantity_bank = PropertyBank()
        self.price_bank = PropertyBank()
        self.min_quantity_bank = PropertyBank()

    def load_from_csv(self, filename):
        with open(filename, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                props = [
                    meta["type"](row[attr]) for attr, meta in Product.PROTO.items()
                ]
                self.add_product(*props)

    def save_to_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=Product.__slots__)
            writer.writeheader()
            for prop in self.id_bank.bank:
                prop = prop.links[0]
                slots = {s: getattr(prop, s).value for s in Product.__slots__}
                writer.writerow(slots)

    def add_product(self, _id, name, category, quantity, price, min_quantity):
        if quantity < 0 or price < 0 or min_quantity < 0:
            raise ValueError("integer properties can't be negative")

        product = Product()
        product.id = self.id_bank.put(_id, product)
        product.name = self.name_bank.put(name, product)
        product.category = self.category_bank.put(category, product)
        product.quantity = self.quantity_bank.put(quantity, product)
        product.price = self.price_bank.put(price, product)
        product.min_quantity = self.min_quantity_bank.put(min_quantity, product)

    def delete_product(self, _id) -> bool:
        product = self.id_bank.get(_id)
        if product is None:
            return False
        product = product[0]

        self.id_bank.delete(_id, product)
        self.name_bank.delete(product.name, product)
        self.category_bank.delete(product.category, product)
        self.quantity_bank.delete(product.quantity, product)
        self.price_bank.delete(product.price, product)
        self.min_quantity_bank.delete(product.min_quantity, product)

        return True

    def update_quantity(self, _id, new_quantity):
        if new_quantity < 0:
            raise ValueError("quantity can't be negative")

        product = self.id_bank.get(_id)
        if product is None:
            return False
        product = product[0]

        self.quantity_bank.delete(product.quantity, product)
        product.quantity = self.quantity_bank.put(new_quantity, product)
        return True

    def find_by_name(self, name):
        yield from self._generate_report_header()
        for name in self.name_bank.get(name):
            yield self._format_product(name)

    def find_by_category(self, category):
        yield from self._generate_report_header()
        for category in self.category_bank.get(category):
            yield self._format_product(category)

    def find_by_price_range(self, min_price, max_price):
        yield from self._generate_report_header()
        for price in self.price_bank.get_by_slice(min_price, max_price):
            yield self._format_product(price)

    @staticmethod
    def cut_value(value, width: int) -> str:
        value = str(value)
        if len(value) <= width:
            return value.ljust(width)
        return "%s..." % value[: width - 3]

    def _format_product(self, product: Product) -> str:
        return " | ".join(
            self.cut_value(getattr(product, attr).value, max(len(attr), meta["width"]))
            for attr, meta in Product.PROTO.items()
        )

    @staticmethod
    def _generate_report_header() -> str:
        header = " | ".join(
            attr.ljust(meta["width"]) for attr, meta in Product.PROTO.items()
        )
        yield header
        yield "-" * len(header)

    def generate_stock_report(self, filter_by_stock: bool = False) -> str:
        yield from self._generate_report_header()

        if not filter_by_stock:
            for prop in self.id_bank.bank:
                yield self._format_product(prop.links[0])
            return

        for prop in self.quantity_bank.bank:
            quantity = prop.value
            for link in prop.links:
                if quantity >= link.min_quantity.value:
                    continue
                yield self._format_product(link)
