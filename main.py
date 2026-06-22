import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "shopping_list.json"


# Розділ 1: Завантаження та збереження даних (JSON)

def load_data():
    """Завантажує дані з JSON файлу."""
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


# Розділ 2: Допоміжні функції системи

def get_next_id(data):
    """Генерує унікальний ID для нового товару."""
    if not data:
        return 1
    return max(item['id'] for item in data) + 1


def display_table(items_to_show):
    """Допоміжна функція для красивого виведення таблиці товарів."""
    print(f"{'ID':<4} | {'Назва':<20} | {'Кількість':<10} | {'Ціна':<10} | {'Категорія':<15} | {'Статус':<10}")
    print("-" * 75)
    for item in items_to_show:
        status = "Куплено" if item["is_bought"] else "Не куплено"
        print(f"{item['id']:<4} | {item['name']:<20} | {item['quantity']:<10} | {item['price']:<10.2f} | {item['category']:<15} | {status:<10}")
    print("-" * 75)


def get_total_info(data):
    """Повертає загальну суму та суму до оплати."""
    total_all = sum(item["quantity"] * item["price"] for item in data)
    total_remaining = sum(item["quantity"] * item["price"] for item in data if not item["is_bought"])
    return total_all, total_remaining


# Розділ 3: Основні операції з товарами (бізнес-логіка)

def add_item(data, name=None, quantity=None, price=None, category=None):
    if name is None:
        print("\n--- Додавання нового товару ---")
        name = input("Введіть назву товару: ").strip()
    name = name.strip()
    while not name:
        print("Назва не може бути порожньою!")
        name = input("Введіть назву товару: ").strip()
        name = name.strip()

    if quantity is None:
        while True:
            try:
                quantity = float(input("Введіть кількість (наприклад, 2 або 1.5): "))
                if quantity <= 0:
                    print("Кількість повинна бути більшою за 0!")
                    continue
                break
            except ValueError:
                print("Некоректний ввід! Будь ласка, введіть число.")

    if price is None:
        while True:
            try:
                price = float(input("Введіть орієнтовну ціну за одиницю (грн): "))
                if price <= 0:
                    print("Ціна повинна бути більшою за 0!")
                    continue
                break
            except ValueError:
                print("Некоректний ввід! Будь ласка, введіть число.")

    if category is None:
        category = input("Введіть категорію (наприклад, Продукти, Техніка): ").strip()
    category = category.strip() or "Інше"

    new_item = {
        "id": get_next_id(data),
        "name": name,
        "quantity": quantity,
        "price": price,
        "category": category,
        "is_bought": False,
    }

    data.append(new_item)
    save_data(data)
    return new_item


def mark_as_bought(data, item_id=None):
    if item_id is None:
        print("\n--- Відмітити товар як куплений ---")
        if not data:
            print("Список порожній.")
            return None

        while True:
            try:
                item_id = int(input("Введіть ID товару, який ви купили: "))
                break
            except ValueError:
                print("Некоректний ввід! ID має бути цілим числом.")

    for item in data:
        if item["id"] == item_id:
            if item["is_bought"]:
                return item
            item["is_bought"] = True
            save_data(data)
            return item

    return None


# Розділ 4: Фільтрація, активний список, архів та видалення

def view_items(data, filter_mode="all", category=None):
    if filter_mode == "active":
        filtered_list = [item for item in data if not item["is_bought"]]
    elif filter_mode == "archive":
        filtered_list = [item for item in data if item["is_bought"]]
    elif filter_mode == "category":
        if category is None:
            return [], 0, 0
        filtered_list = [item for item in data if item["category"].lower() == category.lower()]
    else:
        filtered_list = data

    total_all, total_remaining = get_total_info(data)
    return filtered_list, total_all, total_remaining


def delete_item(data, mode="single", item_id=None, confirm=False):
    if not data:
        return False

    if mode == "single":
        if item_id is None:
            return False
        for item in data:
            if item["id"] == item_id:
                data.remove(item)
                save_data(data)
                return True
        return False

    if mode == "clear_bought":
        start_count = len(data)
        data[:] = [item for item in data if not item["is_bought"]]
        save_data(data)
        return start_count - len(data)

    if mode == "clear_all" and confirm:
        data.clear()
        save_data(data)
        return True

    return False


