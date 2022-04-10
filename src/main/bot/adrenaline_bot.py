import os
import pickle
import vk_api
import requests
import time as t
from random import randint
from src.main.bot.constants import *
from src.main.bot.open_keys import *
from src.main.user.client import Client
from src.main.bot.errors import AmountError
from src.main.bot.utility_funcs import format_input, print_error


def handle_admin_delivery_and_get_energy_amount(current_user, text):
    """
    Выделение количества энергетиков на завозе.

    Внимание! Меняет значения полей menu_mode, energy_amount экземпляра
    current_user класса Admin.

    :param current_user: объект админа
    :param text: текст сообщения
    :raise AmountError: в случае если число введено некорректно
    :return: количество энерегтиков после завоза
    """
    energy_amount = int(text)
    if energy_amount < 0:
        raise AmountError
    current_user.set_menu_mode('main')
    current_user.set_energy_amount(energy_amount)
    return str(energy_amount)


def handle_admin_new_deal_and_get_energy_amount(current_user, text, time):
    """
    Выделение количества энергетиков после сделки.

    Внимание! Меняет значения полей menu_mode, energy_amount, deals
    экземпляра current_user класса Admin.

    :param current_user: объект админа
    :param text: текст сообщения
    :param time: время отправки сообщения
    :raise AmountError: в случае если число введено некорректно
    :return: количество энергетиков после совершения сделки
    """
    sold = int(text)
    energy_amount = current_user.get_energy_amount()
    if sold > energy_amount or sold < 1:
        raise AmountError
    current_user.set_menu_mode('main')
    new_energy_amount = energy_amount - sold
    current_user.set_energy_amount(new_energy_amount)
    if sold > 0:
        current_user.new_deal([sold, time])
    return str(new_energy_amount)


def check_and_create_backup_directory():
    """
    Проверка на наличие и в случае необходимости создание директории с файлами бэкапа.
    """
    if not os.path.exists(USER_RESOURCES_PATH):
        os.mkdir(USER_RESOURCES_PATH)


