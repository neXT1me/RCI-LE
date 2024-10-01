from pyvisa import *
import command_gen
from time import sleep

def get_info_instrument():
    rm = ResourceManager()
    return rm.list_resources()


def check_connected_device(list_id):
    instrument = {}

    # Проверка на подключенные устройства
    if not list_id:
        return print('Нет подключенных устройств')
    else:
        for i in range(len(list_id)):
            try:
                key = i
                instrument[i] = rm.open_resource(list_id[i])
            except:
                print(f'Ошибка по id: {list_id[i]}')
    return instrument

# Функция глубокой проверки подключенного устройства (Наличие обратной связи с прибором) ФГП
def checking_for_feedback(rm, inst_name):
    # Попытка на подкоючение, если его нет значит нет подключения к прибору и проверка не прошла
    try:
        with rm.open_resource(inst_name) as inst:
            # Проведения проверки для типа связи TCPIP
            if 'TCPIP' in inst_name: # Тут желательно описать считываение комманд с данных по прибору
                inst.write('*IDN?')
                return inst.read(), 'TCPIP', inst_name[inst_name.index(':')+2:][:inst_name[inst_name.index(':')+2:].index(':')]

            # Проведения проверки для последовательной связи
            elif 'ASRL' in inst_name:
                command_inst_for_com = [[':ADR{};', ':MDL?;'], ['ADR {}', '*IDN?']]
                with open('address_data.txt') as file:
                    file.readline()
                    file.readline()
                    adr_com = {i[0]: i[1] for i in [i.split('-') for i in file.readline().strip().split(', ')]}
                    for i in command_inst_for_com:
                        adr = adr_com[inst_name[inst_name.index('L') + 1:inst_name.index('::')]]
                        command = i[0].format(adr)
                        try:
                            inst.write(command)
                            sleep(0.015)
                            name = inst.query(i[1], 0.03)
                            return name.strip()+' '+adr.strip(), 'COM', adr
                        except:
                            return None, None, None
    except:
        print(f'Устройство: {inst_name} - может иметь ряд проблем: \n\t1) Нет открытия порта связи;'
              f'\n\t2) Нет отклика на отпраку команды.'
              f'\n\tЕсли данное устройство не требуется к эксплуатации, то отключите его не нагружая систему')
        return None, None, None


if __name__ == '__main__':
    # Сбор инфо по подключенным устройствам
    rm = ResourceManager('@py')
    list_id = rm.list_resources()
    print(list_id)
    # Активные приборы (проверка)
    instrument = check_connected_device(list_id)
    command_gen.output(instrument[1], 'freq 100')