import numpy as np
from datetime import timedelta
from queue import Queue

from customer import Customer
from checkout import Checkout


def generate_clients(lambda_arrival, start_time, end_time, mu_service, sigma_service):
    """
    Generuje listę klientów w oparciu o rozkład wykładniczy odstępów między przyjściami.
    """
    clients = []
    current_time = start_time

    while current_time < end_time:
        inter_arrival_time = np.random.exponential(scale=1.0 / lambda_arrival)  # w minutach
        current_time += timedelta(minutes=inter_arrival_time)
        if current_time >= end_time:
            break
        clients.append(Customer(mu_service, sigma_service, current_time))

    return clients


def a_scenario(lambda_arrival, start_time, end_time, mu_service, sigma_service, num_checkouts,
               print_logs=False, seed=None):
    """
    Scenariusz A: wszyscy klienci trafiają do jednej wspólnej kolejki.
    Obsługa nowych klientów (oraz pobieranie z kolejki) odbywa się tylko do godziny 22:00.
    Jeśli klient rozpoczął obsługę przed 22:00, dokończy ją nawet po zamknięciu.

    Dodatkowo rejestrowana jest historia długości kolejki tylko do godziny 22:00.
    """
    if seed is not None:
        np.random.seed(seed)

    # Generowanie klientów – tylko ci, którzy przyjdą przed end_time
    clients = generate_clients(lambda_arrival, start_time, end_time, mu_service, sigma_service)

    # Tworzenie kas i wspólnej kolejki
    global_queue = Queue()
    checkouts = [Checkout(i + 1) for i in range(num_checkouts)]

    # Statystyki
    total_clients = len(clients)
    served_clients = 0
    total_wait_time = 0.0
    max_wait_time = 0.0

    checkout_usage = {checkout.id: 0 for checkout in checkouts}
    checkout_busy_time = {checkout.id: timedelta(0) for checkout in checkouts}

    # Historia kolejki – rejestrowana tylko do godziny 22:00
    queue_history = []

    current_time = start_time
    unarrived_clients = list(clients)

    # Pętla symulacyjna – nowe zgłoszenia i rozpoczęcie obsługi tylko do 22:00.
    # Po 22:00 pozwalamy tylko zakończyć obsługę już rozpoczętych klientów.
    while current_time <= end_time or any(not ch.free for ch in checkouts):
        # Rejestrujemy stan kolejki tylko, gdy jesteśmy w godzinach otwarcia
        if current_time <= end_time:
            queue_history.append((current_time, global_queue.qsize()))

        # Sprawdzamy, czy klienci zakończyli obsługę
        for checkout in checkouts:
            if not checkout.free and checkout.customer.finish_time <= current_time:
                if print_logs:
                    print(
                        f"Klient {checkout.customer.id} zakończył obsługę w kasie {checkout.id} o czasie {current_time}")
                busy = checkout.customer.finish_time - checkout.customer.service_start_time
                checkout_busy_time[checkout.id] += busy
                checkout.customer_out()

        # Jeśli jesteśmy przed 22:00, przyjmujemy nowych klientów i rozpoczynamy obsługę
        if current_time <= end_time:
            # Dodajemy nowych klientów, którzy przybyli do tej minuty
            arriving_now = [c for c in unarrived_clients if c.arrival_time <= current_time]
            for client in arriving_now:
                global_queue.put(client)
                if print_logs:
                    print(f"Klient {client.id} przybył do kolejki o czasie {current_time}")
            unarrived_clients = [c for c in unarrived_clients if c.arrival_time > current_time]

            # Jeśli kasa jest wolna i w kolejce jest klient, rozpoczynamy obsługę
            for checkout in checkouts:
                if checkout.free and not global_queue.empty():
                    next_client = global_queue.get()
                    wait_time = (current_time - next_client.arrival_time).total_seconds() / 60.0
                    total_wait_time += wait_time
                    if wait_time > max_wait_time:
                        max_wait_time = wait_time

                    next_client.calculate_finish_time(current_time)
                    checkout.customer_in(next_client)
                    checkout_usage[checkout.id] += 1
                    served_clients += 1

                    if print_logs:
                        print(
                            f"Klient {next_client.id} rozpoczął obsługę w kasie {checkout.id} o czasie {current_time}")
        # Po 22:00 już nie przyjmujemy nowych klientów – tylko czekamy na zakończenie obsługi

        current_time += timedelta(minutes=1)

    avg_wait = total_wait_time / served_clients if served_clients > 0 else 0.0

    return {
        "Scenario": "A",
        "Generated Clients": total_clients,
        "Served Clients": served_clients,
        "Remaining Clients": global_queue.qsize(),
        "Avg Wait Time (min)": avg_wait,
        "Max Wait Time (min)": max_wait_time,
        "Checkout Usage": checkout_usage,
        "Checkout Busy Time": {cid: bt.total_seconds() / 60.0 for cid, bt in checkout_busy_time.items()},
        "Queue History": queue_history  # Historia zapisana tylko do godziny 22:00
    }


