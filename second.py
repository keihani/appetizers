import time
from datetime import datetime

try:
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("\rCurrent Time: " + current_time, end="")
        time.sleep(1)
except KeyboardInterrupt:
    print("\n Exited the live clock.")
