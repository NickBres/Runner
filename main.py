import pygame
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        self.player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [self.player_walk1, self.player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

        self.x = x
        self.y = y
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.y:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > self.y:
            self.rect.bottom = self.y

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def animation_state(self):
        if self.rect.bottom < self.x:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        if type == 'Fly':
            fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            self.y = y - 85
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            self.y = y

        self.animation_index = 0
        self.x = x
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    curr_time = pygame.time.get_ticks()  # returns time since pygame init
    score = (curr_time - start_time) // 1000
    score_str = 'Score: ' + str(score)
    score_surf = font.render(score_str, False, text_color)
    score_rect = score_surf.get_rect(center=(screen_width / 2, screen_height / 6))
    screen.blit(score_surf, score_rect)
    return score


def collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        return True
    return False



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
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

# background
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player(100, sky_surf.get_height()))

obstacle_group = pygame.sprite.Group()

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

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()
                    obstacle_group.empty()
        else:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['Fly', 'Snail', 'Snail', 'Snail']), randint(900, 1100), sky_surf.get_height()))

    # draw background
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, sky_surf.get_height()))

    if game_active:
        best = display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        if collisions():
            game_active = False
            logo = 'Score: ' + str(best)
            logo_surf = font.render(logo, False, (111, 196, 169))
            logo_rect = logo_surf.get_rect(center=(screen_width / 2, 80))
    else:
        screen.fill((94, 129, 162))
        screen.blit(stand_surf, stand_rect)
        screen.blit(instr_surf, instr_rect)
        screen.blit(logo_surf, logo_rect)

    pygame.display.update()
    clock.tick(60)  # limit the loop to 60 times per sec
