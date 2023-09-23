"""
Скрипт создает приложение Tkinter для выбора и анализа зависимостей.

Автор: Давтян Эдмон
"""
from tkinter import Label, Button, Checkbutton, IntVar
from tkinter.constants import LEFT
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
from tkinter import messagebox as mbx


def check(variables):
    """
    Устанавливает значение первых шести переменных равным 1.

    Аргументы:
        variables (список): Список переменных.

    Возвращает:
        None
    """
    for var in variables[:6]:
        var.set(1)


def grap(app_local):
    """
    Создает окно с флажками и кнопками для выбора и анализа зависимостей.

    Аргументы:
        app_local (tk.Tk): Объект приложения Tkinter.

    Возвращает:
        None
    """
    # Создаем список переменных для флажков
    vars_list = [IntVar() for i in range(6)]

    # Создаем новое окно
    newWindow = tk.Toplevel(app_local)
    newWindow.geometry('540x360+100+100')

    # Создаем метку
    labelExample = tk.Label(newWindow, text="Какие зависимости вы бы хотели проанализировать?")
    labelExample.pack()

    # Устанавливаем значения флажков по умолчанию
    for i in range(6):
        vars_list[i].set(-1)

    # Создаем флажки
    c0 = Checkbutton(newWindow, text="Распределение периода занятости среди юношей",
                     variable=vars_list[0], onvalue=1, offvalue=0)

    c1 = Checkbutton(newWindow, text="Распределение периода занятости среди девушек",
                     variable=vars_list[1], onvalue=1, offvalue=0)

    c2 = Checkbutton(newWindow, text="Распределение студентов по часам самоподготовки в неделю",
                     variable=vars_list[2], onvalue=1, offvalue=0)

    c3 = Checkbutton(newWindow, text="Соотношение результата технического теста к количеству часов самоподготовки",
                     variable=vars_list[3], onvalue=1, offvalue=0)

    c4 = Checkbutton(newWindow, text="Распределение принятия на работу от этнической группы",
                     variable=vars_list[4], onvalue=1, offvalue=0)

    c5 = Checkbutton(newWindow, text="Распределение итоговых оценок в зависимости от статуса отношений",
                     variable=vars_list[5], onvalue=1, offvalue=0)

    # Создаем кнопки
    all_button = Button(newWindow, text="Выбрать все", command=lambda: check(vars_list))
    plot_button = Button(newWindow, text="Построить графики", command=lambda: create_grap(app_local, vars_list))

    # Размещаем флажки и кнопки в окне
    c0.pack()
    c1.pack()
    c2.pack()
    c3.pack()
    c4.pack()
    c5.pack()
    all_button.pack()
    plot_button.pack()


