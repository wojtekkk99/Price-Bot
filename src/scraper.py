import math
import os
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.products import Offer


class Scraper:
    """
    Class that represent Webscraper
    """
    pages = {
        'olx': "https://www.olx.pl/",
        'otomoto': "https://www.otomoto.pl/osobowe/"
    }

    @staticmethod
    def initialize_browser(web_page):
        """
        Initialize browser and go to page
        :return:
        """
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # options.add_argument("--headless")

        chrome_driver = os.getcwd() + "\\chromedriver.exe"

        driver = webdriver.Chrome(chrome_driver, options=options)
        driver.get(Scraper.pages.get(web_page))
        accept_cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable
                                                         ((By.XPATH, "//*[@id='onetrust-accept-btn-handler']")))
        accept_cookies.click()

        return driver


class OtomotoScraper(Scraper):
    """
    Class that represent Otomoto search
    """

    def __init__(self, brand: str, model: str, generation: str, price: tuple, delay: int = 10):
        self.driver = super(OtomotoScraper, self).initialize_browser("otomoto")
        self.brand = brand
        self.model = model
        self.generation = generation
        self.price = price
        self.delay = delay
        self.current_page = 1

    def fill_form(self):
        # Brand
        input_elem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                                                                    ((By.XPATH,
                                                                      "//*[@id='select2-param571-container']/span"))).click()
        input_elem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                                                                    ((By.XPATH, "/html/body/span/span/span[1]/input")))
        input_elem.send_keys(self.brand)
        input_elem.send_keys(Keys.ENTER)

        # Model
        input_elem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                                                                    ((By.XPATH,
                                                                      "//*[@id='select2-param573-container']"))).click()
        input_elem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                                                                    ((By.XPATH, "/html/body/span/span/span[1]/input")))
        input_elem.send_keys(self.model)
        input_elem.send_keys(Keys.ENTER)

        # Price from
        input_elem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                                                                    ((By.CSS_SELECTOR,
                                                                      "#param_price > div > div > div.filter-item.filter-item-from.rel.numeric-item.price > span"))).click()
        input_elem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                     ((By.CSS_SELECTOR, "body > span > span > span.select2-search.select2-search--dropdown > input")))
        input_elem.send_keys(self.price[0])
        input_elem.send_keys(Keys.ENTER)

        # Price to
        input_elem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                     ((By.CSS_SELECTOR,
                       "#param_price > div > div > div.filter-item.filter-item-to.rel.numeric-item.price"))).click()
        input_elem = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                     ((By.CSS_SELECTOR, "body > span > span > span.select2-search.select2-search--dropdown > input")))
        input_elem.send_keys(self.price[1])
        input_elem.send_keys(Keys.ENTER)

    def get_element_list(self) -> list:
        search_list = self.driver.find_elements_by_css_selector\
            ("#body-container > div.container-fluid.container-fluid-sm > div:nth-child(1) > div > div.om-list-container > div.offers.list > article")
        product_list = []

        for elem in search_list:
            title = self.driver.find_element_by_class_name("offer-title__link").text
            year = elem.find_element_by_css_selector\
                ("div.offer-item__wrapper > div.offer-item__content.ds-details-container > ul > li:nth-child(1)").text
            mileage = elem.find_element_by_css_selector\
                ("div.offer-item__wrapper > div.offer-item__content.ds-details-container > ul > li:nth-child(2)").text
            engine_capacity = elem.find_element_by_css_selector\
                ("div.offer-item__wrapper > div.offer-item__content.ds-details-container > ul > li:nth-child(3)").text
            fuel_type = elem.find_element_by_css_selector\
                ("div.offer-item__wrapper > div.offer-item__content.ds-details-container > ul > li:nth-child(4)").text
            price = elem.find_element_by_class_name("offer-item__price")
            product = Offer(title, year, mileage, engine_capacity, fuel_type, price)
            product_list.append(product)

        return product_list

    def next_page(self) -> None:
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                                                     ((By.XPATH, "//*[@id='body-container']/div[2]/div[2]/ul/li[{}]"
                                                       .format(self.current_page+1)))).click()
        self.current_page += 1


class OLXScraper(Scraper):
    """
    Class that represent OLX search
    """

    def __init__(self, target, price_range_down=0, price_range_up=1000, delay=10):
        self.driver = super().initialize_browser("olx")
        self.target = target
        self.price_range_down = price_range_down
        self.price_range_up = price_range_up
        self.delay = delay

    def search(self):
        search_bar = WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable
                                                                  ((By.CSS_SELECTOR, "input[id='headerSearch']")))
        search_bar.send_keys(self.target)
        search_bar.send_keys(Keys.RETURN)
        self.set_filtres()

    def set_filtres(self):
        try:
            filter_down = self.driver.find_element_by_xpath("//*[@id='param_price']/div[2]/div[1]/a/span[1]")
            filter_down.click()
            filter_down = self.driver.find_element_by_xpath \
                ("// *[ @ id = 'param_price'] / div[2] / div[1] / label / input")
            filter_down.send_keys(self.price_range_down)

            filter_up = self.driver.find_element_by_xpath("//*[@id='param_price']/div[2]/div[2]/a/span[1]")
            filter_up.click()
            filter_up = self.driver.find_element_by_xpath("//*[@id='param_price']/div[2]/div[2]/label/input")
            filter_up.send_keys(self.price_range_up)
            self.get_element_list()
        except TimeoutException:
            print("Loading took too much time!")

    def get_element_list(self) -> list:
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

        search_list = self.driver.find_elements_by_class_name("offer-wrapper")
        product_list = []

        for elem in search_list:
            try:
                product_list.append(elem.text)

            except NoSuchElementException:
                print("Not found ", elem.text)
            except StaleElementReferenceException:
                print('StaleElementReferenceException ', elem.text)

        return product_list


if __name__ == "__main__":

    scraper = OLXScraper("Volvo V40", )

    scraper.fill_form()
    scraper.get_element_list()
