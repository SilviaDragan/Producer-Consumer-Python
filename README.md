# Dragan Silvia 331CB - Tema 1 ASC


### Marketplace:
    The marketplace holds the producers' list, and carts' list.
    The operations of generating a new producer id, generating a new 
    cart id, searching + removing/adding a roduct from a producer's list
    when adding or removing from cart are synchronized using locks.
    Other operations, like appending an element to a list, are
    already thread-safe.
    
    Items that a consumer adds to a cart are removed from the producer's list of
    available products. If the customer removes a product from his cart,
    the product is returned to his initial producer, therefore made available
    to other clients again.
    
### Consumer:
    Iterating the list of carts, the consumer can add and remove items
    from his cart, and waits when the product he wants to add to his cart
    is not available.
    
    The action of printing the items bought after placing an order is
    sychronized using a lock, because I have found that stdout is a shared
    resource, therefore not thread-safe.

### Producer:
    While the program is running, the producers try to publish their
    products, waiting in beetween publishes.
    
### Unit testing:
    I have implemented a suite of tests for the class Marketplace.
    Each method tests the return values and the actions of the methods
    implemented in marketplace.

### Git:
_https://github.com/SilviaDragan/Tema1ASC.git_