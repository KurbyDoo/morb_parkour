from random import randint
import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk = []
        for i in range(4):
            self.player_walk.append(pygame.transform.rotozoom(pygame.image.load(f'graphics/player/frame_{i}.png').convert_alpha(), 0, 0.1))
        # player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        # player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        # self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.transform.rotozoom(pygame.image.load('graphics/player/frame_1.png').convert_alpha(), 0, 0.1)

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump_effect.wav')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -14

        if keys[pygame.K_LEFT] and self.rect.left:
            self.rect.x -= 7

        if keys[pygame.K_RIGHT] and self.rect.right:
            self.rect.x += 4

        if sum(keys) == 0:
            self.rect.x -= 3
            self.walking = False
        
        else:
            self.walking = True

    def update_gravity(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update_frames(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump

        elif self.walking:
            self.player_index += 0.1
            self.image = self.player_walk[int(self.player_index % 4)]

        else:
            self.image = self.player_walk[0]

    def update(self):
        self.player_input()
        self.update_gravity()
        self.update_frames()

    def reset(self):
        self.rect.bottom = 300
        self.rect.midbottom = (100, 300)
        self.gravity = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.type = type
        if self.type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/morb1.png').convert_alpha()
            fly_1 = pygame.transform.rotozoom(fly_1, 2, 0.15)
            fly_2 = pygame.image.load('graphics/fly/morb2.png').convert_alpha()
            fly_2 = pygame.transform.rotozoom(fly_2, -2, fly_1.get_width()/fly_2.get_width())
            self.frames = [fly_1, fly_2]
            self.y_pos = 170

        elif self.type == 'snail':
            snail_1 = pygame.transform.scale(pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('graphics/snail/daroll1.png').convert_alpha(), True, False), 0, 0.1), (pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('graphics/snail/daroll1.png').convert_alpha(), True, False), 0, 0.1).get_width() * 1.5, pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('graphics/snail/daroll1.png').convert_alpha(), True, False), 0, 0.1).get_height())) # .convert_alpha() removes clear textures
            snail_2 = pygame.transform.rotozoom(pygame.transform.flip(pygame.image.load('graphics/snail/daroll2.png').convert_alpha(), True, False), 0, 0.1)
            self.frames = [snail_1, snail_2]
            self.y_pos = 300
        

        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), self.y_pos))

    def update_frames(self):
        if self.type == 'fly':
            self.animation_index += 0.15
            self.image = self.frames[int(self.animation_index % 2)]

        elif self.type == 'snail':
            self.animation_index += 0.1
            self.image = self.frames[int(self.animation_index % 2)]

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.update_frames()
        self.rect.x -= 5

def display_score(text, fill = (200, 200, 200)):
    score_surface = test_font.render(text, False, fill)
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)

def collision():
    # return True
    global start_time
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False) or player.sprite.rect.right < 0 or player.sprite.rect.left > screen.get_width():
        obstacle_group.empty()
        player.sprite.reset()
        sky_rect_1.left = 0
        sky_rect_2.left = sky_rect_1.right
        ground_rect_1.left = 0
        ground_rect_2.left = ground_rect_1.right
        pygame.mixer.stop()
        death_effect.play()
        start_time = pygame.time.get_ticks()//1000
        return False
    
    return True

def updateBackground():
    sky_rect_1.x -= 1
    sky_rect_2.x -= 1

    if sky_rect_1.right < 0:
        sky_rect_1.left = sky_rect_2.right

    if sky_rect_2.right < 0:
        sky_rect_2.left = sky_rect_1.right
        
    ground_rect_1.x -= 3
    ground_rect_2.x -= 3

    if ground_rect_1.right < 0:
        ground_rect_1.left = ground_rect_2.right

    if ground_rect_2.right < 0:
        ground_rect_2.left = ground_rect_1.right

# nessesary to start pygame / starting the engine of the car
pygame.init()

screen = pygame.display.set_mode((800, 400)) # initialise screen, a tuple parameter is required for width and height (width, height)
pygame.display.set_caption('Pygame Window :)') # set the title of the game window, string as input
clock = pygame.time.Clock() # internal clock of the game
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # takes font type (file or None) and font size (int)
game_active = False
start_time = 0
score = 0
background_music = pygame.mixer.Sound('audio/background_music.wav')
background_music.set_volume(0.1)
background_music.play(loops=True)

death_effect = pygame.mixer.Sound('audio/death_sound_effect.wav')
death_effect.set_volume(0.2)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert() # .convert() converts png to images pygame can work with
new_sky_surface = pygame.transform.scale(pygame.image.load('graphics/new_sky.png').convert_alpha(), (800, 350))
sky_rect_1 = sky_surface.get_rect(topleft = (0, 0))
sky_rect_2 = sky_surface.get_rect(topleft = (sky_surface.get_width(), 0))

ground_surface = pygame.image.load('graphics/ground.png').convert()
new_ground_surface = pygame.transform.scale(pygame.image.load('graphics/new_ground.png').convert_alpha(), (800, 250))
ground_rect_1 = ground_surface.get_rect(topleft = (0, sky_surface.get_height() - 150))
ground_rect_2 = ground_surface.get_rect(topleft = (ground_surface.get_width(), sky_surface.get_height() - 150))


player_stand = pygame.image.load('graphics/player/endImage.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 0.5) 
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render("Press Space To Start",False, (211, 255, 255))
game_name_rect = game_name.get_rect(center = (400, 340))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)


while True: # game loop
    for event in pygame.event.get(): # loop through pygame events
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
                
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 4) == 3:
                    # obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100), 300)))
                    obstacle_group.add(Obstacle('fly'))
                else:
                    # obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100), 210)))
                    obstacle_group.add(Obstacle('snail'))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.stop()
                background_music.play()
                game_active = True
                start_time = pygame.time.get_ticks()//1000
                

    if game_active:
        # draw elements
        screen.blit(new_sky_surface, sky_rect_1) # surface to place, tuple with x and y
        screen.blit(new_sky_surface, sky_rect_2) # surface to place, tuple with x and y
        screen.blit(new_ground_surface, ground_rect_1) # surface to place, tuple with x and y
        screen.blit(new_ground_surface, ground_rect_2) # surface to place, tuple with x and y

        updateBackground()


        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        score = pygame.time.get_ticks()//1000 - start_time
        display_score(f'Score: {score}')

        game_active = collision()

    else:
        screen.fill((0, 0, 0))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        if start_time == 0:
            display_score('ESCAPE MORB', fill = (211, 255, 255))

        else:
            display_score(f'Get Morbed. Your Score: {score}', fill = (211, 255, 255))

    
    pygame.display.update() # add things to display surface
    clock.tick(60) # game will run at 60fps

