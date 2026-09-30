import pytest

from models import Customer, FoodItem, Menu, Order


def make_item(name="Spicy Burger", price=8.99, category="Entrees", popularity_rating=4.5):
    return FoodItem(name, price, category, popularity_rating)


# --- construction & getters ---

def test_food_item_stores_attributes():
    item = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    assert item.get_name() == "Spicy Burger"
    assert item.get_price() == 8.99
    assert item.get_category() == "Entrees"
    assert item.get_popularity_rating() == 4.5


def test_food_item_allows_zero_price():
    item = FoodItem("Free Sample", 0, "Snacks", 1.0)
    assert item.get_price() == 0


# --- setters update values ---

def test_food_item_set_name_updates_value():
    item = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    item.set_name("Mild Burger")
    assert item.get_name() == "Mild Burger"


def test_food_item_set_price_updates_value():
    item = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    item.set_price(9.99)
    assert item.get_price() == 9.99


def test_food_item_set_category_updates_value():
    item = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    item.set_category("Specials")
    assert item.get_category() == "Specials"


def test_food_item_set_popularity_rating_updates_value():
    item = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    item.set_popularity_rating(5.0)
    assert item.get_popularity_rating() == 5.0


# --- negative price rejected ---

def test_food_item_negative_price_raises_value_error():
    with pytest.raises(ValueError):
        FoodItem("Spicy Burger", -8.99, "Entrees", 4.5)


def test_food_item_set_negative_price_raises_value_error():
    item = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    with pytest.raises(ValueError):
        item.set_price(-1)
    # original value is unchanged after the rejected update
    assert item.get_price() == 8.99


# --- type checking ---

def test_food_item_non_numeric_price_raises_type_error():
    with pytest.raises(TypeError):
        FoodItem("Spicy Burger", "8.99", "Entrees", 4.5)


def test_food_item_bool_price_raises_type_error():
    with pytest.raises(TypeError):
        FoodItem("Spicy Burger", True, "Entrees", 4.5)


def test_food_item_non_string_name_raises_type_error():
    with pytest.raises(TypeError):
        FoodItem(123, 8.99, "Entrees", 4.5)


def test_food_item_non_string_category_raises_type_error():
    with pytest.raises(TypeError):
        FoodItem("Spicy Burger", 8.99, 42, 4.5)


def test_food_item_non_numeric_popularity_rating_raises_type_error():
    with pytest.raises(TypeError):
        FoodItem("Spicy Burger", 8.99, "Entrees", "high")


def test_food_item_set_non_numeric_price_raises_type_error():
    item = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    with pytest.raises(TypeError):
        item.set_price("free")


# --- Order ---

def test_new_order_has_no_items():
    order = Order()
    assert order.get_selected_items() == []


def test_new_order_total_is_zero():
    order = Order()
    assert order.compute_total() == 0


def test_order_add_item_and_compute_total():
    burger = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = FoodItem("Large Soda", 2.50, "Drinks", 3.0)
    order = Order()
    order.add_item(burger)
    order.add_item(soda)
    assert order.get_selected_items() == [burger, soda]
    assert order.compute_total() == pytest.approx(11.49)


def test_order_add_same_item_twice_counts_it_twice():
    soda = FoodItem("Large Soda", 2.50, "Drinks", 3.0)
    order = Order()
    order.add_item(soda)
    order.add_item(soda)
    assert order.get_selected_items() == [soda, soda]
    assert order.compute_total() == pytest.approx(5.00)


