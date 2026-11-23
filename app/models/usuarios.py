class User:

    def __init__(self, username, email, senha):
        self.username = username
        self.email = email
        self.senha = senha

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}'')>"