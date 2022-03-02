from random import randint
import vk_api
import requests
import time as t

MAX_INT = 2147483647
VK_TOKEN = 'f8d3e63fa555d25cb165f67626537b4f2eb1fd5ae397db5c216051a8683ac2ac51b84732e6ce69ca88ca8'
LONG_POLL_SERVER_URL = 'https://api.vk.com/method/messages.getLongPollServer'


def format_input(answer):
    return answer.lower().replace(' ', '')


def print_error(error_message):
    print('\033[31mError! Message:')
    print(error_message)
    print('\033[0m')


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

    def write_msg(self, user_id, message):
        values = {'user_id': user_id, 'message': message, 'random_id': randint(0, MAX_INT)}
        self.vk_session.method('messages.send', values=values)

    def get_username(self, user_id):
        response = self.vk_session.method('users.get', {'user_ids': user_id})[0]
        return [response['first_name'], response['last_name']]

    def set_long_poll_server_params(self):
        values = {'lp_version': 3}
        long_poll = self.vk_session.method('messages.getLongPollServer', values=values)
        self.long_poll_server = long_poll['server']
        self.long_poll_key = long_poll['key']
        self.long_poll_ts = long_poll['ts']

    def get_response(self):
        data = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=2'.format(
            server=self.long_poll_server,
            key=self.long_poll_key,
            ts=self.long_poll_ts)).json()
        return data

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
                            self.write_msg(user_id, '%Ответ пользователю%')
                            if text:
                                print(first_name + ' ' + second_name + ': "' + text + '" [' + t.ctime(time) + ']')
                            # обработка вложений (больше 10 к сообщению прикреплять запрещено самим вк)
                            for i in range(1, 11):
                                if 'attach' + str(i) + '_type' in media.keys():
                                    print('    ' + media['attach' + str(i) + '_type'] + ': ' + media['attach' + str(i)])
            self.long_poll_ts = response['ts']


bot = Adrenaline_bot()
bot.start_bot()