# Розділ 5: Головний керований цикл програми (MENU)

def main():
    shopping_list = load_data()

    while True:
        print("\n===== ПЛАНУВАЛЬНИК ПОКУПОК =====")
        print("1. Переглянути список покупок / Статистику")
        print("2. Додати новий товар")
        print("3. Відмітити товар як куплений")
        print("4. Видалення товарів / Очищення списку")
        print("5. Вийти з програми")

        choice = input("Оберіть дію (1-5): ").strip()

        if choice == "1":
            print("\n--- Список покупок ---")
            if not shopping_list:
                print("Ваш список покупок порожній.")
                continue

            print("1. Показати ВСІ товари")
            print("2. Перегляд АКТИВНОГО списку (тільки некуплені)")
            print("3. Перегляд АРХІВУ (вже куплені товари)")
            print("4. Фільтрувати за конкретною категорією")
            sub_choice = input("Оберіть варіант відображення (1-4): ").strip()

            if sub_choice == "2":
                filtered_list, total_all, total_remaining = view_items(shopping_list, filter_mode="active")
                print("\n--- АКТИВНИЙ СПИСОК ПОКУПОК ---")
            elif sub_choice == "3":
                filtered_list, total_all, total_remaining = view_items(shopping_list, filter_mode="archive")
                print("\n--- АРХІВ КУПЛЕНИХ ТОВАРІВ ---")
            elif sub_choice == "4":
                cat_search = input("Введіть назву категорії для фільтрації: ").strip()
                filtered_list, total_all, total_remaining = view_items(shopping_list, filter_mode="category", category=cat_search)
                print(f"\nТовари у категорії '{cat_search}':")
            else:
                filtered_list, total_all, total_remaining = view_items(shopping_list)
                print("\n--- Список покупок ---")

            if not filtered_list:
                print("Товарів за вказаними критеріями не знайдено.")
                continue

            display_table(filtered_list)
            print(f"Загальна вартість усього списку: {total_all:.2f} грн")
            print(f"Залишилося сплатити (за некуплені товари): {total_remaining:.2f} грн")
        elif choice == "2":
            added_item = add_item(shopping_list)
            print(f"Товар '{added_item['name']}' успішно додано до списку!")
        elif choice == "3":
            item = mark_as_bought(shopping_list)
            if item is None:
                print("Товар не знайдено або список порожній.")
            elif item["is_bought"]:
                print(f"Товар '{item['name']}' успішно позначено як куплений!")
            else:
                print(f"Товар '{item['name']}' вже був позначений як куплений.")
        elif choice == "4":
            print("\n--- Видалення товарів / Очищення ---")
            if not shopping_list:
                print("Список порожній.")
                continue

            print("1. Видалити один товар за ID")
            print("2. Очистити лише КУПЛЕНІ товари")
            print("3. Повністю очистити список покупок")
            sub_choice = input("Оберіть дію (1-3): ").strip()

            if sub_choice == "1":
                while True:
                    try:
                        item_id = int(input("Введіть ID товару, який потрібно видалити: "))
                        break
                    except ValueError:
                        print("Некоректний ввід! ID має бути цілим числом.")
                if delete_item(shopping_list, mode="single", item_id=item_id):
                    print(f"Товар з ID {item_id} видалено зі списку.")
                else:
                    print(f"Товар з ID {item_id} не знайдено.")
            elif sub_choice == "2":
                removed = delete_item(shopping_list, mode="clear_bought")
                print(f"Очищено куплених товарів: {removed} шт.")
            elif sub_choice == "3":
                confirm = input("Ви впевнені, що хочете повністю очистити список? (y/n): ").strip().lower()
                if confirm in ('y', 'так'):
                    delete_item(shopping_list, mode="clear_all", confirm=True)
                    print("Список покупок повністю очищено!")
        elif choice == "5":
            print("Дякуємо за використання планувальника покупок! До побачення.")
            break
        else:
            print("Некоректний вибір! Будь ласка, введіть число від 1 до 5.")


