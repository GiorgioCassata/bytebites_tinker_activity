# FoodItem: a single menu item's data (name, price, category, popularity rating).
class FoodItem:
    def __init__(self, name, price, category, popularity_rating):
        pass


# Order: a customer's selected items for one transaction; computes total cost.
class Order:
    def __init__(self):
        pass

    def add_item(self, food_item):
        pass

    @property
    def selected_items(self):
        pass

    def compute_total_cost(self):
        pass

    def item_count(self):
        pass


# Menu: holds the full collection of FoodItems and supports filtering by category.
class Menu:
    def __init__(self):
        pass

    def add_item(self, food_item):
        pass

    @property
    def items(self):
        pass

    def filter_by_category(self, category):
        pass

    def filter_by_min_popularity(self, min_rating):
        pass

    def filter_by_price_range(self, min_price, max_price):
        pass

    def sort_by_price(self, ascending=True):
        pass

    def sort_by_popularity(self, descending=True):
        pass


# Customer: tracks name and purchase history; isVerifiedCustomer() checks
# tracked profile data (name, history) rather than login credentials.
class Customer:
    def __init__(self, name):
        pass

    def add_order(self, order):
        pass

    @property
    def purchase_history(self):
        pass

    def is_verified_customer(self):
        pass

    def total_spent(self):
        pass
