class Client:
    def __init__(self, client_id, mode='start'):
        self.user_id = client_id
        self.menu_mode = mode
        self.deals = 0

    def get_user_id(self):
        return self.user_id

    def get_menu_mode(self):
        return self.menu_mode

    def get_number_of_deals(self):
        return self.deals
