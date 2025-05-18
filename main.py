from ext.inventory import Product, InventorySystem


def _input(string: str, prop: str | None = None):
    value = input(string).strip()
    if prop is None:
        return value
    return Product.PROTO[prop]["type"](value)


def main():
    system = InventorySystem()
    system.load_from_csv("assortment.csv")

    while True:
        print("\nМеню:")
        print("0. Общий отчет")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Обновить количество")
        print("4. Поиск по названию")
        print("5. Поиск по категории")
        print("6. Поиск по диапазону цен")
        print("7. Отчет по запасам")
        print("8. Сохранить и выйти")

        try:
            choice = _input("Выберите пункт: ")
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not choice.isdigit():
            continue
        choice = int(choice)

        if choice == 0:
            for r in system.generate_stock_report():
                print(r)

        elif choice == 1:
            _id = _input("ID: ", "id")
            name = _input("Название: ", "name")
            category = _input("Категория: ", "category")
            quantity = _input("Количество: ", "quantity")
            price = _input("Цена: ", "price")
            min_qty = _input("Мин. допустимое количество: ", "min_quantity")
            system.add_product(_id, name, category, quantity, price, min_qty)

        elif choice == 2:
            _id = _input("ID для удаления: ", "id")
            result = system.delete_product(_id)
            print("Удалено." if result is True else "Товар не найден.")

        elif choice == 3:
            _id = _input("ID товара: ", "id")
            qty = _input("Новое количество: ", "quantity")
            if system.update_quantity(_id, qty):
                print("Количество обновлено.")
            else:
                print("Товар не найден.")

        elif choice == 4:
            name = _input("Введите название: ", "name")
            results = system.find_by_name(name)
            for r in results:
                print(r)

        elif choice == 5:
            category = _input("Введите категорию: ", "category")
            results = system.find_by_category(category)
            for r in results:
                print(r)

        elif choice == 6:
            min_p = _input("Мин. цена: ", "price")
            max_p = _input("Макс. цена: ", "price")
            results = system.find_by_price_range(min_p, max_p)
            for r in results:
                print(r)

        elif choice == 7:
            for r in system.generate_stock_report(filter_by_stock=True):
                print(r)

        elif choice == 8:
            system.save_to_csv("assortment.csv")
            print("Сохранено. Выход.")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
