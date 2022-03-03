import vk_api
import requests
import time as t
from random import randint
import src.main.bot.errors as e
import src.main.bot.read_json as rj

MAX_INT = 2147483647
VK_TOKEN = 'f8d3e63fa555d25cb165f67626537b4f2eb1fd5ae397db5c216051a8683ac2ac51b84732e6ce69ca88ca8'
LONG_POLL_SERVER_URL = 'https://api.vk.com/method/messages.getLongPollServer'

ADMIN_MAIN_MENU_KEYBOARD = rj.read_json('admin_main_menu')
ADMIN_BACK_KEYBOARD = rj.read_json('admin_back')
KEYBOARD_TEST = rj.read_json('main_menu')

ADMIN_LIST = []


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

    # заполнение списка id админов
    def fill_admin_list(self):
        for i in range(len(self.admins)):
            ADMIN_LIST.append(self.admins[i].get_user_id())

    # обработчик входящего сообщения
    def new_message(self, user_id, first_name, time, text, media):
        if str(user_id) in ADMIN_LIST:
            self.new_admin_message(user_id, time, text)
        else:
            self.new_client_message(user_id, first_name, time, text, media)

    # если пишет админ
    def new_admin_message(self, user_id, time, text):
        current_user = None
        for i in range(len(self.admins)):
            if str(user_id) == self.admins[i].get_user_id():
                current_user = self.admins[i]
                break
        if current_user.get_menu_mode() == 'main':
            if text == 'На связи':
                self.send_message(
                    user_id,
                    'Статус: Online!',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
                current_user.set_online()
            elif text == 'Занят':
                self.send_message(
                    user_id,
                    'Статус: Offline!',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
                current_user.set_offline()
            elif text == 'Мои продажи':
                self.send_message(
                    user_id,
                    'Вы провели ' + str(len(current_user.get_deals_list())) + ' сделок!',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
            elif text == 'Новый завоз':
                self.send_message(
                    user_id,
                    'Сколько энергетиков сейчас на руках?',
                    ADMIN_BACK_KEYBOARD
                )
                current_user.set_menu_mode('delivery')
            elif text == 'Новая сделка':
                self.send_message(
                    user_id,
                    'Сколько энергетиков продано?',
                    ADMIN_BACK_KEYBOARD
                )
                current_user.set_menu_mode('new_deal')
            else:
                self.send_message(
                    user_id,
                    'Я не понимаю тебя :(',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
        elif current_user.get_menu_mode() == 'delivery':
            if text == 'Назад':
                self.send_message(
                    user_id,
                    'Возвращаюсь назад...',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
                current_user.set_menu_mode('main')
            else:
                try:
                    energy_amount = int(text)
                    self.send_message(
                        user_id,
                        'У тебя теперь ' + str(energy_amount) + ' энергетиков!',
                        ADMIN_MAIN_MENU_KEYBOARD
                    )
                    current_user.set_energy_amount(energy_amount)
                    current_user.set_menu_mode('main')
                except ValueError:
                    self.send_message(
                        user_id,
                        'Неверное значение, попробуй еще раз!',
                        ADMIN_BACK_KEYBOARD
                    )
        elif current_user.get_menu_mode() == 'new_deal':
            if text == 'Назад':
                self.send_message(
                    user_id,
                    'Возвращаюсь назад...',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
                current_user.set_menu_mode('main')
            else:
                try:
                    sold = int(text)
                    energy_amount = current_user.get_energy_amount()
                    if sold > energy_amount or sold < 1:
                        raise e.AmountError
                    new_energy_amount = energy_amount - sold
                    current_user.set_energy_amount(new_energy_amount)
                    current_user.set_menu_mode('main')
                    if sold > 0:
                        current_user.new_deal([sold, time])
                    self.send_message(
                        user_id,
                        'У тебя теперь ' + str(new_energy_amount) + ' энергетиков!',
                        ADMIN_MAIN_MENU_KEYBOARD
                    )
                except ValueError:
                    self.send_message(
                        user_id,
                        'Неверное значение, попробуй еще раз!',
                        ADMIN_BACK_KEYBOARD
                    )
                except e.AmountError:
                    self.send_message(
                        user_id,
                        'У тебя нет столько энергетиков!',
                        ADMIN_BACK_KEYBOARD
                    )
        elif current_user.get_menu_mode() == 'start':
            if text == 'Начать':
                current_user.set_menu_mode('main')
                self.send_message(
                    user_id,
                    'Поехали!',
                    ADMIN_MAIN_MENU_KEYBOARD
                )

    # если пишет покупатель
    def new_client_message(self, user_id, first_name, time, text, media):
        pass

    # добавление id админа в список
    def add_new_admin(self, admin_obj):
        self.admins.append(admin_obj)

    def start_bot(self):
        # авторизация сообщества
        self.login_as_group()
        if self.vk_session is None:
            print_error('VK session is Null!')
            exit(1)

        # установка параметров LongPoll сервера
        self.set_long_poll_server_params()

        # заполнения списка админов
        self.fill_admin_list()

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
                            self.new_message(user_id, first_name, time, text, media)
                            if text:
                                print(first_name + ' ' + second_name + ': "' + text + '" [' + t.ctime(time) + ']')
                            # обработка вложений (прикреплять больше 10 запрещено самим вк)
                            for i in range(1, 11):
                                if 'attach' + str(i) + '_type' in media.keys():
                                    print('    ' + media['attach' + str(i) + '_type'] + ': ' + media['attach' + str(i)])
            self.long_poll_ts = response['ts']
