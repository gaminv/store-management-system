import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from models.database import get_db_connection
from models.auth import authenticate_user
from datetime import datetime
import tkinter.filedialog as filedialog

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Store Management")
        self.user_authenticated = False
        self.current_user_role = None  # Роль текущего пользователя
        self.show_login_screen()

    def show_login_screen(self):
        """Экран входа."""
        login_window = tk.Toplevel(self.root)
        login_window.title("Вход")
        login_window.geometry("550x200")

        tk.Label(login_window, text="Имя пользователя:").pack()
        username_var = tk.StringVar()
        tk.Entry(login_window, textvariable=username_var).pack()

        tk.Label(login_window, text="Пароль:").pack()
        password_var = tk.StringVar()
        tk.Entry(login_window, textvariable=password_var, show="*").pack()

        def login():
            username = username_var.get()
            password = password_var.get()
            user_data = authenticate_user(username, password)
            if user_data:
                self.user_authenticated = True
                self.current_user_role = user_data['role']  # Сохраняем роль
                login_window.destroy()
                self.create_main_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")

        tk.Button(login_window, text="Войти", command=login).pack()

    def create_main_menu(self):
        """Создает главное меню приложения."""
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Справочники
        directories_menu = tk.Menu(menu, tearoff=0)
        directories_menu.add_command(label="Товары", command=self.manage_warehouses)
        directories_menu.add_command(label="Статьи расходов", command=self.manage_expense_items)
        menu.add_cascade(label="Справочники", menu=directories_menu)

        # Журналы
        journals_menu = tk.Menu(menu, tearoff=0)
        journals_menu.add_command(label="Журнал продаж", command=self.manage_sales_log)
        journals_menu.add_command(label="Журнал расходов", command=self.manage_charges_log)
        menu.add_cascade(label="Журналы", menu=journals_menu)

        # Отчеты
        reports_menu = tk.Menu(menu, tearoff=0)
        reports_menu.add_command(label="Прибыль за месяц", command=self.show_monthly_profit)
        reports_menu.add_command(label="Пять самых доходных товаров", command=self.show_top_5_profitable_products)
        menu.add_cascade(label="Отчеты", menu=reports_menu)

    def manage_warehouses(self):
        """Управление справочником товаров."""
        self.generic_management_window("Товары", "warehouses",
                                       [("id", "ID"), ("name", "Наименование"), ("quantity", "Количество"),
                                        ("amount", "Цена")])

    def manage_expense_items(self):
        """Управление справочником статей расходов."""
        self.generic_management_window("Статьи расходов", "expense_items", [("id", "ID"), ("name", "Наименование")])

    def manage_sales_log(self):
        """Управление журналом продаж."""
        self.generic_management_window(
            "Журнал продаж", "sales",
            [("id", "ID"), ("warehouse_id", "Товар"), ("quantity", "Количество"), ("amount", "Цена"),
             ("sale_date", "Дата")])

    def manage_charges_log(self):
        """Управление журналом расходов."""
        self.generic_management_window(
            "Журнал расходов", "charges",
            [("id", "ID"), ("amount", "Сумма"), ("expense_item_id", "Статья расхода"), ("charge_date", "Дата")])

    def create_input_field(self, parent, label, default_text):
        """Создает поле ввода с начальным текстом, который исчезает при фокусе и восстанавливается при потере фокуса"""
        var = tk.StringVar()

        # Вставляем начальный текст
        entry = tk.Entry(parent, textvariable=var)
        entry.insert(0, default_text)

        # При фокусе очищаем поле
        def on_focus_in(event):
            if var.get() == default_text:
                var.set('')

        # Если поле теряет фокус и пустое, восстанавливаем текст
        def on_focus_out(event):
            if var.get() == '':
                var.set(default_text)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return entry, var

    def generic_management_window(self, title, table, columns):
        """Обобщенный метод для управления записями таблиц."""
        window = tk.Toplevel(self.root)
        window.title(title)

        tree = ttk.Treeview(window, columns=[col[0] for col in columns], show="headings")
        for col in columns:
            tree.heading(col[0], text=col[1])
        tree.grid(row=0, column=0, columnspan=3)

        # Функция для обновления таблицы
        def refresh_table():
            try:
                with get_db_connection() as conn:
                    cur = conn.cursor()
                    for row in tree.get_children():
                        tree.delete(row)
                    cur.execute(f"SELECT {', '.join(col[0] for col in columns)} FROM {table}")
                    for row in cur.fetchall():
                        tree.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении данных: {e}")

        # Если текущий пользователь - это user, то отображаем только таблицу, без дополнительных полей
        if self.current_user_role == 'user':
            refresh_table()  # Показываем только таблицу с данными
            return  # Для пользователя нет кнопок и текстовых полей, поэтому завершить функцию

        # Для администраторов создаем текстовые поля и кнопки
        entry_vars = {}  # Словарь для хранения переменных ввода
        for i, col in enumerate(columns[1:]):
            entry, var = self.create_input_field(window, col[1], f"{col[1]}")
            entry.grid(row=1, column=i)
            entry_vars[col[0]] = var

        def add_entry():
            """Добавить новую запись в таблицу."""
            if self.current_user_role != 'admin':
                messagebox.showerror("Ошибка", "У вас нет прав для добавления данных.")
                return

            # Собираем значения из полей ввода
            values = []
            for col in columns[1:]:
                value = entry_vars[col[0]].get().strip()  # Получаем значения из полей
                if value == "":
                    if col[0] in ['quantity', 'amount']:  # Если это числовые поля, можно оставить NULL
                        values.append(None)
                    else:
                        values.append(None)  # Для строковых полей можно оставить пустое значение (None)
                else:
                    # Для числовых полей пытаемся привести к нужному типу
                    if col[0] in ['quantity']:
                        try:
                            values.append(int(value))  # Преобразуем в целое число
                        except ValueError:
                            messagebox.showerror("Ошибка", f"Поле {col[1]} должно содержать число.")
                            return
                    elif col[0] in ['amount']:
                        try:
                            values.append(float(value))  # Преобразуем в число с плавающей точкой
                        except ValueError:
                            messagebox.showerror("Ошибка", f"Поле {col[1]} должно содержать число.")
                            return
                    else:
                        values.append(value)  # Строковые данные добавляем как есть

            # Проверяем, что обязательные поля (например, name) не пустые
            if not values[0]:  # если значение для name пустое
                messagebox.showerror("Ошибка", "Поле 'Наименование' обязательно для заполнения!")
                return

            # Формируем запрос с placeholders для безопасных вставок
            placeholders = ', '.join(['%s'] * len(values))  # Заполнители для значений

            try:
                with get_db_connection() as conn:
                    cur = conn.cursor()
                    query = f"INSERT INTO {table} ({', '.join(col[0] for col in columns[1:])}) VALUES ({placeholders})"
                    cur.execute(query, values)
                    conn.commit()
                    refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении данных: {e}")

        def delete_entry():
            if self.current_user_role != 'admin':
                messagebox.showerror("Ошибка", "У вас нет прав для удаления данных.")
                return
            selected_item = tree.selection()
            if selected_item:
                item_id = tree.item(selected_item[0])["values"][0]
                try:
                    with get_db_connection() as conn:
                        cur = conn.cursor()
                        cur.execute(f"DELETE FROM {table} WHERE id = %s", (item_id,))
                        conn.commit()
                        refresh_table()
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при удалении данных: {e}")

        def edit_entry():
            if self.current_user_role != 'admin':
                messagebox.showerror("Ошибка", "У вас нет прав для редактирования данных.")
                return
            selected_item = tree.selection()
            if selected_item:
                item_id = tree.item(selected_item[0])["values"][0]
                values = tree.item(selected_item[0])["values"][1:]

                edit_window = tk.Toplevel(self.root)
                edit_window.title(f"Редактирование {title}")

                edit_entry_vars = {col[0]: tk.StringVar(value=values[i]) for i, col in enumerate(columns[1:])}
                for i, col in enumerate(columns[1:]):
                    tk.Label(edit_window, text=col[1]).grid(row=i, column=0)
                    tk.Entry(edit_window, textvariable=edit_entry_vars[col[0]]).grid(row=i, column=1)

                def save_changes():
                    updated_values = [edit_entry_vars[col[0]].get() for col in columns[1:]]
                    set_clause = ', '.join([f"{col[0]} = %s" for col in columns[1:]])
                    try:
                        with get_db_connection() as conn:
                            cur = conn.cursor()
                            cur.execute(f"UPDATE {table} SET {set_clause} WHERE id = %s", (*updated_values, item_id))
                            conn.commit()
                            edit_window.destroy()
                            refresh_table()
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Ошибка при сохранении изменений: {e}")

                tk.Button(edit_window, text="Сохранить изменения", command=save_changes).grid(row=len(columns) - 1,
                                                                                              column=1)

        if self.current_user_role == 'admin':
            tk.Button(window, text="Добавить", command=add_entry).grid(row=2, column=0)
            tk.Button(window, text="Удалить", command=delete_entry).grid(row=2, column=1)
            tk.Button(window, text="Редактировать", command=edit_entry).grid(row=2, column=2)

        refresh_table()

    def show_monthly_profit(self):
        """Рассчитать и показать прибыль за месяц."""
        month = simpledialog.askstring("Прибыль за месяц", "Введите месяц (формат YYYY-MM):")
        if not month:
            return

        try:
            # Проверяем, что введенная дата имеет правильный формат
            datetime.strptime(month, '%Y-%m')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат месяца. Используйте формат YYYY-MM.")
            return

        # Добавляем день (01) к введенному месяцу
        month_start_date = f"{month}-01"
        month_end_date = f"{month}-01"  # Конец месяца с использованием SQL

        try:
            # Считаем прибыль: доходы от продаж минус расходы
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT get_monthly_profit(%s)", (month_start_date,))

                profit = cur.fetchone()[0]

                # Если прибыли нет, приравниваем к 0
                if profit is None:
                    profit = 0

                messagebox.showinfo("Прибыль за месяц", f"Прибыль за {month}: {profit} рублей")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расчете прибыли: {e}")

    def show_top_5_profitable_products(self):
        """Показать 5 самых доходных товаров и сохранить отчет в файл."""
        start_date = simpledialog.askstring("Топ-5 товаров", "Введите начальную дату (формат YYYY-MM-DD):")
        end_date = simpledialog.askstring("Топ-5 товаров", "Введите конечную дату (формат YYYY-MM-DD):")
        if not start_date or not end_date:
            return

        try:
            # Проверяем, что введенные даты имеют правильный формат
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат дат. Используйте формат YYYY-MM-DD.")
            return

        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM get_top_5_profitable_products(%s, %s)", (start_date, end_date))
            results = cur.fetchall()
            if not results:
                messagebox.showinfo("Топ-5 товаров", "Нет данных за указанный период.")
                return

            report_lines = [f"{row[0]}: {row[1]} рублей" for row in results]
            report = "\n".join(report_lines)

            # Показать результаты в окне
            messagebox.showinfo("Топ-5 товаров", report)

            # Сохранение отчета в файл
            file_path = filedialog.asksaveasfilename(
                title="Сохранить отчет",
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write("Топ-5 самых доходных товаров\n")
                        file.write(f"Период: {start_date} - {end_date}\n\n")
                        file.write(report)
                    messagebox.showinfo("Сохранение", f"Отчет успешно сохранен: {file_path}")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось сохранить отчет: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
