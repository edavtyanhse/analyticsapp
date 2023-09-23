"""
Описание программы: Графический интерфейс для работы с таблицами данных HR.
Автор: Давтян Эдмон
"""

import tkinter as tk
import libraries
import scripts


if __name__ == '__main__':
    """
    Основная функция программы.
    """
    root = tk.Tk()
    root.geometry('1280x720+10+10')
    root.title('HR for students')

    topframe = tk.Frame(root, bg='#006666')
    topframe.pack(side=tk.TOP)

    app_local = libraries.TestApp(root)
    app_local.pack(fill=tk.BOTH, expand=1)

    button_bg = '#80c9b3'
    button_fg = 'white'

    def import_table_wrapper():
        """
        Функция-обертка для импорта таблицы.

        Вызывает функцию import_tab с переданным объектом приложения.
        """
        libraries.import_tab(app_local)


    def save_table_wrapper():
        """
        Функция-обертка для сохранения таблицы.

        Вызывает функцию save_tab с переданным объектом приложения.
        """
        libraries.save_tab(app_local)


    def add_table_wrapper():
        """
        Функция-обертка для добавления таблицы.

        Вызывает функцию add_tab с переданным объектом приложения.
        """
        libraries.add_tab(app_local)


    def pivot_table_wrapper():
        """
        Функция-обертка для объединения таблиц.

        Вызывает функцию pivot_tab с переданным объектом приложения.
        """
        libraries.pivot_tab(app_local)


    def search_wrapper():
        """
        Функция-обертка для поиска в таблице.

        Вызывает функцию search с переданным объектом приложения.
        """
        libraries.search(app_local)


    def add_rows_wrapper():
        """
        Функция-обертка для добавления строк в таблицу.

        Вызывает функцию add_rows с переданным объектом приложения.
        """
        libraries.add_rows(app_local)


    def add_cols_wrapper():
        """
        Функция-обертка для добавления столбцов в таблицу.

        Вызывает функцию add_cols с переданным объектом приложения.
        """
        libraries.add_cols(app_local)


    def delete_rows_wrapper():
        """
        Функция-обертка для удаления строк из таблицы.

        Вызывает функцию delete_rows с переданным объектом приложения.
        """
        libraries.delete_rows(app_local)


    def delete_cols_wrapper():
        """
        Функция-обертка для удаления столбцов из таблицы.

        Вызывает функцию delete_cols с переданным объектом приложения.
        """
        libraries.delete_cols(app_local)


    def open_image_wrapper():
        """
        Функция-обертка для открытия изображения.

        Вызывает функцию open_image с переданным объектом приложения.
        """
        scripts.open_image(app_local)


    def graphics():
        """
        Функция-обертка для генерации графиков.

        Вызывает функцию grap с переданным объектом приложения.
        """
        scripts.grap(app_local)


    def stat():
        """
        Функция-обертка для генерации статистического отчета.

        Вызывает функцию statistical_report с переданным объектом приложения.
        """
        libraries.statistical_report(app_local)


    def simple():
        """
        Функция-обертка для генерации простого отчета.

        Вызывает функцию generate_report с переданным объектом приложения.
        """
        libraries.generate_report(app_local)


    def merge_tab_wrapper():
        """
        Функция-обертка для объединения таблиц.

        Вызывает функцию merge_tab с переданным объектом приложения.
        """
        libraries.merge_tab(app_local)

    b1 = tk.Button(topframe, text="Открыть", command=import_table_wrapper, bg=button_bg, fg=button_fg)
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b2 = tk.Button(topframe, text="Найти", command=search_wrapper, bg=button_bg, fg=button_fg)
    b2.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(topframe, text="Графики", command=graphics, bg=button_bg, fg=button_fg)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    b4 = tk.Button(topframe, text="Названия столбцов", command=open_image_wrapper, bg=button_bg, fg=button_fg)
    b4.pack(side=tk.LEFT, padx=5, pady=5)
    b5 = tk.Button(topframe, text="Сохранить как...", command=save_table_wrapper, bg=button_bg, fg=button_fg)
    b5.pack(side=tk.LEFT, padx=5, pady=5)
    b6 = tk.Button(topframe, text="Сводная таблица", command=pivot_table_wrapper, bg=button_bg, fg=button_fg)
    b6.pack(side=tk.LEFT, padx=5, pady=5)
    b7 = tk.Button(topframe, text="Статистический отчет", command=stat, bg=button_bg, fg=button_fg)
    b7.pack(side=tk.LEFT, padx=5, pady=5)
    b8 = tk.Button(topframe, text="Простой отчет", command=simple, bg=button_bg, fg=button_fg)
    b8.pack(side=tk.LEFT, padx=5, pady=5)
    b9 = tk.Button(topframe, text="+Объект", command=add_rows_wrapper, bg=button_bg, fg=button_fg)
    b9.pack(side=tk.LEFT, padx=5, pady=5)
    b10 = tk.Button(topframe, text="+Параметр", command=add_cols_wrapper, bg=button_bg, fg=button_fg)
    b10.pack(side=tk.LEFT, padx=5, pady=5)
    b11 = tk.Button(topframe, text="-Объект", command=delete_rows_wrapper, bg=button_bg, fg=button_fg)
    b11.pack(side=tk.LEFT, padx=5, pady=5)
    b12 = tk.Button(topframe, text="-Параметр", command=delete_cols_wrapper, bg=button_bg, fg=button_fg)
    b12.pack(side=tk.LEFT, padx=5, pady=5)
    b13 = tk.Button(topframe, text="Добавить", command=add_table_wrapper, bg=button_bg, fg=button_fg)
    b13.pack(side=tk.LEFT, padx=5, pady=5)
    b14 = tk.Button(topframe, text="Объединить", command=merge_tab_wrapper, bg=button_bg, fg=button_fg)
    b14.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()
