"""Module containing substitution matrix BUT! it has also implemented mechanism for 1 + 1 evolution.
Evolutionary algorithm simply generates parameters from normal distribution and then add this parameters
multiplied by sigma to substitution matrix."""

import numpy as np
from symmetric_matrix import SymmetricMatrix

# evolutionary algorithm parameters
m = 10
c_parameters = [0.82, 1.2]
sigma_min = 0.05

A = 0
G = 1
C = 2
T = 3


class SubstitutionMatrix:

    # Initial change should be true if we want our initial matrix to be different
    def __init__(self, initial_change=False):
        self.best_substitution_matrix = SymmetricMatrix(5)
        self.best_substitution_matrix.set_from_list([10,
                                                     -1, 7,
                                                     -3, -5, 9,
                                                     -4, -3, 0, 8,
                                                     -5, -5, -5, -5, 2])
        self.substitution_matrix = self.best_substitution_matrix.copy()
        self.sigma = 0.5
        self.m_counter = 0
        self.iter_better_choice = 0
        self.gap_penalty = -5
        self.best_gap_penalty = -5
        if initial_change:
            self.change_substitution_matrix(True)
        self.best_bootstrap_value = 0

    def __getitem__(self, key):
        return self.substitution_matrix[key]

    # Function changes parameters of matrix and checks m_counter
    # Initial change should be True for parallel 1+1 algorithm so it'll start from different matrices
    def change_substitution_matrix(self, initial_change=False):
        if not initial_change:
            # We're here generating numbers from normal distribution to use it for mutation
            s = np.random.normal(0, 1, 15)
        else:
            s = np.random.random_sample(15)
            s *= 4

        s_sigma = np.random.normal(0, 1)

        self.gap_penalty += self.sigma * s_sigma
        # add_from_list simply takes whole list and adds first element of list to first element of matrix
        # This method is optimized for symmetric matrix
        self.substitution_matrix.add_from_list(s)

        # Checks whether we should update our sigma
        if not initial_change:
            self.m_counter += 1
            if self.m_counter >= m:
                self.change_sigma()
        else:
            self.equal_substitution_matrices(True)

    # Updating sigma when m_counter reached certain value
    def change_sigma(self):
        phi = self.iter_better_choice / m
        if phi > 0.2:
            # Increasing the search radius
            self.sigma *= c_parameters[1]
        elif phi < 0.2:
            # Decreasing the search radius
            self.sigma *= c_parameters[0]
        else:
            pass
        self.m_counter = 0
        self.iter_better_choice = 0

    # Checks if new matrix is better than best
    def has_better_bootstrap_value(self, new_Value):
        print("New tree: " + str(new_Value))
        print("Best tree: " + str(self.best_bootstrap_value))
        if new_Value >= self.best_bootstrap_value:
            # Result hasn't declined, we're setting new best matrix
            self.best_bootstrap_value = new_Value
            self.iter_better_choice += 1
            self.equal_substitution_matrices(True)
            return True
        else:
            # Result is worse, we're keeping old matrix
            self.equal_substitution_matrices(False)
            return False

    # Method changes best substitution matrix if old one wasn't better
    def equal_substitution_matrices(self, new_best=False):
        if new_best:
            self.best_substitution_matrix = self.substitution_matrix.copy()
        else:
            self.substitution_matrix = self.best_substitution_matrix.copy()

    def reached_stop(self):
        return self.sigma < sigma_min
