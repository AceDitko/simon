import pygame
import random
import time

pygame.init()

screen = pygame.display.set_mode((640, 640))

running = True
clock = pygame.time.Clock()
x = 0

delta_time = 0.1

colours = {0: "green",
           1: "red",
           2: "blue",
           3: "yellow"}

triangles = {"green": ((165, 110), (320, 265), (475, 110)),
             "red": ((160, 115), (315, 270), (160, 425)),
             "blue": ((480, 115), (325, 270), (480, 425)),
             "yellow": ((165, 430), (320, 275), (475, 430))}

sequence = []
flash_duration = 2

def draw_board():
    pygame.draw.rect(screen, "black", (150, 100, 340, 340))
    pygame.draw.polygon(screen, "white", ((165, 110), (320, 265), (475, 110)))
    pygame.draw.polygon(screen, "white", ((160, 115), (315, 270), (160, 425)))
    pygame.draw.polygon(screen, "white", ((480, 115), (325, 270), (480, 425)))
    pygame.draw.polygon(screen, "white", ((165, 430), (320, 275), (475, 430)))

    #pygame.draw.polygon(screen, "green", ((165, 110), (320, 265), (475, 110)))
    #pygame.draw.polygon(screen, "red", ((160, 115), (315, 270), (160, 425)))
    #pygame.draw.polygon(screen, "blue", ((480, 115), (325, 270), (480, 425)))
    #pygame.draw.polygon(screen, "yellow", ((165, 430), (320, 275), (475, 430)))

def flash(colour):
    pygame.draw.polygon(screen, colour, triangles[colour])

def increment_sequence(sequence):
    sequence.append(colours[random.randint(0, 3)])

def run_sequence(sequence, start_time):
    increment_sequence(sequence)
    for colour in sequence:
        flash(colour, start_time)
        start_time += flash_duration


sequence_start_time = None

while running:
    mouse = pygame.mouse.get_pos()
    screen.fill((255, 255, 255))
    
    x += 50 * delta_time
    if x >640:
        x = 0

    pygame.draw.rect(screen, "black", (5+x, 5, 10, 10))    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if (sequence_start_time is None) or (time.time() - sequence_start_time > len(sequence) * flash_duration):
                    increment_sequence(sequence)
                    sequence_start_time = time.time()
                    print(sequence)

    draw_board()

    if sequence_start_time is not None:
        elapsed = time.time() - sequence_start_time
        total_duration = len(sequence) * flash_duration
        if elapsed < total_duration:
            flash(sequence[int((elapsed-total_duration)//flash_duration)])
    
    
    pygame.display.flip()
    delta_time = clock.tick(60)
    
    delta_time = max(0.01, min(0.1, delta_time))

pygame.quit()