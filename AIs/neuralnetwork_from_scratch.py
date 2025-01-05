import tensorflow_datasets as tfds
from matplotlib import pyplot as plt
import numpy as np
np.set_printoptions(suppress=True)

def mnist_as_arrays(show_info=True):
    mnist_data, info = tfds.load("mnist", with_info=True)
    if show_info:
        print(info)
    X_train = np.zeros((info.splits['train'].num_examples, np.prod(info.features['image'].shape)))
    Y_train = np.zeros_like(X_train[:, 0])
    i = -1
    for ex in tfds.as_numpy(mnist_data['train']):
        i += 1
        X_train[i] = ex['image'].flatten()
        Y_train[i] = ex['label']

    X_test = np.zeros((info.splits['test'].num_examples, np.prod(info.features['image'].shape)))
    Y_test = np.zeros_like(X_test[:, 0])
    i = -1
    for ex in tfds.as_numpy(mnist_data['test']):
        i += 1
        X_test[i] = ex['image'].flatten()
        Y_test[i] = ex['label']

    print('data loaded'); return X_train, Y_train, X_test, Y_test
X_train, Y_train, X_test, Y_test = mnist_as_arrays()

def get_SGD_batch(n):
    taken = []
    Xs, Ys = np.zeros_like(X_train)[:n], np.zeros(n)
    for i in range(n):
        j = np.random.randint(0, X_train.shape[0])
        while j in taken:
            j = np.random.randint(0, X_train.shape[0])
        else:
            taken.append(j)
        Xs[i] = X_train[j]; Ys[i] = Y_train[j]

    return Xs, Ys

def initweights(seed=None):
    if seed:
        np.random.seed(seed)

    W1 = np.random.rand(15, X_test.shape[1] + 1) - 0.5
    W2 = np.random.rand(15, 16) - 0.5
    W3 = np.random.rand(10, 16) - 0.5
    return W1, W2, W3
W1, W2, W3 = initweights()

def fwdprop(x, y):
    true_y = np.zeros(10); true_y[int(y)] = 1 # one hot encoded true label

    Z1 = np.dot(np.append(x, bias_scalar), W1.T) # appending 1 for bias
    A1 = Z1.clip(min=0) # reLU activation
    Z2 = np.dot(np.append(A1, bias_scalar), W2.T)
    A2 = Z2.clip(min=0) # reLU activation
    Z3 = np.dot(np.append(A2, bias_scalar), W3.T)
    Z3_scaled = Z3 / logits_scalar
    A3 = np.exp(Z3_scaled) / np.sum(np.exp(Z3_scaled)) # softmax activation
    return true_y, A3, A2, Z2, A1, Z1, x

def backprop(true_y, A3, A2, Z2, A1, Z1, x):
    dZ3 = 2 * (A3 - true_y) / logits_scalar # CCE loss and softmax derivative
    dW3 = np.outer(np.append(A2, bias_scalar), dZ3)
    dZ2 = np.dot(dZ3, W3)[:-1] * (Z2 >= 0) # d_reLU(Z) = 0 if Z <= 0 else 1
    dW2 = np.outer(np.append(A1, bias_scalar), dZ2)
    dZ1 = np.dot(dZ2, W2)[:-1] * (Z1 >= 0)
    dW1 = np.outer(np.append(x, bias_scalar), dZ1)

    return dW1.T, dW2.T, dW3.T

def get_wgrad(Xs, Ys):
    n = Xs.shape[0]
    avg_dW1, avg_dW2, avg_dW3 = np.zeros_like(W1), np.zeros_like(W2), np.zeros_like(W3)
    loss = 0
    for i in range(n):
        fwd = fwdprop(Xs[i], Ys[i])
        loss += -np.sum(fwd[0] * np.log(fwd[1]))
        dw1, dw2, dw3 = backprop(fwd[0], fwd[1], fwd[2], fwd[3], fwd[4], fwd[5], fwd[6])
        avg_dW1 += dw1; avg_dW2 += dw2; avg_dW3 += dw3
    return avg_dW1 / n, avg_dW2 / n, avg_dW3 / n, loss / n

bias_scalar = 255 # all hyperparams
logits_scalar = 100
batch_size = 5000
epoch_count = 200
learning_rate = 0.05

prev_train_loss = np.inf
for i in range(epoch_count):

    Xbatch, Ybatch = get_SGD_batch(batch_size)
    dw1, dw2, dw3, train_loss = get_wgrad(Xbatch, Ybatch)
    print(f'{i} train loss: {train_loss:.10f} | learning rate: {np.round(learning_rate, 7)}')

    if train_loss > prev_train_loss:
        learning_rate /= 2
    else:
        learning_rate += 0.01

    prev_train_loss = train_loss
    W1 -= dw1 * learning_rate; W2 -= dw2 * learning_rate; W3 -= dw3 * learning_rate

# code to display image and prediction after training
while True:
    i = np.random.randint(0, X_test.shape[0])
    truth, pred, _, _, _, _, _ = fwdprop(X_test[i], Y_test[i])
    for j in range(10):
        print(np.round(pred[j], 3), truth[j])
    print()
    plt.imshow(X_test[i].reshape(28, 28), interpolation='nearest')
    plt.show()