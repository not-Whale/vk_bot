class Admin:
    """Класс админа для бота."""

    def __init__(self, user_id, room_number, sberbank_card, tinkoff_card, telephone_number, menu_mode='start'):
        self.user_id = user_id
        self.room_number = room_number
        self.menu_mode = menu_mode
        self.sberbank_card = sberbank_card
        self.tinkoff_card = tinkoff_card
        self.telephone_number = telephone_number
        self.energy_amount = 0
        self.is_online = False
        self.deals = []

    def get_user_id(self):
        """Получение значения поля user_id"""
        return self.user_id

    def get_room_number(self):
        """Получение значения поля room_number"""
        return self.room_number

    def get_online_status(self):
        """Получение значения поля is_online"""
        return self.is_online

    def get_deals_list(self):
        """Получение значения поля deals"""
        return self.deals

    def get_menu_mode(self):
        """Получение значения поля menu_mode"""
        return self.menu_mode

    def get_energy_amount(self):
        """Получение значения поля energy_amount"""
        return self.energy_amount

    def get_sberbank_card(self):
        """Получение значения поля sberbank_card"""
        return self.sberbank_card

    def get_tinkoff_card(self):
        """Получение значения поля tinkoff_card"""
        return self.tinkoff_card

    def get_telephone_number(self):
        """Получение значения поля telephone_number"""
        return self.telephone_number

    def set_online(self):
        """Изменение статуса админа на online"""
        self.is_online = True

    def set_offline(self):
        """Изменение статуса админа на offline"""
        self.is_online = False

    def set_menu_mode(self, menu_mode):
        """Установка положения в меню."""
        self.menu_mode = menu_mode

    def set_energy_amount(self, amount):
        """Установка количества энерегетиков"""
        self.energy_amount = amount

    def new_deal(self, time):
        """Добавление новой сделки"""
        self.deals.append(time)
