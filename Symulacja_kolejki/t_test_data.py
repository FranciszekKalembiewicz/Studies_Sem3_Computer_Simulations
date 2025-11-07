import os
import pandas as pd
from datetime import datetime
from scenarios import a_scenario, b_scenario

# Ustawione parametry eksperymentu
num_checkouts = 6
mu_service = 5
sigma_service = 0.5
lambda_arrival = 1.1

# Czas działania sklepu
START_TIME = datetime.strptime("2024-12-04 06:00", "%Y-%m-%d %H:%M")
END_TIME = datetime.strptime("2024-12-04 22:00", "%Y-%m-%d %H:%M")

# Listy, w których będziemy zapisywać średni czas oczekiwania dla obu scenariuszy
avg_wait_A_list = []
avg_wait_B_list = []

# Liczba powtórzeń symulacji (dla testu statystycznego)
NUM_SIMULATIONS = 100

# Pętla wykonująca 100 symulacji – dla każdego powtórzenia używamy innego seed (np. seed = numer powtórzenia)
for rep in range(1, NUM_SIMULATIONS + 1):
    seed_val = rep  # Dla uproszczenia seed = numer powtórzenia

    # Uruchomienie symulacji dla scenariusza A (wspólna kolejka)
    a_stats = a_scenario(
        lambda_arrival=lambda_arrival,
        start_time=START_TIME,
        end_time=END_TIME,
        mu_service=mu_service,
        sigma_service=sigma_service,
        num_checkouts=num_checkouts,
        print_logs=False,
        seed=seed_val
    )

    # Uruchomienie symulacji dla scenariusza B (łączna kolejka – agregacja liczby klientów we wszystkich kolejkach)
    b_stats = b_scenario(
        lambda_arrival=lambda_arrival,
        start_time=START_TIME,
        end_time=END_TIME,
        mu_service=mu_service,
        sigma_service=sigma_service,
        num_checkouts=num_checkouts,
        print_logs=False,
        seed=seed_val
    )

    # Zbieramy średni czas oczekiwania dla obu scenariuszy
    avg_wait_A_list.append(a_stats["Avg Wait Time (min)"])
    avg_wait_B_list.append(b_stats["Avg Wait Time (min)"])

# Wypisujemy listy w konsoli
print("Avg Wait Time for Scenario A (100 simulations):")
print(avg_wait_A_list)
print("Avg Wait Time for Scenario B (100 simulations):")
print(avg_wait_B_list)

# Zapisujemy dane do pliku CSV
output_file = "t_test_data.csv"
df = pd.DataFrame({
    "Scenario A": avg_wait_A_list,
    "Scenario B": avg_wait_B_list
})
df.to_csv(output_file, index=False)

print(f"Dane zapisane do pliku: {output_file}")
