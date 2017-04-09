import logging
import gevent


logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(threadName)s] %(message)s')
log = logging.getLogger()
# log.setLevel(logging.INFO)
# log.setFormatter('%(levelname)s %(threadName)s %(message)s')
