# core/scraper_engine.py

"""
This module contains the main scraping logic for Kiwi.com.
It interacts with the webpage using Selenium, handles modals, clicks elements,
extracts flight details, and processes all flight cards.
"""

import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)
from core.browser_manager import BrowserManager
from config.selectors import KiwiSelectors
from core.data_handler import process_all_cards  # Importing original process_all_cards function
import random





class KiwiFlightScraper:
    """Selenium-based flight search scraper for Kiwi.com."""

    def __init__(self, departure, destination, departure_date, return_date, departure_month, return_month,
                 headless=True):
        """
        Initialize the scraper with required parameters.

        :param departure: Departure location.
        :param destination: Destination location.
        :param departure_date: Departure date.
        :param return_date: Return date.
        :param departure_month: Departure month.
        :param return_month: Return month.
        :param headless: Run browser in headless mode (default=False).
        """
        self.departure = departure
        self.destination = destination
        self.departure_date = departure_date
        self.return_date = return_date
        self.departure_month = departure_month
        self.return_month = return_month
        self.browser_manager = BrowserManager(headless=headless)
        self.driver = self.browser_manager.create_driver()

    def random_delay(self, min_delay=2, max_delay=3):
        """Introduce a random delay to simulate human behavior."""
        time.sleep(random.uniform(min_delay, max_delay))

    def open_website(self):
        """Open Kiwi website and handle pop-ups."""
        self.driver.get(KiwiSelectors.BASE_URL)
        self.random_delay()

    def close_pre_fetched_departure(self):
        """Remove any pre-filled departure location if present."""
        try:
            svg_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, KiwiSelectors.REMOVE_PRE_FETCHED_DEPARTURE))
            )
            svg_element.click()
            #print("[INFO] Removed pre-filled departure location.")
        except TimeoutException:
            print("[INFO] No pre-filled departure location found.")

    def enter_text(self, by, value, text, timeout=10):
        """Enter text into a field with error handling."""
        try:
            input_element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))
            input_element.clear()
            input_element.send_keys(text)
            return True
        except TimeoutException:
            return False

    def click_element(self, by, value, timeout=10):
        """Click an element, handling common exceptions."""
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, value)))
            element.click()
            return True
        except (ElementClickInterceptedException, StaleElementReferenceException):
            time.sleep(2)
        except TimeoutException:
            print(f"[ERROR] Element {value} not found.")
            return False
        return False

    def accept_terms(self):
        """Accept Kiwi.com terms if the button exists."""
        return self.click_element(By.XPATH, KiwiSelectors.COOKIE_ACCEPT_BTN)

    def add_place(self):

        """Click the 'Add place' button after a random delay."""
        self.random_delay(min_delay=2, max_delay=3)  # Random delay before clicking
        self.click_element(By.XPATH, KiwiSelectors.ADD_PLACE_BUTTON)# Using selector from selectors.py
            # print("[INFO] Clicked the 'Add place' button successfully.")




    def set_departure(self):
        """Set the departure location."""
        self.click_element(By.XPATH, KiwiSelectors.DEPARTURE_INPUT)
        self.close_pre_fetched_departure()
        self.enter_text(By.XPATH, KiwiSelectors.DEPARTURE_INPUT, self.departure)
        #print(f"[INFO] Entered departure: {self.departure}")

    def set_destination(self):
        """Set the destination location."""
        self.click_element(By.XPATH, KiwiSelectors.DESTINATION_INPUT)
        self.enter_text(By.XPATH, KiwiSelectors.DESTINATION_INPUT, self.destination)
        #print(f"[INFO] Entered destination: {self.destination}")

    def select_date(self, target_month, target_date):
        """Select a departure or return date from the calendar."""
        attempts = 0
        while attempts < 5:
            try:
                displayed_months = [elem.text.strip() for elem in WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, KiwiSelectors.DATE_PICKER_MONTH_BUTTONS)))]

                if target_month in displayed_months:
                    day_selector = KiwiSelectors.CALENDAR_DAY_SELECTOR.format(target_date)
                    self.click_element(By.CSS_SELECTOR, day_selector)
                    #print(f"[INFO] Selected date: {target_date}")
                    break
                else:
                    self.click_element(By.CSS_SELECTOR, KiwiSelectors.DATE_PICKER_NEXT_BTN)
                    time.sleep(2)
                    attempts += 1
            except Exception as e:
                print(f"[ERROR] Could not select date {target_date}: {e}")
                break

    def set_dates(self):
        """Click the date input field and set departure and return dates."""
        self.click_element(By.XPATH, KiwiSelectors.DATE_INPUT_FIELD)
        time.sleep(1)
        self.click_element(By.XPATH, KiwiSelectors.DATE_INPUT_FIELD)
        self.select_date(self.departure_month, self.departure_date)
        time.sleep(2)
        self.select_date(self.return_month, self.return_date)
        self.click_element(By.XPATH, KiwiSelectors.SET_DATES_BUTTON)

    def search_flights(self):
        """Click the search button to find flights."""
        self.click_element(By.XPATH, KiwiSelectors.SEARCH_BUTTON)
        #print("[INFO] Search initiated.")
        time.sleep(5)  # Ensure page load

        # **Switch to second tab if available**
        self.change_driver_position()

        # **Process all flight cards**
        process_all_cards(self.driver)

    def change_driver_position(self):
        """Switch to second tab after search."""
        window_handles = self.driver.window_handles
        if len(window_handles) > 1:
            self.driver.switch_to.window(window_handles[1])
            #print(f"[INFO] Switched to the second tab. Current URL: {self.driver.current_url}")
        else:
            print("[INFO] No second tab found. Continuing on the current page.")

