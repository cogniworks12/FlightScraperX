"""
Entry point for the Kiwi Flight Scraper.
This script initializes a single scraper instance for a specific route.
"""

from core.scraper_engine import KiwiFlightScraper


def run_scraper():
    """
    Initializes and runs the KiwiFlightScraper for Chicago to London.
    """
    departure = "Chicago"
    destination = "London"
    departure_date = "2025-02-06"
    return_date = "2025-03-01"
    departure_month = "February 2025"
    return_month = "March 2025"

    print(f"\n[INFO] Starting scraper for: {departure} -> {destination}")

    # Initialize the scraper
    scraper = KiwiFlightScraper(
        departure=departure,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        departure_month=departure_month,
        return_month=return_month,
        headless=False  # Set to True to run in headless mode
    )

    # Start the scraping process
    scraper.open_website()     # Open Kiwi.com and handle pop-ups
    scraper.accept_terms()      # Accept cookies if prompted
    scraper.set_departure()
    scraper.random_delay()
    scraper.add_place()
    scraper.set_destination()
    scraper.random_delay()
    scraper.add_place()
    scraper.set_dates()         # Select departure & return dates
    scraper.search_flights()    # Click search and process results

    print(f"[INFO] Scraper finished for: {departure} -> {destination}\n")


if __name__ == "__main__":
    run_scraper()
