from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def call_user(name):
  # search for user
  elem = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Search Messenger"]'))
      )
  elem.clear()
  elem.send_keys(name)

  xpath1 = "//ul[@role='listbox']/li[1]/ul[1]/div[2]"
  if name == "Giorgi Shengelaia":
    xpath1 = "//ul[@role='listbox']/li[1]/ul[1]/div[3]"
  elem = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, xpath1))
      )
  elem.click()

  # start voice call
  elem = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Start a voice call"]'))
      )
  elem.click()

def open_messenger(username, password):
  driver.get("https://messenger.com")
  elem = driver.find_element(By.ID, "email")
  elem.clear()
  elem.send_keys(username)

  elem = driver.find_element(By.ID, "pass")
  elem.clear()
  elem.send_keys(password)

  elem = driver.find_element(By.ID, "loginbutton")
  elem.click()

def hang_up():
  # if there are two winodws, then close the second one
  if (len(driver.window_handles) == 2):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    driver.close()
    driver.switch_to.window(window_handles[0])

def get_dial_input():
  # wait for the dial to be moved
  # wait a little bit more
  # if the dial is not moved, then return the number
  GPIO.wait_for_edge(channel, GPIO.RISING)
  GPIO.wait_for_edge(channel, GPIO_RISING, timeout=5000)

username = "568711563"
password = "Giosoft123"
name = "Giorgi Shengelaia"

# json to dictionary

chrome_options = Options()
# enable microphone
chrome_options.add_argument("--use-fake-ui-for-media-stream")

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver = webdriver.Chrome(r'/usr/bin/chromedriver')

open_messenger(username, password)

while True:
  number = get_dial_input()

  # map number to name

  # i want the hang up button to work from the time
  # when the start a call button is pressed
  # the button should be released first and then it should be pressed

  call_user(name)


  


input()

