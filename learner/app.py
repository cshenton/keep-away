from keras.models import Sequential
from keras.layers import Dense, Activation

def init_model():
    """
    Layers and compiles the Keras model
    """
    model = Sequential([
        Dense(32, input_shape=(784,)),
        Activation('relu'),
        Dense(10),
        Activation('softmax'),
    ])

    adam = Adam(lr=1e-6)
    model.compile(loss='mse',optimizer=adam)
    return model

def replay():
    """
    Gets a random sample of remembered data from redis
    """
    pass

def update(model):
    """
    Trains model on replayed dta
    """
    X, y = replay()
    # Or model.fit_generator(data_generator, steps_per_epoch, epochs)
    model.train_on_batch(X, y)

def main():
    """
    Actual run loop
    """
    # init model
    # loop
    # grab some data
    # batch update the model
    # every now and then repersist the graph to redis
    pass
