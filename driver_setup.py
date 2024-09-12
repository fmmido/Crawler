from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Set Firefox options for headless browsing
firefox_options = Options()
firefox_options.add_argument("--headless")

# Set path to geckodriver
service = Service('/usr/local/bin/geckodriver')

def create_driver():
    return webdriver.Firefox(service=service, options=firefox_options)
