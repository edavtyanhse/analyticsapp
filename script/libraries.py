"""
Этот скрипт создает приложение Tkinter для выбора и анализа зависимостей.

Автор: Давтян Эдмон
"""
import os
import tkinter.filedialog as fl
import tkinter.messagebox as mbx
import tkinter.simpledialog as sl
import tkinter as tk
import pandas as pd
import numpy as np
from pandastable import Table, MultipleValDialog


# Импортирует таблицу из файла в приложение
def import_tab(app_local):
    """
    Импортирует таблицу из файла в приложение.

    Предлагает пользователю выбрать файл и определяет его расширение. В зависимости от расширения,
    функция загружает таблицу из файла Excel (xls или xlsx) или импортирует ее из файла CSV.

    Args:
        app_local (Tk): Экземпляр приложения Tkinter.

    Returns:
        None
    """
    # Запрос выбора файла у пользователя
    file_name = fl.askopenfilename()
    # Определение расширения файла
    file_extension = file_name.split('.')[-1]
    # Загрузка таблицы из файла Excel
    if file_extension == 'xls' or file_extension == 'xlsx':
        app_local.table.loadExcel(file_name)
    # Импорт таблицы из файла CSV
    elif file_extension == 'csv':
        ans = sl.askstring("Разделитель", "Введите разделитель:")
        app_local.table.importCSV(file_name, sep=ans)
    else:
        # Ошибка при неподдерживаемом формате файла
        mbx.showerror("Ошибка", "Файл должен быть в формате csv или xls (xlsx)")


def add_tab(app_local):
    """
    Добавляет новую вкладку с дочерней таблицей в приложение.

    Функция создает новую дочернюю таблицу в основной таблице приложения. Пользователю предлагается
    выбрать файл и определить его расширение. Если расширение файла - 'csv', пользователю предлагается
    ввести разделитель и данные из файла CSV импортируются в дочернюю таблицу. Если расширение файла
    - 'xls' или 'xlsx', данные загружаются из файла Excel в дочернюю таблицу. Если расширение файла
    не 'csv', 'xls' или 'xlsx', отображается сообщение об ошибке.

    Args:
        app_local (Tk): Экземпляр приложения Tkinter.

    Returns:
        None
    """
    # Создание дочерней таблицы в основной таблице
    app_local.table.createChildTable(None)

    # Запрос выбора файла у пользователя
    file_name = fl.askopenfilename()
    # Определение расширения файла
    file_extension = file_name.split('.')[-1]

    # Импорт данных из файла CSV
    if file_extension == 'csv':
        ans = sl.askstring("Разделитель", "Введите разделитель:")
        app_local.table.child.importCSV(file_name, sep=ans)
    # Загрузка данных из файла Excel
    elif file_extension == 'xls' or file_extension == 'xlsx':
        app_local.table.child.loadExcel(file_name)
    else:
        # Ошибка при неподдерживаемом формате файла
        mbx.showerror("Ошибка", "Файл должен быть в формате csv или xls (xlsx)")


