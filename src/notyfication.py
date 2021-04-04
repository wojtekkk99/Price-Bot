import time
from plyer import notification

from target_data import Database as Database
from src.scraper import Scraper
from .utils import util as utilities


class Deals:
    def __init__(self):
        self.database = Database.DataBase()
        self.target_data = self.database.target_base

    def new_target(self, target: str, price_range_down, price_range_up) -> None:
        self.database.new_target(target, price_range_down, price_range_up)

    @staticmethod
    def search_targets(self, target, price_range_down, price_range_up) -> list:
        scraper = Scraper(target, price_range_down, price_range_up)
        return scraper.search()

    def notify(self, product_lst):
        notification.notify(
            title="New offers",
            message=" You have got {} new offers on OLX".format(len(product_lst))
        )

if __name__ == "__main__":
    deals = Deals()