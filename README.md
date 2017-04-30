# Keep Away
Toy demonstration of integrating ML architecture with a web app.

## Structure

This game pits you against an AI controlled dot on a grid matrix. Your goal is to get away from the AI, its goal is to touch you. However, it starts off super dumb, so you'll have to train it.

This application has three components

- Webserver + frontend: a simple javascript game
- Trainer: receives game data and updates Q-reinforcement algorithm
- Inferer: exposes api for webserver to consume

## Comms

Data is moved about as so

- The js client sends its state to the backend webserver on each loop. The webserver responds with the next action. This is combined with user input to produce the new game state.
- The webserver exposes a pubsub feed of game input state, action, and output state using ZeroMQ, which is published at a well known port.
- The trainer consumes from that feed, and uses the data to update a reinforcement learning model, which is persisted to Redis
- The inferer reads the model from Redis, and exposes a webserver which allows for querying of optimal actions given game state.
- The webserver queries the inferer API for information about how to act

## Why?

This game is really a metaphor for any B2C type web application. Your customers are acting in a particular way, and you want to change application state to produce an outcome that is desirable. This could be by

- recommending particular products
-

The high query frequency of this game allows for a neat demonstration of how this architecture can handle quite high volumes of throughput with little overthinking.

## Throughput

Fill this out later showing the data throughput of parts of the system.

## Credits

Credit to https://github.com/lostdecade/simple_canvas_game on which the game portion of this repo is based.
