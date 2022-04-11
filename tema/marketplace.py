"""
This module represents the Marketplace.
Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
import unittest
from tema.product import Tea, Coffee

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

        self.product_add_lock = Lock()
        self.product_remove_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.producers_register_lock:
            self.current_id_producer += 1

        # the marketplace has a list of producers
        # each producer keeps a list of published products
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
        if len(self.producers[int(producer_id)]) > self.qsize:
            return False

        self.producers[int(producer_id)].append(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id
        """
        with self.new_cart_lock:
            self.current_cart_id += 1
            cart = []

        self.carts.append(cart)
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
        cart = self.carts[cart_id]
        with self.product_add_lock:
            # remove item from producer's list
            count = 0
            found = False
            for count,producer in enumerate(self.producers):
                if product in producer:
                    # remove from producer's list so item is
                    # not available to other clients
                    producer.remove(product)
                    found = True
                    break
            if not found:
                return False
        # add item to cart with produce's id
        product_with_producer = tuple((product, count))
        cart.append(product_with_producer)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to remove from cart
        """
        cart = self.carts[cart_id]
        with self.product_remove_lock:
            # search for product in cart
            for elem in cart:
                if elem[0].name == product.name:
                    # return product to producer
                    producer = elem[1]
                    self.producers[producer].append(product)
                    # remove frfom client's cart
                    cart.remove(elem)
                    break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts[cart_id]


class TestMarketplace(unittest.TestCase):
    """
    Class for testing marketplace functionality
    """
    def setUp(self):
        self.market = Marketplace(3)
        self.market.register_producer()
        self.p_1 = Coffee("Americano", 9, "medium", "high")
        self.p_2 = Tea("Lipton", 15, "green")

    def test_register(self):
        """
        Tests if the marketplace generates correct ids for producers
        """
        self.market.register_producer()
        self.market.register_producer()
        self.assertEqual(self.market.current_id_producer, 2, 'wrong producer id')

    def test_publish(self):
        """
        Tests if the products are successfully published
        """
        self.assertEqual(self.market.publish(0, self.p_1), True, 'cannot publish')
        self.market.publish(0, self.p_1)
        self.market.publish(0, self.p_1)
        self.market.publish(0, self.p_2)
        self.market.publish(0, self.p_2)
        self.assertEqual(self.market.publish(0, self.p_1), False, 'should not have published')

    def test_new_cart(self):
        """
        Tests if the makertplace genertes correct ids for carts
        """
        self.market.new_cart()
        self.market.new_cart()
        self.market.new_cart()
        self.assertEqual(self.market.current_cart_id, 2, 'wrong cart id')

    def test_add(self):
        """
        Tests if a client can access an unpublished product,
        if products are edded successfully to carts
        and if the added products are made unavailable to other clients
        """
        self.market.new_cart()
        self.assertEqual(self.market.add_to_cart(0, self.p_1), False, 'product is not published')

        self.market.publish(0, self.p_1)
        self.assertEqual(self.market.add_to_cart(0, self.p_1), True, 'product not added')

        self.market.publish(0, self.p_2)
        self.market.publish(0, self.p_1)
        self.assertEqual(self.market.add_to_cart(0, self.p_2), True, 'product not added')

        self.market.register_producer()
        self.market.publish(1, self.p_1)
        self.market.publish(1, self.p_2)
        self.market.new_cart()
        self.market.add_to_cart(1, self.p_2)

        products = [self.p_1]
        self.assertEqual(self.market.producers[1], products, 'product is still available')

    def test_remove(self):
        """
        Tests if products are removed successfully to carts
        and if the added products are made unavailable to other clients
        """
        self.market.new_cart()
        self.market.publish(0, self.p_1)
        self.market.publish(0, self.p_2)
        self.market.add_to_cart(0, self.p_1)
        self.market.add_to_cart(0, self.p_2)
        self.market.remove_from_cart(0, self.p_1)

        cart = [tuple((self.p_2, 0))]

        self.assertEqual(self.market.carts[0], cart, 'cart data incorrect')

        products = [self.p_1]
        self.assertEqual(self.market.producers[0], products, 'product not returned to proucer')


if __name__ == '__main__':
    unittest.main()
