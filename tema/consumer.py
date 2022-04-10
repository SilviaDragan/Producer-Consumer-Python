"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.market = marketplace
        self.wait_time = retry_wait_time
        self.name = kwargs['name']


    def run(self):
        for cart in self.carts:
            cid = self.market.new_cart()
            for action in cart:
                # verifica daca type e add sau remove
                for i in range(int(action["quantity"])):
                    if action["type"] == "add":
                        # print("add")
                        added = self.market.add_to_cart(cid, action["product"])
                        while not added:
                            sleep(self.wait_time)
                            added = self.market.add_to_cart(cid, action["product"])
                    elif action["type"] == "remove":
                        # print("remove")
                        self.market.remove_from_cart(cid, action["product"])

            products = self.market.place_order(cid)
            for p in products:
                print(f"{self.name} bought {p[0]}")

