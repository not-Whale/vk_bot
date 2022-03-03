import json
from random import randint
import vk_api
import requests
import time as t

MAX_INT = 2147483647
VK_TOKEN = 'f8d3e63fa555d25cb165f67626537b4f2eb1fd5ae397db5c216051a8683ac2ac51b84732e6ce69ca88ca8'
LONG_POLL_SERVER_URL = 'https://api.vk.com/method/messages.getLongPollServer'

LOPATA_ID = '448223022'
DK_ID = ''
POLAND_ID = ''
ADMIN_LIST = [LOPATA_ID, DK_ID, POLAND_ID]

with open('../resources/buttons/main_menu.json', 'r', encoding='utf-8-sig') as test_key:
    KEYBOARD_TEST = json.load(test_key)
    KEYBOARD_TEST = json.dumps(KEYBOARD_TEST, ensure_ascii=False).encode('utf-8-sig')
    KEYBOARD_TEST = str(KEYBOARD_TEST.decode('utf-8-sig'))


def format_input(answer):
    return answer.lower().replace(' ', '')


def print_error(error_message):
    print('\033[31mError! Message:')
    print(error_message)
    print('\033[0m')


def read_json(file_name):
    with open('../resources/buttons/' + file_name + '.json', 'r', encoding='utf-8-sig') as json_keyboard:
        keyboard = json.dumps(json.load(json_keyboard), ensure_ascii=False).encode('utf-8-sig')
    return str(keyboard.decode('utf-8-sig'))


class Adrenaline_bot:
    def __init__(self):
        # объект сессии авторизации
        self.vk_session = None
        # настройки LongPoll
        self.long_poll_server = None
        self.long_poll_key = None
        self.long_poll_ts = None
        # для авторизации через пользователя
        self.auth_code = None
        self.remember_code = None
        # администраторы и клиенты
        self.admins = []
        self.clients = []

    # слушатель кода двухфакторки
    def auth_handler(self):
        self.auth_code = input('Введите код аутентификации...')
        while True:
            remember_device = format_input(input('Запомнить пользователя? (yes/no)'))
            if remember_device == 'yes':
                self.remember_code = True
                break
            elif remember_device == 'no':
                self.remember_code = False
                break
            print('Неверный формат ввода!')

    # авторизация пользователя
    def login_as_user(self):
        login, password = 'your_login', 'your_password'
        self.vk_session = vk_api.VkApi(
            login, password,
        )
        try:
            self.vk_session.auth()
            print('Авторизация пользователя успешна!')
        except vk_api.TwoFactorError:
            self.login_as_user_two_factor()
        except vk_api.AuthError as error_message:
            print_error(error_message)
            self.vk_session = None

    # авторизация пользователя с двухфакторкой
    def login_as_user_two_factor(self):
        login, password = 'your_login', 'your_password'
        self.vk_session = vk_api.VkApi(
            login, password,
            auth_handler=self.auth_handler
        )
        try:
            self.vk_session.auth()
            print('Двухфакторная авторизация пользователя успешна!')
        except vk_api.AuthError as error_message:
            print_error(error_message)
            self.vk_session = None

    # авторизация как сообщество
    def login_as_group(self):
        try:
            self.vk_session = vk_api.VkApi(token=VK_TOKEN)
            print('Авторизация сообщества успешна!')
        except vk_api.ApiError as error_message:
            print_error(error_message)
            self.vk_session = None
        except vk_api.VkApiError as error_message:
            print_error(error_message)
            self.vk_session = None

    # написать в чатик
    def send_message(self, user_id, message, keyboard=''):
        if keyboard == '':
            values = {'user_id': user_id, 'message': message, 'random_id': randint(0, MAX_INT)}
        else:
            values = {'user_id': user_id, 'message': message, 'random_id': randint(0, MAX_INT), 'keyboard': keyboard}
        self.vk_session.method('messages.send', values=values)

    # получить информацию об имени пользователя
    def get_username(self, user_id):
        response = self.vk_session.method('users.get', {'user_ids': user_id})[0]
        return [response['first_name'], response['last_name']]

    # инициализировать LongPoll
    def set_long_poll_server_params(self):
        values = {'lp_version': 3}
        long_poll = self.vk_session.method('messages.getLongPollServer', values=values)
        self.long_poll_server = long_poll['server']
        self.long_poll_key = long_poll['key']
        self.long_poll_ts = long_poll['ts']

    # get запрос к LongPoll
    def get_response(self):
        data = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=2'.format(
            server=self.long_poll_server,
            key=self.long_poll_key,
            ts=self.long_poll_ts)).json()
        return data

    # def change_lopata_status(self):
    #     self.is_lopata_home = not self.is_lopata_home
    #
    # def change_dk_status(self):
    #     self.is_dk_home = not self.is_dk_home
    #
    # def change_poland_status(self):
    #     self.is_poland_home = not self.is_poland_home
    #
    # def find_seller(self):
    #     if self.is_poland_home:
    #         pass
    #     elif self.is_dk_home:
    #         pass
    #     elif self.is_lopata_home:
    #         pass
    #     else:
    #         print('Нас пока что нет в общежитии, но мы обязательно свяжемся с вами!')
    #         ''' И сюда нужно колл о заказе прикрепить '''

    def new_message(self, user_id, first_name, flags, time, text, media):
        if str(user_id) in ADMIN_LIST:
            self.new_admin_message(user_id, flags, time, text, media)
        else:
            self.new_client_message(user_id, first_name, flags, time, text, media)

    def new_admin_message(self, admin_id, flags, time, text, media):
        pass

    def new_client_message(self, client_id, first_name, flags, time, text, media):
        pass

    def start_bot(self):
        # авторизация сообщества
        self.login_as_group()
        if self.vk_session is None:
            print_error('VK session is Null!')
            exit(1)

        # установка параметров LongPoll сервера
        self.set_long_poll_server_params()

        # цикл запросов к LongPoll серверу
        while True:
            response = self.get_response()
            updates = response['updates']
            if updates:
                print(updates)
                for update in updates:
                    action_code = update[0]
                    # набор текста пользователем
                    if action_code == 61:
                        user_id = update[1]
                        username = self.get_username(user_id)
                        first_name = username[0]
                        second_name = username[1]
                        print(first_name + ' ' + second_name + ' печатает...')
                    # новое сообщение в диалоге
                    elif action_code == 4:
                        user_id = update[3]
                        username = self.get_username(user_id)
                        first_name = username[0]
                        second_name = username[1]
                        flags = update[2]
                        time = update[4]
                        text = update[5]
                        media = update[6]
                        # если сообщение от пользователя
                        if not flags & 2:
                            self.new_message(user_id, first_name, flags, time, text, media)
                            if text:
                                print(first_name + ' ' + second_name + ': "' + text + '" [' + t.ctime(time) + ']')
                            # обработка вложений (прикреплять больше 10 запрещено самим вк)
                            for i in range(1, 11):
                                if 'attach' + str(i) + '_type' in media.keys():
                                    print('    ' + media['attach' + str(i) + '_type'] + ': ' + media['attach' + str(i)])
            self.long_poll_ts = response['ts']
