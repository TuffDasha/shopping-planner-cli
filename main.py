import json
import os

DATA_FILE = "shopping_list.json"

def load_data():
    """Завантажує дані з JSON файлу. Якщо файлу немає, повертає порожній список."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Помилка зчитування файлу даних. Створено новий список.")
        return []

def save_data(data):
    """Зберігає поточний список покупок у JSON файл."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError:
        print("Помилка збереження даних у файл!")

def get_next_id(data):
    """Генерує унікальний ID для нового товару."""
    if not data:
        return 1
    return max(item['id'] for item in data) + 1

def add_item(data):
    print("\n--- Додавання нового товару ---")
    name = input("Введіть назву товару: ").strip()
    while not name:
        print("Назва не може бути порожньою!")
        name = input("Введіть назву товару: ").strip()

    # Обробка некоректного вводу для кількості
    while True:
        try:
            quantity = float(input("Введіть кількість (наприклад, 2 або 1.5): "))
            if quantity <= 0:
                print("Кількість повинна бути більшою за 0!")
                continue
            break
        except ValueError:
            print("Некоректний ввід! Будь ласка, введіть число.")

    # Обробка некоректного вводу для ціни
    while True:
        try:
            price = float(input("Введіть орієнтовну ціну за одиницю (грн): "))
            if price <= 0:
                print("Ціна повинна бути більшою за 0!")
                continue
            break
        except ValueError:
            print("Некоректний ввід! Будь ласка, введіть число.")

    category = input("Введіть категорію (наприклад, Продукти, Техніка): ").strip()
    if not category:
        category = "Інше"

    new_item = {
        "id": get_next_id(data),
        "name": name,
        "quantity": quantity,
        "price": price,
        "category": category,
        "is_bought": False
    }
    
    data.append(new_item)
    save_data(data)
    print(f"Товар '{name}' успішно додано до списку!")

def view_items(data):
    print("\n--- Поточний список покупок ---")
    if not data:
        print("Ваш список покупок порожній.")
        return

    total_sum = 0
    print(f"{'ID':<4} | {'Назва':<20} | {'Кількість':<10} | {'Ціна':<10} | {'Категорія':<15} | {'Статус':<10}")
    print("-" * 75)
    
    for item in data:
        status = "Куплено" if item["is_bought"] else "Не куплено"
        print(f"{item['id']:<4} | {item['name']:<20} | {item['quantity']:<10} | {item['price']:<10.2f} | {item['category']:<15} | {status:<10}")
        if not item["is_bought"]:
            total_sum += item["quantity"] * item["price"]
            
    print("-" * 75)
    print(f"Загальна сума до сплати (за некуплені товари): {total_sum:.2f} грн")

def mark_as_bought(data):
    print("\n--- Відмітити товар як куплений ---")
    if not data:
        print("Список порожній. Немає чого відмічати.")
        return

    while True:
        try:
            item_id = int(input("Введіть ID товару, який ви купили: "))
            break
        except ValueError:
            print("Некоректний ввід! ID має бути цілим числом.")

    for item in data:
        if item["id"] == item_id:
            if item["is_bought"]:
                print(f"Товар '{item['name']}' вже був позначений як куплений.")
            else:
                item["is_bought"] = True
                save_data(data)
                print(f"Товар '{item['name']}' успішно позначено як куплений!")
            return
            
    print(f"Товар з ID {item_id} не знайдено.")

def delete_item(data):
    print("\n--- Видалення товару зі списку ---")
    if not data:
        print("Список порожній.")
        return

    while True:
        try:
            item_id = int(input("Введіть ID товару, який потрібно видалити: "))
            break
        except ValueError:
            print("Некоректний ввід! ID має бути цілим числом.")

    for item in data:
        if item["id"] == item_id:
            data.remove(item)
            save_data(data)
            print(f"Товар '{item['name']}' видалено зі списку.")
            return

    print(f"Товар з ID {item_id} не знайдено.")

def main():
    shopping_list = load_data()
    
    while True:
        print("\n===== ПЛАНУВАЛЬНИК ПОКУПОК =====")
        print("1. Переглянути список покупок")
        print("2. Додати новий товар")
        print("3. Відмітити товар як куплений")
        print("4. Видалити товар зі списку")
        print("5. Вийти з програми")
        
        choice = input("Оберіть дію (1-5): ").strip()
        
        if choice == "1":
            view_items(shopping_list)
        elif choice == "2":
            add_item(shopping_list)
        elif choice == "3":
            mark_as_bought(shopping_list)
        elif choice == "4":
            delete_item(shopping_list)
        elif choice == "5":
            print("Дякуємо за використання планувальника покупок! До побачення.")
            break
        else:
            print("Некоректний вибір! Будь ласка, введіть число від 1 до 5.")

if __name__ == "__main__":
    main()