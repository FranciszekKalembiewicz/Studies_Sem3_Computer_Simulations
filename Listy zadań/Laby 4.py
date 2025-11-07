from datetime import datetime
import uniform
from scipy import stats
from scipy.stats import skew, kurtosis, uniform, t, norm, wilcoxon
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import stats



def sum_of_digits(number):
    return sum(int(digit) for digit in str(number))

def linear_congruential_generator(seed, multiplier, increment, modulus):
    return (multiplier * seed + increment) % modulus

def generate_uniform_sequence(seed, multiplier, increment, modulus, n, m):
    sequence_15 = []
    sequence_120 = []
    current = seed
    for _ in range(n):
        current = linear_congruential_generator(current, multiplier, increment, modulus)
        uniform_number = (current / modulus) * 2 - 1
        sequence_15.append(uniform_number)
    for _ in range(m):
        current = linear_congruential_generator(current, multiplier, increment, modulus)
        uniform_number = (current / modulus) * 2 - 1
        sequence_120.append(uniform_number)
    return sequence_15, sequence_120

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

#a.1) Generator liczb losowych
current_time = datetime.now().strftime("%H%M%S%f")
seed = sum_of_digits(int(current_time))
multiplier = 1103515245
increment = 12345
modulus = 2**31

tab_15, tab_120 = generate_uniform_sequence(seed, multiplier, increment, modulus, 15, 120)

#a.2)
tab_15_random = []
tab_120_random = []
for i in range(0,15):
    random_number = random.uniform(-1,1)
    tab_15_random.append(random_number)
for i in range(0,120):
    random_number = random.uniform(-1,1)
    tab_120_random.append(random_number)

def testy_statystyczne(tab_15, tab_120):
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
    print("\nTest Kolmogorova-Smirnova")
    dane = np.sort(tab_15)
    n = len(dane)
    ecdf = np.arange(1, n+1) / n
    teo_dystrybuanta = uniform.cdf(dane, loc=-1, scale=2)

    D_plus = np.abs(ecdf - teo_dystrybuanta)
    D_minus = np.abs(teo_dystrybuanta - np.arange(0, n) / n)
    D = np.max([D_plus, D_minus])

    alpha = 0.05
    D_kryt = 0.351
    print("H0: nasz rozkład jest normalny")
    print("HA: nasz rozkład NIE jest normalny")
    print("Poziom istotności alfa = 5%")
    print(f"Wartośc testu D wynosi: {D}")
    print(f"Wartość krytyczna dla testu Kolmogorova-Smirnova wynosi: {D_kryt}")
    if D > D_kryt:
        print("Odrzucamy H0")
    else:
        print("Nie ma podstaw do odrzucenia H0")

    print("\nTest Kolmogorova-Smirnova dla 120")
    dane = np.sort(tab_120)
    n = len(dane)
    ecdf = np.arange(1, n+1) / n
    teo_dystrybuanta = uniform.cdf(dane, loc=-1, scale=2)

    D_plus = np.abs(ecdf - teo_dystrybuanta)
    D_minus = np.abs(teo_dystrybuanta - np.arange(0, n) / n)
    D = np.max([D_plus, D_minus])

    alpha = 0.05
    D_kryt = 0.124
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
    print(f"\nŚrednia obliczona dla ciągu 15 to {mean_15}, dla 120 to {mean_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_mean}")
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
    print(f"Zakres obliczony dla ciągu 15 to {range_15}, dla 120 to {range_120}, a teoretyczna wartość dla rozkładu (-1, 1) to {teo_range}\n")

    #c)
    histogram(tab_15, 15)
    histogram(tab_120, 120)

    #d.2)

    print("Założenia")
    print("H0: Średnia z próby równa się 0")
    print("HA: Średnia z próby NIE równa się 0")

    print("\ntest t dla próby 15")
    t = ((mean_15) - 0) / std_dev_15 * math.sqrt(15)
    # Obliczanie wartości krytycznej
    alfa = 0.05 / 2
    df = 15 - 1
    war_kryt_15 = scipy.stats.t.ppf(1 - alfa, df)

    print(f"Wartośc testu t wynosi: {t}")
    print(f"Wartość krytyczna dla testu studenta wynosi: {war_kryt_15}")
    if abs(t) > war_kryt_15:
        print("Odrzucamy H0")
    else:
        print("Nie ma dowodów na odrzucenie H0")

    print("\ntest z dla próby 120")
    print("H0: Średnia z próby równa się 0")
    print("HA: Średnia z próby NIE równa się ")
    z = (mean_120 - 0) / std_dev_120 * math.sqrt(120)
    alfa = 0.05 / 2
    war_kryt_120 = scipy.stats.norm.ppf(1 - alfa)
    print(f"Wartośc testu z wynosi: {z}")
    print(f"Wartość krytyczna dla testu Z wynosi: {war_kryt_120}")
    if abs(t) > war_kryt_120:
        print("Odrzucamy H0")
    else:
        print("Nie ma dowodów na odrzucenie H0")






