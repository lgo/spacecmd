from gevent import monkey
monkey.patch_all()

import logging
import gevent
import paramiko
from binascii import hexlify
from paramiko.py3compat import u
from spacecmd.sshserver import SSHServer
from spacecmd.commands import Ls, Cd, Whoami
from spacecmd.middleware.welcome import WelcomeMiddleware
from spacecmd.util import chunks
from spacecmd.logger import log

# logging.basicConfig(level=logging.INFO, format='%(levelname)s %(threadName)s %(message)s')
# log.s/etLevel(logging.INFO)

HOST_ADDRESS = ''
PORT = 2200

if __name__ == "__main__":
    host_key = paramiko.RSAKey(filename='test_rsa.key')
    fingerprint = ":".join(chunks(u(hexlify(host_key.get_fingerprint())), 2))
    log.info(f'Read host key fingerprint={fingerprint}')
    log.debug(f'Read host key fingerprint={fingerprint}')
    server = SSHServer(
        address=HOST_ADDRESS,
        port=PORT,
        host_key=host_key,
        middleware=[
            WelcomeMiddleware
        ],
        commands=[
            Ls,
            Cd,
            Whoami,
        ],
    )
    server.listen()
