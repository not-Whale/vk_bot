import json


def read_json(file_name):
    """
    Чтение json-клавиатуры из файла.

    :param file_name: путь к файлу
    :return: строковое представление клавиатуры
    """
    with open('../resources/buttons/' + file_name + '.json', 'r', encoding='utf-8-sig') as json_keyboard:
        keyboard = json.dumps(json.load(json_keyboard), ensure_ascii=False).encode('utf-8-sig')
    json_keyboard.close()
    return str(keyboard.decode('utf-8-sig'))


def format_input(answer):
    """
    Удаление пробелов из строки и приведение её к нижнему регистру.

    :param answer: исходная строка
    :return: итоговая строка
    """
    return answer.lower().replace(' ', '')


def print_error(error_message):
    """
    Форматированный вывод ошибки.

    :param error_message: текст ошибки
    :return:
    """
    print('\033[31mError! Message:')
    print(error_message)
    print('\033[0m')
