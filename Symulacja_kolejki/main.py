import math
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scenarios import a_scenario, b_scenario


def plot_comparison(df_comparison):
    """
    Rysuje wykresy słupkowe dla głównych statystyk symulacji, rozmieszczone w siatce 2 kolumnowej.
    """
    df_comparison = df_comparison.set_index("Scenario")
    metrics = df_comparison.columns
    num_metrics = len(metrics)

    ncols = 2
    nrows = math.ceil(num_metrics / ncols)
    fig, axs = plt.subplots(nrows, ncols, figsize=(10, 5 * nrows))

    if nrows == 1 and ncols == 1:
        axs = [axs]
    elif nrows == 1 or ncols == 1:
        axs = axs.flatten()
    else:
        axs = axs.flatten()

    for i, metric in enumerate(metrics):
        ax = axs[i]
        df_comparison[metric].plot(kind='bar', ax=ax, color=['skyblue', 'salmon'])
        ax.set_title(metric)
        ax.set_xlabel("Scenario")
        ax.set_ylabel(metric)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center',
                        xytext=(0, 8), textcoords='offset points')

    for j in range(i + 1, len(axs)):
        fig.delaxes(axs[j])

    plt.tight_layout()
    plt.show()


def plot_queue_history(queue_history, start_time, end_time, title):
    """
    Rysuje wykres liniowy pokazujący ewolucję długości kolejki w czasie.

    Parametry:
      - queue_history: lista krotek (czas, qsize)
      - title: tytuł wykresu (np. "Scenariusz A" lub "Scenariusz B")
    """
    filtered = [(t, q) for t, q in queue_history if start_time <= t <= end_time]
    if not filtered:
        print("Brak danych w wybranym przedziale czasowym.")
        return

    times = [t for t, q in filtered]
    queue_lengths = [q for t, q in filtered]

    plt.figure(figsize=(10, 5))
    plt.plot(times, queue_lengths, marker='o', linestyle='-', color='blue')
    plt.xlabel("Czas")
    plt.ylabel("Liczba klientów w kolejce")
    plt.title(f"Ewolucja długości kolejki w czasie ({title})")
    plt.grid(True)
    plt.xlim(start_time, end_time)
    plt.tight_layout()
    plt.show()


def main():
    """
    Główny punkt wejścia – definiuje parametry symulacji, wywołuje scenariusze,
    tworzy DataFrame z porównaniem wyników oraz wyświetla wizualizacje.
    """
    start_time = datetime.strptime("2024-12-04 06:00", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime("2024-12-04 22:00", "%Y-%m-%d %H:%M")
    lamda_arrival = 1.1
    mu_service = 5
    sigma_service = 1
    num_checkouts = 6

    a_stats = a_scenario(
        lambda_arrival=lamda_arrival,
        start_time=start_time,
        end_time=end_time,
        mu_service=mu_service,
        sigma_service=sigma_service,
        num_checkouts=num_checkouts,
        print_logs=False,
        seed=10
    )

    b_stats = b_scenario(
        lambda_arrival=lamda_arrival,
        start_time=start_time,
        end_time=end_time,
        mu_service=mu_service,
        sigma_service=sigma_service,
        num_checkouts=num_checkouts,
        print_logs=False,
        seed=10
    )

    comparison_data = [
        {
            "Scenario": a_stats["Scenario"],
            "Generated Clients": a_stats["Generated Clients"],
            "Served Clients": a_stats["Served Clients"],
            "Avg Wait Time (min)": a_stats["Avg Wait Time (min)"],
            "Max Wait Time (min)": a_stats["Max Wait Time (min)"]
        },
        {
            "Scenario": b_stats["Scenario"],
            "Generated Clients": b_stats["Generated Clients"],
            "Served Clients": b_stats["Served Clients"],
            "Avg Wait Time (min)": b_stats["Avg Wait Time (min)"],
            "Max Wait Time (min)": b_stats["Max Wait Time (min)"]
        }
    ]

    df_comparison = pd.DataFrame(comparison_data)
    print("\n=== Porównanie scenariuszy A i B ===")
    print(df_comparison)

    plot_comparison(df_comparison)

    # Wykres historii kolejki dla scenariuszu A (jedna kolejka)
    if "Queue History" in a_stats:
        plot_queue_history(a_stats["Queue History"], start_time, end_time, "Scenariusz A")
    else:
        print("Brak danych o historii kolejki w scenariuszu A.")

    # Wykres historii kolejki dla scenariuszu B (łączna liczba klientów we wszystkich kolejkach)
    if "Queue History" in b_stats:
        plot_queue_history(b_stats["Queue History"], start_time, end_time, "Scenariusz B")
    else:
        print("Brak danych o historii kolejki w scenariuszu B.")


if __name__ == "__main__":
    main()
