import time
from gpiozero import MCP3004, Servo
from datetime import datetime, timedelta

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
    while (servo_feedback.value < 0.25): # minimum value
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
  if (input > 0.587 - margin_of_error and input < 0.587 + margin_of_error):
    return 9
  elif (input > 0.683 - margin_of_error and input < 0.683 + margin_of_error):
      return 8
  elif (input > 0.741 - margin_of_error and input < 0.741 + margin_of_error):
      return 7
  else: 
    return "no"
  
myGPIO=25
 
maxPW=(2.0+0.25)/1000
minPW=(1.0-0.40)/1000
 
servo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW)
servo.min()
print("min")
time.sleep(2)
servo_feedback = MCP3004(channel=0)
print(get_dial_input())
