from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy import stats
from scipy.stats import shapiro
from scipy.stats import t
from scipy.stats import ttest_ind

def sum_of_digits(number):
    return sum(int(digit) for digit in str(number))

def linear_congruential_generator(seed, multiplier, increment, modulus):
    return (multiplier * seed + increment) % modulus

def generate_uniform_sequence(seed, multiplier, increment, modulus, n, m):
    sequence_20 = []
    sequence_100 = []
    current = seed
    for _ in range(n):
        current = linear_congruential_generator(current, multiplier, increment, modulus)
        uniform_number = (current / modulus) * 2 - 1
        sequence_20.append(uniform_number)
    for _ in range(m):
        current = linear_congruential_generator(current, multiplier, increment, modulus)
        uniform_number = (current / modulus) * 2 - 1
        sequence_100.append(uniform_number)
    return sequence_20, sequence_100


def generate_normal_sequence(sequence_uniform, mean=0.5, std_dev=0.5):
    normal_sequence = []
    for i in range(0, len(sequence_uniform), 2):
        u1 = sequence_uniform[i]
        u2 = sequence_uniform[i + 1] if i + 1 < len(sequence_uniform) else np.random.uniform(-1, 1)

        # Transformacja Boxa-Mullera
        z0 = np.sqrt(-2 * np.log(abs(u1))) * np.cos(2 * np.pi * u2)
        z1 = np.sqrt(-2 * np.log(abs(u1))) * np.sin(2 * np.pi * u2)

        # Przekształcenie do N(mean, std_dev)
        normal_sequence.append(mean + z0 * std_dev)
        normal_sequence.append(mean + z1 * std_dev)

    return normal_sequence[:len(sequence_uniform)]  # Dopasowanie długości


# Generowanie nasienia na podstawie bieżącego czasu
current_time = datetime.now().strftime("%H%M%S%f")
seed = sum_of_digits(int(current_time))

# Parametry generatora kongruencyjnego
multiplier = 1103515245
increment = 12345
modulus = 2 ** 31

# Generowanie sekwencji równomiernej
tab_20, tab_100 = generate_uniform_sequence(seed, multiplier, increment, modulus, 20, 100)

# Generowanie sekwencji normalnej
normal_sequence_20_LCG = generate_normal_sequence(tab_20)
normal_sequence_100_LCG = generate_normal_sequence(tab_100)

normal_sequence_20_random = []
normal_sequence_100_random = []

for i in range(0,20):
    random_number = np.random.normal(0.5,0.5)
    normal_sequence_20_random.append(random_number)
for i in range(0,100):
    random_number = np.random.normal(0.5,0.5)
    normal_sequence_100_random.append(random_number)


def testy_statystyczne(tab_20, tab_100):
    #b.1
    #Średnia
    mean_20 = np.mean(tab_20)
    mean_100 = np.mean(tab_100)
    #Mediana
    median_20 = np.median(tab_20)
    median_100 = np.median(tab_100)
    #Moda
    mode_20 = stats.mode(tab_20)
    mode_100 = stats.mode(tab_100)
    #Odchylenie standardowe
    std_dev_20 = np.std(tab_20)
    std_dev_100 = np.std(tab_100)
    #Wariancja
    var_20 = np.var(tab_20)
    var_100 = np.var(tab_100)
    #Skośność
    skew_20 = stats.skew(tab_20)
    skew_100 = stats.skew(tab_100)
    #Kurtoza
    kurt_20 = stats.kurtosis(tab_20)
    kurt_100 = stats.kurtosis(tab_100)
    #Zakres (Wybrana)
    range_20 = np.max(tab_20) - np.min(tab_20)
    range_100 = np.max(tab_100) - np.max(tab_100)


    # Wartości teoretyczne
    teo_mean = 0.5
    teo_median = 0.5
    teo_mode = 0.5
    teo_std_dev = 0.5
    teo_var = 0.25
    teo_skew = 0
    teo_kurt = 3
    teo_range = "inf"
