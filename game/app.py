"""
This is a simple web app that plays a game of keep away against the user. Game state is updated at the client by querying the backend api, and the webserver also serves the static html+js at root.
"""
from random import randint
from sanic import Sanic
from sanic import response

app = Sanic(__name__)

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
    body = request.json
    # Do some stuff

    data = {
        'direction': random_direction()
    }
    return response.json(data)

def random_direction():
    """
    Generates and returns a random cardinal direction as a strings
    """
    directions = {
        1: 'up',
        2: 'down',
        3: 'left',
        4: 'right',
    }
    return directions[randint(1,4)]

REQUEST = {
    'hero': {
        'x': int,
        'y': int,
    },
    'monster': {
        'x': int,
        'y': int,
    },
    'caught': bool
}

RESPONSE = {
    'direction': str # one of 'up' 'down' 'left' 'right'
}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, workers=4)
