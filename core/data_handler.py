# core/data_handler.py

"""
This module processes all flight cards, handles "Load more" button,
manages modals, and saves scraped flight details to a JSON file.
"""

import json
import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException
)
from config.selectors import KiwiSelectors





def clean_location(location):
    """Remove unwanted characters (like Unicode symbols) from location names."""
    return re.sub(r'\s*\u2219\s*', '', location).strip()

import random
def click_all_boxes(driver):
    """Clicks all expandable flight information boxes."""
    try:
        original_scroll_position = driver.execute_script("return window.pageYOffset;")
        #print(f"[INFO] Saved original scroll position: {original_scroll_position}")

        boxes = driver.find_elements(By.XPATH, KiwiSelectors.BOX_ELEMENTS)
        for idx, box in enumerate(boxes, start=1):
            #print(f"[INFO] Clicking on Box {idx}...")

            try:
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", box)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(box)).click()
                delay = random.uniform(2.5, 3.5)  # Random delay between clicks
                time.sleep(delay)

            except Exception as e:
                print(f"[ERROR] Could not click Box {idx}: {e}")

        # Restore scroll position after clicking all boxes
        driver.execute_script(f"window.scrollTo(0, {original_scroll_position});")


    except Exception as e:
        print(f"[ERROR] Could not complete clicking all boxes: {e}")



import traceback

from config.save_data import save_flight_data, structure_flight_data

import traceback

import traceback

from config.selectors import KiwiSelectors

import traceback
from config.save_data import save_flight_data


def scrape_information(driver):
    """
    Extracts, structures, and saves flight information immediately after scraping.
    """
    try:
        # ✅ Step 1: Extract flight details
        parents = driver.find_elements(By.XPATH, KiwiSelectors.FLIGHT_DETAILS_PARENT)

        if not parents:
            print("[ERROR] No flight details found.")
            return

        #print(f"[INFO] Detected Flight Type: {'round trip' if len(parents) > 1 else 'one way'}")

        # ✅ Step 2: Structure the extracted data
        flight_data = structure_flight_data(parents)

        # ✅ Debugging: Ensure structured data is correct before saving
        #print("[DEBUG] Structured Flight Data:", flight_data)

        # ✅ Step 3: Save data immediately after extracting a flight
        save_flight_data(flight_data, output_file="json_data/flight_results.json")

        #print("[SUCCESS] Flight data extraction, structuring, and saving completed.")

    except Exception as e:
        print(f"[ERROR] Exception in scrape_information: {traceback.format_exc()}")



def clean_location(location):
    """Remove unwanted characters (like Unicode symbols) from location names."""
    return re.sub(r'\\s*\\u2219\\s*', '', location).strip()


def process_all_cards(driver):
    """
    Process all flight cards on the page, handle "Load more" button if available,
    and save flight details to JSON in real-time.
    """
    visited_indices = set()
    flight_count = 0
    max_flights = 3  # Limit the number of flights

    try:
        while flight_count < max_flights:
            time.sleep(2)
            cards = WebDriverWait(driver, 30).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, KiwiSelectors.FLIGHT_CARDS_WRAPPER)
            )
            #print(f"[INFO] Found {len(cards)} cards.")

            for index, card in enumerate(cards):
                if index in visited_indices or flight_count >= max_flights:
                    continue  # Skip already visited cards or stop if limit reached

                visited_indices.add(index)
                flight_count += 1
             #   print(f"[INFO] Processing flight {flight_count} of {max_flights}...")

                retries = 3
                while retries > 0:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", card)
                        time.sleep(2)
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(card)).click()

                        # Fetch flight price
                        try:
                            time.sleep(2)
                            price_element = card.find_element(By.XPATH, KiwiSelectors.RESULT_CARD_PRICE)
                            flight_price = price_element.text.strip()
                            print(flight_price)
                        except Exception:
                            flight_price = "Not Available"

                        # Handle 'Show Full Details' button if available
                        try:
                            parent_card = driver.find_element(By.CSS_SELECTOR, KiwiSelectors.FULL_DETAILS_PARENT)
                            if parent_card:
                                try:
                                    show_full_details_button = parent_card.find_element(
                                        By.XPATH, KiwiSelectors.SHOW_FULL_DETAILS_BUTTON_1
                                    )
                                    time.sleep(1)
                                    show_full_details_button.click()
                                except NoSuchElementException:
                                    try:
                                        show_full_details_button = parent_card.find_element(
                                            By.XPATH, KiwiSelectors.SHOW_FULL_DETAILS_BUTTON_2
                                        )
                                        time.sleep(1)
                                        time.sleep(2)
                                        show_full_details_button.click()
                                    except NoSuchElementException:
                                        print("[INFO] No 'Show full details' button found.")
                        except NoSuchElementException:
                            print("[INFO] No 'Show full details' button found.")

                        click_all_boxes(driver)

                        # ✅ Extract and Save Data Immediately After Scraping Each Flight
                        scrape_information(driver)  # This call saves data in real-time

                        #input("enter something to continue..")  # Pause to debug if needed

                        driver.back()
                        break

                    except Exception as e:
                        print(f"[ERROR] Exception in processing card {index + 1}: {e}")

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")





