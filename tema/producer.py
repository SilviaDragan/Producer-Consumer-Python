"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.wait_time = republish_wait_time
        self.id = marketplace.register_producer()
        self.name = kwargs['name']
        # print("argumente")
        # for arg in kwargs:
        #     print(arg)
        # print(self.products)

    def run(self):
        # print(self.products)
        # print(len(self.products))

        # while True:
        for (product, no_products, wait_time) in self.products:
            print(product)
            # print(no_products)
            # print(wait_time)
            for i in range(0, no_products):
                # publica produsul
                published = self.marketplace.publish(self.id, product)
                while not published:
                    # sleep + reincearca sa publici
                    sleep(wait_time)
                    # print("no se puede")
                    published = self.marketplace.publish(self.id, product)

                # print("ok am publicat")
                sleep(wait_time)
