import time
from gpiozero import MCP3004

def get_dial_input():
  num_list = []
  timeout = 10
  first_time = True
  end = False
  while True:
    time_start = time.now
    time_end = time_start + timeout
    while (servo.value() < 0.1): # nearly zero
      print(servo.value())
      if (first_time or time.now < time_end):
        end = True
        break
      # wait for 0.01s
    print('hihi')
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
  
servo = MCP3004(channel=0)
get_dial_input()