import csv
from enum import Enum

from .trees import AVLTree


class Property:
    __slots__ = "value", "links", "CAST", "WIDTH"

    @classmethod
    def _cast_value(self, value):
        if self.CAST is int:
            if isinstance(value, int) and value < 0:
                raise ValueError("integer properties cannot be negative")
            if not isinstance(value, int) and not value.isdigit():
                raise TypeError(f"cannot cast {value!r} to positive int")
        return self.CAST(value)

    def __init__(self, value):
        self.value = self._cast_value(value)
        self.links = list()

    def __lt__(self, other) -> bool:
        return self.value < other

    def __le__(self, other) -> bool:
        return self.value <= other

    def __eq__(self, other) -> bool:
        return self.value == other

    def __ne__(self, other) -> bool:
        return self.value != other

    def __ge__(self, other) -> bool:
        return self.value >= other

    def __gt__(self, other) -> bool:
        return self.value > other


class PropertyID(Property):
    CAST, WIDTH = int, 4


class PropertyName(Property):
    CAST, WIDTH = str, 32


class PropertyCategory(Property):
    CAST, WIDTH = str, 32


class PropertyQuantity(Property):
    CAST, WIDTH = int, 8


class PropertyPrice(Property):
    CAST, WIDTH = int, 6


class PropertyMinQuantity(Property):
    CAST, WIDTH = int, 12


class Properties(Enum):
    ID = 0
    NAME = 1
    CATEGORY = 2
    QUANTITY = 3
    PRICE = 4
    MIN_QUANTITY = 5


PROPERTIES = (
    PropertyID,
    PropertyName,
    PropertyCategory,
    PropertyQuantity,
    PropertyPrice,
    PropertyMinQuantity,
)


class Product:
    __slots__ = tuple(p.name.lower() for p in Properties)

    @classmethod
    def keys(self) -> [str]:
        return self.__slots__

    def values(self) -> [Property]:
        return [getattr(self, p).value for p in self.__slots__]

    def items(self) -> [(str, Property)]:
        return [(p, getattr(self, p).value) for p in self.__slots__]


class Bank:
    __slots__ = ("tree",)

    def __init__(self):
        self.tree: [Property] = AVLTree()

    def get(self, value) -> [Product]:
        if (node := self.tree.search(self.tree.root, value)) is None:
            return list()
        return node.key.links

    def get_range(self, _from, _to) -> Product:
        if _from > _to:
            return
        for node in self.tree.traverse_range(self.tree.root, _from, _to):
            yield from node.key.links

    def put(self, value, link: Product, _enum_index: int) -> Property:
        _object = PROPERTIES[_enum_index]
        value = _object._cast_value(value)

        if (node := self.tree.search(self.tree.root, value)) is None:
            _property = _object(value)
            self.tree.root = self.tree.insert(self.tree.root, _property)
        else:
            _property = node.key

        _property.links.append(link)
        return _property

    def delete(self, value, link: Product):
        if (node := self.tree.search(self.tree.root, value)) is None:
            raise ValueError(f"property {value!r} not in bank")
        node.key.links.remove(link)
        if len(node.key.links) == 0:
            self.tree.delete(self.tree.root, value)


class InventorySystem:
    __slots__ = ("banks",)

    def __init__(self):
        self.banks = [Bank() for _ in range(len(Properties))]

    def load_from_csv(self, filename: str):
        with open(filename, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                properties = [row[p] for p in Product.keys()]
                self.add_product(*properties)

    def save_to_csv(self, filename: str):
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=Product.keys())
            writer.writeheader()
            tree = self.banks[Properties.ID.value].tree
            for _property in tree.traverse(tree.root):
                writer.writerow(dict(_property.key.links[0].items()))

    def add_product(self, *properties):
        product = Product()
        for i, _property in enumerate(Product.keys()):
            link = self.banks[i].put(properties[i], product, i)
            if i == 0 and len(link.links) != 1:
                raise ValueError("conflicting ids")
            setattr(product, _property, link)

    def _get_by_id(self, _id: int) -> Product | None:
        links = self.banks[Properties.ID.value].get(_id)
        return None if len(links) == 0 else links[0]

    def delete_product(self, _id: int) -> bool:
        if (product := self._get_by_id(_id)) is None:
            return False
        for i, _property in enumerate(Product.keys()):
            link = getattr(product, _property)
            self.banks[i].delete(link, product)
        return True

    def update_quantity(self, _id: int, quantity: int) -> bool:
        if (product := self._get_by_id(_id)) is None:
            return False
        _enum_index = Properties.QUANTITY.value
        bank = self.banks[_enum_index]

        bank.delete(product.quantity, product)
        product.quantity = bank.put(quantity, product, _enum_index)
        return True

    def find_by_name(self, value: str):
        yield from self._format_header()
        bank = self.banks[Properties.NAME.value]
        if len(value) == 0:
            return
        top = value[:-1] + chr(ord(value[-1]) + 1)

        for product in bank.get_range(value, top):
            yield self._format_product(product)

    def find_by_category(self, value: str):
        yield from self._format_header()
        bank = self.banks[Properties.CATEGORY.value]
        for product in bank.get(value):
            yield self._format_product(product)

    def find_by_price_range(self, _from: int, _to: int):
        yield from self._format_header()
        bank = self.banks[Properties.PRICE.value]
        for product in bank.get_range(_from, _to):
            yield self._format_product(product)

    @staticmethod
    def _cut_value(value, width: int) -> str:
        value = str(value)
        if len(value) <= width:
            return value.ljust(width)
        return "%s..." % value[: width - 3]

    def _format_product(self, product: Product) -> str:
        string = " | ".join(
            self._cut_value(v, PROPERTIES[i].WIDTH)
            for i, v in enumerate(product.values())
        )
        return string

    @staticmethod
    def _format_header() -> str:
        string = " | ".join(
            k.ljust(PROPERTIES[i].WIDTH) for i, k in enumerate(Product.keys())
        )
        yield string
        yield "-" * len(string)

    def generate_stock_report(self, filter_by_stock: bool = False) -> str:
        yield from self._format_header()

        if not filter_by_stock:
            tree = self.banks[Properties.ID.value].tree
            for _property in tree.traverse(tree.root):
                yield self._format_product(_property.key.links[0])
            return

        tree = self.banks[Properties.QUANTITY.value].tree
        for _property in tree.traverse(tree.root):
            for link in _property.key.links:
                if _property.key.value >= link.min_quantity:
                    continue
                yield self._format_product(link)
