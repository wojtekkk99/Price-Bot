from typing import Union

import mysql.connector

from src.products import Target
from src.utils import util as utilities


class DataBase:
    """
    Class representing database.
    """
    SQL_target = "(brand, model, generation, manufacture_date_from, manufacture_date_to, price_from, price_to) VALUES (%s, %s, %s, %i, %i, %i, %i)"
    SQL_product = "(title, year, mileage, engine_capacity, fuel_type, price) VALUES (%s, %i, %s, %s, %s, %i)"

    def __init__(self):
        self.database = self.connect_to_database()
        self.cursor = self.database.cursor()

    @staticmethod
    def connect_to_database():
        with open('login_data.txt', 'r') as file:
            for line in file:
                login, password = line.strip().split(";")

        db = mysql.connector.connect(
            host="localhost",
            user=login,
            passwd=password,
            database="mydatabase"
        )
        return db.cursor()

    def create_table(self, name, **kwargs):
        """
        Create random table
        """
        text = ""
        for attribute, type in kwargs:
            text += attribute + " " + type + ", "
        self.cursor.execute("CREATE TABLE {} ({})".format(name, text[::-2]))

    def add_new_target(self, SQL_target, SQL_product, brand, model, generation, manufacture_date_from,
                       manufacture_date_to, price_from, price_to):
        """
        Method adding new product target to table targets and creating new table for this product
        """
        self.cursor.execute("INSERT INTO Targets {}".format(SQL_target),
                            (
                            brand, model, generation, manufacture_date_from, manufacture_date_to, price_from, price_to))
        self.cursor.execute("CREATE TABLE {} ({})".format(utilities.create_target_name(brand, model), SQL_product))

    def add_product(self, table, products: list):
        """
        Add new products to Table
        products: (brand: str, model: str, generation: str, manufacture_date: tuple, price: tuple)
        """
        for product in products:
            self.cursor.executemany("INSERT INTO {} ".format(table), product)
            self.database.commit()

    def all_targets(self):
        self.cursor.execute("SELECT * FROM targets")
        result = self.cursor.fetchall()
        return result

    def last_element_from_table(self, table):
        return self.cursor.execute("SELECT TOP 1 * FROM {} ORDER BY id DESC".format(table))
