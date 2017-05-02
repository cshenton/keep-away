from keras.models import Sequential
from keras.layers import Dense, Activation

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

if __name__ == '__main__':
    main()
