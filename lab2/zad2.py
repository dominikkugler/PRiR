import threading
import numpy as np

# Macierze wejściowe
matrix1 = np.random.randint(10, size=(3, 3))
matrix2 = np.random.randint(10, size=(3, 3))

# Wynikowa macierz
result_matrix = np.zeros((3, 3))

# Liczba operacji do wykonania
num_operations = 2000

# RLock do synchronizacji dostępu do macierzy wynikowej
lock = threading.RLock()

def multiply_and_sum():
    global result_matrix
    for _ in range(num_operations):
        # Mnożenie macierzy i dodawanie do macierzy wynikowej
        with lock:
            result_matrix += np.dot(matrix1, matrix2)

# Tworzenie wątków
num_threads = 4
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=multiply_and_sum)
    threads.append(thread)
    thread.start()

# Oczekiwanie na zakończenie wszystkich wątków
for thread in threads:
    thread.join()

print("Wynikowa macierz:")
print(result_matrix)