def test_order_remove_item():
    burger = FoodItem("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = FoodItem("Large Soda", 2.50, "Drinks", 3.0)
    order = Order()
    order.add_item(burger)
    order.add_item(soda)
    order.remove_item(burger)
    assert order.get_selected_items() == [soda]
    assert order.compute_total() == pytest.approx(2.50)


def test_order_remove_item_not_present_is_a_no_op():
    soda = FoodItem("Large Soda", 2.50, "Drinks", 3.0)
    unrelated = FoodItem("Fries", 3.25, "Sides", 4.0)
    order = Order()
    order.add_item(soda)
    order.remove_item(unrelated)
    assert order.get_selected_items() == [soda]


def test_order_get_selected_items_returns_a_copy():
    soda = FoodItem("Large Soda", 2.50, "Drinks", 3.0)
    order = Order()
    order.add_item(soda)

    items = order.get_selected_items()
    items.append(FoodItem("Fries", 3.25, "Sides", 4.0))

    assert order.get_selected_items() == [soda]


def test_order_add_item_non_food_item_raises_type_error():
    order = Order()
    with pytest.raises(TypeError):
        order.add_item("not a food item")


def test_order_item_count():
    order = Order()
    assert order.item_count() == 0
    order.add_item(make_item())
    order.add_item(make_item())
    assert order.item_count() == 2


def test_order_remove_item_with_multiple_items_left_recomputes_total():
    burger = make_item("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = make_item("Large Soda", 2.50, "Drinks", 3.0)
    fries = make_item("Fries", 3.25, "Sides", 4.0)
    order = Order()
    order.add_item(burger)
    order.add_item(soda)
    order.add_item(fries)

    order.remove_item(soda)

    assert order.get_selected_items() == [burger, fries]
    assert order.compute_total() == pytest.approx(12.24)


# --- Customer ---

def test_new_customer_has_no_purchase_history():
    customer = Customer("Ada")
    assert customer.get_purchase_history() == []


def test_customer_without_name_is_not_verified():
    customer = Customer("")
    assert customer.is_verified_user() is False


def test_customer_with_name_is_verified():
    customer = Customer("Ada")
    assert customer.is_verified_user() is True


def test_customer_set_name_updates_value():
    customer = Customer("Ada")
    customer.set_name("Grace")
    assert customer.get_name() == "Grace"


def test_customer_add_order_to_history():
    customer = Customer("Ada")
    order = Order()
    order.add_item(FoodItem("Spicy Burger", 8.99, "Entrees", 4.5))

    customer.add_order_to_history(order)

    assert customer.get_purchase_history() == [order]


def test_customer_get_purchase_history_returns_a_copy():
    customer = Customer("Ada")
    order = Order()
    order.add_item(FoodItem("Spicy Burger", 8.99, "Entrees", 4.5))
    customer.add_order_to_history(order)

    history = customer.get_purchase_history()
    history.append(order)

    assert customer.get_purchase_history() == [order]


def test_customer_cannot_add_empty_order_to_history():
    customer = Customer("Ada")
    empty_order = Order()

    with pytest.raises(ValueError):
        customer.add_order_to_history(empty_order)

    assert customer.get_purchase_history() == []


def test_customer_non_string_name_raises_type_error():
    with pytest.raises(TypeError):
        Customer(123)


def test_customer_set_non_string_name_raises_type_error():
    customer = Customer("Ada")
    with pytest.raises(TypeError):
        customer.set_name(123)
    assert customer.get_name() == "Ada"


def test_customer_add_order_to_history_non_order_raises_type_error():
    customer = Customer("Ada")
    with pytest.raises(TypeError):
        customer.add_order_to_history(make_item())


def test_customer_total_spent_sums_all_orders():
    customer = Customer("Ada")

    first_order = Order()
    first_order.add_item(make_item("Spicy Burger", 8.99, "Entrees", 4.5))
    customer.add_order_to_history(first_order)

    second_order = Order()
    second_order.add_item(make_item("Large Soda", 2.50, "Drinks", 3.0))
    second_order.add_item(make_item("Fries", 3.25, "Sides", 4.0))
    customer.add_order_to_history(second_order)

    assert customer.total_spent() == pytest.approx(14.74)


def test_customer_total_spent_with_no_orders_is_zero():
    customer = Customer("Ada")
    assert customer.total_spent() == 0


# --- Menu ---

def test_new_menu_has_no_items():
    menu = Menu()
    assert menu.items == []


def test_menu_add_item():
    menu = Menu()
    burger = make_item()
    menu.add_item(burger)
    assert menu.items == [burger]


def test_menu_items_returns_a_copy():
    menu = Menu()
    burger = make_item()
    menu.add_item(burger)

    items = menu.items
    items.append(make_item("Fries", 3.25, "Sides", 4.0))

    assert menu.items == [burger]


def test_menu_filter_by_category():
    menu = Menu()
    burger = make_item("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = make_item("Large Soda", 2.50, "Drinks", 3.0)
    menu.add_item(burger)
    menu.add_item(soda)

    assert menu.filter_by_category("Entrees") == [burger]


def test_menu_filter_by_min_popularity():
    menu = Menu()
    burger = make_item("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = make_item("Large Soda", 2.50, "Drinks", 3.0)
    menu.add_item(burger)
    menu.add_item(soda)

    assert menu.filter_by_min_popularity(4.0) == [burger]


def test_menu_filter_by_price_range():
    menu = Menu()
    burger = make_item("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = make_item("Large Soda", 2.50, "Drinks", 3.0)
    menu.add_item(burger)
    menu.add_item(soda)

    assert menu.filter_by_price_range(0, 5) == [soda]


def test_menu_sort_by_price_ascending():
    menu = Menu()
    burger = make_item("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = make_item("Large Soda", 2.50, "Drinks", 3.0)
    fries = make_item("Fries", 3.25, "Sides", 4.0)
    menu.add_item(burger)
    menu.add_item(soda)
    menu.add_item(fries)

    assert menu.sort_by_price() == [soda, fries, burger]


def test_menu_sort_by_price_descending():
    menu = Menu()
    burger = make_item("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = make_item("Large Soda", 2.50, "Drinks", 3.0)
    fries = make_item("Fries", 3.25, "Sides", 4.0)
    menu.add_item(burger)
    menu.add_item(soda)
    menu.add_item(fries)

    assert menu.sort_by_price(ascending=False) == [burger, fries, soda]


def test_menu_sort_by_popularity_descending_default():
    menu = Menu()
    burger = make_item("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = make_item("Large Soda", 2.50, "Drinks", 3.0)
    fries = make_item("Fries", 3.25, "Sides", 4.0)
    menu.add_item(burger)
    menu.add_item(soda)
    menu.add_item(fries)

    assert menu.sort_by_popularity() == [burger, fries, soda]


def test_menu_sort_by_popularity_ascending():
    menu = Menu()
    burger = make_item("Spicy Burger", 8.99, "Entrees", 4.5)
    soda = make_item("Large Soda", 2.50, "Drinks", 3.0)
    fries = make_item("Fries", 3.25, "Sides", 4.0)
    menu.add_item(burger)
    menu.add_item(soda)
    menu.add_item(fries)

    assert menu.sort_by_popularity(descending=False) == [soda, fries, burger]

