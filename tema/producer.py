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

    def run(self):
        while True:
            for (product, no_products, wait_time) in self.products:
                # print(f"{product.name} in cantitate {no_products}")
                for i in range(no_products):
                    # publica produsul
                    # print(f"public {i} produs cu numele {product.name}")
                    published = self.marketplace.publish(self.id, product)
                    # print(f"rezultat publicare: {published}")
                    while not published:
                        # sleep + reincearca sa publici
                        sleep(wait_time)
                        published = self.marketplace.publish(self.id, product)
                        # if published:
                            # print(f"am publicat {product.name}")
                    # print(f"am publicat {product.name}")
                # sleep(wait_time)
