import os
import zmq
import logging
from random import random

sub_host = os.getenv('SUB_HOST', 'game')
sub_port = os.getenv('SUB_PORT', 5555)

context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://{}:{}".format(sub_host, sub_port))
socket.setsockopt_string(zmq.SUBSCRIBE, '')

logging.warning("Collecting data from game")
# Just monitor the socket and print every 1000th message
count = 0
while True:
    msg = socket.recv_json()
    if msg['request']['caught']:
        logging.warning(msg)
