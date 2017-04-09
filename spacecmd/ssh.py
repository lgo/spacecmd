import paramiko
import threading
import spacecmd.terminal as terminal
from binascii import hexlify
from paramiko.py3compat import u
import sys
from spacecmd.logger import log

paramiko.util.log_to_file('demo_server.log')


class SSH(paramiko.server.ServerInterface):

    def __init__(self, transport, addr, middleware, commands):
        self.transport = transport
        self.addr = addr
        self.event = threading.Event()
        self.middleware = [ware(self, {}) for ware in middleware]
        self.commands = {command.COMMAND: command(self, {}) for command in commands}
        self.state = {}

    def send(self, msg):
        self.chan.send(msg)

    def sendl(self, msg=""):
        self.send(msg + '\r\n')

    def set_chan(self, chan):
        self.chan = chan

    def post_authenticate(self):
        for middleware in self.middleware:
            middleware.post_authenticate()

    def wait_for_cmd(self):
        self.send("# ")

        command, status = self.get_line(self.chan)
        if status in [TERM, INT]:
            self.chan.close()
            raise Exception("Client terminated")
        elif command == "":
            self.sendl("")
            return

        self.sendl()
        cmd, *args = command.split(" ")
        command_handler = self.commands.get(cmd)
        if command_handler is None:
            self.sendl(f"command not found: {cmd}")
        else:
            command_handler.run(args)

    def get_line(self, echo=True, trim=False, exit=False):
        string = ""
        while True:
            char = u(self.chan.recv(1))
            charcode = ord(char)
            log.info(f"char={char} charcode={charcode}")
            if charcode == None:
                if self.chan.recv_ready():
                    # FIXME: Do special stuff, like read and rewind
                    pass
                else:
                    # Ignore escape character
                    continue
            elif char == "\r":
                break
            elif char in [terminal.TERM, terminal.INT]:
                if exit:
                    raise Exception("Terminating character.")
                return None, char
            elif char == terminal.DELETE and len(string) > 0:
                # Sends backspace, clearing space, then backspace again
                string = string[:-1]
                self.chan.send(terminal.get_value('xterm-256color', terminal.BACKSPACE))
                self.chan.send(' ')
                self.chan.send(terminal.get_value('xterm-256color', terminal.BACKSPACE))
            elif char == terminal.DELETE:
                # Ignore backspace with no string to prevent cursor movement
                continue
            else:
                string += u(char)
                self.chan.send(char)
        return string.strip(), None

    """
    Paramiko ServerInterface for session initiation
    """

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_none(self, username):
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):
        log.info('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
        self.ssh_user_info = (username, key)
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        log.info("Channel PTY request channel={} term={} width={} height={} pixelwidth={} pixelheight={}".format(channel, term, width, height, pixelwidth, pixelheight))
        self.pty_options = (term, width, height, pixelwidth, pixelheight)
        return True
