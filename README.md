# Marketing Automation Toolkit (WhatsApp, Data Cleaning, and 2GIS Scraper)

This repository contains a set of three independent Python scripts designed to automate key tasks in data collection and digital outreach, specifically targeting phone numbers and utilizing WhatsApp Web.

The tools are:
1.  **WhatsApp Message Sender:** Automates sending a predefined message to a list of numbers via WhatsApp Web (stable, persistent login).
2.  **Phone Number Cleaner:** Cleans, deduplicates, and validates raw phone numbers from a file.
3.  **2GIS Phone Number Scraper:** Extracts business phone numbers from the 2GIS directory for a specific rubric and city.

## Setup and Prerequisites

All scripts require **Python 3.x**.

### 1. WhatsApp Message Sender Requirements

* **Python Libraries:**
    ```bash
    pip install selenium
    ```
* **Browser/Driver:**
    * **Google Chrome** (Version 141+ recommended)
    * **ChromeDriver** executable matching your Chrome version, placed in the same directory as the script or specified in `CHROMEDRIVER_PATH`

### 2. 2GIS Phone Number Scraper Requirements

* **Python Libraries:**
    ```bash
    pip install playwright
    playwright install chromium
    ```

## 1. WhatsApp Message Sender (`whatsapp_sender.py`)

This script uses **Selenium** to open WhatsApp Web, maintain a persistent login session, and send messages to a list of phone numbers automatically.

### Configuration Variables
| Variable | Default Value | Purpose |
| :--- | :--- | :--- |
| `MESSAGE_TO_SEND` | Automated test message | The content to be sent. Use `\n` for line breaks. |
| `NUMBERS_FILE` | `output.txt` | The input file containing phone numbers (one per line). |
| `SESSION_DIR` | `C:\Users\Public\whatsapp_session` | Path to save the WhatsApp login session data. **Do not delete this folder.** |
| `CHROMEDRIVER_PATH`| `chromedriver.exe` | Path to your ChromeDriver executable. |


### Usage

1.  Ensure you have a list of cleaned phone numbers in the file specified by `NUMBERS_FILE`.
2.  Run the script:
    ```bash
    python whatsapp_sender.py
    ```
3.  **First Run Only:** The script will open Chrome. If prompted, scan the WhatsApp QR code to log in. Press **Enter** in the console after successfully logging in.
4.  The script will then proceed to send the message to each number with random delays to mimic human behavior and reduce the risk of being blocked.

***

## 2. Phone Number Cleaner (`phone_cleaner.py`)

A utility script to ensure your phone number list is clean, standardized, and free of duplicates before using it for outreach.

### Input/Output

* **Input:** Reads raw numbers from **`a.txt`** (one number per line).
* **Output:** Writes cleaned, sorted, and unique numbers to **`output.txt`**.

### Cleaning Logic

* Removes all non-digit characters (e.g., spaces, dashes, parentheses).
* Filters out duplicates.
* Validates numbers, keeping only those that are **10 digits or longer**.
* Sorts the final list numerically.

### Usage

1.  Place your raw list of phone numbers into a file named **`a.txt`**.
2.  Run the script:
    ```bash
    python phone_cleaner.py
    ```
3.  The clean list will be saved to **`output.txt`**, ready for use with the WhatsApp Sender.

***

## 3. 2GIS Phone Number Scraper (`2gis_scraper.py`)

This tool leverages **Playwright** to scrape phone numbers for businesses from the 2GIS online directory.

### Configuration

* **Search Rubric:** The script is currently configured to search for **'цветы'** (flowers) using the `rubricId/389`. To adapt it for other business categories, modify the `SEARCH_TEMPLATE` URL.
* **Output File:** Results are saved to **`phones_2gis.txt`**.

### Usage

1.  Run the script:
    ```bash
    python 2gis_scraper.py
    ```
2.  When prompted, **enter the city slug** (e.g., `almaty`, `astana`).
3.  The scraper will navigate through search result pages, visit each firm's page, click the "Show phone" button, and extract the number.
4.  All unique phone numbers collected are saved to `phones_2gis.txt` upon completion.

### Disclaimer

Web scraping may violate the terms of service of the target website (2GIS). Use this tool responsibly, adhere to ethical scraping guidelines, and ensure compliance with all applicable laws and regulations.


### Lisence 

This project is released under the MIT License. You are free to use, modify, and distribute it for personal or commercial purposes.
