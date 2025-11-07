class Checkout:
    def __init__(self, id):
        self.id = id
        self.free = True
        self.customer = None

    def custsomer_in(self, customer_id):
        self.free = False
        self.customer = customer_id

    def customer_out(self):
        self.free = True
        self.customer = None




