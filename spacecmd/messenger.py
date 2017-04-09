class Messenger(object):

    def __init__(self, term, state):
        self.term = term

    def get(self, key, default=None):
        return self.term.state.get(key, default)

    def set(self, key, value):
        self.term.state[key] = value

class Command(Messenger):

    def run(self, args):
        result, error = self.check_args(args)
        if result:
            self.action(args)
        else:
            self.term.sendl(error)
            # FIXME: Set error status

    def action(self, *args):
        raise NotImplementedError

    def check_args(*args):
        return True

class Middleware(Messenger):
    def post_authenticate(self):
        pass

    def pre_command(self):
        pass

    def post_command(self):
        pass

    def pre_exit(self):
        pass
