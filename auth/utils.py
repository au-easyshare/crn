from flask_login import LoginManager, UserMixin

login_manager = LoginManager()


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(userid):
    return User(userid)
