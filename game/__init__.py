"""
This is a simple web app that plays a game of keep away against the user. Game state is updated at the client by querying the backend api, and the webserver also serves the static html+js at root.
"""
from sanic import Sanic

app = Sanic(__name__)

# Serves files from the static folder to the URL /static
app.static('/', './static')

# Add a single POST endpoint for the API
@app.post('/api/action')
async def action_handler(request):
    """
    When a user posts game state, the server should respond with the action for the game AI to take.
    """
    return text('POST request - {}'.format(request.json))
