from inventory_system import InventorySystem


# todo сделать общую функцию для обработки input()
# todo как-нибудь красивее выводить найденные результаты?


def main():
    system = InventorySystem(100)
    system.load_from_csv("assortment.csv")

    while True:
        print("\nМеню:")
        print("1. Добавить товар")
        print("2. Удалить товар")
        print("3. Обновить количество")
        print("4. Поиск по названию")
        print("5. Поиск по категории")
        print("6. Поиск по диапазону цен")
        print("7. Отчет по запасам")
        print("8. Сохранить и выйти")
        choice = input("Выберите пункт: ")

        if choice == "1":
            _id = int(input("ID: "))
            name = input("Название: ")
            category = input("Категория: ")
            quantity = int(input("Количество: "))
            price = int(input("Цена: "))
            min_qty = int(input("Мин. допустимое количество: "))
            system.add_product(_id, name, category, quantity, price, min_qty)

        elif choice == "2":
            _id = int(input("ID для удаления: "))
            result = system.delete_product(_id)
            print("Удалено." if result is not None else "Товар не найден.")

        elif choice == "3":
            _id = int(input("ID товара: "))
            qty = int(input("Новое количество: "))
            if system.update_quantity(_id, qty):
                print("Количество обновлено.")
            else:
                print("Товар не найден.")

        elif choice == "4":
            name = input("Введите часть названия: ")
            results = system.find_by_name(name)
            for r in results:
                print(r)

        elif choice == "5":
            category = input("Введите категорию: ")
            results = system.find_by_category(category)
            for r in results:
                print(r)

        elif choice == "6":
            min_p = int(input("Мин. цена: "))
            max_p = int(input("Макс. цена: "))
            results = system.find_by_price_range(min_p, max_p)
            for r in results:
                print(r)

        elif choice == "7":
            system.generate_stock_report()

        elif choice == "8":
            system.save_to_csv("assortment.csv")
            print("Сохранено. Выход.")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
