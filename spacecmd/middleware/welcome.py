from spacecmd.messenger import Middleware

class WelcomeMiddleware(Middleware):

    def post_authenticate(self):
        if self.get('name') is None:
            self.term.sendl("Who are you, newcomer?")
            self.term.send("Name: ")
            name, _ = self.term.get_line(exit=True)
            self.term.sendl()
            self.set('name', name)
        else:
            name = self.get('name')
            self.term.sendl("Welcome back, f{name}")
