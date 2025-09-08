import pygame
import cv2
import mediapipe as mp
import os
import sys
import random
from pygame import mixer

# getting mediapipe ready
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils

# opening camera
cap = cv2.VideoCapture(0)

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 45
FPS = 90

# Colors
WHITE = (0, 0, 255)
BLUE = (0, 225, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Mario Game")

# Load Mario character images
mario_image = pygame.image.load("mario64.png")
mario_flipped_image = pygame.transform.flip(mario_image, True, False)

# Load enemy image
enemy_image = pygame.image.load("enemy.png")
enemy_flipped_image = pygame.transform.flip(enemy_image, True, False)

# Load bullet image
bullet_image = pygame.image.load("bullet.png")

# Load cloud image
cloud_image = pygame.image.load("cloud.png")

# Load sun image
sun_image = pygame.image.load("sun.png")

# Load tree image
tree_image = pygame.image.load("tree.png")

# Load coin image
coin_image = pygame.image.load("coin.png")

# Set up Mario's initial position and image
mario_rect = mario_image.get_rect()
mario_rect.topleft = (100, HEIGHT - GROUND_HEIGHT - mario_rect.height)
mario_direction = "right"

# Set up enemy variables
sky_enemies = []
max_sky_enemies = 5
sky_enemy_spawn_rate = 0.02
enemy_speed = 3.2

# Set up bullet variables
bullets = []
bullet_speed = 10

# Set up cloud variables
clouds = []
cloud_speed = 6

# Set up tree variables
trees = []
tree_speed = 4

# Set up coin variables
coins = []
max_coins = 5
coin_spawn_rate = 0.08

score = 0

# music for game
mixer.init()
music_files = ["mario_jump.mp3", "bullet.mp3", "coin.mp3", "mario dies.mp3", "power up.mp3", "play.mp3"]
pygame.mixer.music.set_volume(0.7)


pygame.mixer.music.load(music_files[-1])
pygame.mixer.music.play(-1)

# Set up the sun's position
sun_rect = sun_image.get_rect()
sun_rect.topleft = (50, 50)  # Adjust the position as needed

# Set up the clock to control the frame rate
clock = pygame.time.Clock()

# Set up Mario's movement variables
mario_speed = 10
jump_height = 6
is_jumping = False
jump_count = jump_height
gravity = 4.0


# Function to create a new cloud
def create_cloud():
    cloud_rect = cloud_image.get_rect()
    cloud_rect.topleft = (WIDTH, random.randint(50, 200))
    return cloud_rect


# Function to create a new tree
def create_tree():
    tree_rect = tree_image.get_rect()
    tree_rect.topleft = (WIDTH, HEIGHT - GROUND_HEIGHT - tree_rect.height)
    return tree_rect


# Function to create a new enemy in the sky
def create_sky_enemy():
    enemy_rect = enemy_image.get_rect()
    enemy_rect.topleft = (random.randint(0, WIDTH - enemy_rect.width), random.randint(0, HEIGHT // 2))
    return enemy_rect


# Function to create a new bullet
def create_bullet():
    bullet_rect = bullet_image.get_rect()
    if mario_direction == "right":
        bullet_rect.topleft = (mario_rect.right, mario_rect.centery - bullet_rect.height // 2)
    else:
        bullet_rect.topleft = (mario_rect.left - bullet_rect.width, mario_rect.centery - bullet_rect.height // 2)
    return bullet_rect


# Function to create a new coin
def create_coin():
    coin_rect = coin_image.get_rect()
    coin_rect.topleft = (random.randint(0, WIDTH - coin_rect.width), random.randint(0, HEIGHT - GROUND_HEIGHT - coin_rect.height))
    return coin_rect


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:

            bullets.append(create_bullet())

    # Remove sky enemies that go off-screen
    sky_enemies = [enemy for enemy in sky_enemies if 0 < enemy.x < WIDTH]

    # Move clouds and create new ones
    for cloud_rect in clouds:
        cloud_rect.x -= cloud_speed

    # Check if a new cloud should be created
    if not clouds or clouds[-1].right < WIDTH - random.randint(100, 300):
        clouds.append(create_cloud())

    # Move trees and create new ones
    for tree_rect in trees:
        tree_rect.x -= tree_speed

    # Check if a new tree should be created
    if not trees or trees[-1].right < WIDTH - random.randint(200, 400):
        trees.append(create_tree())

    # Update bullet logic
    for bullet in bullets:
        if mario_direction == "right":
            bullet.x += bullet_speed
        else:
            bullet.x -= bullet_speed

         
            # Check for collisions between bullets and enemies
            for bullet in bullets[:]:
                for enemy in sky_enemies[:]:
                    if bullet.colliderect(enemy):
                        score +=20
                        bullets.remove(bullet)
                        sky_enemies.remove(enemy)

                # Create new sky enemies
                if len(sky_enemies) < 5 and random.random() < 0.02:
                    sky_enemies.append(create_sky_enemy())

            # Check for collisions with Mario
            for enemy in sky_enemies:
                if mario_rect.colliderect(enemy):
                    print("Game Over! Enemy touched Mario.")
                    pygame.quit()
                    sys.exit()

    # Draw background
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    # Draw Mario
    if mario_direction == "right":
        screen.blit(mario_image, mario_rect)
    else:
        screen.blit(mario_flipped_image, mario_rect)

        # Draw sky enemies
    for enemy in sky_enemies:

        screen.blit(enemy_image, enemy)

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet_image, bullet)

    # Draw clouds
    for cloud_rect in clouds:
        screen.blit(cloud_image, cloud_rect)

    # Draw trees
    for tree_rect in trees:
        screen.blit(tree_image, tree_rect)

    # Spawn coins randomly
    if random.random() < coin_spawn_rate and len(coins) < 5:
        coins.append(create_coin())

    # Draw coins
    for coin_rect in coins:
        screen.blit(coin_image, coin_rect)

    # Check if Mario collects coins
    for coin_rect in coins[:]:
        if mario_rect.colliderect(coin_rect):
            score += 10
            coins.remove(coin_rect)

    font = pygame.font.Font(None, 36)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # Update game logic
    keys = pygame.key.get_pressed()

    # Handle jumping
    if not is_jumping:
        if keys[pygame.K_UP]:
            is_jumping = True
    else:
        if jump_count >= -jump_height:
            mario_rect.y -= (jump_count ** 2) * 0.5 * gravity
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = jump_height

    # Simulate gravity
    if mario_rect.y < HEIGHT - GROUND_HEIGHT - mario_rect.height:
        mario_rect.y += gravity

        # Update sky enemy logic
        if random.random() < sky_enemy_spawn_rate and len(sky_enemies) < max_sky_enemies:
            new_enemy = create_sky_enemy()
            sky_enemies.append(new_enemy)

        for enemy in sky_enemies:
            # Move sky enemies
            enemy.x += enemy_speed

            # Check for collisions with Mario
            if mario_rect.colliderect(enemy):
                print("The Score Obtained:", score)
                print("Game Over! Enemy touched Mario.")
                pygame.quit()
                sys.exit()

    # set up hand tracker
    success, img = cap.read()
    img1 = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img1.shape
                if id == 0:
                    x = []
                    y = []
                x.append(int((lm.x) * w))
                y.append(int((1 - lm.y) * h))

                # This will track the hand gestures
                if len(y) > 20:
                    if ((x[2] > x[4]) and (not (y[8] > y[6])) and (not (y[12] > y[10])) and (not (y[16] > y[14])) and (
                    not (y[20] > y[18]))) and mario_rect.left > 0:
                        mario_direction = "left"
                        mario_rect.x -= mario_speed

                    elif (not (x[2] > x[4]) and not (y[8] > y[6]) and not (y[12] > y[10]) and not (y[16] > y[14]) and (
                            y[20] > y[18])) and mario_rect.right < WIDTH:
                        mario_direction = "right"
                        mario_rect.x += mario_speed

                    elif (not (x[2] > x[4]) and (y[8] > y[6]) and not (y[12] > y[10]) and not (y[16] > y[14]) and (
                                y[20] > y[18])) and mario_rect.y > 0:
                            is_jumping = True
                            mario_rect.y -= gravity ** 2
                            jump_count -= 1

                    if ((x[2] > x[4]) and (y[8] > y[6]) and (y[12] > y[10]) and (y[16] > y[14]) and (y[20] > y[18])):
                        bullets.append(create_bullet())
                    
                    elif (not(x[2] > x[4]) and not(y[8] > y[6]) and not(y[12] > y[10]) and not(y[16] > y[14]) and not(y[20] > y[18])):
                        mario_rect.y += gravity ** 2

        mpdraw.draw_landmarks(img1, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("img", img1)
    cv2.waitKey(1)
    pygame.display.update()
