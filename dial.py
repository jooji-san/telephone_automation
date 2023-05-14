import time
from gpiozero import MCP3004, Servo
from datetime import datetime, timedelta

def get_dial_input():
  num_list = []
  timeout = timedelta(seconds=10)
  first_time = True
  end = False
  while True:
    time_start = datetime.now()
    time_end = time_start + timeout
    while (servo_feedback.value < 0.1): # nearly zero
      print(servo_feedback.value)
      if (not first_time and time.now < time_end):
        end = True
        break
      # wait for 0.01s
    print('hihi')
    if (end):
      if (len(num_list) == 0):
          return -1
      number_str = ''.join(map(str, num_list))
      number = int(number_str)
      return number
      
    
    first_time = False
    prev = servo_feedback.value
    print("0 sec")
    time.sleep(1)
    print("1 sec")
    while (prev != servo_feedback.value):
      prev = servo_feedback.value
      time.sleep(1)
    
    num = to_num(servo_feedback.value)
    num_list.append(num)
    servo.min()

def to_num(input):
  if (input > 0 and input < 0.5):
    return 1
  else: 
    return 0
  
servo = Servo(25)
servo.min()
servo_feedback = MCP3004(channel=0)
get_dial_input()
