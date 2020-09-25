import random
import time
from yeelight import Bulb
bulb=Bulb("192.168.1.116")

while True:

    bulb.set_rgb(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    time.sleep(1.1)
    # bulb.turn_off()
    # time.sleep(10)
    # bulb.turn_on()
