import tkinter as tk
from tkinter import ttk


def setup_custom_style():
    style = ttk.Style()

    # Настраиваем тему 'clam' (можно изменить на 'alt', 'default', 'classic')
    style.theme_use('clam')

    # Изменение цвета фона и текста вкладок
    style.configure('TNotebook.Tab',
                    background='lightblue',  # цвет вкладки
                    foreground='black',  # цвет текста на вкладке
                    padding=[10, 5],  # отступы внутри вкладки
                    font=('Helvetica', 12),
                    focuscolor=style.configure(".", background='lightblue')['background'])  # убираем фокус

    # Цвет активной вкладки
    style.map('TNotebook.Tab',
              background=[('selected', 'deepskyblue'), ('!selected', 'lightblue')],
              foreground=[('selected', 'white'), ('!selected', 'black')],
              focuscolor=[('selected', 'deepskyblue'),
                          ('!selected', 'lightblue')])  # убираем пунктир на активной вкладке