class Adrenaline_bot:
    """Бот для обработки сообщений в личных сообщениях сообщества или страницы вк."""
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
        # загрузка, если есть, базы пользователей
        self.load_clients()
        self.load_admins()

    def auth_handler(self):
        """
        Слушатель кода двухфакторной аутентификации.

        Внимание! Меняет значение полей auth_code, remember_code.

        :return:
        """
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
        """
        Авторизация в качестве пользователя.

        Метод используется в случае, если происходит авторизация аккаунта
        без двухфакторной аутентификации, иначе вызывается метод login_as_user_two_factor.

        Внимание! Меняет значение поля vk_session.

        :return:
        """
        self.vk_session = vk_api.VkApi(
            VK_LOGIN, VK_PASSWORD
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
        """
        Авторизация в качестве пользователя (с двухфакторной аутентификацией).

        Внимание! Меняет значение поля vk_session.

        :return:
        """
        self.vk_session = vk_api.VkApi(
            VK_LOGIN, VK_PASSWORD,
            auth_handler=self.auth_handler
        )
        try:
            self.vk_session.auth()
            print('Двухфакторная аутентификация пользователя прошла успешно!')
        except vk_api.AuthError as error_message:
            print_error(error_message)
            self.vk_session = None

    def login_as_group(self):
        """
        Авторизация в качестве сообщества (используется в актуальной версии).

        Внимание! Меняет значение поля vk_session.

        :return:
        """
        try:
            self.vk_session = vk_api.VkApi(token=VK_TOKEN)
            print('Авторизация сообщества успешна!')
        except vk_api.ApiError as error_message:
            print_error(error_message)
            self.vk_session = None
        except vk_api.VkApiError as error_message:
            print_error(error_message)
            self.vk_session = None

    def save_clients(self):
        """
        Сохранение списка клиентов в pickle-файл.

        :return:
        """
        check_and_create_backup_directory()
        with open(CLIENTS_PICKLE_PATH, 'wb') as clients_list:
            pickle.dump(self.clients, clients_list)
        clients_list.close()

    def save_admins(self):
        """
        Сохранение списка админов в pickle-файл.

        :return:
        """
        check_and_create_backup_directory()
        with open(ADMINS_PICKLE_PATH, 'wb') as admins_list:
            pickle.dump(self.admins, admins_list)
        admins_list.close()

    def load_clients(self):
        """
        Загрузка списка клиентов из pickle-файла.

        Внимание! Меняет значение поля clients.

        :return:
        """
        check_and_create_backup_directory()
        if os.path.exists(CLIENTS_PICKLE_PATH):
            with open(CLIENTS_PICKLE_PATH, 'rb') as clients_list:
                self.clients = pickle.load(clients_list)
            clients_list.close()

    def load_admins(self):
        """
        Загрузка списка админов из pickle-файла.

        Внимание! Меняет значение поля admins.

        :return:
        """
        check_and_create_backup_directory()
        if os.path.exists(ADMINS_PICKLE_PATH):
            with open(ADMINS_PICKLE_PATH, 'rb') as admins_list:
                self.admins = pickle.load(admins_list)
            admins_list.close()

    def set_clients_actual_keyboard(self):
        """
        Установка последней активной клавиатуры для клиента.

        Метод отправляет сообщение каждому клиенту, который ранее писал боту,
        с оповещением о том, что бот был перезапущен, и возвращает последнюю
        актуальную клавиатуру.

        :return:
        """
        for i in range(len(self.clients)):
            self.send_message(
                self.clients[i].get_user_id(),
                'Бот был перезапущен, '
                'Вы были возвращены на посленднюю точку взаимодействия с ним!',
                KEYBOARDS['client_' + self.clients[i].get_menu_mode()]
            )

    def set_admins_actual_keyboard(self):
        """
        Установка последней активной для админа.

        Метод отправляет сообщение каждому админу в списке админов, сообщая
        о том, что бот был перезапущен, если админ уже пользовался ботом ранее,
        либо с сообщением о том, что нужно запустить бота, если админ добавлен
        в список, но еще не пользовался ботом.

        :return:
        """
        for i in range(len(self.admins)):
            if self.admins[i].get_menu_mode() != 'start':
                self.send_message(
                    self.admins[i].get_user_id(),
                    'Бот был перезапущен!',
                    KEYBOARDS['admin_' + self.admins[i].get_menu_mode()]
                )
            else:
                self.send_message(
                    self.admins[i].get_user_id(),
                    'Напиши "Начать", чтобы перезапустить бота'
                )

    def send_message(self, user_id, message, keyboard=''):
        """
        Отправка сообщения в чат.

        :param user_id: индивидуальный номер диалога
        :param message: сообщение, которое необходимо отправить
        :param keyboard: строковое представление json-клавиатуры, defaults to ''
        :return:
        """
        if keyboard == '':
            values = {'user_id': user_id, 'message': message, 'random_id': randint(0, MAX_INT)}
        else:
            values = {'user_id': user_id, 'message': message, 'random_id': randint(0, MAX_INT), 'keyboard': keyboard}
        self.vk_session.method('messages.send', values=values)

    def get_username(self, user_id):
        """
        Определение имени пользователя по его id.

        :param user_id: id пользователя вк
        :returns: имя и фамилия пользователя
        """
        response = self.vk_session.method('users.get', {'user_ids': user_id})[0]
        return response['first_name'], response['last_name']

    def set_long_poll_server_params(self):
        """
        Инициализация LongPoll-сервера для получения сообщений.

        Внимание! Меняет значения полей long_poll_server, long_poll_key,
        long_poll_ts.

        :return:
        """
        values = {'lp_version': 3}
        long_poll = self.vk_session.method('messages.getLongPollServer', values=values)
        self.long_poll_server = long_poll['server']
        self.long_poll_key = long_poll['key']
        self.long_poll_ts = long_poll['ts']

    def get_response(self):
        """
        Отправка get-запроса к LongPoll-серверу и получение ответа.

        :return: ответ LongPoll-сервера
        """
        data = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2&version=2'.format(
            server=self.long_poll_server,
            key=self.long_poll_key,
            ts=self.long_poll_ts)).json()
        return data

    def fill_admin_list(self):
        """
        Заполнение списка id админов в случае перезапуска бота.

        Метод предназначен для восстановления списка id админов в случае перезапуска
        бота и последующего восстановления списка админов из pickle-файла.

        Внимание! Изменяет значение глобальной переменной ADMIN_LIST.

        :return:
        """
        for i in range(len(self.admins)):
            ADMIN_LIST.append(self.admins[i].get_user_id())

    def new_message(self, user_id, first_name, time, text):
        """
        Определение отправителя и дальнейшая обработка входящего сообщения.

        Метод определяет тип отправителя: клиент или админ, после чего вызывает
        соответствующий метод (либо new_admin_message, либо new_client_message).

        :param user_id: индивидуальный номер диалога
        :param first_name: имя отправителя сообщения
        :param time: время отправления сообщения
        :param text: текст сообщения
        :return:
        """
        if str(user_id) in ADMIN_LIST:
            self.new_admin_message(user_id, time, text)
        else:
            self.new_client_message(user_id, first_name, text)

    def define_admin_from_message(self, user_id):
        """
        Нахождения объекта админа по его id вк.

        :param user_id: id пользователя вк
        :return: объект админа либо None
        """
        for i in range(len(self.admins)):
            if str(user_id) == self.admins[i].get_user_id():
                return self.admins[i]
        else:
            return None

    def define_client_from_message(self, first_name, user_id):
        """
        Нахождение существующего объекта клиента по его id вк либо добавление нового.

        :param first_name: имя клиента (используется для инициализации нового объекта)
        :param user_id: id пользователя вк
        :return: объект клиента
        """
        for i in range(len(self.clients)):
            if user_id == self.clients[i].get_user_id():
                return self.clients[i]
        else:
            current_user = Client(user_id, first_name)
            self.clients.append(current_user)
            self.save_clients()
            return current_user

    def new_admin_message(self, user_id, time, text):
        """
        Обработка сообщения от админа.

        Метод определяет объект отправителя сообщения, после чего обрабатывает
        входящее сообщение в зависимости от его фактического положения в меню
        клавиатур.

        Внимание! Меняет значения полей menu_mode, is_online, energy amount,
        deals экземпляра current_user класса Admin.

        :param user_id: индивидуальный номер диалога
        :param time: время отправки сообщения
        :param text: текст сообщения
        :return:
        """
        current_user = self.define_admin_from_message(user_id)
        if current_user is None:
            print_error('Админа не найдено в списке!')
            exit(1)
        if current_user.get_menu_mode() == 'start':
            if text == 'Начать':
                current_user.set_menu_mode('main')
                self.save_admins()
                self.send_message(
                    user_id,
                    'Поехали!',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    'Чтобы запустить бота напиши "Начать"'
                )
        elif current_user.get_menu_mode() == 'main':
            if text == 'На связи':
                current_user.set_online()
                self.send_message(
                    user_id,
                    'Статус: Online!'
                )
            elif text == 'Занят':
                current_user.set_offline()
                self.send_message(
                    user_id,
                    'Статус: Offline!'
                )
            elif text == 'Мои продажи':
                self.send_message(
                    user_id,
                    'Ты провел ' + str(len(current_user.get_deals_list())) + ' сделок!'
                )
            elif text == 'Новый завоз':
                current_user.set_menu_mode('delivery')
                self.save_admins()
                self.send_message(
                    user_id,
                    'Сколько энергетиков сейчас на руках?',
                    GO_BACK_KEYBOARD
                )
            elif text == 'Новая сделка':
                current_user.set_menu_mode('new_deal')
                self.save_admins()
                self.send_message(
                    user_id,
                    'Сколько энергетиков продано?',
                    GO_BACK_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    'Такой команды нет, ты меня не обманешь)'
                )
        elif current_user.get_menu_mode() == 'delivery':
            if text == 'Назад':
                current_user.set_menu_mode('main')
                self.save_admins()
                self.send_message(
                    user_id,
                    'Возвращаюсь назад...',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
            else:
                try:
                    energy_amount = handle_admin_delivery_and_get_energy_amount(current_user, text)
                    self.save_admins()
                    self.send_message(
                        user_id,
                        'У тебя теперь ' + energy_amount + ' энергетиков!',
                        ADMIN_MAIN_MENU_KEYBOARD
                    )
                except ValueError:
                    self.send_message(
                        user_id,
                        'Неверное значение, попробуй еще раз!'
                    )
                except AmountError:
                    self.send_message(
                        user_id,
                        'У тебя не может быть отрицательное число энергетиков, попробуй еще раз!'
                    )
        elif current_user.get_menu_mode() == 'new_deal':
            if text == 'Назад':
                current_user.set_menu_mode('main')
                self.save_admins()
                self.send_message(
                    user_id,
                    'Возвращаюсь назад...',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
            else:
                try:
                    new_energy_amount = handle_admin_new_deal_and_get_energy_amount(current_user, text, time)
                    self.save_admins()
                    self.send_message(
                        user_id,
                        'У тебя теперь ' + new_energy_amount + ' энергетиков!',
                        ADMIN_MAIN_MENU_KEYBOARD
                    )
                except ValueError:
                    self.send_message(
                        user_id,
                        'Неверное значение, попробуй еще раз!'
                    )
                except AmountError:
                    self.send_message(
                        user_id,
                        'У тебя нет столько энергетиков!'
                    )
        elif current_user.get_menu_mode() == 'need_help':
            if text == 'Я помог':
                current_user.set_menu_mode('main')
                self.save_admins()
                self.send_message(
                    user_id,
                    'Отлично, не забудь внести сделку в базу!',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
            elif text == 'Назад':
                current_user.set_menu_mode('main')
                self.save_admins()
                self.send_message(
                    user_id,
                    'Жалко этого добряка...',
                    ADMIN_MAIN_MENU_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    'Ты помог человеку или его уже не спасти?'
                )

    def note_new_client_action(self, current_client, current_admin=None):
        """
        Отправка сообщений админам о ключевых действиях клиента.

        :param current_client: объект клиента
        :param current_admin: объект админа (если он уже привязан к клиенту)
        :return:
        """
        if current_client.get_menu_mode() == 'main':
            for admin in self.admins:
                self.send_message(
                    admin.get_user_id(),
                    f'[id{current_client.get_user_id()}|{current_client.get_user_name()}] запустил бота!'
                )
        elif current_client.get_menu_mode() == 'cart':
            for admin in self.admins:
                self.send_message(
                    admin.get_user_id(),
                    f'[id{current_client.get_user_id()}|{current_client.get_user_name()}] хочет сделать заказ!'
                )
        elif current_client.get_menu_mode() == 'payment_check':
            self.send_message(
                current_admin.get_user_id(),
                f'[id{current_client.get_user_id()}|{current_client.get_user_name()}] заплатил!'
            )
        elif current_client.get_menu_mode() == 'order_done':
            self.send_message(
                current_admin.get_user_id(),
                f'[id{current_client.get_user_id()}|{current_client.get_user_name()}] направляется к тебе!'
            )

    def new_client_message(self, user_id, first_name, text):
        """
        Обработка сообщения от клиента.

        Метод определяет объект отправителя сообщения, после чего обрабатывает
        входящее сообщение в зависимости от его фактического положения в меню
        клавиатур.

        Внимание! Меняет значения полей menu_mode, energy amount, deals,
        current_order экземпляра current_user класса Client.

        :param user_id: индивидуальный номер диалога
        :param first_name: имя отправителя
        :param text: текст сообщения
        :return:
        """
        current_user = self.define_client_from_message(first_name, user_id)
        if current_user.get_menu_mode() == 'start':
            if text == 'Начать':
                current_user.set_menu_mode('main')
                self.save_clients()
                self.send_message(
                    user_id,
                    'Поехали!',
                    CLIENT_MAIN_MENU_KEYBOARD
                )
                self.note_new_client_action(current_user)
            else:
                self.send_message(
                    user_id,
                    'Для запуска бота напишите "Начать"'
                )
        elif current_user.get_menu_mode() == 'main':
            if text == 'Моя статистика':
                self.send_message(
                    user_id,
                    f'Сделок совершено: {current_user.get_number_of_deals()}\n'
                    f'Энергетиков преобретено: {current_user.get_energy_amount()}'
                )
            elif text == 'Купить энергетики':
                current_user.set_menu_mode('cart')
                self.save_clients()
                self.send_message(
                    user_id,
                    'Сколько энергетиков Вам нужно?',
                    CLIENT_CART_KEYBOARD
                )
                self.note_new_client_action(current_user)
            elif text == 'Хочу сотрудничать':
                link = self.vk_session.method('users.get', values={'user_ids': f'{LOPATA_ID}'})[0]['id']
                self.send_message(
                    user_id,
                    'Если Вы хотите обсудить возможность сотрудничества, '
                    'получения скидки или просто поговорить с Лопатусом), '
                    f'пишите [id{link}|сюда]!'
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING) - 1)]
                )
        elif current_user.get_menu_mode() == 'cart':
            if text == '1':
                current_user.get_current_order().set_energy_amount(1)
                self.find_free_admin_and_continue(current_user)
            elif text == '2':
                current_user.get_current_order().set_energy_amount(2)
                self.find_free_admin_and_continue(current_user)
            elif text == '3':
                current_user.get_current_order().set_energy_amount(3)
                self.find_free_admin_and_continue(current_user)
            elif text == '4':
                current_user.get_current_order().set_energy_amount(4)
                self.find_free_admin_and_continue(current_user)
            elif text == 'Хочу больше!':
                current_user.set_menu_mode('big_order')
                self.save_clients()
                self.send_message(
                    user_id,
                    'Сколько энергетиков Вы хотите купить?',
                    GO_BACK_KEYBOARD
                )
            elif text == 'Назад':
                current_user.set_menu_mode('main')
                self.save_clients()
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
                    raise AmountError
                else:
                    current_user.get_current_order().set_energy_amount(amount)
                    self.find_free_admin_and_continue(current_user)
            except ValueError:
                if text == 'Назад':
                    current_user.set_menu_mode('cart')
                    self.save_clients()
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
            except AmountError:
                self.send_message(
                    user_id,
                    'Вы хотите отдать нам энергетики? Так нельзя! :)'
                )
        elif current_user.get_menu_mode() == 'payment_method':
            if text == 'Переводом на Тинькофф по ссылке':
                current_user.set_menu_mode('payment_check')
                self.save_clients()
                self.send_message(
                    user_id,
                    f'К оплате '
                    f'{current_user.get_current_order().get_energy_amount() * ONE_ENERGY_DRINK_PRICE} '
                    f'рублей. '
                    'Чтобы перевести деньги на счёт Тинькофф, перейдите по ссылке: \n'
                    f'{PAY_URL}',
                    CLIENT_PAYMENT_CHECK_KEYBOARD
                )
            elif text == 'Переводом на карту Сбербанка':
                current_user.set_menu_mode('payment_check')
                self.save_clients()
                self.send_message(
                    user_id,
                    f'К оплате '
                    f'{current_user.get_current_order().get_energy_amount() * ONE_ENERGY_DRINK_PRICE} '
                    f'рублей. \n'
                    f'Номер карты Сбербанк:\n'
                    f'{current_user.get_current_order().get_admin().get_sberbank_card()}\n'
                    f'Перевод по номеру телефона:\n'
                    f'{current_user.get_current_order().get_admin().get_telephone_number()}',
                    CLIENT_PAYMENT_CHECK_KEYBOARD
                )
            elif text == 'Переводом на карту Тинькофф':
                current_user.set_menu_mode('payment_check')
                self.save_clients()
                self.send_message(
                    user_id,
                    f'К оплате '
                    f'{current_user.get_current_order().get_energy_amount() * ONE_ENERGY_DRINK_PRICE} '
                    f'рублей. \n'
                    f'Номер карты Тинькофф:\n'
                    f'{current_user.get_current_order().get_admin().get_tinkoff_card()}\n'
                    f'Перевод по номеру телефона:\n'
                    f'{current_user.get_current_order().get_admin().get_telephone_number()}',
                    CLIENT_PAYMENT_CHECK_KEYBOARD
                )
            elif text == 'Оплачу наличными при получении':
                self.client_order_done(current_user)
            elif text == 'Назад':
                current_user.get_current_order().clear_order()
                current_user.set_menu_mode('cart')
                self.save_clients()
                self.send_message(
                    user_id,
                    'Возвращаюсь назад...',
                    CLIENT_CART_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING))]
                )
        elif current_user.get_menu_mode() == 'admin_delay':
            if text == 'Мне помогли':
                current_user.set_menu_mode('order_done')
                self.save_clients()
                self.send_message(
                    user_id,
                    'Мы рады, что все хорошо!',
                    CLIENT_ORDER_DONE_KEYBOARD
                )
            elif text == 'Отменить заказ':
                current_user.set_menu_mode('main')
                self.save_clients()
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
        elif current_user.get_menu_mode() == 'payment_check':
            if text == 'Оплата произведена':
                self.client_order_done(current_user)
                self.note_new_client_action(current_user, current_user.get_current_order().get_admin())
            elif text == 'Назад':
                current_user.set_menu_mode('payment_method')
                self.save_clients()
                self.send_message(
                    user_id,
                    'Возвращаюсь назад...',
                    CLIENT_PAYMENT_METHOD_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING))]
                )
        elif current_user.get_menu_mode() == 'order_done':
            self.note_new_client_action(current_user, current_user.get_current_order().get_admin())
            if text == 'Я получил заказ':
                current_user.set_menu_mode('main')
                current_user.new_deal(current_user.get_current_order().get_energy_amount())
                current_user.get_current_order().clear_order()
                self.save_clients()
                self.send_message(
                    user_id,
                    'Спасибо, что выбираете нас! '
                    'Мы будем очень рады если Вы оставите отзыв: '
                    f'{FEEDBACK_URL}',
                    CLIENT_MAIN_MENU_KEYBOARD
                )
            else:
                self.send_message(
                    user_id,
                    MISUNDERSTANDING[randint(0, len(MISUNDERSTANDING))]
                )

    def client_order_done(self, current_user):
        """
        Переход к стадии получения заказа в случае оплаты наличными.

        Внимание! Меняет значение поля menu_mode экземпляра current_user
        класса Client.

        :param current_user: объект клиента
        :return:
        """
        current_user.set_menu_mode('order_done')
        self.save_clients()
        self.send_message(
            current_user.get_user_id(),
            f'Подходите в '
            f'{current_user.get_current_order().get_admin().get_room_number()} '
            f'комнату. Заказ уже ждет Вас!',
            CLIENT_ORDER_DONE_KEYBOARD
        )

    def get_free_admin(self, current_client):
        """
        Поиск свободного админа с нужным количеством энергетиков.

        :param current_client: объект клиента
        :return: объект искомого админа
        """
        for i in range(len(self.admins)):
            current_admin = self.admins[i]
            if current_admin.get_online_status() and \
                    current_admin.get_energy_amount() >= \
                    current_client.get_current_order().get_energy_amount():
                return current_admin
        return None

    def find_free_admin_and_continue(self, current_user):
        """
        Проверка на наличие свободных админов и оповещение клиента о дальнейших дейсвтиях.

        Метод совершает поиск свободного админа. В случае положительного результата,
        клиенту отправляется инструкция о дальнейших действиях (куда подойти и забрать
        свой заказ), в противном случае отправляется сообщение о том, что можно подождать,
        пока кто-то из админов освободится, либо отменить свой заказ.

        Внимание! Меняет поле menu_mode экземпляра current_user класса Client.

        :param current_user: объект клиента
        :return:
        """
        free_admin = self.get_free_admin(current_user)
        if free_admin is None:
            current_user.set_menu_mode('admin_delay')
            self.save_clients()
            self.send_message(
                current_user.get_user_id(),
                'К сожалению, нас сейчас нет в общежитии или мы все спим. '
                'Не нажимайте ничего, и мы свяжемся в вами (администраторам уже звонят!). '
                'Либо Вы можете отменить заказ и попробовать еще раз позже.',
                CLIENT_DELAY_KEYBOARD
            )
            self.note_admins_about_new_delay(current_user)
        else:
            current_user.set_menu_mode('payment_method')
            current_user.get_current_order().set_admin(free_admin)
            self.save_clients()
            self.send_message(
                current_user.get_user_id(),
                'Выберите удобный способ оплаты...',
                CLIENT_PAYMENT_METHOD_KEYBOARD
            )

    def note_admins_about_new_delay(self, current_user):
        """
        Оповещение админов об ожидании обработки нового заказа.

        Внимание! Меняет значение поле menu_mode экземляров класса Admins
        из списка админов - поля admins.

        :param current_user: объект клиента
        :return:
        """
        for i in range(len(self.admins)):
            self.admins[i].set_menu_mode('need_help')
            self.save_admins()
            self.send_message(
                self.admins[i].get_user_id(),
                f'Поступил новый заказ от @id{current_user.get_user_id()}. '
                f'Ответь ему, как только появится время!!!',
                ADMIN_NEED_HELP_KEYBOARD
            )

    def add_new_admin(self, admin_obj):
        """
        Добавление админа в список.

        Внимание! Меняет значение поля admins.

        :param admin_obj: объект админа
        :return:
        """
        for i in range(len(self.admins)):
            if admin_obj == self.admins[i]:
                break
        else:
            self.admins.append(admin_obj)
            self.save_admins()

    def start_bot(self):
        """
        Инициализация и запуск бота.

        :return:
        """
        # авторизация сообщества
        self.login_as_group()
        if self.vk_session is None:
            print_error('VK session is Null!')
            exit(1)

        # установка параметров LongPoll сервера
        self.set_long_poll_server_params()

        # заполнения списка админов
        self.fill_admin_list()

        # загрузка актуальных клавиатур
        self.set_admins_actual_keyboard()
        self.set_clients_actual_keyboard()

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
                        first_name, second_name = self.get_username(user_id)
                        print(first_name + ' ' + second_name + ' печатает...')
                    # новое сообщение в диалоге
                    elif action_code == 4:
                        user_id = update[3]
                        first_name, second_name = self.get_username(user_id)
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
