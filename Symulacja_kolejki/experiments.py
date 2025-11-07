import os
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scenarios import a_scenario, b_scenario

# Ustawienia folderów do zapisu wyników i wykresów
BASE_DIR = "experiment_results"
SCENARIO_A_FOLDER = os.path.join(BASE_DIR, "scenario_A")
SCENARIO_B_FOLDER = os.path.join(BASE_DIR, "scenario_B")
CHARTS_FOLDER = os.path.join(BASE_DIR, "charts")
CSV_FOLDER = os.path.join(BASE_DIR, "csv")
os.makedirs(SCENARIO_A_FOLDER, exist_ok=True)
os.makedirs(SCENARIO_B_FOLDER, exist_ok=True)
os.makedirs(CHARTS_FOLDER, exist_ok=True)
os.makedirs(CSV_FOLDER, exist_ok=True)

# Parametry eksperymentu
num_checkouts_list = [4, 6]
mu_service_list = [3, 5]
sigma_service_list = [0.5, 1.5]
lambda_arrival_list = [0.9, 1.1]

# Tworzymy listę wszystkich kombinacji parametrów (16 kombinacji)
experiments = list(itertools.product(num_checkouts_list, mu_service_list, sigma_service_list, lambda_arrival_list))

# Ustawienia symulacji: czas działania sklepu
START_TIME = datetime.strptime("2024-12-04 06:00", "%Y-%m-%d %H:%M")
END_TIME   = datetime.strptime("2024-12-04 22:00", "%Y-%m-%d %H:%M")

# Lista, w której będziemy zbierać wyniki poszczególnych powtórzeń
results_list = []

# Pętla eksperymentalna: dla każdej kombinacji parametrów
for exp_idx, (num_checkouts, mu_service, sigma_service, lambda_arrival) in enumerate(experiments, start=1):
    # Dla każdego zestawu parametrów wykonujemy 3 powtórzenia
    for rep in range(1, 4):
        # Ustawiamy unikalny seed (np. kombinacja numeru eksperymentu i powtórzenia)
        seed_val = exp_idx * 100 + rep

        # Uruchamiamy symulację dla scenariusza A (wspólna kolejka)
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

        # Uruchamiamy symulację dla scenariusza B (łączna kolejka – agregacja liczby klientów we wszystkich kolejkach)
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

        # Zapisujemy wyniki (kluczowe statystyki) dla obu scenariuszy
        results_list.append({
            "Experiment": exp_idx,
            "Repetition": rep,
            "Scenario": "A",
            "num_checkouts": num_checkouts,
            "mu_service": mu_service,
            "sigma_service": sigma_service,
            "lambda_arrival": lambda_arrival,
            "Generated Clients": a_stats["Generated Clients"],
            "Served Clients": a_stats["Served Clients"],
            "Avg Wait Time (min)": a_stats["Avg Wait Time (min)"],
            "Max Wait Time (min)": a_stats["Max Wait Time (min)"]
        })
        results_list.append({
            "Experiment": exp_idx,
            "Repetition": rep,
            "Scenario": "B",
            "num_checkouts": num_checkouts,
            "mu_service": mu_service,
            "sigma_service": sigma_service,
            "lambda_arrival": lambda_arrival,
            "Generated Clients": b_stats["Generated Clients"],
            "Served Clients": b_stats["Served Clients"],
            "Avg Wait Time (min)": b_stats["Avg Wait Time (min)"],
            "Max Wait Time (min)": b_stats["Max Wait Time (min)"]
        })

        # Zapisywanie wykresów – tylko dla pierwszego powtórzenia (rep == 1)
        if rep == 1:
            # Wykres ewolucji kolejki dla scenariusza A
            plt.figure(figsize=(10, 5))
            filtered_a = [(t, q) for t, q in a_stats["Queue History"] if START_TIME <= t <= END_TIME]
            if filtered_a:
                times = [t for t, q in filtered_a]
                queue_lengths = [q for t, q in filtered_a]
                plt.plot(times, queue_lengths, marker='o', linestyle='-', color='blue')
                plt.xlabel("Czas")
                plt.ylabel("Liczba klientów w kolejce")
                plt.title(f"Scenariusz A - Exp{exp_idx} (num_checkouts={num_checkouts}, mu={mu_service}, sigma={sigma_service}, lambda={lambda_arrival})")
                plt.grid(True)
                plt.xlim(START_TIME, END_TIME)
                filename = os.path.join(SCENARIO_A_FOLDER, f"Exp{exp_idx}_ScenarioA_num{num_checkouts}_mu{mu_service}_sigma{sigma_service}_lambda{lambda_arrival}.png")
                plt.savefig(filename)
            plt.close()

            # Wykres ewolucji kolejki dla scenariusza B
            plt.figure(figsize=(10, 5))
            filtered_b = [(t, q) for t, q in b_stats["Queue History"] if START_TIME <= t <= END_TIME]
            if filtered_b:
                times = [t for t, q in filtered_b]
                queue_lengths = [q for t, q in filtered_b]
                plt.plot(times, queue_lengths, marker='o', linestyle='-', color='red')
                plt.xlabel("Czas")
                plt.ylabel("Łączna liczba klientów w kolejkach")
                plt.title(f"Scenariusz B - Exp{exp_idx} (num_checkouts={num_checkouts}, mu={mu_service}, sigma={sigma_service}, lambda={lambda_arrival})")
                plt.grid(True)
                plt.xlim(START_TIME, END_TIME)
                filename = os.path.join(SCENARIO_B_FOLDER, f"Exp{exp_idx}_ScenarioB_num{num_checkouts}_mu{mu_service}_sigma{sigma_service}_lambda{lambda_arrival}.png")
                plt.savefig(filename)
            plt.close()

