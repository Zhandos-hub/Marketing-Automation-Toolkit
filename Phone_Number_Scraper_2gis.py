
"""
2GIS Phone Number Scraper

This script scrapes phone numbers for flower shops (to adapt for other rubrics change 'цветы' in the URL and 'rubricId' as needed)
from 2GIS for a user-specified city.

It navigates through search pages, opens each firm's page,
clicks the "Show phone" button, and saves the unique numbers
to 'phones_2gis.txt'.
"""

import time
import sys
from playwright.sync_api import sync_playwright

# Search URL template, {city} and {page} will be formatted.
rubric_id = 389  # Rubric ID for "Flowers"
rubric="цветы"
SEARCH_TEMPLATE = "https://2gis.kz/{city}/search/{rubric}/rubricId/{rubric_id}/page/{page}"
OUTPUT_FILE = "phones_2gis.txt"

def main():
    """Main function to run the scraper."""
    
    city = input("Enter city (e.g., almaty): ").strip().lower()
    if not city:
        print("Error: City cannot be empty.", file=sys.stderr)
        sys.exit(1)

    # Use a set to store unique phone numbers
    phones = set()

    print(f"Starting scraper for city: {city}")

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            )

            page_number = 1
            while True:
                url = SEARCH_TEMPLATE.format(city=city, page=page_number)
                print(f"\n=== Page {page_number}: {url}")
                
                try:
                    resp = page.goto(url, timeout=20000)
                    if not resp or resp.status != 200:
                        print(f"  Failed to load page (Status: {resp.status if resp else 'N/A'}). Exiting loop.")
                        break
                except Exception as e:
                    print(f"  Error loading page: {e}. Exiting loop.")
                    break

                # Wait for at least one search result (snippet)
                try:
                    page.wait_for_selector("a[href*='/firm/']", timeout=10000)
                except Exception:
                    print("  No snippets found. This is the end.")
                    break

                # Collect unique firm URLs from the page
                elems = page.query_selector_all("a[href*='/firm/']")
                firm_urls = []
                for a in elems:
                    href = a.get_attribute("href")
                    if not href:
                        continue
                    
                    full_url = href if href.startswith("http") else "https://2gis.kz" + href
                    if full_url not in firm_urls:
                        firm_urls.append(full_url)

                print(f"  Found {len(firm_urls)} firms on this page.")

                # Visit each firm's page to get the phone number
                for firm_url in firm_urls:
                    try:
                        page.goto(firm_url, timeout=15000)
                        
                        # Wait for and click the "Show phone" button
                        btn = page.wait_for_selector("button:has-text('Показать телефон')", timeout=5000)
                        btn.click()
                        
                        # Wait for the phone link (tel:) to appear
                        link = page.wait_for_selector("a[href^='tel:']", timeout=5000)
                        href = link.get_attribute("href")  # e.g., "tel:+77001234567"
                        
                        num = href.split("tel:")[1]
                        clean_num = "".join(ch for ch in num if ch.isdigit())
                        
                        if clean_num not in phones:
                            print(f"  Found number: {clean_num}")
                            phones.add(clean_num)
                        
                    except Exception as e:
                        print(f"  Warning: Could not find phone. {e}")
                    
                    time.sleep(0.3) # Small delay between firms

                # Try to go to the next page
                page_number += 1
                time.sleep(0.5) # Small delay between search pages

            browser.close()

    except Exception as e:
        print(f"\nA critical error occurred: {e}", file=sys.stderr)
    
    finally:
        # Save the results
        if phones:
            try:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    for n in sorted(phones):
                        f.write(n + "\n")
                print(f"\nDone! Collected {len(phones)} unique numbers.")
                print(f"Results saved to {OUTPUT_FILE}")
            except Exception as e:
                print(f"\nError saving to file: {e}", file=sys.stderr)
        else:
            print("\nNo phone numbers were collected.")

        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()