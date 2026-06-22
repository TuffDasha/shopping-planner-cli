import unittest
# Тимчасово підміняємо файл даних для тесту
import main
main.DATA_FILE = "shopping_list_test.json"

class TestShoppingPlanner(unittest.TestCase):
    
    def test_get_next_id_empty_list(self):
        """Тест: якщо список порожній, перший ID має бути 1"""
        empty_list = []
        result = main.get_next_id(empty_list)
        self.assertEqual(result, 1)

    def test_get_next_id_with_items(self):
        """Тест: ID має бути на 1 більшим за максимальний існуючий ID"""
        sample_data = [
            {"id": 1, "name": "Молоко", "price": 40.0, "quantity": 1, "category": "Продукти", "is_bought": False},
            {"id": 5, "name": "Хліб", "price": 20.0, "quantity": 1, "category": "Продукти", "is_bought": True}
        ]
        result = main.get_next_id(sample_data)
        # Максимальний ID у списку — 5, отже наступний має бути 6
        self.assertEqual(result, 6)

if __name__ == "__main__":
    unittest.main()