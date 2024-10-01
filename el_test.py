import customtkinter as ctk

# Инициализация библиотеки customtkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Основное окно
root = ctk.CTk()
root.geometry("400x300")

# Функция для переключения вкладок
def show_frame(frame):
    frame.tkraise()

# Фрейм для вкладок (кнопок)
tab_frame = ctk.CTkFrame(root, height=40)
tab_frame.pack(side="top", fill="x")

# Основные фреймы для вкладок
frame1 = ctk.CTkFrame(root)
frame2 = ctk.CTkFrame(root)
frame3 = ctk.CTkFrame(root)

for frame in (frame1, frame2, frame3):
    frame.place(x=0, y=40, relwidth=1, relheight=1)

# Добавление контента в фреймы
label1 = ctk.CTkLabel(frame1, text="This is Tab 1")
label1.pack(pady=20)

label2 = ctk.CTkLabel(frame2, text="This is Tab 2")
label2.pack(pady=20)

label3 = ctk.CTkLabel(frame3, text="This is Tab 3")
label3.pack(pady=20)

# Кнопки для переключения вкладок
button1 = ctk.CTkButton(tab_frame, text="Tab 1", command=lambda: show_frame(frame1))
button1.pack(side="left", expand=True)

button2 = ctk.CTkButton(tab_frame, text="Tab 2", command=lambda: show_frame(frame2))
button2.pack(side="left", expand=True)

button3 = ctk.CTkButton(tab_frame, text="Tab 3", command=lambda: show_frame(frame3))
button3.pack(side="left", expand=True)

# Показываем первую вкладку по умолчанию
show_frame(frame1)

# Запуск основного цикла
root.mainloop()