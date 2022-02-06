from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_driver(headless=True):
	if headless:
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		try:
			driver = webdriver.Chrome(options=chrome_options)
		except:
			driver = webdriver.Chrome(
				ChromeDriverManager().install(), options=chrome_options
			)
	else:
		try:
			driver = webdriver.Chrome()
		except:
			driver = webdriver.Chrome(ChromeDriverManager().install())
	return driver

def get_soup_from_driver(driver):
	return BeautifulSoup(driver.page_source, 'html.parser')
