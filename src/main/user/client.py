class Client:
    def __init__(self, client_id, first_name, menu_mode='start'):
        self.user_id = client_id
        self.name = first_name
        self.menu_mode = menu_mode
        self.deals = 0
        self.energy_amount = 0

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

    def set_menu_mode(self, menu_mode):
        self.menu_mode = menu_mode
