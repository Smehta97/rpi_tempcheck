#!/usr/bin/env python3

import subprocess
import logging
import time
from gpiozero import OutputDevice


ON_THRESHOLD = 50.0 # (degrees Celsius) Fan kicks on at this temperature.
OFF_THRESHOLD = 40.0  # (degress Celsius) Fan shuts off at this temperature.
FAN_PIN = 18  # Which GPIO pin you're using to control the fan.
LED_PIN = 23 # GPIO for LED
TIME_INTERVAL = 5

def get_temp():
    """Get the core temperature.

    Run a shell script to get the core temp and parse the output.

    Raises:
        RuntimeError: if response cannot be parsed.
    Returns:
        float: The core temperature in degrees Celsius.
    """

    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not parse temperature output.')


if __name__ == '__main__':
    # Logger
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger(__name__)

    # Validate the on and off thresholds
    if OFF_THRESHOLD >= ON_THRESHOLD:
        raise RuntimeError('OFF_THRESHOLD must be less than ON_THRESHOLD')

    fan = OutputDevice(FAN_PIN)
    led = OutputDevice(LED_PIN)

    is_active = False
    
    while True:
        temp = get_temp()
        logger.debug("measure_temp: {}".format(temp))

        if temp >= ON_THRESHOLD:
            if not is_active:
                fan.on()
                led.on()
                logger.info("FAN ON -> temp: {}".format(temp))
                is_active = True

        if temp <= OFF_THRESHOLD:
            if is_active:
                fan.off()
                led.off()
                logger.info("FAN OFF -> temp: {}".format(temp))
                is_active = False

        time.sleep(TIME_INTERVAL)