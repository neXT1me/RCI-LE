import pyvisa
# import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import style_notebook

import threading
import time
import json
import re

from set_of_interfaces import load_func_gui


def find_object_index(objects_list, attr_name, attr_value):
    """
    Находит индекс объекта в списке объектов по заданному параметру.

    :param objects_list: Список объектов.
    :param attr_name: Имя атрибута для поиска.
    :param attr_value: Значение атрибута для поиска.
    :return: Индекс объекта или None, если объект не найден.
    """
    for index, obj in enumerate(objects_list):
        # Проверяем, если объект имеет нужное свойство и его значение совпадает с искомым
        if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
            return index
    return None

# class

class LabInstrument:
    '''
    Класс объектов "Лабораторные инструменты".
    В данный класс входят праметры для отправки и приема команд на устройство.
    '''
    def __init__(self, rm: pyvisa.ResourceManager, resource_name:str):
        self.rm = rm
        self.resource_name = resource_name
        self.interface_type = None
        self.communication_channel = None

        self.address = None
        self.address_com = None

        self.manufacturer = None
        self.model = None

        self.format_command = None
        # Коданда определяющее модель
        self.command_identification = None
        self.delay = 0
        # Команда определяющая устройтва
        self.device_detection_command = None
        self.ready_status = False
        self.frame = None


        self.open_channel()


    def open_channel(self):
        '''
        Функция для открытия канала связи, проверки обратной связи
        и определения прочих параметров устройства
        4 - rs232/485
        6 - TCPIP

        '''
        info_commands = {4:['{start}MDL?{end}', '{start}*IDN?{end}'], 6: ['*IDN?']}
        format_commands = [[':', '', ';'], ['', ' ', '']]
        try:
            self.communication_channel = self.rm.open_resource(self.resource_name)
        except:
            print('Не удалось открыть канал связи с устройством')
            return None
        self.interface_type = self.communication_channel.interface_type.value
        # TCPIP
        if self.interface_type == 6:
            for command in info_commands[6]:
                try:
                    text = self.communication_channel.query(command)
                    # Обработка полученных данных
                    idn_info = text.split(',')
                    self.manufacturer = idn_info[0]
                    self.model = idn_info[1]
                    print(self.model)
                    self.ready_status = True
                    self.command_identification = command
                    # self.frame = loaыфd_func_gui(self.model)(tk.Frame(), self.communication_channel)
                    break
                except:
                    pass
            else:
                return None
            return text

        # Serial
        elif self.interface_type == 4:
            com_adr = str(re.search(r'\d{1,2}' ,
                                    re.search(r'ASRL\d{1,2}::', self.resource_name).group()).group()).zfill(2)
            # Выгружаем данные
            try:
                with open('serial_address.json', 'r') as f_adr:
                    self.address = json.loads(f_adr.read())[com_adr]
            except:
                print('Нет адреса устройства')

            # Обратная связь
            for form in format_commands:
                for command in info_commands[4]:
                    command_send = command.format(start=form[0], end=form[2])
                    for i in range(2):
                        try:
                            if i == 1:
                                ddc = '{start}ADR{mid}{address}{end}'.format(start=form[0], mid=form[1], end=form[2],
                                                                             address=self.address)
                                self.communication_channel.write(ddc)
                                time.sleep(0.03)
                            text = self.communication_channel.query(command_send, 0.03)
                            self.delay = 0.03

                            self.command_identification = command_send
                            self.device_detection_command = ddc
                            self.ready_status = True
                            if 'IDN' in command_send:
                                idn_info = text.split(',')
                                self.manufacturer = idn_info[0]
                                self.model = idn_info[1]
                            elif 'MDL' in command_send:
                                self.model = text

                            return 0
                        except:
                            continue
                else:
                    return None


    def write(self, command):
        if self.communication_channel:
            if self.device_detection_command:
                self.communication_channel.write(self.device_detection_command)
                time.sleep(self.delay)
                self.communication_channel.write(command)
            else:
                self.communication_channel.write(command)
        else:
            # raise pyvisa.LibraryError("dopystim")
            pass

    def read(self):
        if self.communication_channel:
            return self.communication_channel.read()
        else:
            # raise pyvisa.LibraryError("dopystim")
            pass


    def query(self, command):
        if self.communication_channel:
            if self.device_detection_command:
                self.communication_channel.write(self.device_detection_command, delay=self.delay)

                return self.communication_channel.query(command, delay=self.delay)

            else:
                return self.communication_channel.query(command, delay=self.delay)
        else:
            raise pyvisa.LibraryError(f"Не открыт канал передачи данных с данным устройстом :{self.interface_type}")


    def test_feedback(self):
        if self.ready_status:
            if self.communication_channel:
                if self.device_detection_command:
                    self.communication_channel.write(self.device_detection_command, delay=self.delay)
                    try:
                        self.communication_channel.query(self.command_identification, delay=self.delay)
                    except:
                        self.ready_status = None
                else:
                    try:
                        self.communication_channel.query(self.command_identification, delay=self.delay)
                    except:
                        self.ready_status = None

    def __del__(self):
        if self.frame:
            self.frame.destroy()
        if self.communication_channel:
            self.communication_channel.close()


