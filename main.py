import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "shopping_list.json"

# СЬОГОДНІ: Базові заглушки та ініціалізація структури даних
def load_data():
    if not os.path.exists(DATA_FILE): return []
    return []

def save_data(data):
    pass

def get_total_info(data):
    return 0, 0

def add_item(data, **kwargs):
    return {"name": kwargs.get("name", "Тест")}

def mark_as_bought(data, item_id=None):
    return None

def view_items(data, **kwargs):
    return [], 0, 0

def delete_item(data, **kwargs):
    return False

# СЬОГОДНІ: Повний рендеринг графічної оболонки (GUI)
def create_gui():
    root = tk.Tk()
    root.title("Планувальник покупок")
    root.geometry("1100x650")
    root.minsize(980, 550)

    style = ttk.Style(root)
    style.theme_use("clam")

    def refresh_data():
        tree.delete(*tree.get_children())
        stats_var.set("Всього товарів: 0 | Загалом: 0.00 грн | До оплати: 0.00 грн")
        category_combo["values"] = []

    def add_item_from_form():
        messagebox.showinfo("Етап розробки", "Функціонал додавання інтегрується...")

    def mark_selected():
        messagebox.showinfo("Етап розробки", "Обробник подій буде підключено завтра.")

    def delete_selected():
        pass

    def clear_bought():
        pass

    def clear_all():
        pass

    def apply_filter():
        pass

    # Верхня рама з статистикою
    top_frame = ttk.Frame(root, padding=10)
    top_frame.pack(fill=tk.X)
    stats_var = tk.StringVar(value="Завантаження інтерфейсу...")
    ttk.Label(top_frame, textvariable=stats_var, font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)

    # Рама з елементами керування
    controls_frame = ttk.LabelFrame(root, text="Дії", padding=10)
    controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    ttk.Button(controls_frame, text="Показати всі", command=apply_filter).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(controls_frame, text="Active", command=apply_filter).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(controls_frame, text="Архів", command=apply_filter).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(controls_frame, text="Очищення куплених", command=clear_bought).grid(row=0, column=3, padx=5, pady=5)
    ttk.Button(controls_frame, text="Повне очищення", command=clear_all).grid(row=0, column=4, padx=5, pady=5)

    filter_var = tk.StringVar(value="all")
    ttk.Label(controls_frame, text="Категорія:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    category_combo = ttk.Combobox(controls_frame, state="readonly", width=18)
    category_combo.grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(controls_frame, text="Фільтрувати", command=apply_filter).grid(row=1, column=2, padx=5, pady=5)

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

    tree.heading("id", text="ID"); tree.heading("name", text="Назва")
    tree.heading("quantity", text="Кількість"); tree.heading("price", text="Ціна")
    tree.heading("category", text="Категорія"); tree.heading("status", text="Статус")

    tree.column("id", width=50, anchor=tk.CENTER); tree.column("name", width=260)
    tree.column("quantity", width=90, anchor=tk.CENTER); tree.column("price", width=90, anchor=tk.CENTER)
    tree.column("category", width=180); tree.column("status", width=120, anchor=tk.CENTER)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    bottom_frame = ttk.Frame(root, padding=10)
    bottom_frame.pack(fill=tk.X)
    ttk.Button(bottom_frame, text="Позначити як куплений", command=mark_selected).pack(side=tk.LEFT, padx=5)
    ttk.Button(bottom_frame, text="Видалити вибраний", command=delete_selected).pack(side=tk.LEFT, padx=5)
    ttk.Button(bottom_frame, text="Оновити", command=refresh_data).pack(side=tk.LEFT, padx=5)

    refresh_data()
    root.mainloop()

if __name__ == "__main__":
    create_gui()