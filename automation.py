from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import local
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

from gpiozero import Button, MCP3004, Servo

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
  elem = driver.find_element(By.CSS_SELECTOR, '[aria-label="Accept"]')
  return elem != None

def pick_up():
  print("pick up")
  if (not is_incoming()):
    return
  driver.find_element(By.CSS_SELECTOR, '[aria-label="Accept"]').click()

def hang_up():
  if btn.wait_for_release(timeout=1):
    print("local config")
    local.turn_on_ap()
    if not local.is_connected():
      print("show wifi config")
    print("login")
    btn.wait_for_press()
    local.turn_off_ap()
    print("restart the device. flash the LEDs")
  else:
    print("hang up")
    # if there are two winodws, then close the second one
    if (len(driver.window_handles) == 2):
      window_handles = driver.window_handles
      driver.switch_to.window(window_handles[1])
      driver.close()
      driver.switch_to.window(window_handles[0])


def get_dial_input():
  num_list = []
  timeout = timedelta(seconds=3)
  first_time = True
  end = False
  while True:
    servo.detach()
    time_start = datetime.now()
    time_end = time_start + timeout
    print("this is value " + str(servo_feedback.value))
    while (servo_feedback.value < 0.27): # minimum value
      print(servo_feedback.value)
      if (not first_time and datetime.now() > time_end):
        print("ending")
        end = True
        break
      time.sleep(0.01)

    print('hihi')
    if (end):
      if (len(num_list) == 0):
          return -1
      number_str = ''.join(map(str, num_list))
      number = int(number_str)
      return number
      
    
    first_time = False
    prev = servo_feedback.value
    time.sleep(1)
    while (abs(prev - servo_feedback.value) > 0.05):
      print("hey")
      prev = servo_feedback.value
      time.sleep(1)

    print(prev - servo_feedback.value) 
    num = to_num(servo_feedback.value)
    if (num != "no"):
        num_list.append(num)
    else:
        print("no")
    print(num_list)
    servo.min()
    time.sleep(1)

def to_num(input):
  margin_of_error = 0.04
  if (input > 0.48 - margin_of_error and input < 0.48 + margin_of_error):
    return 9
  elif (input > 0.55 - margin_of_error and input < 0.55 + margin_of_error):
      return 8
  elif (input > 0.66 - margin_of_error and input < 0.66 + margin_of_error):
      return 7
  elif (input > 0.73 - margin_of_error and input < 0.73 + margin_of_error):
      return 6
  else: 
    return "no"

def turn_on_active_leds():
  configJson = {"Giorgi Shengelaia": "123"}
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
  print(f'led is on N{n + 3}')
    
# json to dictionary
def get_config_json():
    with open('../config.json', 'r') as f:
        json_lines = f.read()
        config = json.loads(json_lines)
        print(config)
        return config

def get_name_from_number(input_number):
  for name, number in config.items():
    if number == input_number:
      return name

username = config["messenger_credentials"].keys()[0]
password = config["messenger_credentials"].values()[0]

btn = Button(2, bounce_time = 0.2)

btn.when_pressed = hang_up_or_local_config
btn.when_released = pick_up

myGPIO=25
 
maxPW=(2.0+0.25)/1000
minPW=(1.0-0.45)/1000
 
servo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW)
servo.min()
servo.detach()

time.sleep(2)
servo_feedback = MCP3004(channel=0)

config = get_config_json()

chrome_options = Options()
# enable microphone
chrome_options.add_argument("--use-fake-ui-for-media-stream")

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver = webdriver.Chrome(r'/usr/bin/chromedriver')

open_messenger(username, password)

number = get_dial_input()
print(number)
  # map number to name
name = get_name_from_number(number)
print(name)
  # i want the hang up button to work from the time
  # when the start a call button is pressed
  # the button should be released first and then it should be pressed
call_user(name)

input()

