# browser_manager.py

"""
This module manages Selenium WebDriver setup, configurations, and optimizations.
It includes options for headless mode, proxy handling, and user-agent rotation.
"""

import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class BrowserManager:
    """Manages the Selenium WebDriver with customizable options."""

    # List of user agents to randomize requests
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36"
    ]

    def __init__(self, headless=False, use_proxy=False, proxy_list=None):
        """
        Initialize the browser manager with options.

        :param headless: Run Chrome in headless mode.
        :param use_proxy: Enable proxy support.
        :param proxy_list: List of proxy addresses to use.
        """
        self.headless = headless
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list if proxy_list else []

    def get_random_user_agent(self):
        """Return a random user agent from the predefined list."""
        return random.choice(self.USER_AGENTS)

    def get_random_proxy(self):
        """Return a random proxy from the provided list if enabled."""
        if self.use_proxy and self.proxy_list:
            return random.choice(self.proxy_list)
        return None

    def create_driver(self):
        """
        Create and configure the Selenium WebDriver with necessary options.

        :return: Configured WebDriver instance.
        """
        chrome_options = Options()

        # Apply headless mode if enabled
        if self.headless:
            chrome_options.add_argument("--headless=new")

        # Set random user-agent
        user_agent = self.get_random_user_agent()
        chrome_options.add_argument(f"user-agent={user_agent}")

        # Disable automation detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Maximize the window for visibility
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")

        # Handle proxy settings if enabled
        proxy = self.get_random_proxy()
        if proxy:
            chrome_options.add_argument(f"--proxy-server={proxy}")

        # Install WebDriver and initialize the browser
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Prevent detection by modifying WebDriver properties
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver

    @staticmethod
    def close_driver(driver):
        """Gracefully close the WebDriver instance."""
        try:
            driver.quit()
            print("[INFO] WebDriver closed successfully.")
        except Exception as e:
            print(f"[ERROR] Error while closing WebDriver: {e}")