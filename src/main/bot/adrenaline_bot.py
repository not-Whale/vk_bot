import vk_api
import requests
import time as t
from random import randint
import src.main.bot.errors as e
import src.main.bot.read_json as rj
import src.main.user.client as client

MAX_INT = 2147483647
LOPATA_ID = '448223022'
PAY_URL = 'https://www.tinkoff.ru/rm/kravchenko.danila5/Nbfxk55061/'
LONG_POLL_SERVER_URL = 'https://api.vk.com/method/messages.getLongPollServer'
VK_TOKEN = 'f8d3e63fa555d25cb165f67626537b4f2eb1fd5ae397db5c216051a8683ac2ac51b84732e6ce69ca88ca8'

ADMIN_MAIN_MENU_KEYBOARD = rj.read_json('admin_main_keyboard')
ADMIN_NEED_HELP_KEYBOARD = rj.read_json('admin_need_help_keyboard')

CLIENT_MAIN_MENU_KEYBOARD = rj.read_json('client_main_keyboard')
CLIENT_CART_KEYBOARD = rj.read_json('client_cart_keyboard')
CLIENT_DELAY_KEYBOARD = rj.read_json('client_delay_keyboard')
CLIENT_ORDER_DONE_KEYBOARD = rj.read_json('client_order_done_keyboard')
CLIENT_PAYMENT_CHECK_KEYBOARD = rj.read_json('client_payment_check_keyboard')
CLIENT_PAYMENT_METHOD_KEYBOARD = rj.read_json('client_payment_method_keyboard')

GO_BACK_KEYBOARD = rj.read_json('go_back_keyboard')

ADMIN_LIST = []

MISUNDERSTANDING = [
    'Я не понимаю Вас :(',
    'Можете еще раз повторить? Я не расслышал, что Вы сказали',
    'Вы уверены, что хотите именно это?',
    'Я с радостью поддержал бы беседу, но пока не умею. Давайте сыграем по сценарию!',
    'Ничего не могу разобрать. Повторите, пожалуйста'
]


def format_input(answer):
    return answer.lower().replace(' ', '')


def print_error(error_message):
    print('\033[31mError! Message:')
    print(error_message)
    print('\033[0m')


