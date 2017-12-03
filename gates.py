import RPi.GPIO as GPIO
import time

# Pin Definitions
pwmPin= 18
buttonPin = 17

# Constants
frequency = 50 # Hz
period = 1/frequency
upPulseWidth = 0.002 #ms
downPulseWidth = 0.001 #ms
range = downPulseWidth - upPulseWidth

# Position defined as 0 is up, 1 is down, meaning a rotation of 90 degrees
def boomGatePositionToDutyCycle(position):
	return (position * range  + upPulseWidth) * frequency * 100

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmPin,GPIO.OUT)
GPIO.setup(buttonPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm = GPIO.PWM(pwmPin, frequency) # Hz
pwm.start(boomGatePositionToDutyCycle(0))

try:
	while 1:
		if GPIO.input(buttonPin): # high == not pressed
			print "up"
			duty = boomGatePositionToDutyCycle(0)
		else:
			print "down"
			duty = boomGatePositionToDutyCycle(1)
		pwm.ChangeDutyCycle(duty)
		print (duty)
		time.sleep(0.1)
	
except KeyboardInterrupt:
	pwm.stop()
	GPIO.cleanup()