def b_scenario(lambda_arrival, start_time, end_time, mu_service, sigma_service, num_checkouts,
               print_logs=False, seed=None):
    """
    Scenariusz B: każda kasa ma własną kolejkę. Nowy klient wybiera aktualnie najkrótszą kolejkę.
    Przyjmujemy, że klienci pojawiają się tylko do 22:00, a obsługa trwa do zakończenia bieżących procesów.

    Dodatkowo rejestrowana jest historia łącznej długości kolejek (do godziny 22:00).
    """
    if seed is not None:
        np.random.seed(seed)

    clients = generate_clients(lambda_arrival, start_time, end_time, mu_service, sigma_service)

    queues = [Queue() for _ in range(num_checkouts)]
    checkouts = [Checkout(i + 1) for i in range(num_checkouts)]

    total_clients = len(clients)
    served_clients = 0
    total_wait_time = 0.0
    max_wait_time = 0.0

    checkout_usage = {checkout.id: 0 for checkout in checkouts}
    checkout_busy_time = {checkout.id: timedelta(0) for checkout in checkouts}

    # Historia łącznej długości kolejek – rejestrowana tylko do godziny 22:00
    queue_history = []

    current_time = start_time
    unarrived_clients = list(clients)

    while current_time <= end_time or any(not ch.free for ch in checkouts):
        # Rejestrujemy stan kolejek tylko, gdy jesteśmy w godzinach otwarcia (do 22:00)
        if current_time <= end_time:
            total_queue_length = sum(q.qsize() for q in queues)
            queue_history.append((current_time, total_queue_length))

        for checkout in checkouts:
            if not checkout.free and checkout.customer.finish_time <= current_time:
                if print_logs:
                    print(
                        f"Klient {checkout.customer.id} zakończył obsługę w kasie {checkout.id} o czasie {current_time}")
                busy = checkout.customer.finish_time - checkout.customer.service_start_time
                checkout_busy_time[checkout.id] += busy
                checkout.customer_out()

        if current_time <= end_time:
            arriving_now = [c for c in unarrived_clients if c.arrival_time <= current_time]
            for client in arriving_now:
                # Wybór najkrótszej kolejki
                shortest_q = min(queues, key=lambda q: q.qsize())
                shortest_index = queues.index(shortest_q)
                shortest_q.put(client)
                if print_logs:
                    print(f"Klient {client.id} dołączył do kolejki kasy {shortest_index + 1} o czasie {current_time}")
            unarrived_clients = [c for c in unarrived_clients if c.arrival_time > current_time]

            for i, checkout in enumerate(checkouts):
                if checkout.free and not queues[i].empty():
                    next_client = queues[i].get()
                    wait_time = (current_time - next_client.arrival_time).total_seconds() / 60.0
                    total_wait_time += wait_time
                    if wait_time > max_wait_time:
                        max_wait_time = wait_time
                    next_client.calculate_finish_time(current_time)
                    checkout.customer_in(next_client)
                    checkout_usage[checkout.id] += 1
                    served_clients += 1
                    if print_logs:
                        print(
                            f"Klient {next_client.id} rozpoczął obsługę w kasie {checkout.id} o czasie {current_time}")

        current_time += timedelta(minutes=1)

    avg_wait = total_wait_time / served_clients if served_clients > 0 else 0.0

    return {
        "Scenario": "B",
        "Generated Clients": total_clients,
        "Served Clients": served_clients,
        "Remaining Clients": sum(q.qsize() for q in queues),
        "Avg Wait Time (min)": avg_wait,
        "Max Wait Time (min)": max_wait_time,
        "Checkout Usage": checkout_usage,
        "Checkout Busy Time": {cid: bt.total_seconds() / 60.0 for cid, bt in checkout_busy_time.items()},
        "Queue History": queue_history  # Historia łącznej długości kolejek zapisywana tylko do godziny 22:00
    }
