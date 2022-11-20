from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, deal_table: WebElement):
        self.deal_table = deal_table

    def pull_deal_attrs(self):

        deals = self.deal_table.find_elements(
            By.CSS_SELECTOR, 'div[data-testid="property-card"]'
        )

        hotel_info = []
        for deal in deals:
            hotel_name = deal.find_element(
                By.CSS_SELECTOR, 'div[data-testid="title"]'
            ).get_attribute("innerHTML")
            hotel_rating = (
                deal.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]')
                .get_attribute("innerText")
                .split("\n")
            )
            hotel_score, num_reviews = hotel_rating[0].strip(), hotel_rating[-1].strip()
            hotel_price = (
                deal.find_element(
                    By.CSS_SELECTOR,
                    'div[data-testid="price-and-discounted-price"] span',
                )
                .get_attribute("innerHTML")
                .strip()
                .replace("&nbsp;", "")
            )
            hotel_info.append([hotel_name, hotel_score, num_reviews, hotel_price])

        return hotel_info
        # hotel_score = deal.find_element
