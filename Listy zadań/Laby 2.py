import random
import statistics
from statistics import median
import pandas as pd
import numpy as np
import uniform
from scipy import stats
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, uniform, t, norm

def histogram(array, n):
    # Tworzenie histogramu
    plt.hist(array, bins=10, density=True, alpha=0.6, color='g', edgecolor='black')

    # Ręczne określenie przedziału x i funkcji gęstości
    x = [-1 + i * 0.01 for i in range(201)]  # Generowanie wartości od -1 do 1 z krokiem 0.01
    uniform_pdf = [1 / 2 for _ in x]  # Gęstość rozkładu równomiernego U(-1,1), stała wartość 1/2

    # Rysowanie funkcji gęstości
    plt.plot(x, uniform_pdf, label="Teoretyczna gęstość rozkładu U(-1,1)", color='r')

    # Ustawienia wykresu
    plt.title(f"Histogram dla ciągu {n} elementów z funkcją gęstości U(-1,1)")
    plt.xlabel("Wartości")
    plt.ylabel("Gęstość")
    plt.legend()

    # Wyświetlenie wykresu
    plt.show()

tab_15 = []
tab_120 = []

#a)
for i in range(0,15):
    random_number = random.uniform(-1,1)
    tab_15.append(random_number)
for i in range(0,120):
    random_number = random.uniform(-1,1)
    tab_120.append(random_number)

#b)
#Średnia
mean_15 = np.mean(tab_15)
mean_120 = np.mean(tab_120)
#Mediana
median_15 = np.median(tab_15)
median_120 = np.median(tab_120)
#Moda
mode_15 = stats.mode(tab_15)
mode_120 = stats.mode(tab_120)
#Odchylenie standardowe
std_dev_15 = np.std(tab_15)
std_dev_120 = np.std(tab_120)
#Wariancja
var_15 = np.var(tab_15)
var_120 = np.var(tab_120)
#Skośność
skew_15 = stats.skew(tab_15)
skew_120 = stats.skew(tab_120)
#Kurtoza
kurt_15 = stats.kurtosis(tab_15)
kurt_120 = stats.kurtosis(tab_120)
#Zakres (Wybrana)
range_15 = np.max(tab_15) - np.min(tab_15)
range_120 = np.max(tab_120) - np.max(tab_120)


# Wartości teoretyczne dla rozkładu U(-1, 1)
teo_mean = 0
teo_median = 0
teo_mode = "Brak, szansa na wylosowanie dwóch tych samych liczb jest praktycznie niemożliwa"
teo_std_dev = (1 / (3 ** 0.5))  # sqrt(1/3)
teo_var = 1 / 3
teo_skew = 0
teo_kurt = -6 / 5
teo_range = 2

#d.1
print("Test Shapiro-Wilka\r")

U = []
#liczymy wartość U (Wartość zestandaryzowane)
for i in tab_15:
    U.append((i-mean_15)/std_dev_15)

#Wartości współczynników shaprio wilka z tablic
A = [0.5150, 0.3306, 0.2495, 0.1878, 0.1353, 0.0880, 0.0433, 0.0]
#Liczymy górną część ułamka
P = 0
for i in range(len(A)):
    P+=A[i]*(sorted(U,reverse=True)[i]-sorted(U)[i])
#Liczymy dolną część ułamka
Q = 0
mean_U = statistics.mean(U)
for i in U:
    Q+=(i-mean_U)**2
W = P**2/Q

# Wartośc krytyczna dla testu odczytana z tabelki
war_kryt_sw = 0.881

print("H0: nasz rozkład jest normalny")
print("HA: nasz rozkład NIE jest normalny")
print("Poziom istotności alfa = 5%")
print(f"Wartośc testu W wynosi: {W}")
print(f"Wartość krytyczna dla testu shapiro-wilka wynosi: {war_kryt_sw}")
if W > war_kryt_sw:
    print("Nie ma podstaw na odrzucenie H0")
else:
    print("Odrzucamy H0")


print("\rTest Kolmogorova-Smirnova\r")
dane = np.sort(tab_120)
n = len(dane)
ecdf = np.arange(1, n+1) / n
teo_dystrybuanta = norm.cdf(dane, loc=0.5, scale=0.5)

D_plus = np.abs(ecdf - teo_dystrybuanta)
D_minus = np.abs(teo_dystrybuanta - np.arange(0, n) / n)
D = np.max([D_plus, D_minus])

