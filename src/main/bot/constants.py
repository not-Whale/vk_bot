from src.main.bot.utility_funcs import read_json

MAX_INT = 2147483647
ONE_ENERGY_DRINK_PRICE = 65

LOPATA_ID = '448223022'
SBERBANK_CARD_NUMBER = '1234 1234 1234 1234'
TINKOFF_CARD_NUMBER = '4321 4321 4321 4321'
TELEPHONE_FOR_PAYMENT = '+7(912)345-67-89'

PAY_URL = 'https://www.tinkoff.ru/rm/kravchenko.danila5/Nbfxk55061/'
LONG_POLL_SERVER_URL = 'https://api.vk.com/method/messages.getLongPollServer'
FEEDBACK_URL = 'https://vk.com/adrenaline_ebelke_raskazambusi?w=wall-210973828_1'

VK_TOKEN = 'f8d3e63fa555d25cb165f67626537b4f2eb1fd5ae397db5c216051a8683ac2ac51b84732e6ce69ca88ca8'
VK_LOGIN = 'your_login'
VK_PASSWORD = 'your_password'

CLIENTS_PICKLE_PATH = '../resources/users/clients.pickle'
ADMINS_PICKLE_PATH = '../resources/users/admins.pickle'

ADMIN_MAIN_MENU_KEYBOARD = read_json('admin_main_keyboard')
ADMIN_NEED_HELP_KEYBOARD = read_json('admin_need_help_keyboard')

CLIENT_MAIN_MENU_KEYBOARD = read_json('client_main_keyboard')
CLIENT_CART_KEYBOARD = read_json('client_cart_keyboard')
CLIENT_DELAY_KEYBOARD = read_json('client_delay_keyboard')
CLIENT_ORDER_DONE_KEYBOARD = read_json('client_order_done_keyboard')
CLIENT_PAYMENT_CHECK_KEYBOARD = read_json('client_payment_check_keyboard')
CLIENT_PAYMENT_METHOD_KEYBOARD = read_json('client_payment_method_keyboard')

GO_BACK_KEYBOARD = read_json('go_back_keyboard')

ADMIN_LIST = []

MISUNDERSTANDING = [
    'Я не понимаю Вас :(',
    'Можете еще раз повторить? Я не расслышал, что Вы сказали',
    'Вы уверены, что хотите именно это?',
    'Я с радостью поддержал бы беседу, но пока не умею. Давайте сыграем по сценарию!',
    'Ничего не могу разобрать. Повторите, пожалуйста'
]

KEYBOARDS = {
    'client_main': CLIENT_MAIN_MENU_KEYBOARD,
    'client_cart': CLIENT_CART_KEYBOARD,
    'client_admin_delay': CLIENT_DELAY_KEYBOARD,
    'client_order_done': CLIENT_ORDER_DONE_KEYBOARD,
    'client_payment_check': CLIENT_PAYMENT_CHECK_KEYBOARD,
    'client_payment_method': CLIENT_PAYMENT_METHOD_KEYBOARD,
    'client_go_back': GO_BACK_KEYBOARD,
    'admin_delivery': GO_BACK_KEYBOARD,
    'admin_new_deal': GO_BACK_KEYBOARD,
    'admin_main': ADMIN_MAIN_MENU_KEYBOARD,
    'admin_need_help': ADMIN_NEED_HELP_KEYBOARD
}