#d1
    print("\nTest Shapiro-Wilka dla 20")

    print("H0: nasz rozkład jest normalny")
    print("HA: nasz rozkład NIE jest normalny")
    print("Poziom istotności alfa = 5%")
    stat, p_value = shapiro(tab_20)

    print("Statystyka testowa:", stat)
    print("Wartość p:", p_value)

    # Sprawdzenie, czy p-value jest mniejsze od 0.05 (próg istotności)
    if p_value < 0.05:
        print("Odrzucamy hipotezę zerową - dane nie są zgodne z rozkładem normalnym.")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - dane są zgodne z rozkładem normalnym.")

    print("\nTest Shapiro-Wilka dla 100")

    print("H0: nasz rozkład jest normalny")
    print("HA: nasz rozkład NIE jest normalny")
    print("Poziom istotności alfa = 5%")
    stat, p_value = shapiro(tab_100)

    print("Statystyka testowa:", stat)
    print("Wartość p:", p_value)

    # Sprawdzenie, czy p-value jest mniejsze od 0.05 (próg istotności)
    if p_value < 0.05:
        print("Odrzucamy hipotezę zerową - dane nie są zgodne z rozkładem normalnym.")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - dane są zgodne z rozkładem normalnym.")

    #b.2
    #Porównanie wartości
    print(f"\nŚrednia obliczona dla ciągu 20 to {mean_20}, dla 100 to {mean_100}, a teoretyczna wartość to {teo_mean}")
    print(f"Mediana obliczona dla ciągu 20 to {median_20}, dla 100 to {median_100}, a teoretyczna wartość to {teo_median}")
    print(f"Moda obliczona dla ciągu 20 to {mode_20}, dla 100 to {mode_100}, a teoretyczna wartość to {teo_std_dev}")
    print(f"Odchylenie standardowe obliczone dla ciągu 20 to {std_dev_20}, dla 100 to {std_dev_100}, a teoretyczna wartość to {teo_std_dev}")
    print(f"Wariancja obliczona dla ciągu 20 to {var_20}, dla 100 to {var_100}, a teoretyczna wartość to {teo_var}")
    print(f"Skośność obliczona dla ciągu 20 to {skew_20}, dla 100 to {skew_100}, a teoretyczna wartość to {teo_skew}")
    print(f"Kurtoza obliczona dla ciągu 20 to {kurt_20}, dla 100 to {kurt_100}, a teoretyczna wartość to {teo_kurt}")
    print(f"Zakres obliczony dla ciągu 20 to {range_20}, dla 100 to {range_100}, a teoretyczna wartość to {teo_range}\n")

    #c
    plt.subplot(1,3,1)
    plt.hist(tab_20,color="red",edgecolor = "black")
    plt.subplot(1,3,2)
    plt.hist(tab_100,color="cyan",edgecolor = "black")
    plt.subplot(1,3,3)
    x = np.linspace(-5, 5, 1000)
    pdf = norm.pdf(x, 0.5, 0.5)
    plt.plot(x, pdf,color="green")
    plt.fill_between(x, pdf, alpha=0.3, color='green')

    plt.show()

    #d.2
    # Test statystyczne
    print("\n----------------Test Studenta--------------------")
    print("Założenia")
    print("H0: Średnia z próby równa się 0.5")
    print("HA: Średnia z próby NIE równa się 0.5")

    mu = 0.5
    n = len(tab_20)
    sample_mean = np.mean(tab_20)
    sample_std = np.std(tab_20, ddof=1)  # Odchylenie standardowe z próby (z n-1 stopniami swobody)

    # Obliczanie statystyki t
    t_stat = (sample_mean - mu) / (sample_std / np.sqrt(n))

    # Obliczanie wartości p dla dwustronnego testu t
    df = n - 1
    p_value = 2 * (1 - t.cdf(abs(t_stat), df))

    print("Statystyka t:", t_stat)
    print("Wartość p:", p_value)

    # Sprawdzenie istotności przy poziomie alfa 0.05
    if p_value < 0.05:
        print("Odrzucamy hipotezę zerową - średnia różni się od 0.5")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - średnia nie różni się istotnie od 0.5")

    print("\n----------------Test Z--------------------")
    print("Założenia")
    print("H0: Średnia z próby równa się 0.5")
    print("HA: Średnia z próby NIE równa się 0.5")
    mu = 0.5
    sample_mean = np.mean(tab_100)
    sample_std = np.std(tab_100, ddof=1)  # Odchylenie standardowe z próby
    n = len(tab_100)

    # Obliczanie statystyki z
    z_score = (sample_mean - mu) / (sample_std / np.sqrt(n))

    # Obliczanie wartości p (dla dwustronnego testu z)
    p_value = 2 * (1 - norm.cdf(abs(z_score)))

    print("Statystyka Z:", z_score)
    print("Wartość p:", p_value)

    # Sprawdzenie istotności przy poziomie alfa 0.05
    if p_value < 0.05:
        print("Odrzucamy hipotezę zerową - średnia różni się od 0.5")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - średnia nie różni się istotnie od 0.5")



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

