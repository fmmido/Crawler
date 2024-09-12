from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time

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
