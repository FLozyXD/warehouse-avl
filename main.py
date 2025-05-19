import sys

from ext.inventory import (
    Property,
    PropertyID,
    PropertyName,
    PropertyCategory,
    PropertyQuantity,
    PropertyPrice,
    PropertyMinQuantity,
    InventorySystem,
)


def _input(string: str, _property: Property | None = None):
    value = input(string).strip()
    if value == "":  # Обработка пустых значений
        raise ValueError("Value must be unempty")
    if _property is None:
        return value
    return _property._cast_value(value)


def print_table(strings):
    strings = list(strings)
    if len(strings) <= 2:
        return
    print("\n".join(strings))


def print_menu():
    print()
    print("Меню:")
    print("0. Общий отчет")
    print("1. Добавить товар")
    print("2. Удалить товар")
    print("3. Обновить количество")
    print("4. Поиск по названию")
    print("5. Поиск по категории")
    print("6. Поиск по диапазону цен")
    print("7. Отчет по запасам")
    print("8. Сохранить и выйти")
    print()


def main_loop(system: InventorySystem, filename: str):
    print_menu()
    choice = int(_input("Выберите пункт: "))

    if choice == 0:
        print_table(system.generate_stock_report())

    elif choice == 1:
        _id = _input("ID товара: ", PropertyID)
        name = _input("Название: ", PropertyName)
        category = _input("Категория: ", PropertyCategory)
        quantity = _input("Количество: ", PropertyQuantity)
        price = _input("Цена: ", PropertyPrice)
        min_qty = _input("Мин. допустимое количество: ", PropertyMinQuantity)
        system.add_product(_id, name, category, quantity, price, min_qty)

    elif choice == 2:
        _id = _input("ID для удаления: ", PropertyID)
        result = system.delete_product(_id)
        print("Удалено." if result is True else "Товар не найден.")

    elif choice == 3:
        _id = _input("ID товара: ", PropertyID)
        qty = _input("Новое количество: ", PropertyQuantity)
        if system.update_quantity(_id, qty):
            print("Количество обновлено.")
        else:
            print("Товар не найден.")

    elif choice == 4:
        name = _input("Введите часть названия: ", PropertyName)
        print_table(system.find_by_name(name))

    elif choice == 5:
        category = _input("Введите категорию: ", PropertyCategory)
        print_table(system.find_by_category(category))

    elif choice == 6:
        min_p = _input("Мин. цена: ", PropertyPrice)
        max_p = _input("Макс. цена: ", PropertyPrice)
        print_table(system.find_by_price_range(min_p, max_p))

    elif choice == 7:
        print_table(system.generate_stock_report(True))

    elif choice == 8:
        system.save_to_csv(filename)
        print("Сохранено. Выход.")
        return 0

    else:
        print("Неверный выбор.")


def main():
    system = InventorySystem()

    filename = "assortment.csv" if len(sys.argv) != 2 else sys.argv[1]
    system.load_from_csv(filename)

    while True:
        try:
            if main_loop(system, filename) == 0:
                break
        except (TypeError, ValueError) as e:
            print("Неверный выбор.")
            print(e)
        except (KeyboardInterrupt, EOFError):
            print()
            break


if __name__ == "__main__":
    main()
