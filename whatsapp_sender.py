"""
WhatsApp Message Sender (Stable Persistent Login - Chrome 141+)

Automates sending a predefined message to multiple numbers via WhatsApp Web
using Selenium.

Fixes & Upgrades:
- Keeps WhatsApp login session (no QR scan each time)
- Works with new Chrome 141+ builds
- Stable "Send" button selector
- Handles chat load delays gracefully

Copyright (c) 2025 ZHANDOS NUREKENOV
Licensed under the MIT License.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sys
import random
import os

# Configuration (You can modify these if needed)

# Message to send (can include line breaks with \n)
MESSAGE_TO_SEND = (
    "Hello!\n"
    "This is an automated test message."
)

NUMBERS_FILE = "output.txt"  # List of phone numbers (one per line)
SESSION_DIR = r"C:\Users\Public\whatsapp_session"  # Folder for saving WhatsApp login session
CHROMEDRIVER_PATH = r"chromedriver.exe"  # Path to your ChromeDriver




def load_numbers_from_file(filename: str) -> list[str]:
    """Load phone numbers from a text file."""
    print(f"Loading phone numbers from {filename}...")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            numbers = [line.strip() for line in f if line.strip()]
        if not numbers:
            print(f"Warning: {filename} is empty.")
        else:
            print(f"Loaded {len(numbers)} numbers.")
        return numbers
    except FileNotFoundError:
        print(f"Error: {filename} not found.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return []


def send_message(driver: webdriver.Chrome, phone: str, message: str):
    """Send the message to one phone number safely."""
    print(f"\n--- Attempting to send to: {phone} ---")
    url = f"https://web.whatsapp.com/send?phone={phone}&text&app_absent=0"

    try:
        driver.get(url)

        # Wait for chat input box
        input_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            )
        )
        print("Chat window opened.")

        # Type the message
        input_box.click()
        input_box.clear()

        for i, line in enumerate(message.split("\n")):
            input_box.send_keys(line)
            if i < len(message.split("\n")) - 1:
                input_box.send_keys(Keys.SHIFT + Keys.ENTER)

        time.sleep(1.0)

        # --- Stable Send Button ---
        try:
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[@data-icon="wds-ic-send-filled" or @data-icon="send"]')
                )
            )
        except TimeoutException:
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
            )

        driver.execute_script("arguments[0].click();", send_button)
        print(f"Message sent to {phone}")
        time.sleep(random.uniform(2.0, 4.0))

    except TimeoutException:
        print(f"Timeout for {phone}: Chat not found or WhatsApp slow.")
    except NoSuchElementException as e:
        print(f"Element not found for {phone}: {e}")
    except Exception as e:
        print(f"Unexpected error for {phone}: {e}")


def main():
    """Main runner."""
    phone_numbers = load_numbers_from_file(NUMBERS_FILE)
    if not phone_numbers:
        print("No numbers found. Exiting.")
        input("\n Press Enter to exit...")
        return

    driver = None
    try:
        print("Starting Chrome... Please wait.")
        options = webdriver.ChromeOptions()

        # === Persistent login (no QR every time) ===
        os.makedirs(SESSION_DIR, exist_ok=True)
        options.add_argument(f"user-data-dir={SESSION_DIR}")

        # Stable Chrome setup
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")

        service = Service(executable_path=CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

        # --- Login phase ---
        driver.get("https://web.whatsapp.com")
        print("\n" + "=" * 60)
        print("If you see the QR code for the first time — scan it.")
        print("After scanning, you won’t need to log in again next time!")
        print("=" * 60)
        input("Press Enter after login (or if you’re already logged in)...\n")

        # --- Sending phase ---
        total = len(phone_numbers)
        for i, phone in enumerate(phone_numbers, start=1):
            print(f"\n📨 Sending message {i} of {total}...")
            send_message(driver, phone, MESSAGE_TO_SEND)
            sleep_time = random.uniform(5.0, 10.0)
            print(f"Waiting {sleep_time:.1f}s before next message...")
            time.sleep(sleep_time)

        print("\n All messages sent successfully!")

    except Exception as e:
        print(f"\n Critical error: {e}", file=sys.stderr)

    finally:
        if driver:
            print("Closing browser...")
            driver.quit()
        input("\n Script finished. Press Enter to exit...")


if __name__ == "__main__":
    main()
