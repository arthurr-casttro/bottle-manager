from bottle import template


class Application():

    def __init__(self):
        self.pages = {
            'dashboard': self.dashboard,
            'bebidas': self.bebidas,
            'dashboard2': self.dashboard2
        }


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()


    def helper(self):
        return template('app/views/html/helper')

    def dashboard(self):
        return template('app/views/html/dashboard')

    def bebidas(self):  
        return template('app/views/html/bebidas')

    def dashboard2(self):
        return template('app/views/html/dashboard2')
