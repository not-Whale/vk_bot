class User:
    def __init__(self, user_id, mode='null'):
        self.id = user_id
        self.mode = mode

    def get_user_id(self):
        return self.id

    def get_user_mode(self):
        return self.mode

