import threading
import random
import time

def multiply(vec1,vec2):
    result = []
    for i in range(len(vec1)):
        result.append(vec1[i]*vec2[i])
    return result

def add(vec1,vec2):
    result = []
    for i in range(len(vec1)):
        result.append(vec1[i]+vec2[i])
    return result

def create_threads_multiply(L,vec1,vec2):
    threads = []
    for i in range(L):
        t = threading.Thread(target=multiply, args=(vec1,vec2))
        threads.append(t)
    return threads

def start_threads(threads):
    for t in threads:
        t.start()
    for t in threads:
        t.join()

def create_threads_add(L,vec1,vec2):
    threads = []
    for i in range(L):
        t = threading.Thread(target=add, args=(vec1,vec2))
        threads.append(t)
    return threads

def random_vector(n):
    vec = []
    for i in range(n):
        vec.append(random.randint(0,100))
    return vec

vec_size = int(input("Podaj rozmiar wektora: "))
thread_count = int(input("Podaj ilosc watkow: "))

if __name__=="__main__":
    vec1 = random_vector(vec_size)
    vec2 = random_vector(vec_size)

    time_start = time.time()
    threads = create_threads_multiply(thread_count,vec1,vec2)
    start_threads(threads)
    print("Czas mnozenia: ",time.time()-time_start)
    
    time_start = time.time()
    threads = create_threads_add(thread_count,vec1,vec2)
    start_threads(threads)
    print("Czas dodawania: ",time.time()-time_start)

    time_start = time.time()
    multiply(vec1,vec2)
    print("Czas mnozenia bez watkow: ",time.time()-time_start)

    time_start = time.time()
    add(vec1,vec2)
    print("Czas dodawania bez watkow: ",time.time()-time_start)