def create_grap(app_local, vars_list):
    """
    Создает график на основе выбранных переменных.

    Аргументы:
        app_local (object): Объект приложения.
        vars_list (list): Список выбранных переменных.

    Возвращает:
        None
    """
    # Получаем данные из модели таблицы приложения
    data = app_local.table.model.df

    # Создаем столбец 'st_time' и заполняем его значениями np.nan
    data['st_time'] = np.nan
    df = [data]

    # Преобразуем значения столбца 'studytime' в текстовые метки
    if 'studytime' in data:
        for col in df:
            col.loc[col['studytime'] == 1, 'st_time'] = 'меньше 2'
            col.loc[col['studytime'] == 2, 'st_time'] = 'от 2 до 5'
            col.loc[col['studytime'] == 3, 'st_time'] = 'от 5 до 10'
            col.loc[col['studytime'] == 4, 'st_time'] = 'больше 10'

    # Подсчитываем количество выбранных переменных
    counter = sum([1 if var.get() == 1 else 0 for var in vars_list])

    print(counter)
    if counter == 0:
        return
    if counter == 1:
        # Создаем график с одним подграфиком
        plt.rcParams['font.size'] = '20'
        fig, ax = plt.subplots()
    elif counter == 2:
        # Создаем график с двумя подграфиками
        plt.rcParams['font.size'] = '10'
        fig, ax = plt.subplots(1, 2)
    elif counter <= 4:
        # Создаем график с четырьмя подграфиками
        plt.rcParams['font.size'] = '10'
        fig, ax = plt.subplots(2, 2)
        maxj = 2
    elif counter <= 6:
        # Создаем график с шестью подграфиками
        plt.rcParams['font.size'] = '5'
        fig, ax = plt.subplots(2, 3)
        maxj = 3
    else:
        # Создаем график с восемью подграфиками
        plt.rcParams['font.size'] = '5'
        fig, ax = plt.subplots(2, 4)
        maxj = 4

    error = set()
    i, j = 0, 0
    if vars_list[0].get() == 1:
        if 'YearsOfExp' in data and 'Gender' in data:
            x = np.arange(3)
            grades = list(data[(data.Gender == "male")]["YearsOfExp"])
            y = np.array([grades.count(i) / len(grades) for i in range(3)])
        if counter < 2:
            ax.bar(x, y)
            ax.set_title("Распределение периода занятости среди юношей")
            ax.set_xlabel("Количество лет")
            ax.set_ylabel("Доля юношей")
            ax.set_xticks(x)
            ax.set_xticklabels(range(3))
            ax.set_xlim([0, 2])
        elif counter == 2:
            ax[j].bar(x, y)
            ax[j].set_title("Распределение периода занятости среди юношей")
            ax[j].set_xlabel("Количество лет")
            ax[j].set_ylabel("Доля юношей")
            ax[j].set_xticks(x)
            ax[j].set_xticklabels(range(3))
            ax[j].set_xlim([0, 2])
        else:
            ax[i, j].bar(x, y)
            ax[i, j].set_title("Распределение периода занятости среди юношей", fontsize=5)
            ax[i, j].set_xlabel("Количество лет", fontsize=5)
            ax[i, j].set_ylabel("Доля юношей", fontsize=5)
            ax[i, j].set_xticks(x)
            ax[i, j].set_xticklabels(range(3))
            ax[i, j].set_xlim([0, 2])
        j += 1
    else:
        if 'YearsOfExp' not in data:
            error.add('YearsOfExp')
        if 'Gender' not in data:
            error.add('Gender')

    if vars_list[1].get() == 1:
        if 'YearsOfExp' in data and 'Gender' in data:
            x = np.arange(3)
            grades = list(data[(data.Gender == "female")]["YearsOfExp"])
            y = np.array([grades.count(i) / len(grades) for i in range(3)])
        if counter < 2:
            ax.bar(x, y)
            ax.set_title("Распределение периода занятости среди девушек")
            ax.set_xlabel("Количество лет")
            ax.set_ylabel("Доля девушек")
            ax.set_xticks(x)
            ax.set_xticklabels(range(3))
            ax.set_xlim([0, 2])
        elif counter == 2:
            ax[j].bar(x, y)
            ax[j].set_title("Распределение периода занятости среди девушек")
            ax[j].set_xlabel("Количество лет")
            ax[j].set_ylabel("Доля девушек")
            ax[j].set_xticks(x)
            ax[j].set_xticklabels(range(3))
            ax[j].set_xlim([0, 2])
        else:
            ax[i, j].bar(x, y)
            ax[i, j].set_title("Распределение периода занятости среди женщин", fontsize=5)
            ax[i, j].set_xlabel("Количество лет", fontsize=5)
            ax[i, j].set_ylabel("Доля женщин", fontsize=5)
            ax[i, j].set_xticks(x)
            ax[i, j].set_xticklabels(range(3))
            ax[i, j].set_xlim([0, 2])
        j += 1
    else:
        if 'YearsOfExp' not in data:
            error.add('YearsOfExp')
        if 'Gender' not in data:
            error.add('Gender')

    if vars_list[2].get() == 1:
        if 'studytime' in data:
            if counter > 2 and j == maxj:
                i += 1
                j = 0
            if counter < 2:
                ax.hist(data["st_time"])
                ax.set_title("Распределение студентов по часам самоподготовки в неделю")
                ax.set_xlabel("Количество часов самоподготовки")
                ax.set_ylabel("Количество студентов")
            elif counter == 2:
                ax[j].hist(data["st_time"])
                ax[j].set_title("Распределение студентов по часам самоподготовки в неделю")
                ax[j].set_xlabel("Количество часов самоподготовки")
                ax[j].set_ylabel("Количество студентов")
            else:
                ax[i, j].hist(data["st_time"])
                ax[i, j].set_title("Распределение студентов по часам самоподготовки в неделю", fontsize=5)
                ax[i, j].set_xlabel("Количество часов самоподготовки", fontsize=5)
                ax[i, j].set_ylabel("Количество студентов", fontsize=5)

            j += 1
        else:
            if 'studytime' not in data:
                error.add('studytime')

    if vars_list[3].get() == 1:
        if 'studytime' in data and 'FuncCompSc' in data:
            if counter > 2 and j == maxj:
                i += 1
                j = 0

            studytime = [list(data[(data.st_time == i)]["FuncCompSc"]) for i in
                         ['меньше 2', 'от 2 до 5', 'от 5 до 10', 'больше 10']]

            if counter < 2:
                ax.boxplot(studytime, vert=0, labels=['меньше 2', 'от 2 до 5', 'от 5 до 10', 'больше 10'])
                ax.set_title("Соотношение результата к к/ч самоподготовки")
                ax.set_xlabel("Итоговый результат")
                ax.set_ylabel("Количество часов самоподготовки")
            elif counter == 2:
                ax[j].boxplot(studytime, vert=0, labels=['меньше 2', 'от 2 до 5', 'от 5 до 10', 'больше 10'])
                ax[j].set_title("Соотношение результата к к/ч самоподготовки")
                ax[j].set_xlabel("Итоговый результат")
                ax[j].set_ylabel("Количество часов самоподготовки")
            else:
                ax[i, j].boxplot(studytime, vert=0, labels=['меньше 2', 'от 2 до 5', 'от 5 до 10', 'больше 10'])
                ax[i, j].set_title("Соотношение результата к к/ч самоподготовки", fontsize=5)
                ax[i, j].set_xlabel("Итоговый результат", fontsize=5)
                ax[i, j].set_ylabel("Количество часов самоподготовки", fontsize=5)

            j += 1
        else:
            if 'FuncCompSc' not in data:
                error.add('FuncCompSc')
            if 'studytime' not in data:
                error.add('studytime')

    if vars_list[4].get() == 1:
        if 'EthnicGroup' in data and 'CallForInterview' in data:
            x = np.array([0, 1])
            grades1 = list(data[(data.EthnicGroup == "group A")]["CallForInterview"])
            y1 = np.array([grades1.count(0) / len(grades1), grades1.count(1) / len(grades1)])
            grades2 = list(data[(data.EthnicGroup == "group B")]["CallForInterview"])
            y2 = np.array([grades2.count(0) / len(grades2), grades2.count(1) / len(grades2)])
            grades3 = list(data[(data.EthnicGroup == "group C")]["CallForInterview"])
            y3 = np.array([grades3.count(0) / len(grades3), grades3.count(1) / len(grades3)])
            grades4 = list(data[(data.EthnicGroup == "group D")]["CallForInterview"])
            y4 = np.array([grades4.count(0) / len(grades4), grades4.count(1) / len(grades4)])
            grades5 = list(data[(data.EthnicGroup == "group E")]["CallForInterview"])
            y5 = np.array([grades5.count(0) / len(grades5), grades5.count(1) / len(grades5)])
            if counter < 2:
                ax.bar(x - 0.2, y1, width=0.4, label="Group A")
                ax.bar(x - 0.1, y2, width=0.4, label="Group B")
                ax.bar(x, y3, width=0.4, label="Group C")
                ax.bar(x + 0.1, y4, width=0.4, label="Group D")
                ax.bar(x + 0.2, y5, width=0.4, label="Group E")
                ax.set_title("Распределение принятия на работу от этнической группы")
                ax.set_xlabel("Итог отбора")
                ax.set_ylabel("Этническая группа")
                ax.set_xticks(x)
                ax.set_xticklabels(["Rejected", "Accepted"])
                ax.legend()
            elif counter == 2:
                ax.bar(x - 0.2, y1, width=0.4, label="Group A")
                ax.bar(x - 0.1, y2, width=0.4, label="Group B")
                ax.bar(x, y3, width=0.4, label="Group C")
                ax.bar(x + 0.1, y4, width=0.4, label="Group D")
                ax.bar(x + 0.2, y5, width=0.4, label="Group E")
                ax[j].set_title("Распределение принятия на работу от этнической группы")
                ax[j].set_xlabel("Итог отбора")
                ax[j].set_ylabel("Этническая группа")
                ax[j].set_xticks(x)
                ax[j].set_xticklabels(["Rejected", "Accepted"])
                ax[j].legend()
            else:
                ax[i, j].bar(x - 0.2, y1, width=0.4, label="Group A")
                ax[i, j].bar(x - 0.1, y2, width=0.4, label="Group B")
                ax[i, j].bar(x, y3, width=0.4, label="Group C")
                ax[i, j].bar(x + 0.1, y4, width=0.4, label="Group D")
                ax[i, j].bar(x + 0.2, y5, width=0.4, label="Group E")
                ax[i, j].set_title("Распределение принятия на работу от этнической группы", fontsize=5)
                ax[i, j].set_xlabel("Итог отбора", fontsize=5)
                ax[i, j].set_ylabel("Этническая группа", fontsize=5)
                ax[i, j].set_xticks(x)
                ax[i, j].set_xticklabels(["Rejected", "Accepted"])
                ax[i, j].legend()

            j += 1
        else:
            if 'CallForInterview' not in data:
                error.add('CallForInterview')
            if 'EthnicGroup' not in data:
                error.add('EthnicGroup')

    if vars_list[5].get() == 1:
        if 'Romantic' in data and 'FuncCompSc' in data and 'BehCompScore' in data:
            if counter > 2 and j == maxj:
                i += 1
                j = 0

            if counter < 2:
                colors = np.where(data['Romantic'] == 'yes', 1, 0)
                plt.scatter(data['FuncCompSc'], data['BehCompScore'], c=colors, cmap='tab10')
                plt.title('Распределение итоговых оценок в зависимости от статуса отношений', fontsize=15)
                plt.xlabel("FuncCompSc")
                plt.ylabel("BehCompScore")
            elif counter == 2:
                colors = np.where(data['Romantic'] == 'yes', 1, 0)
                ax[j].scatter(data['FuncCompSc'], data['BehCompScore'], c=colors, cmap='tab10')
                ax[j].set_title('Распределение итоговых оценок в зависимости от статуса отношений', fontsize=15)
                ax[j].set_xlabel("FuncCompSc")
                ax[j].set_ylabel("BehCompScore")
            else:
                colors = np.where(data['Romantic'] == 'yes', 1, 0)
                ax[i, j].scatter(data['FuncCompSc'], data['BehCompScore'], c=colors, cmap='tab10')
                ax[i, j].set_title('Распределение итоговых оценок в зависимости от статуса отношений', fontsize=5)
                ax[i, j].set_xlabel("FuncCompSc")
                ax[i, j].set_ylabel("BehCompScore")

            j += 1
        else:
            if 'Romantic' not in data:
                error.add('Romantic')
            if 'FuncCompSc' not in data:
                error.add('FuncCompSc')
            if 'BehCompScore' not in data:
                error.add('BehCompScore')

    if not error:
        fig.set_figwidth(15)
        fig.set_figheight(10)
        if counter <= 4:
            fig.subplots_adjust(wspace=0.7, hspace=0.5)
        else:
            fig.subplots_adjust(wspace=0.5, hspace=0.3)

        plt.show()
    else:
        mbx.showerror("Ошибка", "Нет необходимых параметров " + ', '.join(error))


# Открывает и отображает изображение в новом окне
def open_image(app_local):
    """
    Открывает и отображает изображение в новом окне.

    Args:
        app_local (Tk): Экземпляр приложения Tkinter.

    Returns:
        None
    """
    # Открытие изображения
    img = Image.open('../output/HR for students.png')
    # Изменение размера изображения
    img = img.resize((1280, 720), Image.ANTIALIAS)
    # Создание объекта ImageTk для отображения в Tkinter
    img = ImageTk.PhotoImage(img)
    # Создание нового окна
    new = tk.Toplevel(app_local)
    # Создание метки для отображения изображения
    label = Label(new, image=img)
    # Привязка изображения к метке
    label.image = img
    # Размещение метки в окне
    label.pack(side=LEFT)
