import random
from spacecmd.messenger import Middleware
import spacecmd.terminal as terminal
import time

class SplashScreen(object):

    def action(self, curses):
        curses.init_space()
        while True:
            if curses.chan.recv_ready():
                while True:
                    char = curses.chan.recv(1)
                    if char in [terminal.TERM, terminal.INT]:
                        curses.chan.close()
                        raise Exception("Client closed")
            instructions = ""
            instructions += terminal.get_value('xterm-256color', terminal.HOME)
            instructions += terminal.get_value('xterm-256color', terminal.FOREGROUND_COLOR(2))
            for x in range(curses.width):
                for y in range(curses.height):
                    rnd = random.getrandbits(2)
                    if rnd == 0:
                        instructions += '0'
                    elif rnd == 1:
                        instructions += '1'
                    else:
                        instructions += ' '
            instructions += terminal.get_value('xterm-256color', terminal.RESET)
            curses.chan.send(instructions)
            time.sleep(0.1)
