# FoodItem: a single menu item's data (name, price, category, popularity rating).
class FoodItem:
    def __init__(self, name, price, category, popularity_rating):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating


# Order: a customer's selected items for one transaction; computes total cost.
class Order:
    def __init__(self):
        self._selected_items = []

    def add_item(self, food_item):
        self._selected_items.append(food_item)

    @property
    def selected_items(self):
        return list(self._selected_items)

    def compute_total_cost(self):
        return sum(item.price for item in self._selected_items)

    def item_count(self):
        return len(self._selected_items)


# Menu: holds the full collection of FoodItems and supports filtering by category.
class Menu:
    def __init__(self):
        self._items = []

    def add_item(self, food_item):
        self._items.append(food_item)

    @property
    def items(self):
        return list(self._items)

    def filter_by_category(self, category):
        return [item for item in self._items if item.category == category]

    def filter_by_min_popularity(self, min_rating):
        return [item for item in self._items if item.popularity_rating >= min_rating]

    def filter_by_price_range(self, min_price, max_price):
        return [item for item in self._items if min_price <= item.price <= max_price]

    def sort_by_price(self, ascending=True):
        return sorted(self._items, key=lambda item: item.price, reverse=not ascending)

    def sort_by_popularity(self, descending=True):
        return sorted(self._items, key=lambda item: item.popularity_rating, reverse=descending)


# Customer: tracks name and purchase history; isVerifiedCustomer() checks
# tracked profile data (name, history) rather than login credentials.
class Customer:
    def __init__(self, name):
        self.name = name
        self._purchase_history = []

    def add_order(self, order):
        self._purchase_history.append(order)

    @property
    def purchase_history(self):
        return list(self._purchase_history)

    def is_verified_customer(self):
        return bool(self.name) and len(self._purchase_history) > 0

    def total_spent(self):
        return sum(order.compute_total_cost() for order in self._purchase_history)
