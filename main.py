"""
Main entry point for the Kiwi Flight Scraper.
This script runs two scraper instances in parallel, waits for them to finish, then starts the next batch.
"""

import threading
import time
from core.scraper_engine import KiwiFlightScraper


def run_scraper(departure, destination, departure_date, return_date, departure_month, return_month):
    """
    Runs a flight scraper instance for a single route.
    """
    print(f"\n[INFO] Starting scraper for: {departure} -> {destination}")

    # ✅ Initialize the scraper
    scraper = KiwiFlightScraper(
        departure=departure,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        departure_month=departure_month,
        return_month=return_month,
        headless=False  # ✅ Run headless for better performance
    )

    try:
        scraper.open_website()
        scraper.accept_terms()
        scraper.set_departure()
        scraper.random_delay()
        scraper.add_place()
        scraper.set_destination()
        scraper.random_delay()
        scraper.add_place()
        scraper.set_dates()
        scraper.search_flights()

    except Exception as e:
        print(f"[ERROR] Exception in scraper for {departure} -> {destination}: {e}")

    finally:
        scraper.driver.quit()  # ✅ Ensure browser closes after execution
        print(f"[INFO] Scraper finished for: {departure} -> {destination}\n")


def main():
    """
    Manages multiple scrapers using multithreading.
    Runs 2 scrapers in parallel, waits for them to finish, then starts the next batch.
    """

    # ✅ Define multiple routes to scrape
    routes = [
        ("Chicago", "London", "2025-02-06", "2025-03-01", "February 2025", "March 2025"),
        ("New York", "Paris", "2025-02-10", "2025-03-05", "February 2025", "March 2025"),
        ("Los Angeles", "LHE", "2025-02-15", "2025-03-10", "February 2025", "March 2025"),
        ("Toronto", "MUX", "2025-02-20", "2025-03-15", "February 2025", "March 2025"),
        ("San Francisco", "Tokyo", "2025-02-25", "2025-03-20", "February 2025", "March 2025"),
        ("Miami", "Dubai", "2025-03-01", "2025-03-25", "March 2025", "March 2025")
    ]

    max_threads = 2  # ✅ Run only 2 scrapers at a time
    active_threads = []

    for i in range(0, len(routes), max_threads):
        batch = routes[i:i + max_threads]  # ✅ Get the next 2 routes

        # ✅ Start two scrapers in parallel
        for route in batch:
            t = threading.Thread(target=run_scraper, args=route)
            t.start()
            active_threads.append(t)

        # ✅ Wait for both scrapers to finish before starting the next batch
        for t in active_threads:
            t.join()

        active_threads = []  # ✅ Reset thread list for the next batch

        # ✅ Add a short delay to avoid detection issues
        time.sleep(5)

    print("\n[INFO] All scraping tasks completed successfully.")


if __name__ == "__main__":
    main()
