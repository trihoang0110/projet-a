from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *ratings):
        star_filter_box = self.driver.find_element(
            By.CSS_SELECTOR, 'div[data-filters-group="class"]'
        )
        for rating in ratings:
            rating_choice = star_filter_box.find_element(
                By.CSS_SELECTOR, f'div[data-filters-item="class:class={rating}"]'
            )
            rating_choice.click()

    def apply_sorting(self):
        sort_options = self.driver.find_element(
            By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]'
        )
        sort_options.click()
        lowest_prices = self.driver.find_element(
            By.CSS_SELECTOR, 'button[data-id="price"]'
        )
        lowest_prices.click()
