import time
from datetime import datetime

try:
    while True:
        now = datetime.now()
        current_time = now.strftime("%S")
        print(current_time)
        time.sleep(1)
except KeyboardInterrupt:
    print("\n Exited the live clock.")
