from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException, 
    TimeoutException, 
    UnexpectedAlertPresentException
)
import time
import traceback

def find_links_with_retry(driver):
    """
    Attempts to find all links on a page with retries for stale element exceptions.
    """
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

def crawl_page(driver, url, visited_urls, url_queue):
    """
    Crawls the page, saves the URLs, and adds any new links to the queue.
    """
    if url in visited_urls or not url.startswith('http'):
        return

    visited_urls.add(url)  # Save the URL before trying to crawl

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

        except UnexpectedAlertPresentException as e:
            print(f"Failed to crawl {url}: Alert Text: {e.alert_text}")
            break  # Exit if an alert is preventing further crawling
        except TimeoutException as e:
            print(f"TimeoutException on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                print(f"Failed to crawl {url} after {max_retries} attempts")
                print(traceback.format_exc())
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")
            print(traceback.format_exc())
