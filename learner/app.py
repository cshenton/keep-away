import asyncio
import aioredis
from keras.models import Sequential
from keras.layers import Dense, Activation

class Memory:
    """
    Layer over redis client that exposes methods for retrieiving a random
    sample of keys.
    """
    async def __init__(self, name, host, port):
        self.name = name
        self.counter = name + '_counter'
        self.redis = await aioredis.create_redis((address, port))

    def key(self, count):
        """
        Responsible for generating keys for memories
        """
        key = self.name + '_memory_' + str(count)
        return key

    async def create(self, data):
        """
        Increments the counter by one, then writes to a key determined by
        the counter's current value.
        """
        tran = self.redis.multi_exec()
        current_count = tran.incr(self.counter)
        new_memory = tran.set(self.key(current_count), data)

class Learner:
    """
    Responsible for training and persisting the Neural Net.
    """
    def __init__(self):
        """
        Initialise the Keras Neural Net and attach it to the object.
        """
        model = Sequential([
            Dense(32, input_shape=(784,)),
            Activation('relu'),
            Dense(10),
            Activation('softmax'),
        ])
        adam = Adam(lr=1e-6)
        model.compile(loss='mse',optimizer=adam)
        self.model = model

    def replay(self):
        """
        Gets a random sample of remembered data from redis
        """
        pass

    def update(self):
        """
        Trains model on replayed dta
        """
        X, y = replay()
        # Or model.fit_generator(data_generator, steps_per_epoch, epochs)
        model.train_on_batch(X, y)

    def save(self, key):
        """
        Pickles and writes model to redis
        """
        pass

async def main():
    """
    Actual run loop
    """
    learner = Learner()
    while True:
        update

    # init model
    # loop
    # grab some data
    # batch update the model
    # every now and then repersist the graph to redis
    pass

if __name__ == '__main__':
    main()



loop = asyncio.get_event_loop()

async def go():
    redis = await aioredis.create_redis(
        ('localhost', 6379), loop=loop)
    await redis.set('my-key', 'value')
    val = await redis.get('my-key')
    print(val)
    redis.close()
    await redis.wait_closed()
loop.run_until_complete(go())
