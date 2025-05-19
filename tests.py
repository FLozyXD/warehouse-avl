import unittest
import tempfile
import os

from ext.inventory import InventorySystem, Product

class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        self.system = InventorySystem()

    def test_add_and_find(self):
        # Добавляем разные товары
        self.system.add_product(1, "Milk", "Dairy", 50, 100, 10)
        self.system.add_product(2, "Bread", "Bakery", 20, 50, 5)
        self.system.add_product(3, "Milk", "Dairy", 30, 120, 15)
        # Поиск по имени 'Milk' должен вернуть два товара
        results = list(self.system.find_by_name("Milk"))
        self.assertGreaterEqual(len(results) - 2, 2, "Должно быть два товара Milk")
        # Поиск по категории 'Dairy' должен вернуть два товара
        results_cat = list(self.system.find_by_category("Dairy"))
        self.assertGreaterEqual(len(results_cat) - 2, 2, "Должно быть два товара категории Dairy")

    def test_price_range_search(self):
        self.system.add_product(1, "Item1", "Cat", 10, 99, 1)
        self.system.add_product(2, "Item2", "Cat", 10, 100, 1)
        self.system.add_product(3, "Item3", "Cat", 10, 150, 1)
        # диапазон включает цену 100, исключает 99
        results = list(self.system.find_by_price_range(100, 150))
        found = [row for row in results if "Item2" in row or "Item3" in row]
        self.assertTrue(any("Item2" in row for row in found))
        self.assertTrue(any("Item3" in row for row in found))
        self.assertFalse(any("Item1" in row for row in results), "Item1 не должен быть включен")

    def test_update_quantity(self):
        self.system.add_product(1, "Prod", "Cat", 50, 100, 10)
        # успешное обновление
        self.assertTrue(self.system.update_quantity(1, 25))
        rows = list(self.system.find_by_name("Prod"))
        self.assertTrue(any("25" in row for row in rows), "Количество должно измениться на 25")
        # обновление несуществующего
        self.assertFalse(self.system.update_quantity(999, 10))
        # отрицательное значение
        with self.assertRaises(ValueError):
            self.system.update_quantity(1, -5)

    def test_delete_product(self):
        self.system.add_product(1, "X", "Y", 5, 10, 1)
        # удаляем существующий
        self.assertTrue(self.system.delete_product(1))
        # повторное удаление
        self.assertFalse(self.system.delete_product(1))
        # удаление несуществующего
        self.assertFalse(self.system.delete_product(999))

    def test_stock_report(self):
        self.system.add_product(1, "A", "C", 2, 100, 5)
        self.system.add_product(2, "B", "C", 10, 50, 5)
        report = list(self.system.generate_stock_report(filter_by_stock=True))
        # header + separator + строки
        # убедимся, что A есть, B нет
        self.assertTrue(any("A" in row for row in report), "A должен быть в отчете")
        self.assertFalse(any("B" in row for row in report if row and row.startswith(' ')), "B не должен быть в отчете")

    def test_save_and_load_csv(self):
        # добавляем товары
        self.system.add_product(1, "Milk", "Dairy", 50, 100, 10)
        self.system.add_product(2, "Bread", "Bakery", 20, 50, 5)
        # сохраняем во временный файл
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        tmp_name = tmp.name
        tmp.close()
        try:
            self.system.save_to_csv(tmp_name)
            new_sys = InventorySystem()
            new_sys.load_from_csv(tmp_name)
            # сравнить по категориям
            orig = len(list(self.system.find_by_category("Dairy")))
            loaded = len(list(new_sys.find_by_category("Dairy")))
            self.assertEqual(orig, loaded)
        finally:
            os.remove(tmp_name)

    def test_invalid_add(self):
        # отрицательные параметры
        with self.assertRaises(ValueError):
            self.system.add_product(1, "Bad", "C", -1, 10, 1)
        with self.assertRaises(ValueError):
            self.system.add_product(1, "Bad", "C", 1, -10, 1)
        with self.assertRaises(ValueError):
            self.system.add_product(1, "Bad", "C", 1, 10, -1)

    def test_find_no_results(self):
        # поиск пустой системы
        name_res = list(self.system.find_by_name("none"))
        cat_res = list(self.system.find_by_category("none"))
        price_res = list(self.system.find_by_price_range(0, 10))
        # должно быть только заголовок и разделитель
        self.assertEqual(len(name_res), 2)
        self.assertEqual(len(cat_res), 2)
        self.assertEqual(len(price_res), 2)

    def test_input_type_errors(self):
        # метод add_product ожидает корректные типы, но если передать строку вместо числа
        with self.assertRaises(TypeError):
            self.system.add_product("not_int", "N", "C", 1, 1, 1)
        self.assertEqual(self.system.update_quantity("not_int", 10), False)
        self.assertEqual(self.system.delete_product("not_int"), False)

if __name__ == '__main__':
    unittest.main()
