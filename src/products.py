class Offer:
    def __init__(self, title: str, year: int, mileage: int, engine_capacity: int, fuel_type: str, price: float):
        self.title = title
        self.year = year
        self.mileage = mileage
        self.engine_capacity = engine_capacity
        self.fuel_type = fuel_type
        self.price = price


class Target:
    def __init__(self, brand: str, model: str, generation: str, manufacture_date: tuple, price: tuple):
        self.brand = brand
        self.model = model
        self.generation = generation
        self.manufacture_date = manufacture_date
        self.price = price

    def manufacture_date_from(self):
        return self.manufacture_date[0]

    def manufacture_date_to(self):
        return self.manufacture_date[1]

    def price_from(self):
        return self.price[0]

    def price_to(self):
        return self.price[1]