def pivot_tab(app_local):
    """
    Генерирует отчет сводной таблицы на основе выбранных атрибутов и метода агрегации.

    Эта функция открывает окно, позволяющее пользователю выбрать два атрибута из данных таблицы
    и указать метод агрегации. Затем она генерирует сводную таблицу на основе выбранных атрибутов
    и отображает результат в новом окне. Пользователь может сохранить отчет в виде текстового файла.

    Аргументы:
        app_local (Tk): Экземпляр приложения Tkinter.

    Возвращает:
        None
    """
    # Запрос названий атрибутов и метода агрегации
    attributes = app_local.table.model.df.columns.tolist()

    # Создание окна выбора атрибутов
    attribute_window = tk.Toplevel()
    attribute_window.title("Выбор атрибутов")
    attribute_window.geometry("300x200")

    # Создание переменных для хранения выбранных атрибутов
    attribute1_var = tk.StringVar()
    attribute2_var = tk.StringVar()

    # Создание выпадающего списка для первого атрибута
    attribute1_label = tk.Label(attribute_window, text="Первый атрибут:")
    attribute1_label.pack()
    attribute1_menu = tk.OptionMenu(attribute_window, attribute1_var, *attributes)
    attribute1_menu.pack()

    # Создание выпадающего списка для второго атрибута
    attribute2_label = tk.Label(attribute_window, text="Второй атрибут:")
    attribute2_label.pack()
    attribute2_menu = tk.OptionMenu(attribute_window, attribute2_var, *attributes)
    attribute2_menu.pack()

    def generate_report():
        """
        Генерирует отчет сводной таблицы на основе выбранных атрибутов и метода агрегации.
        """
        attribute1 = attribute1_var.get()
        attribute2 = attribute2_var.get()
        aggregation = sl.askstring("Метод агрегации", "Введите метод агрегации (например, sum, mean, max, min):",
                                   parent=app_local.table.parentframe)

        if not attribute1 or not attribute2 or not aggregation:
            mbx.showwarning("Ошибка", "Необходимо выбрать атрибуты и ввести метод агрегации.",
                            parent=app_local.table.parentframe)
            return

        # Создание окна отчета
        report_window = tk.Toplevel()
        report_window.title("Сводная таблица")
        report_window.geometry("750x300")

        # Создание текстового поля для отчета
        report_text = tk.Text(report_window)
        report_text.pack(fill=tk.BOTH, expand=True)

        # Создание сводной таблицы
        pivot_table = pd.pivot_table(app_local.table.model.df, index=[attribute1, attribute2], aggfunc=aggregation)

        # Добавление содержимого сводной таблицы в текстовое поле
        report_text.insert(tk.END, str(pivot_table))

        def save_report():
            """
            Сохраняет отчет сводной таблицы в виде текстового файла.
            """
            # Запрашиваем у пользователя путь для сохранения файла
            file_path = fl.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

            if file_path:
                # Сохраняем отчет в указанный файл
                with open(file_path, "w") as f:
                    f.write(str(pivot_table))

        # Создание кнопки для сохранения отчета
        save_button = tk.Button(report_window, text="Сохранить отчет", command=save_report)
        save_button.pack()

        # Запрашиваем у пользователя выбор сохранить отчет или нет при закрытии окна
        report_window.protocol("WM_DELETE_WINDOW", lambda: handle_close_report(report_window))

        def handle_close_report(window):
            """
            Обрабатывает закрытие окна отчета.

            Эта функция вызывается при закрытии окна отчета. Она запрашивает у пользователя подтверждение
            сохранения отчета перед закрытием окна. Если пользователь соглашается, отчет сохраняется
            в виде текстового файла.

            Аргументы:
                window (Tk): Экземпляр окна отчета.

            Возвращает:
                None
            """
            save_confirm = mbx.askyesno("Сохранить отчет", "Хотите сохранить отчет перед закрытием?",
                                        parent=app_local.table.parentframe)
            if save_confirm:
                save_report()
            window.destroy()

    # Создание кнопки для генерации отчета
    generate_button = tk.Button(attribute_window, text="Сгенерировать отчет", command=generate_report)
    generate_button.pack()

    # Запуск главного цикла обработки событий окна выбора атрибутов
    attribute_window.mainloop()


def save_tab(app_local):
    """
    Сохраняет данные таблицы в файл.

    Параметры:
        app_local (object): Объект приложения, содержащий таблицу.

    Возвращает:
        None
    """
    # Запрос пути и имени файла для сохранения
    filename = fl.asksaveasfilename(parent=app_local.table.master,
                                    defaultextension='.csv',
                                    initialdir=os.getcwd(),
                                    filetypes=[("csv", "*.csv"),
                                               ("excel", "*.xls"),
                                               ("html", "*.html"),
                                               ("All files", "*.*")])

    if filename:
        # Сохранение данных таблицы в выбранный файл
        app_local.table.model.save(filename)


