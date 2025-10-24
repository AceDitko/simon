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

sequence_start_time = None
expect_input = False
click_number = 0
score = 0

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
                if ((sequence_start_time is None) or (time.time() - sequence_start_time > len(sequence) * flash_duration)) and not expect_input:
                    increment_sequence(sequence)
                    sequence_start_time = time.time()
                    #print(sequence)
                if expect_input and len(sequence) > 0:
                    if pygame.draw.polygon(screen, sequence[click_number], triangles[sequence[click_number]]).collidepoint(pygame.mouse.get_pos()):
                        flash(sequence[click_number])
                        click_number += 1
                        if click_number == len(sequence):
                            score += 1
                            click_number = 0
                            expect_input = False
                            print(score)
                            increment_sequence(sequence)
                            sequence_start_time = time.time()
                    elif (480 >= mouse[0] >= 160) and (430 >= mouse[1] >= 110):
                        print("Wrong, idiot!")
                        print(f"Sequence was: " + ", ".join([str(i) for i in sequence]).rstrip(","))
                        expect_input = False
                        score = 0
                        click_number = 0
                        sequence = []
                        sequence_start_time = None

    draw_board()

    if sequence_start_time is not None:
        elapsed = time.time() - sequence_start_time
        total_duration = len(sequence) * flash_duration
        if elapsed < total_duration:
            flash(sequence[int((elapsed-total_duration)//flash_duration)])
            if sequence[int((elapsed-total_duration)//flash_duration)] == sequence[-1]:
                expect_input = True
    
    
    pygame.display.flip()
    delta_time = clock.tick(60)
    
    delta_time = max(0.01, min(0.1, delta_time))

pygame.quit()