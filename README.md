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

## Asynchronous Deep Reinforcement Learning

One of the things we have to do to make this viable is to separate the policy function exploration from choices of actions. That is, some (possible stale) version of the policy function is used to choose action based on state, and the total tuple (state, action, reward, new state) arrives at the policy function learner some substantial time later.

This actually makes reinforcement learning as a concept easier to reason about, but it makes our architecture line up with standard libraries a little less.

> For example, the OpenAI gym module directly exposes an environment class that provides immediate feedback to a well defined agent that exists within a particular process.

### Specifics

The data structure persisted on redis is the tensorflow graph for the Q-learning function. When the inferer service is queried with state, it calculates all four outcomes, and chooses one based on the exploration-exploitation tradeoff it wants to make. The transition tuple then eventually makes it to the learner service, which update the Q-learning function.

In this way, the inferer is not the same as a traditional model-server, which is dumb. It makes choices about exploring the state space.

### Pseudocode

```python
from numpy.random import rand

def select_action(Q, state, epsilon):
    """
    w.p. e, choose a random action, else choose the best action given the state
    """
    if rand() < epsilon:
        action = random action
    else:
        action = argmax(Q, state)
    return action

def update_memory(memory):
    """
    Honestly probably just going to store this in redis or something with numbered hashes and just store the number of events in memory to query.
    """
    blah

def update_Q(Q, memory, state, new_state, action, reward, gamma):
    input = [state, action]
    if new_state is terminal:
        output = reward
    else:
        # Guess the max value of the new state
        next_input = [[new_state, a] for a in actions]
        prediction = max(Q.predict(i) for i in next_input)
        # Total value is that discounted plus reward
        output = reward + gamma * prediction
    # Update the model given that x,y pair
    Q.train(input, output) # In the manner of a normal ML model
```


## Credits

Credit to https://github.com/lostdecade/simple_canvas_game on which the game portion of this repo is based.
