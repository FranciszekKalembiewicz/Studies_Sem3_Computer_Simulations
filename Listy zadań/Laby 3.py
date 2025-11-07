import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy
from scipy import stats
import statistics
import pandas as pd

#a
tab_15 = []
tab_120 = []

for i in range(0,15):
    random_number = np.random.normal(0.5,0.5)
    tab_15.append(random_number)
for i in range(0,120):
    random_number = np.random.normal(0.5,0.5)
    tab_120.append(random_number)

#b.1
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


# Wartości teoretyczne
teo_mean = 0.5
teo_median = 0.5
teo_mode = 0.5
teo_std_dev = 0.5
teo_var = 0.25
teo_skew = 0
teo_kurt = 3
teo_range = "inf"

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

#b.2
#Porównanie wartości
print(f"Średnia obliczona dla ciągu 15 to {mean_15}, dla 120 to {mean_120}, a teoretyczna wartość to {teo_mean}")
print(f"Mediana obliczona dla ciągu 15 to {median_15}, dla 120 to {median_120}, a teoretyczna wartość to {teo_median}")
print(f"Moda obliczona dla ciągu 15 to {mode_15}, dla 120 to {mode_120}, a teoretyczna wartość to {teo_std_dev}")
print(f"Odchylenie standardowe obliczone dla ciągu 15 to {std_dev_15}, dla 120 to {std_dev_120}, a teoretyczna wartość to {teo_std_dev}")
print(f"Wariancja obliczona dla ciągu 15 to {var_15}, dla 120 to {var_120}, a teoretyczna wartość to {teo_var}")
print(f"Skośność obliczona dla ciągu 15 to {skew_15}, dla 120 to {skew_120}, a teoretyczna wartość to {teo_skew}")
print(f"Kurtoza obliczona dla ciągu 15 to {kurt_15}, dla 120 to {kurt_120}, a teoretyczna wartość to {teo_kurt}")
print(f"Zakres obliczony dla ciągu 15 to {range_15}, dla 120 to {range_120}, a teoretyczna wartość to {teo_range}")

#c
plt.subplot(1,3,1)
plt.hist(tab_15,color="red",edgecolor = "black")
plt.subplot(1,3,2)
plt.hist(tab_120,color="cyan",edgecolor = "black")
plt.subplot(1,3,3)
x = np.linspace(-5, 5, 1000)
pdf = norm.pdf(x, 0.5, 0.5)
plt.plot(x, pdf,color="green")
plt.fill_between(x, pdf, alpha=0.3, color='green')

plt.show()

#d.2
# Test statystyczne

print("Założenia")
print("H0: Średnia z próby równa się 0.5")
print("HA: Średnia z próby NIE równa się 0.5")

print("\rtest t dla próby 15")
t = ((mean_15)-0)/std_dev_15*math.sqrt(15)
# Obliczanie wartości krytycznej
alfa = 0.05/2
df = 15-1
war_kryt_15 = scipy.stats.t.ppf(1-alfa,df)

print(f"Wartośc testu t wynosi: {t}")
print(f"Wartość krytyczna dla testu studenta wynosi: {war_kryt_15}")
if abs(t) > war_kryt_15:
    print("Odrzucamy H0")
else:
    print("Nie ma dowodów na odrzucenie H0")


print("\rtest z dla próby 120")
print("H0: Średnia z próby równa się 0.5")
print("HA: Średnia z próby NIE równa się 0.5")
z = (mean_120-0)/std_dev_120*math.sqrt(120)
alfa = 0.05/2
war_kryt_120 = scipy.stats.norm.ppf(1-alfa)
print(f"Wartośc testu z wynosi: {z}")
print(f"Wartość krytyczna dla testu Z wynosi: {war_kryt_120}")
if abs(t) > war_kryt_120:
    print("Odrzucamy H0")
else:
    print("Nie ma dowodów na odrzucenie H0")