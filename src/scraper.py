import math
import os
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    """
    Class that defines OLX search
    """
    def __init__(self, target, price_range_down=0, price_range_up=1000, delay=10):
        self.target = target
        self.price_range_down = price_range_down
        self.price_range_up = price_range_up
        self.URL = "https://www.olx.pl/"
        self.driver = self.initialize_browser()
        self.delay = delay

    def initialize_browser(self):
        """
        Automatically initialize browser and go to OLX page
        :return:
        """
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("--headless")

        chrome_driver = os.getcwd() +"\\chromedriver.exe"

        driver = webdriver.Chrome(chrome_driver, options=options)
        driver.get(self.URL)
        accept_cookies =WebDriverWait(driver, 10).until(EC.element_to_be_clickable
                                                ((By.XPATH, "//*[@id='onetrust-accept-btn-handler']")))
        accept_cookies.click()

        return driver

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
            filter_down = self.driver.find_element_by_xpath\
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
    scraper = Scraper(target='iphone', price_range_down=0, price_range_up=1000)
    scraper.search()
