import datetime
import os
import time
from calendar import monthrange
from prettytable import PrettyTable

from selenium import webdriver
from selenium.webdriver.common.by import By

from booking.constant import BASE_URL, CHROME_PATH
from booking.bookingFilter import BookingFiltration
from booking.booking_report import BookingReport

# from selenium.webdriver.support import expected_conditions as EC


class Booking(webdriver.Chrome):
    def __init__(self, tearDown=False, chrome_path=CHROME_PATH):
        self.tearDown = tearDown
        os.environ["PATH"] += chrome_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(6)
        self.maximize_window()

    def land_first_page(self):
        self.get(BASE_URL)

    def choose_currency(self, currency=None):
        currency_button = self.find_element(
            By.CSS_SELECTOR, 'button[data-tooltip-text="Choose your currency"]'
        )
        currency_button.click()

        currency_option = self.find_element(
            By.CSS_SELECTOR,
            f'a[data-modal-header-async-url-param*="changed_currency=1&selected_currency={currency}"]',
        )
        currency_option.click()

    def search_deal(self, destination, check_in_date, check_out_date):
        destination_input = self.find_element(By.ID, "ss")
        destination_input.click()
        destination_input.clear()
        destination_input.send_keys(destination)
        time.sleep(2)
        first_option = self.find_element(
            By.CSS_SELECTOR,
            'ul > li[data-i="0"]',
        )

        print(first_option.get_attribute("data-label"))
        first_option.click()

        check_in_date_object = self.make_date_object(check_in_date, "%Y-%m-%d")
        check_out_date_object = self.make_date_object(check_out_date, "%Y-%m-%d")

        num_clicks = 0
        run = True
        while num_clicks < 2:
            start_date, end_date = self.date_interval()
            date_tables = self.find_elements(By.CLASS_NAME, "bui-calendar__dates")
            for date_object, date in [
                (check_in_date_object, check_in_date),
                (check_out_date_object, check_out_date),
            ]:
                if start_date <= date_object <= end_date:
                    for table in date_tables:
                        try:
                            # print(f'td[data-date="{date}"]')
                            date_to_find = table.find_element(
                                By.CSS_SELECTOR,
                                f'td[data-date="{date}"]',
                            )
                            # checked = date_to_find.find_element(
                            #     By.TAG_NAME, "span"
                            # ).get_attribute("aria-checked")
                            if date_to_find:
                                date_to_find.click()
                                num_clicks += 1
                                break
                        except:
                            pass

            # print(num_clicks)
            if num_clicks < 2:
                next = self.find_element(
                    By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]'
                )
                next.click()

            # try:
            #     next = self.find_element(
            #         By.CSS_SELECTOR, 'div[data-bui-ref="calendar-next"]'
            #     )
            #     next.click()
            # except:
            #     run = False

    def select_adults(self, count=1):
        selection_element = self.find_element(By.ID, "xp__guests__toggle")
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element(
                By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()
            # If the value of adults reaches 1, then we should get out
            # of the while loop
            adults_value_element = self.find_element(By.ID, "group_adults")
            adults_value = adults_value_element.get_attribute(
                "value"
            )  # Should give back the adults count

            if int(adults_value) == 1:
                break

        increase_button_element = self.find_element(
            By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]'
        )

        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def date_interval(self):
        start, end = self.find_elements(By.CSS_SELECTOR, "div.bui-calendar__month")
        start_date = self.make_date_object(start.get_attribute("innerText"), "%B %Y")
        end_date = self.make_date_object(end.get_attribute("innerText"), "%B %Y")
        _, days = monthrange(end_date.year, end_date.month)
        end_date = end_date + datetime.timedelta(days=days - 1)
        print(start_date, end_date)
        return start_date, end_date

    def apply_filter(self, *ratings):
        driver = BookingFiltration(driver=self)
        driver.apply_star_rating(*ratings)
        time.sleep(2)
        driver.apply_sorting()

    def report_deals(self):
        deal_table = self.find_element(By.ID, "search_results_table")

        report = BookingReport(deal_table)
        table = PrettyTable(
            field_names=["hotel_name", "hotel_score", "num_reviews", "hotel_price"]
        )
        table.add_rows(report.pull_deal_attrs())
        print(table)

    @staticmethod
    def make_date_object(date_text, format):
        date_object = datetime.datetime.strptime(date_text, format).date()
        return date_object

    def tear_down(self):
        if self.tearDown:
            print("Exiting the browser....")
            self.quit()
