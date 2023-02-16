import pygame
from random import randint


def display_score():
    curr_time = pygame.time.get_ticks()  # returns time since pygame init
    score = (curr_time - start_time) // 1000
    score_str = 'Score: ' + str(score)
    score_surf = font.render(score_str, False, text_color)
    score_rect = score_surf.get_rect(center=(screen_width / 2, screen_height / 6))
    screen.blit(score_surf, score_rect)
    return score


def obstacle_movement(obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            obstacle_rect.x -= 5

            new_list = [obstacle for obstacle in obstacles if obstacle.x > -100]

            if obstacle_rect.bottom == sky_surf.get_height():
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        return new_list
    return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return True
    return False


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < sky_surf.get_height():  # jump
        player_surf = player_jump
    else:  # walk
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


game_active = False
pygame.init()
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Runner')  # window name
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
text_color = (64, 64, 64)
start_time = 0
best = 0

# background
sky_surf = pygame.image.load(
    'graphics/Sky.png').convert()  # convert it to better format for pygame, for better performance
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Obstacles
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacles = []

# Player
player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_x_pos = 100
player_y_pos = sky_surf.get_height()  # on the ground
player_rect = player_surf.get_rect(
    midbottom=(player_x_pos, player_y_pos))  # now positioning rectangle from midbottom point
player_gravity = 0

# Intro screen
stand_surf = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
stand_surf = pygame.transform.rotozoom(stand_surf, 0, 2)
stand_rect = stand_surf.get_rect(center=(screen_width / 2, screen_height / 2))
instr = 'Press SPACE to start...'
instr_surf = font.render(instr, False, (111, 196, 169))
instr_rect = instr_surf.get_rect(center=(screen_width / 2, screen_height - 80))
logo = 'RUNNER'
logo_surf = font.render(logo, False, (111, 196, 169))
logo_rect = logo_surf.get_rect(center=(screen_width / 2, 80))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
snail_anim_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_anim_timer, 500)
fly_anim_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_anim_timer, 200)

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == sky_surf.get_height():
                    player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == sky_surf.get_height():
                if player_rect.collidepoint(pygame.mouse.get_pos()):
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_rect.bottom = sky_surf.get_height()
                    game_active = True
                    start_time = pygame.time.get_ticks()
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacles.append(snail_surf.get_rect(midbottom=(randint(900, 1100), sky_surf.get_height())))
                else:
                    obstacles.append(
                        fly_surf.get_rect(midbottom=(randint(900, 1100), sky_surf.get_height() - player_surf.get_height())))
            if event.type == snail_anim_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_anim_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]


    # draw background
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, sky_surf.get_height()))

    if game_active:
        obstacles = obstacle_movement(obstacles)
        best = display_score()
        # player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom > sky_surf.get_height(): player_rect.bottom = sky_surf.get_height()
        player_animation()
        screen.blit(player_surf, player_rect)

        if collisions(player_rect, obstacles):
            game_active = False
            logo = 'Score: ' + str(best)
            logo_surf = font.render(logo, False, (111, 196, 169))
            logo_rect = logo_surf.get_rect(center=(screen_width / 2, 80))
            player_rect.bottom = sky_surf.get_height()
            player_gravity = 0
            obstacles.clear()
    else:
        screen.fill((94, 129, 162))
        screen.blit(stand_surf, stand_rect)
        screen.blit(instr_surf, instr_rect)
        screen.blit(logo_surf, logo_rect)

    pygame.display.update()
    clock.tick(60)  # limit the loop to 60 times per sec
