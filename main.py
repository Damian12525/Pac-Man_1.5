from characters import *
from gameState import *
import pygame


def draw_tunnels(currentMap):
    for i in range(len(currentMap.nodeList)):
        if currentMap.nodeList[i].linkedTunelID != -1:
            if currentMap.nodeList[i].type == 1:
                tunel = tunel1
            if currentMap.nodeList[i].type == 2:
                tunel = tunel2
            if currentMap.nodeList[i].type == 4:
                tunel = tunel4
            if currentMap.nodeList[i].type == 8:
                tunel = tunel8

            gameDisplay.blit(tunel, positionToDraw(currentMap.nodeList[i].x - 0.5, currentMap.nodeList[i].y - 0.5))

def change_mode(last_change, scatter_mode):
    if pygame.time.get_ticks()-last_change > 10000:
        return pygame.time.get_ticks(), not scatter_mode
    else:
        return last_change, scatter_mode



pygame.init()
pygame.mixer.init()

for i in range(225, 0, -10):
    gameDisplay.blit(start_screen, (0, 0))
    black_screen.set_alpha(i)
    gameDisplay.blit(black_screen, (0, 0))
    pygame.display.update()

pygame.mixer.music.load('./assets/sound/thunder2.mp3')
pygame.mixer.music.play(-1)
pygame.time.delay(1100)

for i in range(0, 255, 50):
    gameDisplay.blit(start_screen, (0, 0))
    white_screen.set_alpha(i)
    gameDisplay.blit(white_screen, (0, 0))
    pygame.display.update()

i = 0
increment = 10
start = False
want_to_exit = False

selection = 0

while (not start or selection != 0) and not want_to_exit:
    while not start and not want_to_exit:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    start = True

                if event.key == pygame.K_UP:
                    selection = (selection + 1) % 2

                if event.key == pygame.K_DOWN:
                    selection = (selection - 1) % 2


            if event.type == pygame.QUIT:
                want_to_exit = True

        gameDisplay.blit(start_screen, (0, 0))
        gameDisplay.blit(logo, (220, 0))


        if selection == 0:

            press_prompt.set_alpha(i)
            gameDisplay.blit(press_prompt, (450, 450))

            about.set_alpha(255)
            gameDisplay.blit(about,(450,550))



        if selection == 1:

            press_prompt.set_alpha(255)
            gameDisplay.blit(press_prompt, (450, 450))
            about.set_alpha(i)
            gameDisplay.blit(about,(450,550))






        pygame.display.update()

        i += increment
        if i == 0 or i == 150:
            increment *= -1

    if selection == 1:
        back = False
        black_screen.set_alpha(100)
        while not want_to_exit and not back:


            gameDisplay.blit(start_screen,(0,0))
            gameDisplay.blit(black_screen, (0,0))


            gameDisplay.blit(about_screen, (0,0))


            pygame.display.update()




            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 13:

                        back = True
                        start = False

                if event.type == pygame.QUIT:
                    want_to_exit = True




if want_to_exit:
    exit()

# background = pygame.image.load("./tmp/map.png")


pygame.mixer.music.load('./assets/sound/rampage1.mp3')
pygame.mixer.music.play(-1)

font = pygame.font.SysFont("Fipps", 30)

while lives > 0 and not want_to_exit:

    currentMap = createMap(level)
    background = pygame.image.load("./tmp/map.png")
    player = Pacman(currentMap, currentMap.start_node)

    for i in range(ghost_number):
        rnd = int(random.randrange(len(currentMap.nodeList)))
        ghosts.append(Ghost(currentMap, rnd))

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
                if event.key == pygame.K_CAPSLOCK:
                    player.score += 1000
                    Pacman.total_score += 1000


                if event.key == pygame.K_ESCAPE:
                    resume = False
                    black_screen.set_alpha(200)
                    i = 10
                    while not resume:

                        gameDisplay.blit(background, (0, 0))
                        drawPoints(currentMap)
                        draw_rampage_pills(currentMap)
                        player.show()

                        for x in range(len(ghosts)):
                            ghosts[x].show()
                        text = font.render(str(Pacman.total_score), True, (255, 255, 0))
                        gameDisplay.blit(text, (1200, -10))
                        draw_hearts(lives)

                        gameDisplay.blit(black_screen, (0, 0))
                        gameDisplay.blit(logo, (220, 0))
                        resume_prompt.set_alpha(i)
                        gameDisplay.blit(resume_prompt, (400, 750))

                        pygame.display.update()
                        i += increment
                        if i == 0 or i == 150:
                            increment *= -1

                        for x in pygame.event.get():
                            if x.type == pygame.QUIT:
                                # przerywamy petle
                                want_to_exit = True
                                resume = True

                            if x.type == pygame.KEYDOWN:
                                if x.key == pygame.K_ESCAPE:
                                    resume = True


        player.update(currentMap)
        player.eat(currentMap)
        player.eat_rampage_pill(currentMap)
        rampage_mode = player.check_if_rampage()
        lives += player.contact(rampage_mode, currentMap, ghosts)
        won = player.check_if_won(currentMap)
        last_change, scatter_mode = change_mode(last_change, scatter_mode)

        gameDisplay.blit(background, (0, 0))
        drawPoints(currentMap)
        draw_rampage_pills(currentMap)
        player.show()
        text = font.render(str(Pacman.total_score), True, (255, 255, 0))
        gameDisplay.blit(text, (1200, -10))
        gameDisplay.blit(logo2, (560, -10))
        draw_hearts(lives)


        for i in range(len(ghosts)):
            ghosts[i].update(currentMap, player, rampage_mode, scatter_mode)
            ghosts[i].show()

        draw_tunnels(currentMap)



        if rampage_mode:
            rs_alpha = constrain(rs_alpha, 0, 150)
            rs_alpha += rs_increment
            if rs_alpha == 0 or rs_alpha == 150:
                rs_increment *= -1

            red_screen.set_alpha(rs_alpha)
            gameDisplay.blit(red_screen,(0,0))


        else:
            rs_increment = 10
            rs_alpha = 10


        pygame.display.update()

        clock.tick(30)

    if won:
        level = 1 + level % 2
        won = False
        ghosts = []

    if lives == 0:
        gameDisplay.blit(start_screen, (0, 0))
        gameDisplay.blit(logo, (220, 0))
        gameDisplay.blit(game_over, (480,500))
        text = font.render("Score: " + str(Pacman.total_score), True, (255, 255, 0))
        gameDisplay.blit(text, (530, 600))

        pygame.display.update()
        pygame.time.delay(3000)


exit()
