import threading
import time 
event = threading.Event()
def worker():
    print("Worker: Waiting for event")
    event.wait()
    print("Worker: Event set, I can continue")

thread = threading.Thread(target=worker)
thread.start()
time.sleep(2)
print("Main: Setting event")
event.set()
thread.join()
print("Main: Program finished")