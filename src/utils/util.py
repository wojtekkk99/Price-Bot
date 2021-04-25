import os
from typing import Union

from src.products import Offer, Target


def compare(database, target, product_lst) -> Union[int, None]:
    """

    :param target:
    :param product_lst:
    :return: index of last element or none if last element is not found
    """
    last_element = database.last_element_from_table(target)

    for il, product in enumerate(product_lst):
        if last_element == product:
            return il
    return None


def create_sublist(il, product_lst) -> list:
    return product_lst[:il]


def create_target_name(brand, model):
    return str(brand + model)


def convert_offers_to_tuple_list(lst):
    """Converts from list with Offer elements to list with tuple elements"""
    result = []
    for product in lst:
        result.append((product.title, product.year, product.mileage, product.engine_capacity,
                       product.fuel_type, product.price))
    return result


def convert_offers_to_class_list(lst):
    """Converts from list with tuple elements to list with Offers elements"""
    result = []
    for product in lst:
        result.append(Offer(title=product[0], year=product[1], mileage=product[2], engine_capacity=product[3],
                            fuel_type=product[4], price=product[5]))
    return result


def convert_targets_to_tuple_list(lst):
    """Converts from list with Target elements to list with tuple elements"""
    result = []
    for product in lst:
        result.append((product.target, product.model, product.generation, product.manufacture_date,
                       product.price))
    return result


def convert_targets_to_class_list(lst):
    """Converts from list with tuple elements to list with Targets elements"""
    result = []
    for product in lst:
        result.append(Target(brand=product[0], model=product[1], generation=product[2], manufacture_date=product[3],
                            price=product[4]))
    return result