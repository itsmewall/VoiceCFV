from flask_login import LoginManager

class User:
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password
        self.is_active = True  # Set is_active to True by default

    def get_id(self):
        return str(self.id)


login_manager = LoginManager()