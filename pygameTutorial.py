from random import randint
import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -8

    def update_gravity(self):
        self.gravity += 0.3
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update_frames(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            self.image = self.player_walk[int(self.player_index % 2)]

    def update(self):
        self.player_input()
        self.update_gravity()
        self.update_frames()

    def reset(self):
        self.rect.bottom = 300
        self.gravity = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.type = type
        if self.type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            self.y_pos = 210

        elif self.type == 'snail':
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # .convert_alpha() removes clear textures
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            self.y_pos = 300
        

        self.animation_index = 0
        self.image = self.frames[self.animation_index]

        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), self.y_pos))

    def update_frames(self):
        if self.type == 'fly':
            self.animation_index += 0.4
            self.image = self.frames[int(self.animation_index % 2)]

        elif self.type == 'snail':
            self.animation_index += 0.3
            self.image = self.frames[int(self.animation_index % 2)]

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.update_frames()
        self.rect.x -= 5

def display_score(text, fill = (64, 64, 64)):
    score_surface = test_font.render(text, False, fill)
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)

def collision():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        player.sprite.reset()
        return False
    
    return True


# def obstacle_movement(obstacle_list):
#     global game_active
#     if obstacle_list:
#         for obstacle_rect in obstacle_list:
#             obstacle_rect.x -= 5

#             screen.blit(snail_surface if obstacle_rect.bottom == 300 else fly_surface, obstacle_rect)

#             if player_rect.colliderect(obstacle_rect): # check collide with rect
#                 game_active = False
#                 obstacle_list = []

#         obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.right > 0]
#         return obstacle_list
#     return []

# def player_animation():
#     global player_surface
#     global player_index
#     if player_rect.bottom >= 300:
#         player_index += 0.1
#         player_surface = player_walk[int(player_index%2)]

#     else: player_surface = player_jump


# nessesary to start pygame / starting the engine of the car
pygame.init()

screen = pygame.display.set_mode((800, 400)) # initialise screen, a tuple parameter is required for width and height (width, height)
pygame.display.set_caption('Pygame Window :)') # set the title of the game window, string as input
clock = pygame.time.Clock() # internal clock of the game
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # takes font type (file or None) and font size (int)
game_active = False
start_time = 0
score = 0
background_music = pygame.mixer.Sound('audio/music.wav')
background_music.set_volume(0.1)
background_music.play(loops=True)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert() # .convert() converts png to images pygame can work with
sky_rect = sky_surface.get_rect(topleft = (0, 0))

ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(topleft = (0, sky_rect.bottom))

# score_surface = test_font.render('My Game', False, (64, 64, 64)) # takes text info (str), antialisasing (bool), colour (rgb or colour name)
# score_rect = score_surface.get_rect(center = (400, 50))

# Obstacles

# snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() # .convert_alpha() removes clear textures
# snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
# snail_frames = [snail_frame_1, snail_frame_2]
# snail_frame_index = 0
# snail_surface = snail_frames[snail_frame_index]

# snail_rect = snail_surface.get_rect(midbottom = (600, 300))

# fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
# fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
# fly_frames = [fly_frame_1, fly_frame_2]
# fly_frame_index = 0
# fly_surface = fly_frames[fly_frame_index]

# obstacle_rect_list = []

# player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
# player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
# player_walk = [player_walk_1, player_walk_2]
# player_index = 0
# player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

# player_surface = player_walk[player_index]
# # player_rect = pygame.Rect(left, top, width, height) Not common because need the rect of a pre-existing iamge
# player_rect = player_surface.get_rect(midbottom = (80, 300)) # gets rect from image
# player_gravity = 0 

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) 
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render("Press Space To Start",False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 340))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

# snail_animation_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(snail_animation_timer, 500)

# fly_animation_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer, 300)

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

            # if event.type == snail_animation_timer:
            #     snail_frame_index = (snail_frame_index + 1) % 2
            #     snail_surface = snail_frames[snail_frame_index]

            # if event.type == fly_animation_timer:
            #     fly_frame_index = (fly_frame_index + 1) % 2
            #     fly_surface = fly_frames[fly_frame_index]

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP and player_rect.bottom >= 300:
            #         player_gravity = -8

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # player_rect.midbottom = (80, 300)
                # player_gravity = 0
                start_time = pygame.time.get_ticks()//1000
                

    if game_active:
        # draw elements
        screen.blit(sky_surface, sky_rect) # surface to place, tuple with x and y
        screen.blit(ground_surface, ground_rect) # surface to place, tuple with x and y

        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surface,score_rect)
        score = pygame.time.get_ticks()//1000 - start_time
        display_score(f'Score: {score}')

        # pygame.draw.line(screen, 'black', (0, 0), (screen.get_width(), screen.get_height()))
        # pygame.draw.ellipse(screen, 'brown', pygame.Rect(50, 200, 100, 100))

        # update snail
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = screen.get_width()

        # screen.blit(snail_surface, snail_rect)

        # Player
        # player_gravity += 0.3
        # player_rect.y += player_gravity

        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collision()

        # player_animation()
        # screen.blit(player_surface, player_rect)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        # screen.blit(game_message, game_message_rect)
        if start_time == 0:
            display_score('ESCAPE MORB', fill = (111, 196, 169))

        else:
            display_score(f'Get Morbed. Your Score: {score}', fill = (111, 196, 169))

    
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_space]:
    #     print('jump')


    ### MOUSE COLLISION
    # check for hover
    # if player_rect.collidepoint(mouse_pos): # check collide with tuple (x, y)
        # player_rect.x -= 1

    
    pygame.display.update() # add things to display surface
    clock.tick(60) # game will run at 60fps

