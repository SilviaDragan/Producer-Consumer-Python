"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.qsize = queue_size_per_producer
        self.carts = []
        self.current_cart_id = -1
        self.new_cart_lock = Lock()

        self.current_id_producer = -1
        self.producers = []
        self.producers_register_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.producers_register_lock:
            self.current_id_producer += 1
        """
        cum arata lista de producatori
        producers[id_producer] = [produse]
        """
        self.producers.append([])

        return self.current_id_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        print(f"{producer_id} publica {product}")
        if len(self.producers[int(producer_id)]) > self.qsize:
            return False

        self.producers[int(producer_id)].append(product)

        for i in range(len(self.producers)):
            print(i)
            print(self.producers[i])
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.new_cart_lock:
            self.current_cart_id += 1
            c = {self.current_cart_id: []}

        self.carts.append(c)
        return self.current_cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # daca elementul e blocat, returneaza fals
        # daca nu e blocat, adauga in cart si blocheaza-l
        return self.carts[cart_id].add_product(product)

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # deblocheaza produsul si baga-l inapoi
        # self.carts[cart_id].remove_product(product)
        pass

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        pass
        # return self.carts[cart_id].get_products()
