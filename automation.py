from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()

driver.get("https://messenger.com")
elem = driver.find_element(By.ID, "email")
elem.clear()
elem.send_keys("599934767")

elem = driver.find_element(By.ID, "pass")
elem.clear()
elem.send_keys("Giosoft123")

elem = driver.find_element(By.ID, "loginbutton")
elem.click()
