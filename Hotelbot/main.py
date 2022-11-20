from booking.booking import Booking
import datetime

if __name__ == "__main__":
    bot = Booking(tearDown=False)
    bot.land_first_page()
    bot.choose_currency("USD")
    bot.search_deal("Berlin", "2022-11-28", "2022-12-02")
    bot.select_adults(5)
    bot.click_search()
    bot.apply_filter(5)
    bot.refresh()
    bot.report_deals()
    bot.tear_down()
