import theano
from theano import tensor as T
import numpy as np
from AutoEncoder import *

index = T.lscalar()

wordVectors = theano.shared(value = np.zeros((20, 5), dtype=theano.config.floatX))

x = T.ivector('x')

batch_size = 5
learning_rate = 0.05
n_hidden = 50
training_epochs = 3
n_train_batches = 20
end_token = T.lscalar()

decoder_params = {
	'H1' : theano.shared(value = np.zeros((n_hidden, n_hidden), dtype=theano.config.floatX), borrow=True),
	'Y' : theano.shared(value = np.zeros((n_hidden, 20), dtype=theano.config.floatX), borrow=True),
	'C' : theano.shared(value = np.zeros((n_hidden, n_hidden), dtype=theano.config.floatX), borrow=True),
	'S' : theano.shared(value = np.zeros((20, n_hidden), dtype=theano.config.floatX), borrow=True),
	'B' : theano.shared(value = np.zeros(20, dtype=theano.config.floatX), borrow=True)
}
encoder_params = {
	'H2' : theano.shared(value = np.zeros((n_hidden, n_hidden), dtype=theano.config.floatX), borrow=True)
}

autoencoder = AutoEncoder(encoder_params, decoder_params, wordVectors, end_token, batch_size, input = x, n_hidden = n_hidden)
cost, updates = autoencoder.get_cost_updates(learning_rate = learning_rate)
train_autoencoder = theano.function([index, end_token], cost, updates = updates, givens = {x: X_train[index]})

start_time = time.clock()
for epoch in xrange(training_epochs):
	c = []
	for batch_index in xrange(n_train_batches):
		c.append(train_autoencoder(batch_index, 0))

	print 'Training epoch %d, cost ' % epoch, numpy.mean(c)

end_time = time.clock()
training_time = (end_time - start_time)
print training_time / 60.0