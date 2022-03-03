class Admin:
    def __init__(self, user_id, pay_url, room_number):
        self.user_id = user_id
        self.room_number = room_number
        self.pay_url = pay_url
        self.menu_mode = 'start'
        self.is_home = False
        self.deals = []

    def get_user_id(self):
        return self.user_id

    def get_room_number(self):
        return self.room_number

    def get_pay_url(self):
        return self.pay_url

    def get_status(self):
        return self.is_home

    def get_deals_list(self):
        return self.deals

    def get_menu_mode(self):
        return self.menu_mode

    def change_status(self):
        self.is_home = not self.is_home

    def set_menu_mode(self, menu_mode):
        self.menu_mode = menu_mode

    def new_deal(self, time):
        self.deals.append(time)