def merge_tab(app_local):
    """
    Объединяет таблицы.

    Параметры:
        app_local (object): Объект приложения, содержащий таблицы.

    Возвращает:
        None
    """
    if app_local.table.child is None:
        # Проверка на наличие добавочного справочника
        mbx.showwarning("Нет добавочного справочника", 'Вам необходимо загрузить справочник',
                        parent=app_local.table.parentframe)
        return

    # Объединение таблиц
    merged_table = pd.merge(app_local.table.model.df, app_local.table.child.model.df)
    print(merged_table)

    # Обновление данных таблицы
    app_local.table.model.df = merged_table
    app_local.table.update()
    app_local.table.redraw()
    app_local.table.tableChanged()


def search(app_local):
    """
    Открывает строку поиска в приложении для выполнения запросов к таблице.

    Параметры:
        app_local (object): Объект приложения, в котором будет открыта строка поиска.

    Возвращает:
        None
    """
    app_local.table.queryBar()


def add_rows(app_local):
    """
    Добавляет строки в таблицу в приложении.

    Параметры:
    - app_local (object): Объект приложения, в котором находится таблица.

    Возвращает:
    None
    """
    # Запрос количества объектов для добавления
    num = sl.askinteger("Сколько объектов добавить?", "Количество объектов:",
                        initialvalue=1, parent=app_local.table.parentframe)
    if not num:
        return

    # Сохранение текущего состояния таблицы
    app_local.table.storeCurrent()
    df = app_local.table.model.df

    if len(df) == 0:
        # Если таблица пуста, создание нового DataFrame с указанным количеством строк
        app_local.table.model.df = pd.DataFrame(pd.Series(range(num)))
        return

    try:
        ind = app_local.table.model.df.index.max() + 1
    except:
        ind = len(df) + 1

    # Создание нового DataFrame с пустыми значениями и указанным количеством строк
    new = pd.DataFrame(np.nan, index=range(ind, ind + num), columns=df.columns)
    app_local.table.model.df = pd.concat([df, new])
    app_local.table.model.df = app_local.table.model.df.convert_dtypes()

    # Обновление цветов строк таблицы
    app_local.table.update_rowcolors()

    # Перерисовка таблицы
    app_local.table.redraw()

    # Изменение таблицы (обновление внутреннего состояния)
    app_local.table.tableChanged()


def add_cols(app_local):
    """
    Добавляет столбцы в таблицу в приложении.

    Параметры:
    - app_local (object): Объект приложения, в котором находится таблица.

    Возвращает:
    None
    """
    # Задание типов столбцов
    coltypes = ['object', 'int64']

    # Открытие диалогового окна для ввода типов и имен столбцов
    d = MultipleValDialog(title='Новый параметр', initialvalues=(coltypes, ''),
                          labels=('Тип параметра', 'Имя параметра'),
                          types=('combobox', 'string'), parent=app_local.table.parentframe)

    if d.result is None:
        return
    else:
        dtype = d.results[0]
        newname = d.results[1]

    if newname is not None:
        if newname in app_local.table.model.df.columns:
            # Проверка наличия столбца с таким же именем
            mbx.showwarning("Ошибка", "Такой параметр уже существует!", parent=app_local.table.parentframe)
        else:
            # Сохранение текущего состояния таблицы
            app_local.table.storeCurrent()

            # Создание нового столбца с указанным именем и типом данных
            data = pd.Series(dtype=dtype)
            app_local.table.model.df[newname] = data
            app_local.table.model.df = app_local.table.model.df.convert_dtypes()

            # Настройка ширины родительского окна таблицы
            app_local.table.parentframe.configure(width=app_local.table.width)

            # Обновление цветов строк таблицы
            app_local.table.update_rowcolors()

            # Перерисовка таблицы
            app_local.table.redraw()

            # Изменение таблицы (обновление внутреннего состояния)
            app_local.table.tableChanged()


