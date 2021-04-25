import time
import schedule
from plyer import notification

from data import Database
from src.scraper import OLXScraper, OtomotoScraper
from src.utils import util


class Deals:
    def __init__(self):
        self.database = Database.DataBase()
        self.new_offers = 0

    def search_targets(self, target) -> None:
        self.search_otomoto()
        # self.search_olx()

    def search_otomoto(self):
        lst_targets = util.convert_targets_to_class_list(self.database.all_targets())
        for product_data in lst_targets:
            scraper = OtomotoScraper(brand=product_data.brand,
                                     model=product_data.model,
                                     generation=product_data.generation,
                                     price=product_data.price)
            scraper.fill_form()

            while True:
                product_list = scraper.get_element_list()
                last_element_index = util.compare(self.database, util.create_target_name(brand=product_data.brand,
                                                                          model=product_data.model), product_list)
                if last_element_index is not None:
                    product_list = util.create_sublist(last_element_index, product_list)
                    self.database.add_product(util.create_target_name(product_data.brand, product_data.model),
                                              product_list)
                    self.new_offers += len(product_list)
                    break
                else:
                    self.database.add_product(util.create_target_name(product_data.brand, product_data.model),
                                              product_list)
                    self.new_offers += len(product_list)
                    scraper.next_page()

    schedule.every().day.at("10:00").do(search_targets)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    pass
