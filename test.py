import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry('900x600')
        self.resizable(False, False)

        self.grid_rowconfigure(index=0, weight=1)
        # self.grid_columnconfigure(index=1, weight=40)
        # self.grid_rowconfigure(index=0, weight=1)
        # self.grid_columnconfigure(index=0, weight=1)

        self.notebook = ttk.Notebook(self, )
        self.notebook.grid(row=0, column=1, sticky="nsew")
        # self.notebook.pack(anchor='e', expand=True, fill=tk.BOTH)
        for i in range(5):
            a = tk.Frame()
            tk.Button(a).pack()
            self.notebook.add(a, text=str(i))
        self.notebook.add(ctk.CTkFrame(self.notebook), text="dopestim vkluchim eto")

        self.frame_menu = ctk.CTkFrame(self, border_color='red', border_width=2)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        # self.frame_menu.pack(anchor='w')
        self.setup_custom_style()


    def setup_custom_style(self):
        self.style = ttk.Style()

        # Настраиваем тему 'clam' (можно изменить на 'alt', 'default', 'classic')
        self.style.theme_use('clam')

        # Изменение цвета фона и текста вкладок
        self.style.configure('TNotebook.Tab',
                             background='lightblue',  # цвет вкладки
                             foreground='black',  # цвет текста на вкладке
                             padding=[20, 10],  # отступы внутри вкладки
                             width=15,
                             font=('Helvetica', 12))

        # Цвет активной вкладки
        self.style.map('TNotebook.Tab',
                       padding=[('selected', [20,10]), ('!selected', [10,5])],
                       background=[('selected', 'deepskyblue'), ('!selected', '#ED9121')],
                       foreground=[('selected', 'white'), ('!selected', 'black')],
                       focuscolor=[('selected', 'deepskyblue'),
                                   ('!selected', 'lightblue')])  # убираем пунктир на активной вкладке

if __name__ == '__main__':
    app = App()
    app.mainloop()