from Customer import Customer
from Checkout import Checkout
from queue import Queue
from datetime import datetime, timedelta
import numpy as np

#parameters
start_time = datetime.strptime("2024-12-04 10:00", "%Y-%m-%d %H:%M")
end_time = datetime.strptime("2024-12-04 11:00", "%Y-%m-%d %H:%M")
lamda_arrival = 5
mu_service = 5
sigma_service = 2


current_time = start_time
clients = []





def generate_clients(lambda_arrival):
    current_time = start_time
    while current_time < end_time:
        # Random time delay betweeen clients
        inter_arrival_time = np.random.exponential(scale=1 / lambda_arrival)
        current_time += timedelta(minutes=inter_arrival_time)

        if current_time < end_time:  # Time must be in right range
            clients.append(Customer(mu_service, sigma_service, current_time))


def a_scenario(checkouts = list, lambda_arrival=lamda_arrival):
    generate_clients(lambda_arrival = lambda_arrival)
    global_queue = Queue()
    checkouts = [Checkout(i + 1) for i in range(6)]

    current_time = start_time

    while current_time <= end_time or not global_queue.empty() or any(not checkout.free for checkout in checkouts):
        # new state of checkouts
        for checkout in checkouts:
            if not checkout.free and checkout.customer.finish_time <= current_time:
                print(f"Klient {checkout.customer.id} zakończył obsługę w kasie {checkout.id} o czasie {current_time}")
                checkout.customer_out()

        # adding customers to queue
        for client in clients[:]:
            if client.starting_time <= current_time:
                global_queue.put(client)
                print(f"Klient {client.id} przybył do kolejki o czasie {current_time}")
                clients.remove(client)

        # adding customers to queues
        if checkout.free and not global_queue.empty():
            next_client = global_queue.get()
            next_client.calculate_finish_time(current_time)  # Wywołanie metody
            checkout.custsomer_in(next_client)
            print(f"Klient {next_client.id} rozpoczął obsługę w kasie {checkout.id} o czasie {current_time}")


        print(f"Czas: {current_time}")
        print(f"Kolejka: {global_queue.qsize()} klienci")
        print(
            f"Kasy: {[f'Kasa {checkout.id}: wolna' if checkout.free else f'Kasa {checkout.id}: zajęta' for checkout in checkouts]}")

        current_time += timedelta(minutes=1)

a_scenario()