def delete_rows(app):
    """
    Удаляет строки из таблицы в приложении.

    Параметры:
    - app (object): Объект приложения, в котором находится таблица.

    Возвращает:
    None
    """
    # Запрос на количество удаляемых объектов
    num = sl.askinteger("Сколько объектов удалить?", "Количество объектов:",
                        initialvalue=1, parent=app.table.parentframe)
    if not num:
        return

    # Сохранение текущего состояния таблицы
    app.table.storeCurrent()
    df = app.table.model.df

    # Проверка на наличие данных в таблице
    if len(df) == 0:
        return

    indices = []
    for _ in range(num):
        # Запрос на индекс строки для удаления
        ind = sl.askinteger("Введите индекс строки для удаления", "Индекс строки:",
                            initialvalue=1, minvalue=1, maxvalue=len(df), parent=app.table.parentframe)
        if ind is None:
            return
        indices.append(ind)

    # Удаление выбранных строк из таблицы
    app.table.model.df = df.drop(indices)
    app.table.model.df = app.table.model.df.convert_dtypes()

    # Обновление цветов строк таблицы
    app.table.update_rowcolors()

    # Перерисовка таблицы
    app.table.redraw()

    # Изменение таблицы (обновление внутреннего состояния)
    app.table.tableChanged()


def delete_cols(app):
    """
    Удаляет столбцы из таблицы в приложении.

    Параметры:
    - app (object): Объект приложения, в котором находится таблица.

    Возвращает:
    None
    """
    # Запрос имени удаляемого столбца
    colname = sl.askstring("Удаление столбца", "Введите имя столбца для удаления:",
                           parent=app.table.parentframe)
    if colname is None:
        return

    # Проверка наличия столбца с указанным именем
    if colname not in app.table.model.df.columns:
        mbx.showwarning("Ошибка",
                        "Столбец с таким именем не существует!",
                        parent=app.table.parentframe)
    else:
        # Сохранение текущего состояния таблицы
        app.table.storeCurrent()

        # Удаление указанного столбца из таблицы
        app.table.model.df = app.table.model.df.drop(columns=[colname])
        app.table.model.df = app.table.model.df.convert_dtypes()

        # Настройка ширины родительского окна таблицы
        app.table.parentframe.configure(width=app.table.width)

        # Обновление цветов строк таблицы
        app.table.update_rowcolors()

        # Перерисовка таблицы
        app.table.redraw()

        # Изменение таблицы (обновление внутреннего состояния)
        app.table.tableChanged()


