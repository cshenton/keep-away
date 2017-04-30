import os
import zmq

game_host = os.getenv('GAME_HOST', 'game')
game_port = os.getenv('GAME_PORT', 5555)

context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting data from game")
socket.connect("tcp://localhost:5555")

# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"

# Python 2 - ascii bytes to unicode str
if isinstance(zip_filter, bytes):
    zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

# Process 5 updates
total_temp = 0
for update_nbr in range(5):
    string = socket.recv_string()
    zipcode, temperature, relhumidity = string.split()
    total_temp += int(temperature)

print("Average temperature for zipcode '%s' was %dF" % (
      zip_filter, total_temp / (update_nbr+1))
)
