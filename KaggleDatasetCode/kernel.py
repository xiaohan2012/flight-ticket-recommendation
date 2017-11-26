import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_kernels


def compute_gaussian_kernel(x, z, sigma):
    """Computes Gaussian kernel between two vectors."""
    return np.exp((-1.0 * np.linalg.norm(x - z)) / (2.0 * np.power(sigma, 2)))


def compute_polynomial_kernel(X):
    return ((X.T.dot(X) + 1) ** 2)


def compute_submatrix(X, Z, sigma):
    """Computes Gaussian kernel matrix between X and Z."""
    x_len, _ = X.shape
    z_len, _ = Z.shape
    out = np.zeros((x_len, z_len))
    for x_ind, x_row in enumerate(X):
        for z_ind, z_row in enumerate(Z):
            out[x_ind, z_ind] = compute_gaussian_kernel(x_row, z_row, sigma)

    return out


def compute_submatrix_opt(X, sigma):
    #return pairwise_kernels(X, metric="linear")
   # return pairwise_kernels(X, metric="cosine")
    return pairwise_kernels(X, metric="rbf", gamma=sigma)
    #return pairwise_kernels(X, metric="polynomial", degree=3, gamma=1, coef0=1)

def sigmoid(x):
    return 1 / (1 + np.exp(-x)) - 0.5


#def compute_happiness(artist_indexes):
#    for offer in range(1, first_artist.shape[0] // 30):
 #       for artist in artist:
 #       c = cost(first_artist, 1, 1, offer) + cost(second_artist, 1, 1, offer) + cost(third_artist, 1, 1, offer)

def compute_happiness(K, artist_indexes, happy_coef, unhappy_coef, num_recommendations):
    num_artists = len(artist_indexes)

    selected = K[artist_indexes, :]
    sums = np.sum(selected, axis=0).reshape((1, -1))

    #print(sums)
    expectation = happy_coef * sums + unhappy_coef * (np.ones((1, sums.shape[1])) - sums)

    sorted_indexes = np.argsort(-expectation)[0]
    taken_indexes = sorted_indexes[0:num_recommendations]
    taken = expectation[0, taken_indexes]

    result = np.sum(taken) + num_recommendations * unhappy_coef

    return result


def main():
    with open("uam.matrix", "rb") as f:
        user_artist_matrix = pickle.load(f)

    smoothed = user_artist_matrix

    K = compute_submatrix_opt(smoothed.T, 0.01)
    K -= np.diag(K) * np.eye(K.shape[0])
    K /= np.linalg.norm(K)
    #artist_indexes = [149, 150, 151, 0, 5 , 10, 25]
    artist_indexes = range(0, K.shape[0])
    #artist_indexes = [0]
    costs = []

    for offer in range(1, K.shape[0]):
        c = compute_happiness(K, artist_indexes, 1 -1, offer)

        costs.append(c)

    plt.plot(range(1, K.shape[0]), costs)
    plt.savefig("plot.pdf")

    plot_kernel(K)


def plot_kernel(K):
    plt.imshow(K)
    plt.colorbar()
    plt.savefig("kern.pdf")
    # plt.yscale('log')
    # plt.hist((user_artist_matrix.reshape((-1, 1))), bins=np.logspace(0, 2, 6))
    # plt.show()


if __name__ == "__main__":
    main()
