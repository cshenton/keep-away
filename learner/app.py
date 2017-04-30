import os
import zmq
from random import random

sub_host = os.getenv('SUB_HOST', 'game')
sub_port = os.getenv('SUB_PORT', 5555)

context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting data from game")
socket.connect("tcp://{}:{}".format(sub_host, sub_port))
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

# Just monitor the socket and print every 1000th message
while True:
    msg = socket.recv_json()
    if random() < 0.001:
        print(msg)
