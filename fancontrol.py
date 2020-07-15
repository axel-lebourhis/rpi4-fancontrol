#!/usr/bin/env python3

import subprocess
import time
import sys

from gpiozero import PWMOutputDevice

GPIO_PIN = 17
WAIT_TIME = 5
MAX_PWM = 1.0
MIN_PWM = 0.5

temp_steps = [55.0, 60.0, 65.0, 70.0]
pwm_steps = [0.0, 0.5, 0.8, 1.0]

def get_temp():
	output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output = True)
	temp_str = output.stdout.decode()
	try:
		return float(temp_str.split('=')[1].split('\'')[0])
	except(IndexError, ValueError):
		raise RuntimeError('Could not parse temp output.')

if __name__ == '__main__':
	if len(temp_steps) != len(pwm_steps):
		raise RuntimeError('Temp steps and PWM steps arrays are not of the same size.')

	fan = PWMOutputDevice(GPIO_PIN, frequency=100)
	fan.on()

	print("Fan curve is:")
	for i in range(0, len(temp_steps)):
		print("temp: " + str(temp_steps[i]) + " pwm: " + str(pwm_steps[i]) )

	try:
		while True:
			temp = get_temp()
			print("CPU Temp is " + str(temp))
			step_idx = 0
			pwm = 0

			for i in range(0, len(temp_steps)):
				step_idx = i
				if temp < temp_steps[i]:
					break
			if step_idx == 0:
				# temp is less or equal to first step, pwm is the minimum value
				pwm = pwm_steps[0]
			elif step_idx == (len(temp_steps)-1):
				# temp is higher or equal to final step, pwm is the max value
				pwm = pwm_steps[len(temp_steps)-1]
			else:
				# between 2 steps, interpolate the 2 pwm steps
				pwm_low = pwm_steps[step_idx -1]
				pwm_high = pwm_steps[step_idx]
				temp_low = temp_steps[step_idx -1]
				temp_high = temp_steps[step_idx]
				pwm = pwm_low + (temp - temp_low) * ( (pwm_high - pwm_low)/(temp_high - temp_low) )
				if pwm > MAX_PWM:
					pwm = MAX_PWM
				elif pwm < MIN_PWM:
					pwm = MIN_PWM

			# apply new fan speed and wait until next loop
			print("PWM applied " + str(pwm))
			fan.value = pwm
			time.sleep(WAIT_TIME)
	except:
		# process interrupted
		print("Fan control interrupted")
		fan.off()
		raise
		sys.exit()

