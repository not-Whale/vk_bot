class Order:
    """Класс заказа клиента."""
    def __init__(self, client_id):
        self.client_id = client_id
        self.energy_amount = 0
        self.admin = None

    def set_energy_amount(self, energy_amount):
        """Установка количества заказанных энерегетиков."""
        self.energy_amount = energy_amount

    def set_admin(self, admin):
        """Установка привязанного к заказу админа."""
        self.admin = admin

    def get_admin(self):
        """Получение значения поля admin."""
        return self.admin

    def get_energy_amount(self):
        """Получение значение поля energy_amount."""
        return self.energy_amount

    def clear_order(self):
        """Удаление заказа."""
        self.energy_amount = 0
        self.admin = None
