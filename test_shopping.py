# test_shopping.py
# Автоматизовані модульні тести для функцій get_total_info та view_items

import json
import os
import unittest
import main  # Імпортуємо головний модуль програми

TEST_FILE = "test_shopping_list.json"

class TestShoppingListLogic(unittest.TestCase):

    def setUp(self):
        """Ініціалізація тестового середовища та запис контрольних даних."""
        main.DATA_FILE = TEST_FILE
        self.test_data = [
            {"id": 1, "name": "Молоко", "quantity": 2.0, "price": 40.0, "category": "Продукти", "is_bought": False},
            {"id": 2, "name": "Хліб", "quantity": 1.0, "price": 25.0, "category": "Продукти", "is_bought": True},
            {"id": 3, "name": "Навушники", "quantity": 1.0, "price": 1200.0, "category": "Техніка", "is_bought": False}
        ]
        with open(TEST_FILE, "w", encoding="utf-8") as f:
            json.dump(self.test_data, f, ensure_ascii=False, indent=4)

    def tearDown(self):
        """Очищення тестового середовища після виконання тесту."""
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_financial_calculation(self):
        """Тест 1: Перевірка коректності розрахунку фінансової статистики."""
        # Формула: (2*40) + (1*25) + (1*1200) = 80 + 25 + 1200 = 1305.0
        # До оплати (некуплені: 1 та 3): 80 + 1200 = 1280.0
        total_all, total_remaining = main.get_total_info(self.test_data)
        
        self.assertEqual(total_all, 1305.0, f"Очікувалось 1305.0, отримано {total_all}")
        self.assertEqual(total_remaining, 1280.0, f"Очікувалось 1280.0, отримано {total_remaining}")
        print(" ✓ Тест 1: Розрахунок фінансової статистики виконано успішно.")

    def test_active_filter(self):
        """Тест 2: Перевірка фільтрації активних (некуплених) товарів."""
        filtered, _, _ = main.view_items(self.test_data, filter_mode="active")
        
        # Має залишитися рівно 2 товари (Молоко та Навушники)
        self.assertEqual(len(filtered), 2)
        self.assertFalse(filtered[0]["is_bought"])
        self.assertFalse(filtered[1]["is_bought"])
        print(" ✓ Тест 2: Фільтрація активних товарів працює коректно.")

    def test_archive_filter(self):
        """Тест 3: Перевірка фільтрації архівних (куплених) товарів."""
        filtered, _, _ = main.view_items(self.test_data, filter_mode="archive")
        
        # Має залишитися рівно 1 товар (Хліб)
        self.assertEqual(len(filtered), 1)
        self.assertTrue(filtered[0]["is_bought"])
        self.assertEqual(filtered[0]["name"], "Хліб")
        print(" ✓ Тест 3: Фільтрація архіву куплених товарів працює коректно.")

if __name__ == "__main__":
    unittest.main()