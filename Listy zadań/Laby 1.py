import random
import matplotlib.pyplot as plt
#a
#ilość prób
k = {
    10: 1.833,
    100: 1.660,
    1000: 1.645
}
Chi_stat = {
    10: [0]*11,
    100: [0]*11,
    1000: [0]*11
}
for z in k:
    wynik = 0
    tab = []
    var = 0
    odl = 0
    for i in range(0,z):
        x = abs(random.uniform(0,20) - 10)
        y = abs(random.uniform(0,20) - 10)

        odl = float((x**2 + y**2)**0.5)
        pkt = 0
        if odl <= 1:
            pkt = 10
        elif odl >= 1 and odl <= 2:
            pkt = 9
        elif odl >= 2 and odl <= 3:
            pkt = 8
        elif odl >= 3 and odl <= 4:
            pkt = 7
        elif odl >= 4 and odl <= 5:
            pkt = 6
        elif odl >= 5 and odl <= 6:
            pkt = 5
        elif odl >= 6 and odl <= 7:
            pkt = 4
        elif odl >= 7 and odl <= 8:
            pkt = 3
        elif odl >= 8 and odl <= 9:
            pkt = 2
        elif odl >= 9 and odl <= 10:
            pkt = 1
        else:
            pkt = 0
        wynik += pkt
        tab.append(pkt)
#b
    sre = wynik/z
    for l in tab:
        var += (l-sre)**2
    odl = (var/z)**0.5
    print(f"Odchylenie standardowe dla próby ",z," to ",odl)
#c
    ocz_sre = 5
    t_stat = (sre - ocz_sre) / (odl / (z)**0.5)
    print("Dane są wylosowane z modułu random więc są niezależne, więc spełniają wymagania dla testu")
    print("Hipoteza zerowa: Średni wynik jest statystycznie istotnie większy od 5")
    print("Hipoteza alternatywna: Średni wynik jest statystycznie istotnie nie jest wiekszy 5")
    print(f"Dla próby z {z} powtórzeń, poziom istotności to 5%, statystyka testowa to {t_stat}, a wartość krytyczna wynosi {k[z]}")
    if t_stat > k[z]:
        print("Odrzucamy hipotezę zerową")
    else:
        print("Nie ma podstaw do odrzucenia hipotezy zerowej")

    for i in tab:
        Chi_stat[z][i] += 1

#d Tworzenie histogramu
    plt.hist(tab, bins=range(12), edgecolor='black')
    plt.title(f"Histogram dla {z} prób")
    plt.xlabel("Punkty")
    plt.ylabel("Częstość")
    plt.show()

#e
Chi_result = []
for i in Chi_stat:
    chi_test = 0
    exp_value = i/11
    for observed in Chi_stat[i]:
        chi_test += (observed - exp_value)**2/exp_value
    Chi_result.append(chi_test)

df = 11-1
pi = 0.05
critical_value = 18.31

for i, chi_test in zip([10, 100, 1000], Chi_result):
    if chi_test > critical_value:
        print(f"Wartość {chi_test} przekracza wartość krytyczną {critical_value}")
        print(f"Odrzucamy hipotezę o rozkładzie równomienym dla {i} prób")
    else:
        print(f"Wartość {chi_test} nie przekracza wartości krytycznej {critical_value}. ")
        print( f"Brak podstaw do odrzucenia hipotezy o rozkładzie równomiernym dla {i} prób.")