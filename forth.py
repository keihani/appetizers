import random
from time import sleep

try:
    while True:
        rnd = int(random.random() * 60)
        print("\r %d" % rnd, end="")
        sleep(1)
except KeyboardInterrupt:
    print("\nEnd of generation")
