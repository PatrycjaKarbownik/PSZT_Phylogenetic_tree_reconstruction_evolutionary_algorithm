import numpy as np

# evolutionary algorithm parameters
m = [10]
c_parameters = [0.82, 1.2]
sigma_min = [0.05]

A = 0
G = 1
C = 2
T = 3

class SubstitutionMatrix():

    # initial_change = True wtedy gdy chcemy by poczatkowa macierz substytucji byla inna
    def __init__(self, initial_change = False):
        self.best_substitution_matrix = [[10, -1, -3, -4],
                                         [-1,  7, -5, -3],
                                         [-3, -5,  9,  0],
                                         [-4, -3,  0,  8]]
        self.substitution_matrix = [[10, -1, -3, -4],
                                    [-1,  7, -5, -3],
                                    [-3, -5,  9,  0],
                                    [-4, -3,  0,  8]]

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
    def changeSubstitutionMatrix(self, initial_change = False):
        if not initial_change:
            s = np.random.normal(0, 1, 11)
        else:
            s = np.random.random_sample(11)
            s *= 4

        """Changes -> substitution_matrix's coeficients and gap_penalty """
        self.gap_penalty += self.sigma * s[10]
        #diagonal
        self.substitution_matrix[A][A] += self.sigma * s[0]
        self.substitution_matrix[G][G] += self.sigma * s[1]
        self.substitution_matrix[C][C] += self.sigma * s[2]
        self.substitution_matrix[T][T] += self.sigma * s[3]
        # [i][i-1]
        self.substitution_matrix[G][A] += self.sigma * s[4]
        self.substitution_matrix[C][G] += self.sigma * s[5]
        self.substitution_matrix[T][C] += self.sigma * s[6]
        # [i][i+1]
        self.substitution_matrix[A][G] = self.substitution_matrix[G][A]
        self.substitution_matrix[G][C] = self.substitution_matrix[C][G]
        self.substitution_matrix[C][T] = self.substitution_matrix[T][C]
        # [i][i-2]
        self.substitution_matrix[C][A] += self.sigma * s[7]
        self.substitution_matrix[T][G] += self.sigma * s[8]
        # [i][i+2]
        self.substitution_matrix[A][C] = self.substitution_matrix[C][A]
        self.substitution_matrix[G][T] = self.substitution_matrix[T][G]
        # [i][i-3]
        self.substitution_matrix[T][A] += self.sigma * s[9]
        # [i][i+3]
        self.substitution_matrix[A][T] = self.substitution_matrix[T][A]

        if not initial_change:
            self.m_counter += 1
            if self.m_counter >= m[0]:
                self.changeSigma()
        else:
            self.equalSubstitutionMatricies(True)

    # aktualizuje sigme jesli na to czas - wywolana w changeSubstitutionMatrix()
    def changeSigma(self):
        phi = self.iter_better_choice/m[0]
        if phi > 0.2:
            """zwiekszamy promien szukania"""
            self.sigma *= c_parameters[1]
        elif phi < 0.2:
            """zmniejszamy promien szukania"""
            self.sigma *= c_parameters[0]
            """sprawdzamy warunek stopu"""
            if self.sigma < sigma_min:
                pass
        else:
            pass
        self.m_counter = 0
        self.iter_better_choice =0

    # sprawdza czy nowa macierz dala lepszy wynik niz dotychczas najlepszy
    def checkIfBetterBootstrapValue(self, new_Value):
        if new_Value >= self.best_bootstrap_value:
            """wynik sie nie pogorszyl"""
            self.best_bootstrap_value = new_Value
            self.iter_better_choice += 1
            self.equalSubstitutionMatricies(True)
        else:
            """wynik sie pogorszyl - stara macierz zostaje"""
            self.equalSubstitutionMatricies(False)

    # wyrownuje macierze substytucji (zwykla i best) wedlug decyzji: False - 'cofamy krok'; True - 'stawiamy krok'
    def equalSubstitutionMatricies(self, new_best = False):
        if new_best:
            self.best_gap_penalty = self.gap_penalty
            # diagonal
            self.best_substitution_matrix[A][A] = self.substitution_matrix[A][A]
            self.best_substitution_matrix[G][G] = self.substitution_matrix[G][G]
            self.best_substitution_matrix[C][C] = self.substitution_matrix[C][C]
            self.best_substitution_matrix[T][T] = self.substitution_matrix[T][T]
            # [i][i-1]
            self.best_substitution_matrix[G][A] = self.substitution_matrix[G][A]
            self.best_substitution_matrix[C][G] = self.substitution_matrix[C][G]
            self.best_substitution_matrix[T][C] = self.substitution_matrix[T][C]
            # [i][i+1]
            self.best_substitution_matrix[A][G] = self.substitution_matrix[A][G]
            self.best_substitution_matrix[G][C] = self.substitution_matrix[G][C]
            self.best_substitution_matrix[C][T] = self.substitution_matrix[C][T]
            # [i][i-2]
            self.best_substitution_matrix[C][A] = self.substitution_matrix[C][A]
            self.best_substitution_matrix[T][G] = self.substitution_matrix[T][G]
            # [i][i+2]
            self.best_substitution_matrix[A][C] = self.substitution_matrix[A][C]
            self.best_substitution_matrix[G][T] = self.substitution_matrix[G][T]
            # [i][i-3]
            self.best_substitution_matrix[T][A] = self.substitution_matrix[T][A]
            # [i][i+3]
            self.best_substitution_matrix[A][T] = self.substitution_matrix[A][T]
        else:
            self.gap_penalty = self.best_gap_penalty
            # diagonal
            self.substitution_matrix[A][A] = self.best_substitution_matrix[A][A]
            self.substitution_matrix[G][G] = self.best_substitution_matrix[G][G]
            self.substitution_matrix[C][C] = self.best_substitution_matrix[C][C]
            self.substitution_matrix[T][T] = self.best_substitution_matrix[T][T]
            # [i][i-1]
            self.substitution_matrix[G][A] = self.best_substitution_matrix[G][A]
            self.substitution_matrix[C][G] = self.best_substitution_matrix[C][G]
            self.substitution_matrix[T][C] = self.best_substitution_matrix[T][C]
            # [i][i+1]
            self.substitution_matrix[A][G] = self.best_substitution_matrix[A][G]
            self.substitution_matrix[G][C] = self.best_substitution_matrix[G][C]
            self.substitution_matrix[C][T] = self.best_substitution_matrix[C][T]
            # [i][i-2]
            self.substitution_matrix[C][A] = self.best_substitution_matrix[C][A]
            self.substitution_matrix[T][G] = self.best_substitution_matrix[T][G]
            # [i][i+2]
            self.substitution_matrix[A][C] = self.best_substitution_matrix[A][C]
            self.substitution_matrix[G][T] = self.best_substitution_matrix[G][T]
            # [i][i-3]
            self.substitution_matrix[T][A] = self.best_substitution_matrix[T][A]
            # [i][i+3]
            self.substitution_matrix[A][T] = self.best_substitution_matrix[A][T]

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