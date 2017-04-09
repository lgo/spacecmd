import spacecmd.terminal as terminal

class Curses(object):

    def __init__(self, chan, height, width):
        self.chan = chan
        self.height = height
        self.width = width

        self.panel = [None for _ in range(width * height)]
        self._buffer = []

    def set(self, x, y, char, special={}):
        self.panel[x + y * self.width] = (char, special)
        self._buffer.append((x, y, char, special))

    def flush(self, full=False):
        instructions = ""
        for x, y, char, special in self._buffer:
            if 'fg' in special:
                instructions += self.color_selection(special['fg'])
            instructions += terminal.get_value('xterm-256color', terminal.CURSOR_POS(x,y))
            instructions += char
            if 'fg' in special:
                instructions += terminal.get_value('xterm-256color', terminal.RESET)
        self.chan.send(instructions)

    def full_flush(self):
        """
        Rewrite the entire height+width section
        """
        pass


    def init_space(self):
        """
        Create the initial space, i.e. height amount of newlines
        """
        self.chan.send(terminal.get_value('xterm-256color', terminal.CLEAR))

    def color_selection(self, color):
        if color == 'green':
            return terminal.get_value('xterm-256color', terminal.FOREGROUND_COLOR(2))
