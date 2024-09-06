## Website Crawler for pen testing (for dynamic websites using Selenium)

This project is a simple web crawler built using Selenium and Python. It navigates to a starting URL, collects all links from the page, and recursively crawls these links while storing the crawled URLs in a text file.

It utilizes Selenium WebDriver to crawl dynamic websites, including those with JavaScript-generated content. It efficiently navigates and indexes URLs from the starting page, handling JavaScript rendering and AJAX requests. The URLs are saved to a timestamped file in the format crawled_urls_YYYYMMDD_HHMMSS.txt. Skills demonstrated include Python, Selenium, web scraping, handling dynamic JavaScript content, and browser automation.

## Features

- **Headless Browser**: The crawler uses Firefox in headless mode for efficient crawling.
- **URL Queue**: A queue is maintained to manage the URLs that need to be visited.
- **Automatic URL Saving**: The list of visited URLs is saved periodically and at the end of the crawling process.
- **Error Handling**: Handles crawling exceptions and ensures the browser is closed when the script ends.

## Requirements

- Python 3.x
- Selenium
- Firefox and Geckodriver

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/fmmido/Website-Crawler-for-pen-testing.git
    ```

2. Install required Python packages:
    ```bash
    pip install selenium
    ```

3. Make sure you have **Geckodriver** installed and in your system's PATH.

4. Ensure that Firefox is installed on your system.

## Usage

1. Open the terminal and navigate to the project directory:
    ```bash
    cd your-repository
    ```

2. Run the script:
    ```bash
    python3 crawler.py
    ```

3. The URLs will be crawled from the starting page and saved in a file with the format `crawled_urls_YYYYMMDD_HHMMSS.txt`.

## Configuration

You can modify the starting URL and the path to Geckodriver in the script:
- **Starting URL**: Change the `start_url` variable in the script.
- **Geckodriver Path**: If Geckodriver is not in your default path, modify the path in the line:
  ```python
  service = Service('/path/to/geckodriver')
r for pen testing (Web Crawler using Selenium)

This project is a simple web crawler built using Selenium and Python. It navigates to a starting URL, collects all links from the page, and recursively crawls these links while storing the crawled URLs in a text file.

## Features

- **Headless Browser**: The crawler uses Firefox in headless mode for efficient crawling.
- **URL Queue**: A queue is maintained to manage the URLs that need to be visited.
- **Automatic URL Saving**: The list of visited URLs is saved periodically and at the end of the crawling process.
- **Error Handling**: Handles crawling exceptions and ensures the browser is closed when the script ends.

## Requirements

- Python 3.x
- Selenium
- Firefox and Geckodriver

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/fmmido/Website-Crawler-for-pen-testing.git
    ```

2. Install required Python packages:
    ```bash
    pip install selenium
    ```

3. Make sure you have **Geckodriver** installed and in your system's PATH.

4. Ensure that Firefox is installed on your system.

## Usage

1. Open the terminal and navigate to the project directory:
    ```bash
    cd your-repository
    ```

2. Run the script:
    ```bash
    python3 crawler.py
    ```

3. The URLs will be crawled from the starting page and saved in a file with the format `crawled_urls_YYYYMMDD_HHMMSS.txt`.

## Configuration

You can modify the starting URL and the path to Geckodriver in the script:
- **Starting URL**: Change the `start_url` variable in the script.
- **Geckodriver Path**: If Geckodriver is not in your default path, modify the path in the line:
  ```python
  service = Service('/path/to/geckodriver')
