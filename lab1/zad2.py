import threading
import time

event = threading.Event()

def function(i):
    print("start Thread %i\n" % i)
    event.wait()
    print("end Thread %i\n" % i)
    return


t1 = threading.Thread(target=function, args=(1,))
t2 = threading.Thread(target=function, args=(2,))

t3 = threading.Thread(target=function, args=(3,))
t4 = threading.Thread(target=function, args=(4,))
t5 = threading.Thread(target=function, args=(5,))
t1.start()
t2.start()
time.sleep(2)
event.set()
t1.join()
t2.join()
t3.start()
t4.start()
t5.start()
t3.join()
t4.join()
t5.join()

print("End program")
# Wniosek: Wykonanie wszystkich watkow zajmuje ok. 5 sekund,
# dzieki metodzie join() zeby watki 3,4,5 mogly sie rozpoczac, musza poczekac na zakonczenie
# watkow 1 i 2