# issue 18
def find_free_admin():
    return None


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
    def new_message(self, user_id, first_name, time, text):
        if str(user_id) in ADMIN_LIST:
            self.new_admin_message(user_id, time, text)
        else:
            self.new_client_message(user_id, first_name, text)

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
                    GO_BACK_KEYBOARD
                )
                current_user.set_menu_mode('delivery')
            elif text == 'Новая сделка':
                self.send_message(
                    user_id,
                    'Сколько энергетиков продано?',
                    GO_BACK_KEYBOARD
                )
                current_user.set_menu_mode('new_deal')
            else:
                self.send_message(
                    user_id,
                    'Такой команды нет, ты меня не обманешь)',
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
                        GO_BACK_KEYBOARD
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
                        GO_BACK_KEYBOARD
                    )
                except e.AmountError:
                    self.send_message(
                        user_id,
                        'У тебя нет столько энергетиков!',
                        GO_BACK_KEYBOARD
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
    def new_client_message(self, user_id, first_name, text):
        # current_user = None
        for i in range(len(self.clients)):
            if user_id == self.clients[i].get_user_id():
                current_user = self.clients[i]
                break
        else:
            current_user = client.Client(user_id, first_name)
            self.clients.append(current_user)
        if current_user.get_menu_mode() == 'start':
            if text == 'Начать':
                current_user.set_menu_mode('main')
                self.send_message(
                    user_id,
                    'Поехали!',
                    CLIENT_MAIN_MENU_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    'Для запуска бота напишите "Начать"'
                )
        elif current_user.get_menu_mode() == 'main':
            if text == 'Моя статистика':
                self.send_message(
                    user_id,
                    f'{current_user.get_user_name()}, '
                    f'Вы совершили {current_user.get_number_of_deals()} сделок, '
                    f'преобретя {current_user.get_energy_amount()} энергетиков!'
                )
            elif text == 'Купить энергетики':
                current_user.set_menu_mode('cart')
                self.send_message(
                    user_id,
                    'Сколько энергетиков Вам нужно?',
                    CLIENT_CART_KEYBOARD
                )
            elif text == 'Хочу сотрудничать':
                link = self.vk_session.method('users.get', values={'user_ids': f'{LOPATA_ID}'})[0]['id']
                self.send_message(
                    user_id,
                    'Если хочешь обсудить возможность сотрудничества, '
                    'получения скидки или просто поговорить с Лопатусом), '
                    f'пиши [id{link}|сюда]!'
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING) - 1)]
                )
        elif current_user.get_menu_mode() == 'cart':
            if text == '1':
                current_user.get_current_order().set_energy_amount(1)
                self.check_free_admin(current_user)
            elif text == '2':
                current_user.get_current_order().set_energy_amount(2)
                self.check_free_admin(current_user)
            elif text == '3':
                current_user.get_current_order().set_energy_amount(3)
                self.check_free_admin(current_user)
            elif text == '4':
                current_user.get_current_order().set_energy_amount(4)
                self.check_free_admin(current_user)
            elif text == 'Хочу больше!':
                current_user.set_menu_mode('big_order')
                self.send_message(
                    user_id,
                    'Сколько энергетиков Вы хотите купить?',
                    GO_BACK_KEYBOARD
                )
            elif text == 'Назад':
                current_user.set_menu_mode('main')
                self.send_message(
                    user_id,
                    'Возвращаюсь назад...',
                    CLIENT_MAIN_MENU_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING))]
                )
        elif current_user.get_menu_mode() == 'big_order':
            try:
                amount = int(text)
                if amount < 1:
                    raise e.AmountError
                else:
                    current_user.get_current_order().set_energy_amount(amount)
                    self.check_free_admin(current_user)
            except ValueError:
                if text == 'Назад':
                    current_user.set_menu_mode('cart')
                    self.send_message(
                        user_id,
                        'Возращаюсь назад...',
                        CLIENT_CART_KEYBOARD
                    )
                else:
                    self.send_message(
                        user_id,
                        'Не получилось обработать Ваш запрос. '
                        'Введите числом, сколько энергетиков Вам нужно!'
                    )
            except e.AmountError:
                self.send_message(
                    user_id,
                    'Вы хотите отдать нам энергетики? Так нельзя! :)'
                )
        elif current_user.get_menu_mode() == 'payment_method':
            if text == 'Переводом на Тинькофф по ссылке':
                current_user.set_menu_mode('payment_check')
                self.send_message(
                    user_id,
                    f'К оплате {current_user.get_current_order().get_energy_amount() * 65} рублей. '
                    'Чтобы перевести деньги на счёт Тинькофф, перейдите по ссылке: '
                    f'{PAY_URL}',
                    CLIENT_PAYMENT_CHECK_KEYBOARD
                )
            elif text == 'Переводом на карту Сбербанка':
                current_user.set_menu_mode('payment_check')
                self.send_message(
                    user_id,
                    f'К оплате {current_user.get_current_order().get_energy_amount() * 65} рублей. '
                    'Номер карты Сбербанк: 1234 1234 1234 1234'
                    'Перевод по номеру телефона: +7(900)123-45-67',
                    CLIENT_PAYMENT_CHECK_KEYBOARD
                )
            elif text == 'Переводом на карту Тинькофф':
                current_user.set_menu_mode('payment_check')
                self.send_message(
                    user_id,
                    f'К оплате {current_user.get_current_order().get_energy_amount() * 65} рублей. '
                    'Номер карты Тинькофф: 4321 4321 4321 4321'
                    'Перевод по номеру телефона: +7(900)123-45-67',
                    CLIENT_PAYMENT_CHECK_KEYBOARD
                )
            elif text == 'Оплачу наличными при получении':
                self.send_order_done_message(current_user)
            elif text == 'Отменить заказ':
                current_user.get_current_order().clear_order()
                current_user.set_menu_mode('main')
                self.send_message(
                    user_id,
                    'Заказ отменен!',
                    CLIENT_MAIN_MENU_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING))]
                )
        # issue 16
        elif current_user.get_menu_mode() == 'admin_delay':
            for i in range(len(self.admins)):
                self.send_message(
                    self.admins[i].get_user_id(),
                    f'Поступил новый заказ от @id{user_id}. '
                    f'Ответь ему, как только появится время!!!',
                    ADMIN_NEED_HELP_KEYBOARD
                )
        elif current_user.get_menu_mode() == 'payment_check':
            if text == 'Оплата произведена':
                self.send_order_done_message(current_user)
            elif text == 'Назад':
                current_user.set_menu_mode('payment_method')
                self.send_message(
                    user_id,
                    'Возращюсь назад...',
                    CLIENT_PAYMENT_METHOD_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING))]
                )
        elif current_user.get_menu_mode() == 'order_done':
            if text == 'Я получил заказ':
                current_user.set_menu_mode('main')
                current_user.get_current_order().clear_order()
                self.send_message(
                    user_id,
                    'Спасибо, что выбираете нас!',
                    CLIENT_MAIN_MENU_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING))]
                )

    def send_order_done_message(self, current_user):
        current_user.set_menu_mode('order_done')
        self.send_message(
            current_user.get_user_id(),
            f'Подходите в {current_user.get_current_order().get_admin().get_room_number()} '
            f'комнату. Заказ уже ждет Вас!',
            CLIENT_ORDER_DONE_KEYBOARD
        )

    def check_free_admin(self, current_user):
        free_admin = find_free_admin()
        if free_admin is None:
            current_user.set_menu_mode('admin_delay')
            self.send_message(
                current_user.get_user_id(),
                'К сожалению, нас сейчас нет в общежитии или мы все спим. '
                'Не нажимайте ничего, и мы свяжемся в вами. '
                'Либо Вы можете отменить заказ и попробовать еще раз позже.',
                CLIENT_DELAY_KEYBOARD
            )
        else:
            current_user.set_menu_mode('payment_method')
            current_user.get_current_order().set_admin(free_admin)
            self.send_message(
                current_user.get_user_id(),
                'Выберите удобный способ оплаты...',
                CLIENT_PAYMENT_METHOD_KEYBOARD
            )

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
                            self.new_message(user_id, first_name, time, text)
                            if text:
                                print(first_name + ' ' + second_name + ': "' + text + '" [' + t.ctime(time) + ']')
                            # обработка вложений (прикреплять больше 10 запрещено самим вк)
                            for i in range(1, 11):
                                if 'attach' + str(i) + '_type' in media.keys():
                                    print('    ' + media['attach' + str(i) + '_type'] + ': ' + media['attach' + str(i)])
            self.long_poll_ts = response['ts']
