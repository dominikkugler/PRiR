import pygame
import random
import threading
import time

# Inicjalizacja Pygame
pygame.init()

# Rozmiary ekranu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Kolory
BLACK = (0, 0, 0)

# Tworzenie ekranu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rysowanie figur geometrycznych")

# Semafor
draw_semaphore = threading.Semaphore()

# Funkcja rysująca prostokąt
def draw_rectangle():
    while True:
        # Oczekiwanie na uzyskanie dostępu do rysowania
        draw_semaphore.acquire()

        # Losowy rozmiar prostokąta
        width = random.randint(20, 200)
        height = random.randint(20, 200)

        # Losowa pozycja prostokąta
        x = random.randint(0, SCREEN_WIDTH - width)
        y = random.randint(0, SCREEN_HEIGHT - height)

        # Losowy kolor wypełnienia
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Rysowanie prostokąta
        pygame.draw.rect(screen, color, (x, y, width, height))

        # Odświeżenie ekranu
        pygame.display.flip()

        # Odblokowanie semafora po zakończeniu rysowania
        draw_semaphore.release()

        # Opóźnienie przed kolejnym rysowaniem
        time.sleep(0.5)

# Tworzenie wątków
num_threads = 5
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=draw_rectangle)
    threads.append(thread)
    thread.start()

# Główna pętla programu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
