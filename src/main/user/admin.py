class Admin:
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
        return self.user_id

    def get_room_number(self):
        return self.room_number

    def get_online_status(self):
        return self.is_online

    def get_deals_list(self):
        return self.deals

    def get_menu_mode(self):
        return self.menu_mode

    def get_energy_amount(self):
        return self.energy_amount

    def get_sberbank_card(self):
        return self.sberbank_card

    def get_tinkoff_card(self):
        return self.tinkoff_card

    def get_telephone_number(self):
        return self.telephone_number

    def set_online(self):
        self.is_online = True

    def set_offline(self):
        self.is_online = False

    def set_menu_mode(self, menu_mode):
        self.menu_mode = menu_mode

    def set_energy_amount(self, amount):
        self.energy_amount = amount

    def new_deal(self, time):
        self.deals.append(time)
