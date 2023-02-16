import pygame

pygame.init()
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Runner')  # window name
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)

# background
sky_surf = pygame.image.load(
    'graphics/Sky.png').convert()  # convert it to better format for pygame, for better performance
ground_surf = pygame.image.load('graphics/ground.png').convert()

# snail
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # convert it without background
snail_x_pos = screen_width
snail_y_pos = sky_surf.get_height()
snail_rect = snail_surf.get_rect(midbottom=(snail_x_pos, snail_y_pos))

# player
player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_x_pos = 100
player_y_pos = sky_surf.get_height()  # on the ground
player_rect = player_surf.get_rect(
    midbottom=(player_x_pos, player_y_pos))  # now positioning rectangle from midbottom point

# score
score = 0
score_str = 'Score: ' + str(score)
score_surf = font.render(score_str, False, 'White')
score_rect = score_surf.get_rect(center=(screen_width / 2, screen_height / 2))

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw background
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, sky_surf.get_height()))

    # draw objects
    screen.blit(snail_surf, snail_rect)
    screen.blit(player_surf, player_rect)
    screen.blit(score_surf, score_rect)

    player_rect.left += 1

    snail_rect.left -= 3
    if snail_rect.right <= 0: snail_rect.left = screen_width

    if player_rect.colliderect(snail_rect):
        score += 1
        score_str = 'Score: ' + str(score)
        score_surf = font.render(score_str, False, 'White')
        score_rect = score_surf.get_rect(center=(screen_width / 2, screen_height / 2))

    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint((mouse_pos)) and pygame.mouse.get_pressed()[0]:  # mouse touched the player and pressed
        print('Touch')

    pygame.display.update()
    clock.tick(60)  # limit the loop to 60 times per sec
