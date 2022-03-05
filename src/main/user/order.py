class Order:
    def __init__(self, client_id):
        self.client_id = client_id
        self.energy_amount = 0
        self.admin = None

    def set_energy_amount(self, energy_amount):
        self.energy_amount = energy_amount

    def set_admin(self, admin):
        self.admin = admin

    def get_admin(self):
        return self.admin

    def get_energy_amount(self):
        return self.energy_amount

    def clear_order(self):
        self.energy_amount = 0
        self.admin = None
