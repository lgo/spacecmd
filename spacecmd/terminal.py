import os

TERM = '\x03'
INT = '\x04'
BACKSPACE = '\x08'
DELETE = '\x7f'

LARROW = 67
RARROW = 68


def fetch_operation_value(terminal, operation):
    return os.popen(f"tput -T {terminal} {operation}").read()

class TerminalCompatability(object):

    def __init__(self, terminal):
        self.terminal = terminal
        self.operations = {}

    def get(self, operation):
        if operation not in self.operations:
            val = fetch_operation_value(self.terminal, operation)
            self.operations[operation] = val
        return self.operations[operation]

terminals = {}

def get_value(terminal, value):
    if terminal not in terminals:
        terminals[terminal] = TerminalCompatability(terminal)
    return terminals[terminal].get(value)

# Cursor handling
HOME = "home"
SAVE_CURSOR = "sc"
RECOVER_CURSOR = "rc"
BACKSPACE = "cub1"
CURSOR_INVISIBLE = "civis"
CURSOR_VISIBLE = "cvvis"
def CURSOR_POS(x, y):
    return "cup {x} {y}".format(x=x, y=y)


# Erasing text
CLEAR = "clear"
CLEAR_REST_OF_LINE = "el"
CLEAR_BEGINNING_OF_LINE = "el1"
CLEARING_LINE = "el2" # Note: Does not move cursor

# Text attributes
RESET = "sgr0"
BOLD = "bold"
DIM = "dim"
STANDOUT = "smso"
SET_UNDERSCORE = "smul"
UNSET_UNDERSCORE = "rmul"
BLINK = "blink"
REVERSE = "rev"
HIDDEN = "invis"

# Color
def FOREGROUND_COLOR(color):
    return "setaf {color}".format(color=color)

def BACKGROUND_COLOR(color):
    return "setab {color}".format(color=color)

# Misc.
SAVE_SCREEN = "smcup"
RECOVER_SCREEN = "rmcup"