alpha = 0.05
D_kryt = 1.36 / np.sqrt(n)
print("H0: nasz rozkład jest normalny")
print("HA: nasz rozkład NIE jest normalny")
print("Poziom istotności alfa = 5%")
print(f"Wartośc testu D wynosi: {D}")
print(f"Wartość krytyczna dla testu Kolmogorova-Smirnova wynosi: {D_kryt}")
if D > D_kryt:
    print("Odrzucamy H0")
else:
    print("Nie ma podstaw do odrzucenia H0")


#Porównanie wartości
print(f"Średnia obliczona dla ciągu 15 to {mean_15}, dla 120 to {mean_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_mean}")
print(f"Mediana obliczona dla ciągu 15 to {median_15}, dla 120 to {median_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_median}")
if int(mode_15.count.item()) > 1 or int(mode_120.count.item()) > 1:
    print(f"Moda obliczona dla ciągu 15 to {mode_15} i wystąpiła {mode_15.count.item()}, dla 120 to {mode_120} i wystąpiła {mode_120.count.item()},"
          f"a teoretyczna wartość dla rozkładu (-1, 1) nie istnieje")
else:
    print("Moda dla ciągu 15, 120 i rozkładu (-1, 1) nie istnieje")
print(f"Odchylenie standardowe obliczone dla ciągu 15 to {std_dev_15}, dla 120 to {std_dev_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_std_dev}")
print(f"Wariancja obliczona dla ciągu 15 to {var_15}, dla 120 to {var_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_var}")
print(f"Skośność obliczona dla ciągu 15 to {skew_15}, dla 120 to {skew_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_skew}")
print(f"Kurtoza obliczona dla ciągu 15 to {kurt_15}, dla 120 to {kurt_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_kurt}")
print(f"Zakres obliczony dla ciągu 15 to {range_15}, dla 120 to {range_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_range}")

#c)
histogram(tab_15, 15)
histogram(tab_120, 120)

#d)
exp_mean = 0

#Test dla 15
sample_mean = mean_15  # Średnia z próby
sample_std = std_dev_15  # Odchylenie standardowe z próby
n = len(tab_15)  # Liczność próby

# Obliczenie statystyki t
t_statistic = (sample_mean - exp_mean) / (sample_std / (n**2))

# Zakładamy poziom istotności alpha = 0.05 i symetryczne rozkłady
# Obszar krytyczny (dla dwustronnego testu) na poziomie 5% przy df = n-1
# Aby uprościć, przyjmiemy wartość krytyczną z tabeli t-Studenta dla dużych prób:

t_critical_15 = 2.145  # dla 14 stopni swobody (n-1) przy poziomie istotności 0.05

# Porównanie statystyki t z wartością krytyczną
print(f"\nTest średniej dla próby {n} elementów:")
print(f"Obliczona statystyka t: {t_statistic}")
print(f"Wartość krytyczna t: {t_critical_15}")

if abs(t_statistic) > t_critical_15:
    print("Odrzucamy hipotezę zerową (H0): średnia nie jest równa 0.")
else:
    print("Nie ma podstaw do odrzucenia hipotezy zerowej (H0): średnia jest równa 0.")

#Test dla 120
sample_mean = mean_120  # Średnia z próby
sample_std = std_dev_120  # Odchylenie standardowe z próby
n = len(tab_120)  # Liczność próby

# Obliczenie statystyki t
t_statistic = (sample_mean - exp_mean) / (sample_std / (n**2))

# Zakładamy poziom istotności alpha = 0.05 i symetryczne rozkłady
# Obszar krytyczny (dla dwustronnego testu) na poziomie 5% przy df = n-1
# Aby uprościć, przyjmiemy wartość krytyczną z tabeli t-Studenta dla dużych prób:

t_critical_120 = 1.980  # dla 119 stopni swobody (n-1) przy poziomie istotności 0.05

# Porównanie statystyki t z wartością krytyczną
print(f"\nTest średniej dla próby {n} elementów:")
print(f"Obliczona statystyka t: {t_statistic}")
print(f"Wartość krytyczna t: {t_critical_120}")

if abs(t_statistic) > t_critical_120:
    print("Odrzucamy hipotezę zerową (H0): średnia nie jest równa 0.")
else:
    print("Nie ma podstaw do odrzucenia hipotezy zerowej (H0): średnia jest równa 0.")