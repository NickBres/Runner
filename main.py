import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')  # window name
clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))  # simple surface
test_surface.fill('Red')

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface, (200, 100))  # puts the surface on the screen

    pygame.display.update()
    clock.tick(60)  # limit the loop to 60 times per sec
