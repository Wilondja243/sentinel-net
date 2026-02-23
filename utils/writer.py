import sys
import time

# write the response
def writer(text):
    for t in text:
        sys.stdout.write(t)
        sys.stdout.flush()
        time.sleep(0.05)

    print()