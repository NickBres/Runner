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
sky_surface = pygame.image.load(
    'graphics/Sky.png').convert()  # convert it to better format for pygame, for better performance
ground_surface = pygame.image.load('graphics/ground.png').convert()
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # convert it without background
player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# snail
snail_x_pos = screen_width
snail_y_pos = sky_surface.get_height()
snail_rect = snail_surface.get_rect(midbottom=(snail_x_pos, snail_y_pos))

# player
player_x_pos = 100
player_y_pos = sky_surface.get_height()  # on the ground
player_rect = player_surface.get_rect(
    midbottom=(player_x_pos, player_y_pos))  # now positioning rectangle from midbottom point

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
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)

    player_rect.left += 1

    snail_rect.left -= 3
    if snail_rect.right <= 0: snail_rect.left = screen_width

    if player_rect.colliderect(snail_rect):
        print('Collision')

    pygame.display.update()
    clock.tick(60)  # limit the loop to 60 times per sec
