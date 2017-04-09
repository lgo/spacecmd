import gevent.server
import paramiko
import threading
import socket
import traceback
from spacecmd.ssh import SSH
from spacecmd.middleware.splashscreen import SplashScreen
from spacecmd.curses import Curses

DEFAULTS = {
    'host': 'localhost',
    'port': 2200,
    'host_key': None,
    'middleware': [],
    'commands': [],
}

class SSHServer(object):

    def __init__(self, **kwargs):
        self.options = {**DEFAULTS, **kwargs}

    def listen(self):
        server = gevent.server.StreamServer((self.options['host'], self.options['port']), self.handle_connection)
        server.serve_forever()

    def handle_connection(self, client, addr):
        print('Got a connection!')
        try:
            transport = paramiko.Transport(client)
            try:
                transport.load_server_moduli()
            except:
                print('(Failed to load moduli -- gex will be unsupported.)')
                raise
            transport.add_server_key(self.options['host_key'])
            server = SSH(transport, addr, self.options['middleware'], self.options['commands'])
            try:
                transport.start_server(server=server)
            except paramiko.SSHException:
                print('*** SSH negotiation failed.')
                return 1
                # sys.exit(1)

            # wait for auth
            chan = transport.accept(20)
            if chan is None:
                print('*** No channel.')
                return 1
                # sys.exit(1)
            print('Authenticated!')

            server.set_chan(chan)

            server.event.wait(1)
            if not server.event.is_set():
                print('*** Client never asked for a shell.')
                return 1
                # sys.exit(1)

            # server.post_authenticate()

            curses = Curses(chan, server.pty_options[2], server.pty_options[1])
            SplashScreen().action(curses)

            while True:
                server.wait_for_cmd()
        except Exception as e:
            print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
            traceback.print_exc()
            try:
                transport.close()
            except:
                pass
            return 1
            # sys.exit(1)
