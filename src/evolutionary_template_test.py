import numpy as np
from symmetric_matrix import SymmetricMatrix

# evolutionary algorithm parameters
m = [10]
c_parameters = [0.82, 1.2]
sigma_min = [0.05]

A = 0
G = 1
C = 2
T = 3


class SubstitutionMatrix:

    # initial_change = True wtedy gdy chcemy by poczatkowa macierz substytucji byla inna
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
            self.changeSubstitutionMatrix(True)
        self.best_bootstrap_value = 0

    # funkcja zmienia parametry macierzy substytucji dla aktualnej iteracji oraz pilnuje m_counter
    # initial_change = True dla Zwielokrotnionego 1+1 by startowac z roznych punktow
    def changeSubstitutionMatrix(self, initial_change=False):
        if not initial_change:
            s = np.random.normal(0, 1, 15)
        else:
            s = np.random.random_sample(15)
            s *= 4

        s += self.sigma
        self.substitution_matrix.add_from_list(s)

        if not initial_change:
            self.m_counter += 1
            if self.m_counter >= m[0]:
                self.changeSigma()
        else:
            self.equalSubstitutionMatricies(True)

    # aktualizuje sigme jesli na to czas - wywolana w changeSubstitutionMatrix()
    def changeSigma(self):
        phi = self.iter_better_choice / m[0]
        if phi > 0.2:
            # Increasing the search radius
            self.sigma *= c_parameters[1]
        elif phi < 0.2:
            # Decreasing the search radius
            self.sigma *= c_parameters[0]
            # Checking stop condition
            if self.sigma < sigma_min:
                pass
        else:
            pass
        self.m_counter = 0
        self.iter_better_choice = 0

    # Checks if new matrix is better than best
    def checkIfBetterBootstrapValue(self, new_Value):
        if new_Value >= self.best_bootstrap_value:
            # Result hasn't declined, we're setting new best matrix
            self.best_bootstrap_value = new_Value
            self.iter_better_choice += 1
            self.equalSubstitutionMatricies(True)
        else:
            # Result is worse, we're keeping old matrix
            self.equalSubstitutionMatricies(False)

    # wyrownuje macierze substytucji (zwykla i best) wedlug decyzji: False - 'cofamy krok'; True - 'stawiamy krok'
    def equalSubstitutionMatricies(self, new_best=False):
        if new_best:
            self.best_substitution_matrix = self.substitution_matrix.copy()
        else:
            self.substitution_matrix = self.best_substitution_matrix.copy()

    # chwilowa funkcja do testowania
    def wypiszWymaluj(self):
        print("Wypisz wymaluj")
        print(self.best_bootstrap_value)
        print(self.best_substitution_matrix)
        print(self.substitution_matrix)
        print(self.iter_better_choice)


m1 = SubstitutionMatrix()
m1.wypiszWymaluj()
m2 = SubstitutionMatrix(True)
m2.wypiszWymaluj()
"""
macierz = SubstitutionMatrix()
macierz.wypiszWymaluj()
macierz.changeSubstitutionMatrix()
macierz.checkIfBetterBootstrapValue(1.0)
macierz.wypiszWymaluj()
macierz.changeSubstitutionMatrix()
macierz.checkIfBetterBootstrapValue(0.5)
macierz.wypiszWymaluj()
"""
"""best_a = [[1, 2, 3],
          [4, 5, 6]]
a = best_a.copy()#= [[1, 2, 3],
     #[4, 5, 6]]
a[0][0] = best_a[0][0]
a[0][1] = best_a[0][1]
a[0][2] = best_a[0][2]
a[1][0] = best_a[1][0]
a[1][1] = best_a[1][1]
a[1][2] = best_a[1][2]
best_a[0][0] += 0.5*0.123
#a = [3, 2, 1]
#c = [2, 3, 1]
print(a)
print(best_a)
#print(c)
#for i in range(10):
 #   changeSubstitutionMatrix()

#print(substitution_matrix)
#print(gap_penalty)"""
