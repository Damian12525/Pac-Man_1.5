import random
import pygame
from PIL import Image
import os
import math
import time
import Board

from settings import *
from characters import *
from gameState import *










pygame.init()




pygame.mixer.init()







for i in range(ghost_number):
    rnd = int(random.randrange(len(currentMap.nodeList)))
    ghosts.append(Ghost(rnd))









for i in range(225, 0, -10):
    gameDisplay.blit(start_screen, (0, 0))
    black_screen.set_alpha(i)
    gameDisplay.blit(black_screen, (0, 0))
    pygame.display.update()

pygame.mixer.music.load('./assets/sound/thunder2.mp3')
pygame.mixer.music.play(0)
pygame.time.delay(1100)


for i in range(0, 255, 50):
    gameDisplay.blit(start_screen, (0, 0))
    white_screen.set_alpha(i)
    gameDisplay.blit(white_screen, (0, 0))
    pygame.display.update()


i = 0
increment = 10

while not start and not want_to_exit:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 13:
                start = True
        if event.type == pygame.QUIT:
            want_to_exit = True

    gameDisplay.blit(start_screen, (0, 0))
    gameDisplay.blit(logo,(220,0))
    press_prompt.set_alpha(i)
    gameDisplay.blit(press_prompt,(450,450))
    pygame.display.update()
    i += increment
    if(i == 0 or i == 150):
        increment *= -1

if want_to_exit:
    exit()

background = pygame.image.load("./tmp/map.png")




pygame.mixer.music.load('./assets/sound/rampage1.mp3')
pygame.mixer.music.play(-1)

font = pygame.font.SysFont("Fipps", 30)

while not dead and not want_to_exit and not won:






    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # przerywamy petle
            want_to_exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.control(0, -1)
            if event.key == pygame.K_DOWN:
                player.control(0, 1)
            if event.key == pygame.K_LEFT:
                player.control(-1, 0)
            if event.key == pygame.K_RIGHT:
                player.control(1, 0)

        # print(event)
    player.update()
    player.eat()
    dead = player.contact()
    won = player.check_if_won()


    gameDisplay.blit(background, (0,0))
    drawPoints()
    player.show()
    text = font.render(str(player.score), True, (255, 255, 0))
    gameDisplay.blit(text,(1220,100))
    gameDisplay.blit(logo2,(560,0))



    for i in range(len(ghosts)):
        ghosts[i].update()
        ghosts[i].show()

    pygame.display.update()

    clock.tick(30)

if won:
    print("Gratulacje")

if dead:
    print("RIP")

exit()
