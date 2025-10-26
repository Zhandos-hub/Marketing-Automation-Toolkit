import os
import sys
import subprocess
import importlib.util
import shutil

# Define a list of required Python libraries
REQUIRED_LIBS = ["selenium", "playwright"]

def check_library(name):
    # Define a function to check if a specific Python library is installed
    spec = importlib.util.find_spec(name)
    if spec is None:
        # If the spec is not found, the library is not installed
        print(f"Library '{name}' is not installed.")
        print(f"Install with: pip install {name}")
        return False
    else:
        # If the spec is found, the library is installed
        print(f"Library '{name}' is installed.")
        return True

def get_chrome_version():
    # Define a function to get the installed Google Chrome version
    try:
        # Start a try block to handle potential errors (e.g., Chrome not found)
        if sys.platform.startswith('win'):
            # Check if the operating system is Windows.
            process = subprocess.run(
                r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                capture_output=True, text=True, shell=True
            )
            # Extract the version number from the command's output
            version = process.stdout.split()[-1]
        elif sys.platform.startswith('darwin'):
            # Check if the operating system is macOS
            process = subprocess.run(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                capture_output=True, text=True
            )
            # Extract the version number from the command's output
            version = process.stdout.strip().split()[-1]
        else:
            # Assume the operating system is Linux.
            process = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
            # Extract the version number from the command's output
            version = process.stdout.strip().split()[-1]
        print(f"Google Chrome version: {version}")
        return version
    except Exception:
        # Handle any exceptions that occurred while trying to find Chrome
        print("Chrome not found.")
        print("Install Google Chrome or ensure it's in your PATH.")
        return None

def get_chromedriver_version():
    # Define a function to get the installed ChromeDriver version
    # Find the full path to the 'chromedriver' executable in the system's PATH
    chromedriver_path = shutil.which("chromedriver.exe" if sys.platform.startswith('win') else "chromedriver")
    if not chromedriver_path:
        # If 'chromedriver' is not found in the PATH.
        print("ChromeDriver not found in PATH.")
        print("Download it from: https://chromedriver.chromium.org/downloads")
        return None
    try:
        # Start a try block to handle errors when running chromedriver
        # Run the 'chromedriver --version' command
        process = subprocess.run([chromedriver_path, "--version"], capture_output=True, text=True)
        # Extract the version number (it's usually the second word)
        version = process.stdout.strip().split()[1]
        print(f"ChromeDriver version: {version}")
        return version
    except Exception:
        # Handle any exceptions.
        print("Unable to read ChromeDriver version.")
        return None

def compare_versions(chrome_v, driver_v):
    # Define a function to compare the major versions of Chrome and ChromeDriver
    if not chrome_v or not driver_v:
        # If either version is missing, we can't compare
        print("Cannot compare versions. One of them is missing.")
        return
    
    # Get the major version number for Chrome (e.g., "114" from "114.0.5735.199")
    chrome_major = chrome_v.split('.')[0]
    # Get the major version number for ChromeDriver
    driver_major = driver_v.split('.')[0]
    
    if chrome_major != driver_major:
        # If the major versions do not match
        print(f"Version mismatch detected!")
        print(f"Chrome: {chrome_major}, ChromeDriver: {driver_major}")
        print("Tip: Download the matching ChromeDriver version from:")
        print("https://googlechromelabs.github.io/chrome-for-testing/")
    else:
        # If the major versions match
        print(f"Chrome and ChromeDriver versions match ({chrome_major}).")

def test_playwright_install():
    """Check if Playwright and its browsers are properly installed."""
    try:
        # Try to import the Playwright library
        import playwright
        from playwright.sync_api import sync_playwright

        print("Playwright module is installed.")

        # Try launching Chromium to confirm browser presence
        try:
            # Try to launch the Playwright-managed browser
            with sync_playwright() as pw:
                # Start a Playwright session.
                browser = pw.chromium.launch(headless=True)
                # Immediately close the browser
                browser.close()
                print("Playwright Chromium browser is installed and working.")
        except Exception:
            # Handle errors if the browser launch fails
            print("Playwright browsers not installed or misconfigured.")
            print("Run: playwright install chromium")

    except ImportError:
        # Handle the case where 'pip install playwright' hasn't been run
        print("Playwright module is missing.")
        print("Run: pip install playwright")

def main():
    # Define the main function that orchestrates the checks
    print("\nStarting Environment Diagnostics...\n")
    print("=== Checking Required Python Libraries ===")
    # Check all libraries in the list and store if all are OK
    libs_ok = all(check_library(lib) for lib in REQUIRED_LIBS)

    print("\n=== Checking Browser Versions ===")
    chrome_v = get_chrome_version()
    driver_v = get_chromedriver_version()
    # Compare the two versions
    compare_versions(chrome_v, driver_v)

    print("\n=== Checking Playwright Installation ===")
    # Run the Playwright installation test
    test_playwright_install()

    print("\nDiagnostics completed.\n")
    if not libs_ok:
        print("Some required Python libraries are missing. Please install them before running the main scripts.")
    else:
        print("Your environment is ready!")

    input("\nPress ENTER to exit...")

if __name__ == "__main__":
    main()
