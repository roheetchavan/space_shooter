import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('-:: Space Shooter ::-')

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))

# Laser
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

# background
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

# colour
WHITE = (255,255,255)


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_timer = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
       # pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50))
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = {
        'red'   : (RED_SPACE_SHIP, RED_LASER),
        'blue'  : (BLUE_SPACE_SHIP, BLUE_LASER),
        'green' : (GREEN_SPACE_SHIP, GREEN_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity


def main():
    run = True
    FPS = 60
    level = 1
    lives = 1
    main_font = pygame.font.SysFont('comicsans', 30)
    lost_font = pygame.font.SysFont('comicsans', 30)
    enemies = []
    wave_length = 5
    enemy_velocity = 1

    player_speed = 5
    player = Player(400,400)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))

        # draw text
        level_label = main_font.render(f"Level : {level}", 1, WHITE)
        lives_label = main_font.render(f"Lives : {lives}", 1, WHITE)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, ((WIDTH - level_label.get_width() - 10), 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)
            
        if lost:
            lost_lable = lost_font.render("You Lost !!!", 1, WHITE)
            WIN.blit(lost_lable, (WIDTH/2 - lost_lable.get_width()/2, 250))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(['red', 'blue','green']))
                enemies.append(enemy)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_speed > 0: #left
            player.x -= player_speed
        if keys[pygame.K_d] and player.x + player_speed + player.get_width() < WIDTH: #right
            player.x += player_speed
        if keys[pygame.K_w] and player.y - player_speed > 0: #up
            player.y -= player_speed
        if keys[pygame.K_s] and player.y + player_speed + player.get_height() < HEIGHT: #down
            player.y += player_speed

        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

       

main()