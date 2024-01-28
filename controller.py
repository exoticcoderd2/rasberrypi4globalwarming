import RPi.GPIO as GPIO
import time



# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo motor
servo_pin = 12

# Set the PWM frequency (50 Hz is typical)
pwm_frequency = 50

# Initialize the PWM object
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, pwm_frequency)

GPIO_TRIGGER = 20
GPIO_ECHO = 21
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
container_height=23.368
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
# Start PWM with a duty cycle of 0 (neutral position)
pwm.start(0)

try:
    while True:
        # Move the servo motor to one extreme position (e.g., 0 degrees)
        pwm.ChangeDutyCycle(10)
        time.sleep(3)
        dist = distance()
        level=container_height-dist
        print ("Water level in container 1 = %.1f cm" % level)
        #time.sleep(1)

        # Move the servo motor to the other extreme position (e.g., 180 degrees)
        pwm.ChangeDutyCycle(2)
        time.sleep(3)
        dist = distance()
        level=container_height-dist
        print ("Water level in container 2 = %.1f cm" % level)
        #time.sleep(5)
        


       

except KeyboardInterrupt:
    # Stop PWM and cleanup GPIO when the program is terminated
    pwm.stop()
    GPIO.cleanup()
finally:
    print("clean up") 
    GPIO.cleanup() # cleanup all GPIO 



