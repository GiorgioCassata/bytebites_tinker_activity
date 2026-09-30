# FoodItem: a single menu item's data (name, price, category, popularity rating).
class FoodItem:
    def __init__(self, name, price, category, popularity_rating):
        self.set_name(name)
        self.set_price(price)
        self.set_category(category)
        self.set_popularity_rating(popularity_rating)

    def get_name(self):
        return self._name

    def set_name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self._name = name

    def get_price(self):
        return self._price

    def set_price(self, price):
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if price < 0:
            raise ValueError("price cannot be negative")
        self._price = price

    def get_category(self):
        return self._category

    def set_category(self, category):
        if not isinstance(category, str):
            raise TypeError("category must be a string")
        self._category = category

    def get_popularity_rating(self):
        return self._popularity_rating

    def set_popularity_rating(self, popularity_rating):
        if isinstance(popularity_rating, bool) or not isinstance(popularity_rating, (int, float)):
            raise TypeError("popularity_rating must be a number")
        self._popularity_rating = popularity_rating


# Order: a customer's selected items for one transaction; computes total cost.
class Order:
    def __init__(self):
        self._selected_items = []

    def add_item(self, food_item):
        if not isinstance(food_item, FoodItem):
            raise TypeError("food_item must be a FoodItem")
        self._selected_items.append(food_item)

    def remove_item(self, food_item):
        try:
            self._selected_items.remove(food_item)
        except ValueError:
            pass

    def get_selected_items(self):
        return list(self._selected_items)

    def compute_total(self):
        return sum(item.get_price() for item in self._selected_items)

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
        return [item for item in self._items if item.get_category() == category]

    def filter_by_min_popularity(self, min_rating):
        return [item for item in self._items if item.get_popularity_rating() >= min_rating]

    def filter_by_price_range(self, min_price, max_price):
        return [item for item in self._items if min_price <= item.get_price() <= max_price]

    def sort_by_price(self, ascending=True):
        return sorted(self._items, key=lambda item: item.get_price(), reverse=not ascending)

    def sort_by_popularity(self, descending=True):
        return sorted(self._items, key=lambda item: item.get_popularity_rating(), reverse=descending)


# Customer: tracks name and purchase history.
class Customer:
    def __init__(self, name):
        self.set_name(name)
        self._purchase_history = []

    def get_name(self):
        return self._name

    def set_name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self._name = name

    def add_order_to_history(self, order):
        if not isinstance(order, Order):
            raise TypeError("order must be an Order")
        if order.item_count() == 0:
            raise ValueError("cannot add an empty order to purchase history")
        self._purchase_history.append(order)

    def get_purchase_history(self):
        return list(self._purchase_history)

    def is_verified_user(self):
        return bool(self._name)

    def total_spent(self):
        return sum(order.compute_total() for order in self._purchase_history)
