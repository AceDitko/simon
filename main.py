import pygame
import random
import time

pygame.init()

screen = pygame.display.set_mode((640, 640))

running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

colours = {0: "green",
           1: "red",
           2: "blue",
           3: "yellow"}

triangles = {"green": ((165, 110), (320, 265), (475, 110)),
             "red": ((160, 115), (315, 270), (160, 425)),
             "blue": ((480, 115), (325, 270), (480, 425)),
             "yellow": ((165, 430), (320, 275), (475, 430))}

x = 0
delta_time = 0.1

sequence = []
flash_duration = 2


def draw_board():
    pygame.draw.rect(screen, "black", (150, 100, 340, 340))
    pygame.draw.polygon(screen, "white", ((165, 110), (320, 265), (475, 110)))
    pygame.draw.polygon(screen, "white", ((160, 115), (315, 270), (160, 425)))
    pygame.draw.polygon(screen, "white", ((480, 115), (325, 270), (480, 425)))
    pygame.draw.polygon(screen, "white", ((165, 430), (320, 275), (475, 430)))

    pygame.draw.polygon(screen, (0, 100, 0), ((165, 110), (320, 265), (475, 110)))
    pygame.draw.polygon(screen, (139, 0, 0), ((160, 115), (315, 270), (160, 425)))
    pygame.draw.polygon(screen, (0, 0, 139), ((480, 115), (325, 270), (480, 425)))
    pygame.draw.polygon(screen, (139, 128, 0), ((165, 430), (320, 275), (475, 430)))

def flash(colour):
    pygame.draw.polygon(screen, colour, triangles[colour])

def increment_sequence(sequence):
    sequence.append(colours[random.randint(0, 3)])

def mouse_in_polygon(points, mouse_pos):
    min_x = min(x for x, y in points)
    max_x = max(x for x, y in points)
    min_y = min(y for x, y in points)
    max_y = max(y for x, y in points)

    # Create a transparent temporary surface the shape will fit inside
    temp_surface = pygame.Surface(
        (max_x - min_x + 1, max_y - min_y +1),
        pygame.SRCALPHA
    )

    # Shift the polygon so it starts in top left corner of surface
    # and draw the shape
    shifted_points = [(x - min_x, y - min_y) for x, y in points]
    pygame.draw.polygon(temp_surface, (255, 255, 255), shifted_points)

    # Create a mask from the temporary surface
    mask = pygame.mask.from_surface(temp_surface)

    # Define the mouse coordinates (mx, my) and the
    # local coordinates (lx, ly)
    mx, my = mouse_pos
    lx, ly = int(mx - min_x), int(my - min_y)

    # Check if the mouse coordinates are within the bounds of the mask
    if 0 <= lx < mask.get_size()[0] and 0 <= ly < mask.get_size()[1]:
        return mask.get_at((lx, ly)) != 0
    return False

sequence_start_time = None
victory_start_time = None
expect_input = False
victory_flash = False
click_number = 0
score = 0
high_score = 0

while running:
    mouse = pygame.mouse.get_pos()
    screen.fill((255, 255, 255))
    if score > high_score:
        high_score = score
    high_text = font.render(f"High Score: {high_score}", True, "black")
    current_text = font.render(f"Current Score: {score}", True, "black")

    x += 50 * delta_time
    if x >640:
        x = 0

    pygame.draw.rect(screen, "black", (5+x, 620, 10, 10))    

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
                            victory_flash = True
                            increment_sequence(sequence)
                            victory_start_time = time.time()
                    elif (480 >= mouse[0] >= 160) and (430 >= mouse[1] >= 110):
                        print("Wrong, idiot!")
                        print(f"Sequence was: " + ", ".join([str(i) for i in sequence]).rstrip(","))
                        expect_input = False
                        score = 0
                        click_number = 0
                        sequence = []
                        sequence_start_time = None

    screen.blit(high_text, (10, 10))
    screen.blit(current_text, (10, 40))

    draw_board()

    if sequence_start_time is not None and not victory_flash:
        elapsed = time.time() - sequence_start_time
        total_duration = len(sequence) * flash_duration
        if elapsed < total_duration:
            flash(sequence[int((elapsed-total_duration)//flash_duration)])
            if sequence[int((elapsed-total_duration)//flash_duration)] == sequence[-1]:
                expect_input = True
    elif victory_start_time is not None and victory_flash:
        elapsed = time.time() - victory_start_time
        vic_total_duration = 2.5
        vic_flash_duration = 0.5
        if elapsed < vic_total_duration:
            if int((elapsed-vic_total_duration)//vic_flash_duration) % 2 == 1:
                draw_board()
            else:
                flash("green")
                flash("red")
                flash("blue")
                flash("yellow")
        else:
            victory_flash = False
            sequence_start_time = time.time()
        
    
    if expect_input:
        if mouse_in_polygon(triangles["green"], mouse):
            pygame.draw.polygon(screen, (0, 150, 0), ((165, 110), (320, 265), (475, 110)))
        if mouse_in_polygon(triangles["red"], mouse):
            pygame.draw.polygon(screen, (189, 0, 0), ((160, 115), (315, 270), (160, 425)))
        if mouse_in_polygon(triangles["blue"], mouse):
            pygame.draw.polygon(screen, (0, 0, 189), ((480, 115), (325, 270), (480, 425)))
        if mouse_in_polygon(triangles["yellow"], mouse):
            pygame.draw.polygon(screen, (189, 178, 0), ((165, 430), (320, 275), (475, 430)))

    
            
    
    
        
    
    pygame.display.flip()
    delta_time = clock.tick(60)
    
    delta_time = max(0.01, min(0.1, delta_time))

pygame.quit()