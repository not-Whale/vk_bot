import json


def read_json(file_name):
    with open('../resources/buttons/' + file_name + '.json', 'r', encoding='utf-8-sig') as json_keyboard:
        keyboard = json.dumps(json.load(json_keyboard), ensure_ascii=False).encode('utf-8-sig')
    return str(keyboard.decode('utf-8-sig'))
