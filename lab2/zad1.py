import threading
import random
import time

# Liczba punktów do wygenerowania
total_points = 2000000

# Liczba punktów wewnątrz okręgu (zmienna współdzielona)
points_inside_circle = 0

# Zamka do synchronizacji dostępu do zmiennej współdzielonej
lock = threading.Lock()

def monte_carlo_simulation(points):
    global points_inside_circle

    for _ in range(points):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        distance = x**2 + y**2

        if distance <= 1:
            with lock:
                points_inside_circle += 1

# Tworzenie i startowanie wątków
num_threads = 8
threads = []

points_per_thread = total_points // num_threads

start_time = time.time()  # Mierzenie czasu rozpoczęcia obliczeń

for _ in range(num_threads):
    thread = threading.Thread(target=monte_carlo_simulation, args=(points_per_thread,))
    threads.append(thread)
    thread.start()

# Oczekiwanie na zakończenie wątków
for thread in threads:
    thread.join()

end_time = time.time()  # Mierzenie czasu zakończenia obliczeń
execution_time = end_time - start_time

# Obliczenie wartości liczby pi
pi_approximation = 4 * points_inside_circle / total_points

print(f"Przybliżona wartość liczby pi: {pi_approximation}")
print(f"Czas wykonania obliczeń: {execution_time} sekund")

# Wyniki dla 4 wątków oraz 1000000 punktów:
# Przybliżona wartość liczby pi: 3.142676
#Czas wykonania obliczeń: 1.0608515739440918 sekund

# Wyniki dla 2 wątków oraz 1000000 punktów:
# Przybliżona wartość liczby pi: 3.139896
# Czas wykonania obliczeń: 1.4771089553833008 sekund

# Wyniki dla 8 wątków oraz 1000000 punktów:
# Przybliżona wartość liczby pi: 3.141656
# Czas wykonania obliczeń: 1.1305389404296875 sekund

# Wyniki dla 2 wątków oraz 2000000 punktów:
# Przybliżona wartość liczby pi: 3.141638
# Czas wykonania obliczeń: 2.267024517059326 sekund

# Wyniki dla 4 wątków oraz 2000000 punktów:
# Przybliżona wartość liczby pi: 3.139834 
# Czas wykonania obliczeń: 2.3812544345855713 sekund

# Wyniki dla 8 wątków oraz 2000000 punktów:
# Przybliżona wartość liczby pi: 3.142966
# Czas wykonania obliczeń: 2.514740228652954 sekund

# Z powyższych wyników wychodzi, że zwiększenie liczby wątków nie zawsze przekłada się na skrócenie czasu wykonania obliczeń.
# Bardzo prawdopodobne jest, że istnieje optymalna liczba wątków, która pozwala na uzyskanie najlepszych wyników.
# Niekoniecznie jest to najwyższa liczba wątków, co widać w czasach wykonania oraz dokładności obliczeń.
