from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException, 
    TimeoutException, 
    UnexpectedAlertPresentException
)
import datetime
import time
import traceback

# Define save_urls function
def save_urls(visited_urls):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crawled_urls_{timestamp}.txt"
    with open(filename, 'w') as file:
        for url in sorted(visited_urls):
            file.write(f"{url}\n")
    print(f"URLs saved to {filename}")

# Define find_links_with_retry function
def find_links_with_retry(driver):
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        try:
            links = driver.find_elements(By.TAG_NAME, 'a')
            return links
        except StaleElementReferenceException:
            attempts += 1
            print("Stale element reference exception. Retrying...")
            time.sleep(1)
    return []

# Define crawl_page function
def crawl_page(driver, url, visited_urls, url_queue):
    if url in visited_urls or not url.startswith('http'):
        return
    
    base_timeout = 30  # Starting timeout value in seconds
    max_retries = 5  # Maximum number of retries
    
    for attempt in range(max_retries):
        try:
            print(f"Visiting {url}")
            driver.get(url)
            
            # Wait until the page fully loads (with dynamic timeout)
            WebDriverWait(driver, base_timeout * (2 ** attempt)).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
            )

            visited_urls.add(url)
            print(f"Indexed {len(visited_urls)}: {url}")

            # Extract all anchor tags (links) with retries for stale elements
            links = find_links_with_retry(driver)
            new_links = set()
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if href and (href.startswith('http') or href.startswith('/')):
                        if href.startswith('/'):
                            href = driver.current_url.rstrip('/') + href  # Convert relative URLs to absolute URLs
                        new_links.add(href)
                except StaleElementReferenceException:
                    print("Stale element reference exception when accessing link. Skipping link...")
                    continue

            # Add new links to the queue if not already visited
            for new_link in new_links:
                if new_link not in visited_urls:
                    url_queue.add(new_link)
            break  # Exit loop if successful
            
        except TimeoutException as e:
            print(f"TimeoutException on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                print(f"Failed to crawl {url} after {max_retries} attempts")
                print(traceback.format_exc())
        except UnexpectedAlertPresentException as e:
            print(f"UnexpectedAlertPresentException: {e}")
            print(traceback.format_exc())
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")
            print(traceback.format_exc())

# Create a new instance of the Firefox driver
firefox_options = Options()
firefox_options.add_argument("--headless")
service = Service('/usr/local/bin/geckodriver')
driver = webdriver.Firefox(service=service, options=firefox_options)

visited_urls = set()
url_queue = set()

# Main execution
try:
    # Input the URL to start crawling
    start_url = input("Enter the URL to start crawling: ").strip()
    if not start_url.startswith('http'):
        print("Invalid URL. Please start with 'http' or 'https'.")
        exit(1)

    url_queue.add(start_url)

    while url_queue:
        current_url = url_queue.pop()
        crawl_page(driver, current_url, visited_urls, url_queue)

        # Save URLs after every 10 crawled links
        if len(visited_urls) % 10 == 0:
            save_urls(visited_urls)

        # Delay to avoid rate-limiting or blocking (2 seconds between requests)
        time.sleep(2)

    # Save the remaining URLs when crawling is done
    save_urls(visited_urls)

finally:
    driver.quit()
    print("Script ended")
