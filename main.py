import pygame

pygame.init()

screen = pygame.display.set_mode((640, 640))

running = True
clock = pygame.time.Clock()
x = 0

delta_time = 0.1

while running:
    screen.fill((255, 255, 255))
    x += 50 * delta_time
    if x >640:
        x = 0

    pygame.draw.rect(screen, "black", (5+x, 5, 10, 10))
    pygame.draw.rect(screen, "black", (150, 100, 340, 340))
    pygame.draw.polygon(screen, "white", ((165, 110), (320, 265), (475, 110)))
    pygame.draw.polygon(screen, "white", ((160, 115), (315, 270), (160, 425)))
    pygame.draw.polygon(screen, "white", ((480, 115), (325, 270), (480, 425)))
    pygame.draw.polygon(screen, "white", ((165, 430), (320, 275), (475, 430)))

    pygame.draw.polygon(screen, "green", ((165, 110), (320, 265), (475, 110)))
    pygame.draw.polygon(screen, "red", ((160, 115), (315, 270), (160, 425)))
    pygame.draw.polygon(screen, "blue", ((480, 115), (325, 270), (480, 425)))
    pygame.draw.polygon(screen, "yellow", ((165, 430), (320, 275), (475, 430)))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    pygame.display.update()
    delta_time = clock.tick(60)
    delta_time = max(0.01, min(0.1, delta_time))

pygame.quit()