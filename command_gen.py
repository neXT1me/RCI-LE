import pyvisa
from time import sleep
# автоматический выбор запроса


# --------------------------- Набор комманд для связи "TCPIP" ------------------------------------------
def output(instrument, command, delay=None):
    return instrument.query(command, delay=delay) if '?' in command else instrument.write(command)


# Выдача информации о запросе
def take_info(instrument, command):
    return instrument.query(command)


# Вкл sine сигнал
def func(instrument, func_sign='sin'):
    return instrument.write(f'Func {func_sign}')


# Установка FM (фазовой) модуляции
def state_FM(instrument):
    return instrument.write('source:pm:state on')


# Установка типа модуляции
def modulation_type(instument, type:str, mode):
    mode, type = mode.lower(), type.lower()
    if not mode in ('off', 'on'):
        return ValueError('Выберите один из доступных режимов: on/off')
    elif not type.lower() in ('am', 'fm', 'pm', 'fsk'):
        return ValueError('Выберите один из доступных режимов: am/fm/pm/fsk')
    else:
        return instument.write(f'source:{type}:state {mode}')


if __name__ == '__main__':
    modulation_type(1, 'fm', 'on')
