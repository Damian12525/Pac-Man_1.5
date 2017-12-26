from characters import *
from gameState import *
import pygame


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

while lives > 0 and not want_to_exit and not won:

    currentMap.spawn_rampage_pill()



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

            if event.key == pygame.K_ESCAPE:
                resume = False
                black_screen.set_alpha(200)
                while not resume:

                    gameDisplay.blit(background, (0, 0))
                    drawPoints()
                    draw_rampage_pills()
                    player.show()
                    for i in range(len(ghosts)):
                        ghosts[i].show()
                    text = font.render(str(player.score), True, (255, 255, 0))
                    gameDisplay.blit(text, (1200, -10))
                    draw_hearts(lives)

                    gameDisplay.blit(black_screen, (0, 0))
                    gameDisplay.blit(logo, (220, 0))
                    resume_prompt.set_alpha(i)
                    gameDisplay.blit(resume_prompt, (400, 750))

                    pygame.display.update()
                    i += increment
                    if (i == 0 or i == 150):
                        increment *= -1






                    for x in pygame.event.get():
                        if x.type == pygame.QUIT:
                            # przerywamy petle
                            want_to_exit = True
                            resume = True


                        if x.type == pygame.KEYDOWN:
                            if x.key == pygame.K_ESCAPE:
                                resume = True


        # print(event)
    player.update()
    player.eat()
    player.eat_rampage_pill()
    rampage_mode = player.check_if_rampage()
    lives += player.contact(rampage_mode)
    won = player.check_if_won()






    gameDisplay.blit(background, (0,0))
    drawPoints()
    draw_rampage_pills()
    player.show()
    text = font.render(str(player.score), True, (255, 255, 0))
    gameDisplay.blit(text,(1200,-10))
    gameDisplay.blit(logo2,(560,-10))
    draw_hearts(lives)



    for i in range(len(ghosts)):
        ghosts[i].update()
        ghosts[i].show()

    pygame.display.update()

    clock.tick(30)

if won:
    print("Gratulacje")




exit()