def statistical_report(app_local):
    """
    Генерирует статистический отчет на основе выбранного атрибута в таблице.

    Параметры:
    - app_local (object): Объект приложения, содержащий таблицу.

    Возвращает:
    None
    """
    window = tk.Tk()
    report_window = None
    frequency_table = [None]
    statistics_table = [None]

    def save_report():
        """
        Сохраняет отчет в файл, выбранный пользователем.
        """
        nonlocal report_window, frequency_table, statistics_table

        # Запрашиваем у пользователя путь для сохранения файла
        file_path = fl.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        if file_path:
            # Сохраняем отчет в указанный файл
            with open(file_path, "w") as f:
                if frequency_table[0] is not None:
                    f.write(str(frequency_table[0]))
                elif statistics_table[0] is not None:
                    f.write(str(statistics_table[0]))

    def handle_selection(attribute):
        """
        Обрабатывает выбор атрибута и генерирует соответствующий отчет.

        Параметры:
        - attribute: Выбранный атрибут.
        """
        nonlocal report_window, frequency_table, statistics_table

        window.destroy()  # Закрываем окно выбора атрибута

        if not attribute:
            mbx.showwarning("Ошибка", "Необходимо выбрать атрибут.", parent=app_local.table.parentframe)
            return

        attribute_data = app_local.table.model.df[attribute]

        if attribute_data.dtype == 'object':
            # Генерация отчета для качественного атрибута
            frequency_table[0] = attribute_data.value_counts().reset_index()
            frequency_table[0].columns = ['Значение', 'Частота']
            frequency_table[0]['Процент'] = frequency_table[0]['Частота'] / len(attribute_data) * 100

            # Создаем окно отчета
            report_window = tk.Toplevel()
            report_window.title("Отчет")
            report_window.geometry("500x300")

            # Создаем текстовое поле
            report_text = tk.Text(report_window)
            report_text.pack(fill=tk.BOTH, expand=True)

            # Добавляем содержимое отчета в текстовое поле
            report_text.insert(tk.END, str(frequency_table[0]))

            # Создаем кнопку для сохранения отчета
            save_button = tk.Button(report_window, text="Сохранить отчет", command=save_report)
            save_button.pack()

            # Запрашиваем у пользователя выбор сохранить отчет или нет при закрытии окна
            report_window.protocol("WM_DELETE_WINDOW", handle_close_report)

        elif pd.api.types.is_numeric_dtype(attribute_data):
            # Генерация отчета для количественного атрибута
            statistics_table[0] = pd.DataFrame({
                'Переменная': [attribute],
                'Максимум': [attribute_data.max()],
                'Минимум': [attribute_data.min()],
                'Среднее': [attribute_data.mean()],
                'Дисперсия': [attribute_data.var()],
                'Стандартное отклонение': [attribute_data.std()]
            })

            # Создаем окно отчета
            report_window = tk.Toplevel()
            report_window.title("Отчет")
            report_window.geometry("750x300")

            # Создаем текстовое поле
            report_text = tk.Text(report_window)
            report_text.pack(fill=tk.BOTH, expand=True)

            # Добавляем содержимое отчета в текстовое поле
            report_text.insert(tk.END, str(statistics_table[0]))

            # Создаем кнопку для сохранения отчета
            save_button = tk.Button(report_window, text="Сохранить отчет", command=save_report)
            save_button.pack()

            # Запрашиваем у пользователя выбор сохранить отчет или нет при закрытии окна
            report_window.protocol("WM_DELETE_WINDOW", handle_close_report)

        else:
            mbx.showwarning("Ошибка", "Атрибут должен быть либо качественным, либо количественным.",
                            parent=app_local.table.parentframe)
            return

    def handle_close_report():
        """
        Обрабатывает закрытие окна отчета и предлагает пользователю сохранить отчет.
        """
        nonlocal report_window

        close_report = mbx.askyesno("Сохранить отчет", "Хотите сохранить отчет перед закрытием?", parent=report_window)

        if close_report:
            save_report()  # Сохраняем отчет
        report_window.destroy()  # Закрываем окно отчета

    # Создание окна выбора атрибута
    window.title("Выберите атрибут")
    window.geometry("300x100")

    # Создание выпадающего списка
    attribute_var = tk.StringVar(window)
    attribute_var.set(app_local.table.model.df.columns[0])
    attribute_optionmenu = tk.OptionMenu(window, attribute_var, *app_local.table.model.df.columns)
    attribute_optionmenu.pack()

    # Создание кнопки для подтверждения выбора
    select_button = tk.Button(window, text="Выбрать", command=lambda: handle_selection(attribute_var.get()))
    select_button.pack()

    # Запуск главного цикла окна
    window.mainloop()


