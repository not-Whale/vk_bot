from src.main.bot.utility_funcs import read_json_keyboard_file

MAX_INT = 2147483647
ONE_ENERGY_DRINK_PRICE = 65

LOPATA_ID = '448223022'

LONG_POLL_SERVER_URL = 'https://api.vk.com/method/messages.getLongPollServer'

USER_RESOURCES_PATH = '../resources/users'
CLIENTS_PICKLE_PATH = '../resources/users/clients.pickle'
ADMINS_PICKLE_PATH = '../resources/users/admins.pickle'

ADMIN_MAIN_MENU_KEYBOARD = read_json_keyboard_file('admin_main_keyboard')
ADMIN_NEED_HELP_KEYBOARD = read_json_keyboard_file('admin_need_help_keyboard')

CLIENT_MAIN_MENU_KEYBOARD = read_json_keyboard_file('client_main_keyboard')
CLIENT_CART_KEYBOARD = read_json_keyboard_file('client_cart_keyboard')
CLIENT_DELAY_KEYBOARD = read_json_keyboard_file('client_delay_keyboard')
CLIENT_ORDER_DONE_KEYBOARD = read_json_keyboard_file('client_order_done_keyboard')
CLIENT_PAYMENT_CHECK_KEYBOARD = read_json_keyboard_file('client_payment_check_keyboard')
CLIENT_PAYMENT_METHOD_KEYBOARD = read_json_keyboard_file('client_payment_method_keyboard')

GO_BACK_KEYBOARD = read_json_keyboard_file('go_back_keyboard')

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