class App(tk.Tk):

        def __init__(self):
            super().__init__()
            self.instruments_data = []
            self.rm = pyvisa.ResourceManager('')

            self.geometry('1000x650')
            self.resizable(False, False)


            self.grid_rowconfigure(index=0, weight=1)

            self.grid_columnconfigure(index=1, weight=8)
            self.grid_columnconfigure(index=0, weight=1)

            self.frame_menu = tk.Frame(self, background='red')
            self.frame_menu.grid(row=0, column=0, sticky="nsew")

            self.notebook = ttk.Notebook(self)
            self.notebook.grid(row=0, column=1, sticky="nsew")

            self.butt_instruments = tk.Button(self.frame_menu, text='Instruments', pady=15)
            self.butt_instruments.pack(fill=tk.X, padx=10, pady=10, anchor='s', side='top')

            self.butt_auto_testing = tk.Button(self.frame_menu, text='Auto testing', pady=15, command=self.click_auto_testing)
            self.butt_auto_testing.pack(fill=tk.X, padx=10, pady=1, side='top')

            self.butt_settings = tk.Button(self.frame_menu, text='Settings', pady=15)
            self.butt_settings.pack(fill=tk.X, anchor='s', padx=10, pady=10, side='bottom')
            # # self.setup_custom_style()

            self.protocol('WM_DELETE_WINDOW', self.on_destroy)

            self.frame_auto_testing = tk.Frame(self)
            self.frame_auto_testing.grid(row=0, column=1)
            self.frame_auto_testing.pack_forget()

            for i in range(3):
                a = tk.Frame()
                tk.Button(a).pack()
                self.notebook.add(a, text=i)
            # self.thread = threading.Thread(target=self.test)
            # self.flag_stop = False
            # self.thread.start()

        def click_auto_testing(self):
            self.notebook.grid_remove()
            # self.

        def setup_custom_style(self):
            self.style = ttk.Style()

            # Настраиваем тему 'clam' (можно изменить на 'alt', 'default', 'classic')
            self.style.theme_use('clam')

            # Изменение цвета фона и текста вкладок
            self.style.configure('TNotebook.Tab',
                            background='lightblue',  # цвет вкладки
                            foreground='black',  # цвет текста на вкладке
                            padding=[10, 5],  # отступы внутри вкладки
                            font=('Helvetica', 12))

            # Цвет активной вкладки
            self.style.map('TNotebook.Tab',
                      background=[('selected', 'deepskyblue'), ('!sЦlected', 'lightblue')],
                      foreground=[('selected', 'white'), ('!selected', 'black')],
                      focuscolor=[('selected', 'deepskyblue'),
                                  ('!selected', 'lightblue')])  # убираем пунктир на активной вкладке

        def test(self):
            while not self.flag_stop:
                self.changing_tabs()
                time.sleep(2)
        def changing_tabs(self):
            data_instruments = set([instr.resource_name for instr in self.instruments_data])

            ni_instruments = set(self.rm.list_resources())

            # Обрабатываем ситуации:
            # 1) В драйвере и базе есть инструменты:
            if instruments := list(data_instruments & ni_instruments):
                print(1)
                for instr in instruments:
                    index = find_object_index(self.instruments_data, 'resource_name', instr)
                    self.instruments_data[index].test_feedback()
                    if not self.instruments_data[index].ready_status:
                        del self.instruments_data[index]


            # 2) В драйвере нет инструмента а в базе есть
            if instruments := list(data_instruments - ni_instruments):
                print(2)
                for instr in instruments:
                    index = find_object_index(self.instruments_data, 'resource_name', instr)
                    del self.instruments_data[index]

            # 3) В драйвере есть инструмент, а в базе нет
            if instruments := list(ni_instruments - data_instruments):
                print(3)
                for instr in instruments:
                    self.instruments_data.append(LabInstrument(self.rm, instr))
                    if not self.instruments_data[-1].ready_status:
                        del self.instruments_data[-1]
                    else:
                        self.instruments_data[-1].frame = tk.Frame(self.notebook)
                        self.notebook.add(self.instruments_data[-1].frame, text=self.instruments_data[-1].model)
                        load_func_gui(self.instruments_data[-1].model)(self.instruments_data[-1].communication_channel,
                                                                       self.instruments_data[-1].frame)

        def on_destroy(self):
            self.flag_stop = True
            while self.thread.is_alive():
                pass
            for i in range(len(self.instruments_data)):
                del self.instruments_data[i]
            self.destroy()











if __name__ == '__main__':
    app_1 = App()
    app_1.mainloop()


    # rm = pyvisa.ResourceManager()
    # list_1 = rm.list_resources()
    # print(list_1)
    #
    #
    # a = LabInstrument(rm, list_1[0])
    # print(a.query('*IDN?'))
    # # a.write('test')
