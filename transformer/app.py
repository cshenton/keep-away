"""
Responsible for data munging of stream of data from the webserver. Turns
request and response json, which the webserver understands, in to state
and action arrays in a tuple, which the machine learning algo undertands

That data is then persisted to Redis.
"""
import zmq

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




def transform(msg):
    """
    Takes dict of request and response and returns a tuple of state
    arrays.
    """
    pass

def main():
    """
    Reads from queue, transforms data, writes to Redis
    """
    pass

if __name__ == '__main__':
    main()
