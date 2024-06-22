import pygame
import sys
import settings


# Check for GPIO
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  # ## out in source?
    settings.GPIO_AVAILABLE = True
    print("GPIO AVAILABLE")
    
except Exception:
    _, err, _ = sys.exc_info()
    print("GPIO UNAVAILABLE (%s)" % err)
    settings.GPIO_AVAILABLE = False

try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    settings.SOUND_ENABLED = True
except Exception as e:
    settings.SOUND_ENABLED = False

from pypboy.core import Pypboy

if __name__ == "__main__":
    boy = Pypboy('Pip-Boy 3000 MK IV', settings.WIDTH, settings.HEIGHT)
    print("RUN")
    boy.run()

