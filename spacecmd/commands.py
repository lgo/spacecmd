from spacecmd.messenger import Command

class Cd(Command):
    COMMAND = "cd"

    def check_args(self, args):
        if len(args) != 1:
            return (False, "invalid usage")
        return (True, None)

    def action(self, args):
        directory = self.args[0]
        self.term.send(f"Would have moved to {directory}")
        return 0

class Ls(Command):
    COMMAND = "ls"

    def action(self, args):
        self.term.send("")
        return 0

class Whoami(Command):
    COMMAND = "whoami"

    def check_args(self, args):
        if len(args) > 0:
            return (False, f"usage: {WhoamiCommand.COMMAND}")
        return (True, None)

    def action(self, args):
        name = self.get('name')
        self.term.sendl(f"{name}")
        return 0
