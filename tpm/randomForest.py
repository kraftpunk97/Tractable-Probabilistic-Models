from __future__ import print_function
import numpy as np
import sys
import time
from Util import *
from CLT_class import CLT
from sklearn.utils import resample


class RandomForest():

    def __init__(self):
        self.n_components = 0  # number of components
        self.mixture_probs = None  # mixture probabilities
        self.clt_list = []  # List of Tree Bayesian networks

    '''
        Learn Mixtures of Trees using the EM algorithm.
    '''

    def learn(self, dataset, n_components=2, r=100):
        # For each component and each data point, we have a weight
        weights = np.ones((n_components, dataset.shape[0]))
        self.n_components = n_components

        self.mixture_probs = [1 / n_components] * n_components

        self.clt_list = [CLT() for _ in range(n_components)]

        for k in range(n_components):
            bootstrap_data = resample(dataset)
            self.clt_list[k].learn(bootstrap_data)
            self.clt_list[k].random_forest_update(bootstrap_data, weights[k], r)

    """
        Compute the log-likelihood score of the dataset
    """

    def computeLL(self, dataset):
        ll = 0.0

        for k in range(self.n_components):
            ll += self.clt_list[k].computeLL(dataset)

        return ll


if __name__ == '__main__':

    dataset_list = ['accidents', 'baudio', 'bnetflix', 'jester', 'kdd', 'msnbc', 'nltcs', 'plants', 'pumsb_star',
                    'tretail']

    k_list = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    r_list = [10, 300, 10, 10, 150, 500, 500, 10, 150, 500]

    for i, dataset_name in enumerate(dataset_list):
        ll_vals = []
        for itr in range(5):
            training = '../dataset/' + dataset_name + '.ts.data'
            dataset = Util.load_dataset(training)

            # To learn Chow-Liu trees, you can use
            rf = RandomForest()
            rf.learn(dataset, n_components=k_list[i], r=r_list[i])

            # To compute average log likelihood of a dataset, you can use
            test = '../dataset/' + dataset_name + '.test.data'
            dataset = Util.load_dataset(test)
            ll = rf.computeLL(dataset) / dataset.shape[0]
            ll_vals.append(ll)

        print(f'{dataset_name} dataset-- Average ll: {np.mean(ll_vals)} ;; StDev: {np.std(ll_vals)}')



