# importing libraries
import pygame
import time
import random

import pygame.constants

pygame.mixer.init()

snake_speed = 15

# Initialising pygame
pygame.init()

# Window size
width, height = 600, 500

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(245, 245, 67)
sky = pygame.Color(42, 248, 219)

# Initialise game window
pygame.display.set_caption('Snakes Game')
game_window = pygame.display.set_mode((width, height))
font = pygame.font.SysFont("Arial", 70)

# background screen
background = pygame.image.load('snakeimage/img.png')
background = pygame.transform.scale(background, (600, 500))

# FPS (frames per second) controller
FPS = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake
# body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]
# target position
target_position = [random.randrange(1, (width // 10)) * 10,
                   random.randrange(1, (height // 10)) * 10]
target_spawn = True

# setting default snake direction
# towards right
direction = 'RIGHT'
game_finish = direction

# initial score
score = 0


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_g:
                    pygame.quit()
                    quit()


def message_screen():
    message_screen = font.render("press", True, white)
    game_window.blit(message_screen, (width / 6, height / 6))


def show_text():
    text = font.render('Game Over', True, white)
    game_window.blit(text, (width / 6, height / 6))


with open('high_score.txt.', 'r') as f:
    high_score = f.read()

try:
    highestScore = int(high_score)
except:
    highestScore = 0


# displaying Score function
def show_score(choice, color, font, size, highestScore):
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # displaying text

    if (highestScore < score):
        highestScore = score
    with open('high_score.txt', 'w') as f:
        f.write(str(highestScore))
    # score_surface
    score_surface = score_font.render(
        'Score : ' + str(score) + "    highestScore: " + str(
            highestScore) + "                                   pause = p and play = c  ", True, red)

    # checking highestScore
    # create a rectangular object for the
    # text surface object
    score_rect = score_surface.get_rect()

    game_window.blit(score_surface, score_rect)


# background music
pygame.mixer.music.load('snakeimage/Ayanokoji [AMV] - Sociopath.mp3')
pygame.mixer.music.play()


def game_over():
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render("Your Score is : " + str(score), True, white)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (width / 2, height / 3)

    # Background music
    pygame.mixer.music.load('snakeimage/1_snake_game_resources_crash.mp3')
    pygame.mixer.music.play()

    # blit wil draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)

    show_text()

    pygame.display.flip()

    # after 1 seconds we will quit the
    # program
    time.sleep(2)

    # deactivating pygame library

    pygame.quit()

    # quit the program
    quit()

    # game over function

    # Main Function


while True:

    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_finish = 'UP'
            if event.key == pygame.K_DOWN:
                game_finish = 'DOWN'
            if event.key == pygame.K_LEFT:
                game_finish = 'LEFT'
            if event.key == pygame.K_RIGHT:
                game_finish = 'RIGHT'
            if event.key == pygame.K_p:
                pause()

    # If two keys pressed simultaneously
    # we don't want snake to move into two directionsgit@github.com:Suraj246/SnakeGame.git
    # simultaneously
    if game_finish == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if game_finish == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if game_finish == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if game_finish == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism
    # if target and snakes collide then scores will be
    # incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == target_position[0] and snake_position[1] == target_position[1]:
        score += 10
        target_spawn = False
    else:
        snake_body.pop()

    if not target_spawn:
        target_position = [random.randrange(1, (width // 10)) * 10,
                           random.randrange(1, (height // 10)) * 10]

    target_spawn = True

    game_window.blit(background, (0, 0))
    pygame.display.update()

    for pos in snake_body:
        pygame.draw.rect(game_window, yellow, pygame.Rect(
            pos[0], pos[1], 10, 10))

    pygame.draw.rect(game_window, sky, pygame.Rect(
        target_position[0], target_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > width - 10:
        game_over()

    if snake_position[1] < 0 or snake_position[1] > height - 10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score continuously
    show_score(1, white, 'times new roman', 20, highestScore)

    # Refresh game screen
    pygame.display.update()

    FPS.tick(snake_speed)