def generate_normal_sequence(sequence_uniform, mean=0.5, std_dev=0.5):
    normal_sequence = []
    for i in range(0, len(sequence_uniform), 2):
        u1 = sequence_uniform[i]
        u2 = sequence_uniform[i + 1] if i + 1 < len(sequence_uniform) else np.random.uniform(-1, 1)

        # Transformacja Boxa-Mullera
        z0 = np.sqrt(-2 * np.log(abs(u1))) * np.cos(2 * np.pi * u2)
        z1 = np.sqrt(-2 * np.log(abs(u1))) * np.sin(2 * np.pi * u2)

        # Przekształcenie do N(mean, std_dev)
        normal_sequence.append(mean + z0 * std_dev)
        normal_sequence.append(mean + z1 * std_dev)

    return normal_sequence[:len(sequence_uniform)]  # Dopasowanie długości


# Parametry dla generatora LCG
current_time = datetime.now().strftime("%H%M%S%f")
seed = sum_of_digits(int(current_time))
multiplier = 1103515245
increment = 12345
modulus = 2**31

alpha = 0.05
n20 = 20
n100 = 100


means_20_LCG = []
means_100_LCG = []
means_20_random = []
means_100_random = []

for _ in range(250):
    sample_20_LCG, current = generate_uniform_sequence(seed, multiplier, increment, modulus, n20)
    seed = current
    sample_100_LCG, current = generate_uniform_sequence(seed, multiplier, increment, modulus, n100)
    seed = current
    sample_20_LCG = generate_normal_sequence(sample_20_LCG)
    sample_100_LCG = generate_normal_sequence(sample_100_LCG)
    means_20_LCG.append(np.mean(sample_20_LCG))
    means_100_LCG.append(np.mean(sample_100_LCG))

    # Generator random.uniform dla 20-elementowej i 100-elementowej próbki
    sample_20_random = [np.random.normal(0.5, 0.5) for _ in range(n20)]
    sample_100_random = [np.random.normal(0.5, 0.5) for _ in range(n100)]
    means_20_random.append(np.mean(sample_20_random))
    means_100_random.append(np.mean(sample_100_random))

def test_studenta_dla_dwóch_próbek(tab_20, tab_120):    # Test Wilcoxona dla parowanych danych
    stat, p_value = ttest_ind(tab_20, tab_120)

    print("Statystyka testowa:", stat)
    print("Wartość p:", p_value)

    # Sprawdzenie istotności przy poziomie alfa 0.05
    if p_value < 0.05:
        print("Odrzucamy hipotezę zerową - średnie w obu grupach są różne")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - średnie w obu grupach nie różnią się istotnie")

def test_Schapiro_dla_srednich(tab_20, tab_100):
    print("\nTest Schapiro wilka dla 20")
    print("H0: nasz rozkład jest normalny")
    print("HA: nasz rozkład NIE jest normalny")
    print("Poziom istotności alfa = 5%")
    stat, p_value = shapiro(tab_20)

    print("Statystyka testowa:", stat)
    print("Wartość p:", p_value)

    # Sprawdzenie, czy p-value jest mniejsze od 0.05 (próg istotności)
    if p_value < 0.05:
        print("Odrzucamy hipotezę zerową - dane nie są zgodne z rozkładem normalnym.")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - dane są zgodne z rozkładem normalnym.")


    print("\nTest Schapiro wilka dla 100")

    print("H0: nasz rozkład jest normalny")
    print("HA: nasz rozkład NIE jest normalny")
    print("Poziom istotności alfa = 5%")
    stat, p_value = shapiro(tab_100)

    print("Statystyka testowa:", stat)
    print("Wartość p:", p_value)

    # Sprawdzenie, czy p-value jest mniejsze od 0.05 (próg istotności)
    if p_value < 0.05:
        print("Odrzucamy hipotezę zerową - dane nie są zgodne z rozkładem normalnym.")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej - dane są zgodne z rozkładem normalnym.")

print("----------PRÓBA LCG----------")
testy_statystyczne(normal_sequence_20_LCG, normal_sequence_100_LCG)
print("\n\n\n\n----------PRÓBA RANDOM.Normal----------")
testy_statystyczne(normal_sequence_20_random, normal_sequence_100_random)

print("\n-------------------------Test dla średnich z 250 pomiarów---------------------------\n")
print("-----------PRÓBA Schapiro-Wilka----------")
print(print("----------PRÓBA LCG----------"))
test_Schapiro_dla_srednich(means_20_LCG, means_100_LCG)
print("----------PRÓBA RANDOM.UNIFORM----------")
test_Schapiro_dla_srednich(means_20_random, means_100_random)

print("----------TEST T dla dwóch próbek----------------")
print("Próba dla 20")
test_studenta_dla_dwóch_próbek(means_20_LCG, means_20_random)
print("\nPróba dla 100")
test_studenta_dla_dwóch_próbek(means_100_LCG, means_100_random)
