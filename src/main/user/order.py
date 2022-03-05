class Order:
    def __init__(self, client_id):
        self.client_id = client_id
        self.energy_amount = None
        self.admin = None

    def set_energy_amount(self, energy_amount):
        self.energy_amount = energy_amount

    def set_admin(self, admin):
        self.admin = admin

    def clear_order(self):
        self.energy_amount = None
        self.admin_id = None