# Konwertujemy wyniki do DataFrame
df_results = pd.DataFrame(results_list)

# Zapisujemy wyniki poszczególnych powtórzeń do pliku CSV
csv_file = os.path.join(CSV_FOLDER, "experiment_results.csv")
df_results.to_csv(csv_file, index=False)

# Obliczamy średnie wyniki dla każdej kombinacji parametrów (dla każdego eksperymentu i scenariusza)
avg_results = df_results.groupby(
    ["Experiment", "Scenario", "num_checkouts", "mu_service", "sigma_service", "lambda_arrival"]
).mean().reset_index()

avg_csv_file = os.path.join(CSV_FOLDER, "average_experiment_results.csv")
avg_results.to_csv(avg_csv_file, index=False)

# Dla każdego eksperymentu (16 kombinacji) tworzymy wykresy słupkowe dla średniego i maksymalnego czasu oczekiwania, porównując scenariusze A i B
for exp in avg_results["Experiment"].unique():
    # Filtrujemy wyniki dla danego eksperymentu
    exp_data = avg_results[avg_results["Experiment"] == exp]
    # Założenie: dla każdego eksperymentu mamy dwa wiersze – jeden dla scenariusza A, jeden dla scenariusza B
    if len(exp_data) != 2:
        continue

    num_checkouts = exp_data["num_checkouts"].iloc[0]
    mu_service = exp_data["mu_service"].iloc[0]
    sigma_service = exp_data["sigma_service"].iloc[0]
    lambda_arrival = exp_data["lambda_arrival"].iloc[0]

    # Wykres słupkowy dla średniego czasu oczekiwania
    plt.figure(figsize=(8, 5))
    scenarios = exp_data["Scenario"]
    avg_wait = exp_data["Avg Wait Time (min)"]
    plt.bar(scenarios, avg_wait, color=["blue", "red"])
    plt.xlabel("Scenariusz")
    plt.ylabel("Średni czas oczekiwania (min)")
    plt.title(f"Exp{exp}: Średni czas oczekiwania\n(num_checkouts={num_checkouts}, mu={mu_service}, sigma={sigma_service}, lambda={lambda_arrival})")
    filename = os.path.join(CHARTS_FOLDER, f"Exp{exp}_AvgWait_num{num_checkouts}_mu{mu_service}_sigma{sigma_service}_lambda{lambda_arrival}.png")
    plt.savefig(filename)
    plt.close()

    # Wykres słupkowy dla maksymalnego czasu oczekiwania
    plt.figure(figsize=(8, 5))
    max_wait = exp_data["Max Wait Time (min)"]
    plt.bar(scenarios, max_wait, color=["blue", "red"])
    plt.xlabel("Scenariusz")
    plt.ylabel("Maksymalny czas oczekiwania (min)")
    plt.title(f"Exp{exp}: Maksymalny czas oczekiwania\n(num_checkouts={num_checkouts}, mu={mu_service}, sigma={sigma_service}, lambda={lambda_arrival})")
    filename = os.path.join(CHARTS_FOLDER, f"Exp{exp}_MaxWait_num{num_checkouts}_mu{mu_service}_sigma{sigma_service}_lambda{lambda_arrival}.png")
    plt.savefig(filename)
    plt.close()

print("Eksperymenty zakończone. Wyniki oraz wykresy zapisane w folderze:", BASE_DIR)
