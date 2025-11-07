import numpy as np
from datetime import timedelta


class Customer:
    id_counter = 0  # clinets_counter

    def __init__(self, mu, sigma, starting_time):
        Customer.id_counter += 1
        self.id = Customer.id_counter
        self.paying_time = self.random_time(mu, sigma)  # paying time in minutes
        self.starting_time = starting_time
        self.finish_time = None

    def random_time(self, mu, sigma):
        """"Random paying time in minutes in range(1-30)"""
        time = np.random.normal(mu, sigma)
        while time <= 1 or time >= 30:
            time = np.random.normal(mu, sigma)
        time = round(time)
        return time

    def calculate_finish_time(self, start_time):
        """"Calculating finishing time of paying"""
        self.finish_time = start_time + timedelta(minutes=self.paying_time)
