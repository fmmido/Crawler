from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os

firefox_options = Options()
firefox_options.add_argument("--headless")

service = Service('/usr/local/bin/geckodriver')

driver = webdriver.Firefox(service=service, options=firefox_options)

visited_urls = set()
url_queue = set()

def save_urls():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crawled_urls_{timestamp}.txt"
    with open(filename, 'w') as file:
        for i, url in enumerate(sorted(visited_urls), start=1):
            file.write(f"Indexed {i}: {url}\n")
    print(f"URLs saved to {filename}")

def crawl_page(url):
    if url in visited_urls or not url.startswith('http'):
        return
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))
        )
        visited_urls.add(url)
        print(f"Indexed {len(visited_urls)}: {url}")

        links = driver.find_elements(By.TAG_NAME, 'a')
        new_links = set()
        for link in links:
            href = link.get_attribute('href')
            if href and (href.startswith('http') or href.startswith('/')):
                new_links.add(href)

        for new_link in new_links:
            if new_link not in visited_urls:
                if new_link.startswith('/'):
                    new_link = driver.current_url.rstrip('/') + new_link
                url_queue.add(new_link)

    except Exception as e:
        print(f"Failed to crawl {url}: {e}")

try:
    
    start_url = input("Enter the URL to start crawling: ").strip()
    if not start_url.startswith('http'):
        print("Invalid URL. Please start with 'http' or 'https'.")
        exit(1)
    
    url_queue.add(start_url)

    while url_queue:
        current_url = url_queue.pop()
        crawl_page(current_url)
        if len(visited_urls) % 10 == 0:
            save_urls()

    save_urls()

finally:
    driver.quit()
    print("Script ended")
