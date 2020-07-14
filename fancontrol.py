#!/usr/bin/env python3

import subprocess
import time
import sys

from gpiozero import PWMOutputDevice

GPIO_PIN = 17
WAIT_TIME = 5

temp_steps = [45.0, 50.0, 55.0, 60.0, 65.0, 70.0]
pwm_steps = [0.0, 0.2, 0.3, 0.5, 0.8, 1.0]

def get_temp():
	output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output = True)
	temp_str = output.stdout.decode()
	try:
		return float(temp_str.split('=')[1].split('\'')[0])
	except(IndexError, ValueError):
		raise RuntimeError('Cloud not parse temp output.')

if __name__ == '__main__':
	if len(temp_steps) != len(pwm_steps):
		raise RuntimeError('Temp steps and PWM steps arrays are not of the same size.')

	fan = PWMOutputDevice(GPIO_PIN, frequency=25)
	fan.on()

	try:
		while True:
			temp = get_temp()
			print("CPU Temp is " + str(temp))
			step_idx = 0
			pwm = 0

			for i in range(0, len(temp_steps) - 1):
				step_idx = i
				if temp < temp_steps[i]:
					break

			if step_idx == 0:
				# temp is less or equal to first step, pwm is the minimum value
				pwm = pwm_steps[0]
			elif step_idx == (len(temp_steps) - 1):
				# temp is higher or equal to final step, pwm is the max value
				pwm = pwm_steps[len(temp_steps) - 1]
			else:
				# between 2 steps, interpolate the 2 pwm steps
				pwm_low = pwm_steps[step_idx -1]
				pwm_high = pwm_steps[step_idx]
				temp_low = temp_steps[step_idx -1]
				temp_high = temp_steps[step_idx]
				pwm = pwm_low + (temp - temp_low) * ( (pwm_high - pwm_low)/(temp_high - temp_low) )

			# apply new fan speed and wait until next loop
			fan.value = pwm
			print("PWM applied " + str(pwm))
			time.sleep(WAIT_TIME)
	except:
		# process interrupted
		print("Process terminated, fan will turn at max speed")
		fan.value = 1.0
		raise
		sys.exit()

