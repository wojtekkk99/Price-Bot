import os

class DataBase:
    target_base = {}

    def __init__(self):
        self.target_file()
        self.load_targets()

    @staticmethod
    def target_file(self):
        if not os.path.isfile('./targets.txt'):
            with open('targets.txt', 'x') as file:
                file.write('')

    def load_targets(self):
        with open('targets.txt', "r") as data:
            for line in data:
                target, price_range_down, price_range_up = line.strip().split(";")
                self.target_base[target] = (int(price_range_down), int(price_range_up))

    def new_target(self, target: str, price_range_down: int, price_range_up: int):
        try:
            with open('{}.txt'.format(target), 'x') as file:
                file.write('')
        except FileExistsError:
            pass

        with open('targets.txt', "a") as data:
            data.write(target + ';' + str(price_range_down) + ';' + str(price_range_up) + '\n')
        self.target_base[target] = (int(price_range_down), int(price_range_up))