def sum_of_digits(number):
    return sum(int(digit) for digit in str(number))

def linear_congruential_generator(seed, multiplier, increment, modulus):
    return (multiplier * seed + increment) % modulus

def generate_uniform_sequence(seed, multiplier, increment, modulus, length):
    sequence = []
    current = seed
    for _ in range(length):
        current = linear_congruential_generator(current, multiplier, increment, modulus)
        uniform_number = (current / modulus) * 2 - 1
        sequence.append(uniform_number)
    return sequence, current

# Parametry dla generatora LCG
current_time = datetime.now().strftime("%H%M%S%f")
seed = sum_of_digits(int(current_time))
multiplier = 1103515245
increment = 12345
modulus = 2**31

alpha = 0.05
n15 = 15
n120 = 120


means_15_LCG = []
means_120_LCG = []
means_15_random = []
means_120_random = []

for _ in range(250):
    sample_15_LCG, current = generate_uniform_sequence(seed, multiplier, increment, modulus, n15)
    seed = current
    sample_120_LCG, current = generate_uniform_sequence(seed, multiplier, increment, modulus, n120)
    seed = current
    means_15_LCG.append(np.mean(sample_15_LCG))
    means_120_LCG.append(np.mean(sample_120_LCG))

    # Generator random.uniform dla 15-elementowej i 120-elementowej próbki
    sample_15_random = [random.uniform(-1, 1) for _ in range(n15)]
    sample_120_random = [random.uniform(-1, 1) for _ in range(n120)]
    means_15_random.append(np.mean(sample_15_random))
    means_120_random.append(np.mean(sample_120_random))


def test_wilcoxon(tab_15, tab_120):    # Test Wilcoxona dla parowanych danych
    stat, p_value = stats.wilcoxon(tab_15, tab_120)

    print("Statystyka testowa:", stat)
    print("Wartość p:", p_value)

    # Interpretacja wyniku
    alpha = 0.05  # Poziom istotności
    if p_value < alpha:
        print("Odrzucamy hipotezę zerową - mediany dwóch tablic różnią się")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - mediany dwóch tablic są podobne")

def test_Kolmogorova_dla_srednich(tab_15, tab_120):
    print("\nTest Kolmogorova-Smirnova dla 15")

    stat, p_value = stats.kstest(tab_15, 'norm')

    print("H0: nasz rozkład jest normalny")
    print("HA: nasz rozkład NIE jest normalny")
    print("Poziom istotności alfa = 5%")
    print("Statystyka testowa:", stat)
    print("Wartość p:", p_value)

    alpha = 0.05  # Poziom istotności


    if p_value < alpha:
        print("Odrzucamy hipotezę zerową - dane nie pochodzą z rozkładu normalnego")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - dane mogą pochodzić z rozkładu normalnego")

    print("\nTest Kolmogorova-Smirnova dla 120")

    stat, p_value = stats.kstest(tab_120, 'norm')

    print("H0: nasz rozkład jest normalny")
    print("HA: nasz rozkład NIE jest normalny")
    print("Poziom istotności alfa = 5%")
    print("Statystyka testowa:", stat)
    print("Wartość p:", p_value)

    alpha = 0.05  # Poziom istotności

    if p_value < alpha:
        print("Odrzucamy hipotezę zerową - dane nie pochodzą z rozkładu normalnego")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - dane mogą pochodzić z rozkładu normalnego")



print("----------PRÓBA LCG----------")
testy_statystyczne(tab_15, tab_120)
print("\n\n\n\n----------PRÓBA RANDOM.UNIFORM----------")
testy_statystyczne(tab_15_random, tab_120_random)


print("\n-------------------------Test dla średnich z 250 pomiarów---------------------------\n")


print("-----------PRÓBA Kolmogorova-Smirnova----------")
print(print("----------PRÓBA LCG----------"))
test_Kolmogorova_dla_srednich(means_15_LCG, means_120_LCG)
print("----------PRÓBA RANDOM.UNIFORM----------")
test_Kolmogorova_dla_srednich(means_15_random, means_120_random)

print("----------TEST Wilcoxona----------------")
print("Próba dla 15")
test_wilcoxon(means_15_LCG, means_15_random)
print("\nPróba dla 120")
test_wilcoxon(means_120_LCG, means_120_random)
