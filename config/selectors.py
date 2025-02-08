# selectors.py

"""
This module contains all the necessary XPath and CSS selectors used in the scraper.
Using this centralized file ensures easy maintenance and updates.
"""

class KiwiSelectors:
    """A class containing all the selectors used for web scraping Kiwi.com."""

    # Website URL
    BASE_URL = "https://www.kiwi.com/"

    # Popup & Modal Selectors
    COOKIE_ACCEPT_BTN = "/html/body/div[2]/div[2]/div[1]/section/div/div/div/section/div[2]/button[3]/div"  # Accept cookies
    GOOGLE_SIGNIN_IFRAME = "//iframe[contains(@src, 'accounts.google.com')]"  # Google Sign-in iframe
    CLOSE_MODAL_BUTTON = "//button[contains(@aria-label, 'Close')]"  # Close modal popups

    # **Remove Pre-Fetched Departure Location**
    REMOVE_PRE_FETCHED_DEPARTURE = "div[data-test='PlacePickerInputPlace-close'] > svg"

    # Flight Search Selectors
    DEPARTURE_INPUT = "//input[@data-test='SearchField-input']"
    DESTINATION_INPUT = "(//input[@data-test='SearchField-input'])[2]"
    # "Add Place" Button Selector
    ADD_PLACE_BUTTON = "//button[@aria-label='Add place']"
    SEARCH_BUTTON = "//a[@data-test='LandingSearchButton']"

    # Date Picker Selectors
    DATE_INPUT_FIELD = "//input[@data-test='SearchFieldDateInput' and @name='search-outboundDate']"
    DATE_PICKER_NEXT_BTN = "button[data-test='CalendarMoveNextButton']"
    DATE_PICKER_MONTH_BUTTONS = "button[data-test='DatepickerMonthButton']"
    CALENDAR_DAY_SELECTOR = "div[data-test='CalendarDay'][data-value='{}']"
    SET_DATES_BUTTON = "//div[contains(text(), 'Set dates')]"

    # Flight Search Results Selectors
    FLIGHT_CARDS_WRAPPER = "div[data-test='ResultCardWrapper']"
    RESULT_CARD_PRICE = ".//div[@data-test='ResultCardPrice']//div[contains(@class, 'whitespace-nowrap')]"

    # Flight Details Modal Selectors
    SHOW_FULL_DETAILS_BUTTON_1 = "//a[contains(text(), 'Show full details')]"
    SHOW_FULL_DETAILS_BUTTON_2 = ".//div[contains(text(), 'Show full details')]"

    FULL_DETAILS_PARENT = "div.box-border.w-full.border-b.border-solid.border-b-elevation-flat-border-color.bg-white-normal.px-400.pb-600.pt-400"

    # Clicking all Boxes
    BOX_ELEMENTS = "//div[@class='pt-300' and @role='button' and @tabindex='0']"

    # Flight Information Selectors
    FLIGHT_DETAILS_PARENT = "//div[@class='space-y-300 not-last:mb-200']"

    # Flight Details Extraction
    DEPARTURE_ROOT = ".//div[@class='flex flex-col justify-end']/h3/strong[1]"
    ARRIVAL_ROOT = ".//div[@class='flex flex-col justify-end']/h3/strong[2]"
    TOTAL_DURATION = ".//div[@class='flex flex-col justify-end']//time"

    # Individual Flight Information
    FLIGHT_INFO_TEMPLATE = {
        "Airline": ".//div[p[contains(text(), 'Airline')]]/following-sibling::div",
        "Operating Airline": ".//div[p[contains(text(), 'Operating airline')]]/following-sibling::div",
        "Flight Number": ".//div[p[contains(text(), 'Flight no')]]/following-sibling::div",
        "Seat Pitch": ".//div[p[contains(text(), 'Seat pitch')]]/following-sibling::div",
        "Seat Width": ".//div[p[contains(text(), 'Seat width')]]/following-sibling::div",
        "Seat Recline": ".//div[p[contains(text(), 'Seat recline')]]/following-sibling::div",
        "Audio_Video on Demand": ".//div[p[contains(text(), 'Audio & video on demand')]]/following-sibling::div",
        "In-Seat Power": ".//div[p[contains(text(), 'In-seat power')]]/following-sibling::div",
        "Wi-Fi on Board": ".//div[p[contains(text(), 'Wi-Fi on board')]]/following-sibling::div",
    }

    # Time & Location Extraction
    TIME_SELECTORS = {
        "Departure Time": "(.//div[@data-test='time']//time)[1]",
        "Departure Date": "(.//div[@data-test='time']//time)[2]",
        "Departure Location": "(.//div[@data-test='time'])[1]/following-sibling::div[2]/div[1]",
        "Departure Airport": "(.//div[@data-test='time'])[1]/following-sibling::div[2]/div[2]",
        "Arrival Time": "(.//div[@data-test='time']//time)[3]",
        "Arrival Date": "(.//div[@data-test='time']//time)[4]",
        "Arrival Location": "(.//div[@data-test='time'])[2]/following-sibling::div[2]/div[1]",
        "Arrival Airport": "(.//div[@data-test='time'])[2]/following-sibling::div[2]/div[2]",
    }

    # Total Travel Time
    TOTAL_TRAVEL_TIME = "div.flex.justify-end > div.orbit-text.font-base.text-small.text-primary-foreground"

    # Load More Button
    LOAD_MORE_BUTTON = "//button[contains(text(), 'Load more')]"
