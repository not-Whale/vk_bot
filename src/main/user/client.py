import src.main.user.order as order


class Client:
    def __init__(self, client_id, first_name, menu_mode='start'):
        self.user_id = client_id
        self.name = first_name
        self.menu_mode = menu_mode
        self.deals = 0
        self.energy_amount = 0
        self.current_order = order.Order(client_id)

    def get_user_id(self):
        return self.user_id

    def get_menu_mode(self):
        return self.menu_mode

    def get_number_of_deals(self):
        return self.deals

    def get_user_name(self):
        return self.name

    def get_energy_amount(self):
        return self.energy_amount

    def get_current_order(self):
        return self.current_order

    def set_menu_mode(self, menu_mode):
        self.menu_mode = menu_mode

    def new_deal(self, energy_amount):
        self.deals += 1
        self.energy_amount += energy_amount
