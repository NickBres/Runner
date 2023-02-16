import pygame

pygame.init()
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Runner')  # window name
clock = pygame.time.Clock()

# text creation
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
text_surface = test_font.render('My Game', False, 'White')

# image upload
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
snail_surface = pygame.image.load('graphics/snail/snail1.png')

# snail
snail_x_pos = screen_width
snail_y_pos = sky_surface.get_height() - snail_surface.get_height()  # on the ground

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw background
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, sky_surface.get_height()))

    # draw objects
    screen.blit(text_surface,
                (screen_width / 2 - text_surface.get_width() / 2,
                 screen_height / 2 - text_surface.get_height() / 2))  # in the middle of the screen
    screen.blit(snail_surface, (snail_x_pos, snail_y_pos))

    snail_x_pos -= 3
    if snail_x_pos <= -snail_surface.get_width(): snail_x_pos = screen_width


    pygame.display.update()
    clock.tick(60)  # limit the loop to 60 times per sec
