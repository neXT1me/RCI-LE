import tkinter as tk
import command_gen
import json
import re
import pyvisa


def load_func_gui(model:str):
    gui = {
        'zup_tam': create_widgets_zup,
        '33220A': create_widgets_33220A
    }
    return gui[model]


def create_widgets_33220A(instr, win:tk.Frame):
    but = tk.Button(win, text='Auto-testing')
    but.pack()

def create_widgets_N3300A(instr, win:tk.Frame):
    but = tk.Button(win, text='Auto-testing')
    but.pack()
def create_widgets_zup(win: tk.Frame):
    but = tk.Button(win, text='Auto-testing')
    but.pack()



if __name__ == '__main__':
    pass