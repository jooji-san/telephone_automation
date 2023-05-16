from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

from gpiozero import Button, MCP3004

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

def is_incoming():
  elem = driver.find_element(By.CSS_SELECTOR, '[aria-labelledby=":r42:"]')
  return elem != None

def pick_up():
  if (not is_incoming()):
    return
  driver.find_element(By.CSS_SELECTOR, '[aria-label="Accept"]').click()

def hang_up():
  # if there are two winodws, then close the second one
  if (len(driver.window_handles) == 2):
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[1])
    driver.close()
    driver.switch_to.window(window_handles[0])
  
  turn_on_active_leds()

def get_dial_input():
  num_list = []
  timeout = 10
  first_time = True
  end = False
  while True:
    time_start = time.now
    time_end = time_start + timeout
    while (servo.value() == 0): #nearly zero
      if (first_time or time.now < time_end):
        end = True
        break
      # wait for 0.01s

    if (end):
      number_str = ''.join(map(str, num_list))
      number = int(number_str)
      return number
      
    
    first_time = False
    prev = servo.value()
    time.sleep(1)
    while (prev != servo.value()):
      prev = servo.value()
      time.sleep(1)
    
    num = to_num(servo.value())
    num_list.append(num)

def to_num(input):
  if (input > 0 and input < 0.5):
    return 1
  else: 
    return 0

def turn_on_active_leds():
  configJson = {}
  for counter, key in enumerate(configJson):
    if (is_active(key)):
      led_on(counter)

def is_active(name):
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
  
  result = elem.find_element(By.CLASS_NAME, 'xv9rvxn')
  return result != None
  
  
def led_on(n):
  print(f'led is on N{n + 2}')
    

username = "568711563"
password = "Giosoft123"
name = "Giorgi Shengelaia"

Button.when_pressed = hang_up
Button.when_released = pick_up

servo = MCP3004(channel=0)

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

