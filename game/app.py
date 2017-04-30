"""
This is a simple web app that plays a game of keep away against the user. Game state is updated at the client by querying the backend api, and the webserver also serves the static html+js at root.
"""
import os
from random import randint
from sanic import Sanic
from sanic import response
import zmq

# Grab config from environment vars
web_port = os.getenv('WEBSERVER_PORT', 1337)
pub_port = os.getenv('PUB_PORT', 5555)
inf_host = os.getenv('INFERER_HOST')
inf_port = os.getenv('INFERER_PORT')

app = Sanic(__name__)

# Set up and bind PUB socket
@app.listener('before_server_start')
def zmq_socket(app):
    """
    Given a sanic app object, initialises a ZMQ context object, creates
    a PUB socket, binds it to port 5555, and attaches it to the app
    """
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:{}".format(pub_port))
    app.socket = socket

# Host static files
app.static('/static', '/static')

# Route index to root
@app.route("/")
async def root(request):
    """
    Opens index.html and serves it to the user
    """
    with open('index.html') as f:
        return response.html(f.read())

# Add a single POST endpoint for the API
@app.post('/api/action')
async def action_handler(request):
    """
    When a user posts game state, the server should respond with the action for the game AI to take.
    """
    data = request.json

    # Determine action
    directions = {
        1: 'up',
        2: 'down',
        3: 'left',
        4: 'right',
    }
    direction = directions[randint(1,4)]
    resp = {
        'direction': direction
    }

    # Send request, response pair to pub socket
    msg = {
        'request': data,
        'response': resp
    }
    app.socket.send_json(msg)

    return response.json(resp)

# REQUEST = {
#     'hero': {
#         'x': int,
#         'y': int,
#     },
#     'monster': {
#         'x': int,
#         'y': int,
#     },
#     'caught': bool
# }

# RESPONSE = {
#     'direction': str # one of 'up' 'down' 'left' 'right'
# }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=web_port, workers=4)