def generate_report(app_local):
    """
    Генерирует отчет на основе выбранных столбцов и отфильтрованных строк.

    Параметры:
        - app_local: Объект приложения, содержащий таблицу.
    """
    # Создание окна выбора столбцов
    column_window = tk.Toplevel()
    column_window.title("Выберите атрибуты")
    column_window.geometry("300x200")

    # Создание списка доступных столбцов
    available_columns = app_local.table.model.df.columns

    # Создание Listbox для выбора столбцов
    selected_columns = tk.StringVar(value=available_columns)
    columns_listbox = tk.Listbox(column_window, listvariable=selected_columns, selectmode=tk.MULTIPLE)
    columns_listbox.pack()

    def handle_selection():
        """
        Обрабатывает выбор столбцов и фильтрацию строк.

        Эта функция вызывается, когда пользователь подтверждает выбор столбцов.

        Применяется операция проекции для выбранных столбцов и операция фильтрации для строк.
        Затем создается окно отчета для отображения отфильтрованного DataFrame и предоставления опции сохранения отчета.

        Если не указаны условия фильтрации строк, отображается предупреждающее сообщение.

        Если окно отчета закрывается, пользователю предлагается сохранить отчет перед закрытием.
        """
        selected_indices = columns_listbox.curselection()
        selected_columns = [available_columns[index] for index in selected_indices]

        # Закрытие окна выбора столбцов
        column_window.destroy()

        # Запрос условия фильтрации строк
        rows = sl.askstring("Строки", "Введите условие фильтрации строк:", parent=app_local.table.parentframe)

        if not rows:
            mbx.showwarning("Ошибка", "Пожалуйста, введите условие фильтрации строк", parent=app_local.table.parentframe)
            return

        # Применение операции проекции для выбранных столбцов
        projected_df = app_local.table.model.df[selected_columns]

        # Применение операции фильтрации для строк
        filtered_df = projected_df.query(rows)

        # Создание окна отчета
        report_window = tk.Toplevel()
        report_window.title("Отчет")
        report_window.geometry("750x300")

        # Создание текстового поля
        report_text = tk.Text(report_window)
        report_text.pack(fill=tk.BOTH, expand=True)

        # Добавление содержимого отчета в текстовое поле
        report_text.insert(tk.END, str(filtered_df))

        def save_report():
            """
            Сохраняет отчет в выбранный пользователем файл.

            Эта функция вызывается, когда пользователь нажимает кнопку "Сохранить отчет".

            Пользователю предлагается выбрать путь файла для сохранения отчета в формате текстового файла.
            Если указан путь файла, отчет сохраняется в указанный файл.
            """
            # Запрос пути файла для сохранения отчета
            file_path = fl.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

            if file_path:
                # Сохранение отчета в указанный файл
                with open(file_path, "w") as f:
                    f.write(str(filtered_df))

        # Создание кнопки для сохранения отчета
        save_button = tk.Button(report_window, text="Сохранить отчет", command=save_report)
        save_button.pack()

        # Предложение пользователю подтвердить сохранение отчета при закрытии окна
        report_window.protocol("WM_DELETE_WINDOW", lambda: handle_close_report(report_window))

        def handle_close_report(window):
            """
            Обрабатывает закрытие окна отчета.

            Эта функция вызывается при закрытии окна отчета.

            Пользователю предлагается подтвердить сохранение отчета перед закрытием окна.
            Если пользователь выбирает сохранить отчет, вызывается функция save_report для сохранения отчета.
            Затем окно отчета закрывается.
            """
            close_report = mbx.askyesno("Сохранить отчет", "Вы хотите сохранить отчет перед закрытием?",
                                        parent=window)

            if close_report:
                save_report()  # Сохранение отчета
            window.destroy()  # Закрытие окна отчета

        # Запуск основного цикла окна отчета
        report_window.mainloop()

    # Создание кнопки для подтверждения выбора столбцов
    confirm_button = tk.Button(column_window, text="Создать", command=handle_selection)
    confirm_button.pack()

    # Запуск основного цикла окна выбора столбцов
    column_window.mainloop()


class TestApp(tk.Frame):
    """
    TestApp - пользовательский класс на основе фрейма Tkinter, представляющий основное приложение.

    Предоставляет графический интерфейс пользователя (GUI) для отображения и взаимодействия с таблицами.

    Атрибуты:
        - parent: Родительский виджет.

    Методы:
        - __init__(self, parent): Инициализирует класс TestApp.
    """

    def __init__(self, parent):
        """
        Инициализирует класс TestApp.

        Параметры:
            - parent: Родительский виджет.
        """
        super().__init__(parent)
        self.table = Table(self, showstatusbar=True)
        self.table.show()


if __name__ == "__main__":
    root = tk.Tk()
    app_local = TestApp(root)
    app_local.pack()
    root.mainloop()