# GUI-версія застосунку

def create_gui():
    root = tk.Tk()
    root.title("Планувальник покупок")
    root.geometry("1100x650")
    root.minsize(980, 550)

    style = ttk.Style(root)
    style.theme_use("clam")

    def refresh_data():
        shopping_list = load_data()
        tree.delete(*tree.get_children())
        for item in shopping_list:
            status = "Куплено" if item["is_bought"] else "Не куплено"
            tree.insert(
                "",
                tk.END,
                values=(
                    item["id"],
                    item["name"],
                    item["quantity"],
                    f"{item['price']:.2f}",
                    item["category"],
                    status,
                ),
            )

        total_all, total_remaining = get_total_info(shopping_list)
        stats_var.set(
            f"Всього товарів: {len(shopping_list)} | Загалом: {total_all:.2f} грн | До оплати: {total_remaining:.2f} грн"
        )

        category_values = sorted({item["category"] for item in shopping_list})
        category_combo["values"] = category_values
        if category_values:
            category_combo.current(0)

    def add_item_from_form():
        try:
            name = name_entry.get().strip()
            quantity = float(quantity_entry.get())
            price = float(price_entry.get())
            category = category_entry.get().strip() or "Інше"
            if not name:
                messagebox.showerror("Помилка", "Назва товару не може бути порожньою.")
                return
            if quantity <= 0 or price <= 0:
                messagebox.showerror("Помилка", "Кількість і ціна мають бути більшими за 0.")
                return
            shopping_list = load_data()
            added = add_item(shopping_list, name=name, quantity=quantity, price=price, category=category)
            refresh_data()
            messagebox.showinfo("Успіх", f"Товар '{added['name']}' додано до списку.")
            name_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Помилка", "Кількість і ціна повинні бути числами.")

    def mark_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Увага", "Спочатку виберіть товар.")
            return
        item_id = int(tree.item(selected[0], "values")[0])
        shopping_list = load_data()
        item = mark_as_bought(shopping_list, item_id=item_id)
        if item is None:
            messagebox.showerror("Помилка", "Товар не знайдено.")
            return
        refresh_data()
        if item["is_bought"]:
            messagebox.showinfo("Успіх", f"Товар '{item['name']}' позначено як куплений.")
        else:
            messagebox.showinfo("Успіх", f"Товар '{item['name']}' вже був куплений.")

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Увага", "Спочатку виберіть товар.")
            return
        item_id = int(tree.item(selected[0], "values")[0])
        shopping_list = load_data()
        if delete_item(shopping_list, mode="single", item_id=item_id):
            refresh_data()
            messagebox.showinfo("Успіх", "Товар видалено.")
        else:
            messagebox.showerror("Помилка", "Не вдалося видалити товар.")

    def clear_bought():
        shopping_list = load_data()
        removed = delete_item(shopping_list, mode="clear_bought")
        refresh_data()
        messagebox.showinfo("Успіх", f"Очищено куплених товарів: {removed} шт.")

    def clear_all():
        if not messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете повністю очистити список?"):
            return
        shopping_list = load_data()
        if delete_item(shopping_list, mode="clear_all", confirm=True):
            refresh_data()
            messagebox.showinfo("Успіх", "Список покупок очищено.")

    def apply_filter():
        mode = filter_var.get()
        shopping_list = load_data()
        
        if mode == "category":
            category = category_combo.get().strip()
            if not category:
                messagebox.showwarning("Увага", "Введіть категорію для фільтрації.")
                return
            filtered_list, _, _ = view_items(shopping_list, filter_mode="category", category=category)
        elif mode == "active":
            filtered_list, _, _ = view_items(shopping_list, filter_mode="active")
        elif mode == "archive":
            filtered_list, _, _ = view_items(shopping_list, filter_mode="archive")
        else:
            filtered_list, _, _ = view_items(shopping_list)

        # Рахуємо фінанси СУТО для тих товарів, які пройшли фільтр і будуть показані
        current_total = sum(item["quantity"] * item["price"] for item in filtered_list)
        current_remaining = sum(item["quantity"] * item["price"] for item in filtered_list if not item["is_bought"])

        tree.delete(*tree.get_children())
        for item in filtered_list:
            status = "Куплено" if item["is_bought"] else "Не куплено"
            tree.insert(
                "",
                tk.END,
                values=(
                    item["id"],
                    item["name"],
                    item["quantity"],
                    f"{item['price']:.2f}",
                    item["category"],
                    status,
                ),
            )
        
        stats_var.set(
            f"Показано: {len(filtered_list)} | Загалом: {current_total:.2f} грн | До оплати: {current_remaining:.2f} грн"
        )

    # Верхня рама з статистикою
    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(fill=tk.X)
    stats_var = tk.StringVar(value="")
    ttk.Label(top_frame, textvariable=stats_var, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)

    # Рама з елементами керування
    controls_frame = ttk.LabelFrame(root, text="Дії", padding=10)
    controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    ttk.Button(controls_frame, text="Показати всі", command=lambda: (filter_var.set("all"), apply_filter())).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(controls_frame, text="Активні", command=lambda: (filter_var.set("active"), apply_filter())).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(controls_frame, text="Архів", command=lambda: (filter_var.set("archive"), apply_filter())).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(controls_frame, text="Очищення куплених", command=clear_bought).grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(controls_frame, text="Повне очищення", command=clear_all).grid(row=0, column=4, padx=5, pady=5)

    filter_var = tk.StringVar(value="all")
    ttk.Label(controls_frame, text="Категорія:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    category_combo = ttk.Combobox(controls_frame, state="readonly", width=18)
    category_combo.grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(
        controls_frame,
        text="Фільтрувати",
        command=lambda: (filter_var.set("category"), apply_filter()),
    ).grid(row=1, column=2, padx=5, pady=5)

    # Рама вводу
    input_frame = ttk.LabelFrame(root, text="Додати товар", padding=10)
    input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    ttk.Label(input_frame, text="Назва:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    name_entry = ttk.Entry(input_frame, width=30)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Кількість:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
    quantity_entry = ttk.Entry(input_frame, width=10)
    quantity_entry.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(input_frame, text="Ціна:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
    price_entry = ttk.Entry(input_frame, width=10)
    price_entry.grid(row=0, column=5, padx=5, pady=5)

    ttk.Label(input_frame, text="Категорія:").grid(row=0, column=6, sticky=tk.W, padx=5, pady=5)
    category_entry = ttk.Entry(input_frame, width=18)
    category_entry.grid(row=0, column=7, padx=5, pady=5)

    ttk.Button(input_frame, text="Додати товар", command=add_item_from_form).grid(row=0, column=8, padx=5, pady=5)

    # Рама таблиці
    table_frame = ttk.Frame(root)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    columns = ("id", "name", "quantity", "price", "category", "status")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tree.heading("id", text="ID")
    tree.heading("name", text="Назва")
    tree.heading("quantity", text="Кількість")
    tree.heading("price", text="Ціна")
    tree.heading("category", text="Категорія")
    tree.heading("status", text="Статус")

    tree.column("id", width=50, anchor=tk.CENTER)
    tree.column("name", width=260)
    tree.column("quantity", width=90, anchor=tk.CENTER)
    tree.column("price", width=90, anchor=tk.CENTER)
    tree.column("category", width=180)
    tree.column("status", width=120, anchor=tk.CENTER)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    # Рама з кнопками для дій з таблицею
    bottom_frame = ttk.Frame(root, padding=10)
    bottom_frame.pack(fill=tk.X)
    ttk.Button(bottom_frame, text="Позначити як куплений", command=mark_selected).pack(side=tk.LEFT, padx=5)
    ttk.Button(bottom_frame, text="Видалити вибраний", command=delete_selected).pack(side=tk.LEFT, padx=5)
    ttk.Button(bottom_frame, text="Оновити", command=refresh_data).pack(side=tk.LEFT, padx=5)

    refresh_data()
    root.mainloop()


if __name__ == "__main__":
    create_gui()