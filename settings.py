import pygame
from PIL import Image
import math
import Board
import os
from characters import *
from gameState import *


displayWidth = 1360
displayHeight = 960
ghost_number = 3


rs_alpha = 0
rs_increment = 10



def createMap(_level):


    return Board.Map("./mapFiles/map" + str(_level) + ".txt")




pygame.init()
pygame.display.set_caption('Return of the PAC-ANT')


logo = pygame.image.load("./assets/img/logo2.png")
logo2 = pygame.image.load("./assets/img/logo4.png")

global gameDisplay
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Fipps", 40)
text = font.render("Star game", True, (255,255 , 0))
press_prompt = pygame.Surface((400,100))
press_prompt.blit(text,(0,0))

text = font.render("About me", True, (255,255 , 0))
about = pygame.Surface((400,100))
about.blit(text,(0,0))

text = font.render("New Highscore!!!", True, (255,255 , 0))
new_hs = pygame.Surface((600,100))
new_hs.blit(text,(0,0))



game_over = font.render("Game Over", True, (255,255 , 0))

font = pygame.font.SysFont("Fipps", 30)
text = font.render("Press Esc to resume", True, (255,255 , 0))

resume_prompt = pygame.Surface((600,100))
resume_prompt.blit(text,(0,0))
resume_prompt.convert()


start_screen = pygame.image.load("./assets/img/start_screen2.png")
start_screen = pygame.transform.scale(start_screen, (displayWidth, displayHeight))

im = Image.new('RGB', (displayWidth, displayHeight), (0, 0, 0))
im.save("./assets/img/black_screen.png")
black_screen = pygame.image.load("./assets/img/black_screen.png")
black_screen.convert()


im = Image.new('RGB', (displayWidth, displayHeight), (255, 0, 0))
im.save("./assets/img/red_screen.png")
red_screen = pygame.image.load("./assets/img/red_screen.png")
red_screen.convert()


im = Image.new('RGB', (displayWidth, displayHeight), (255, 255, 255))
im.save("./assets/img/white_screen.png")
white_screen = pygame.image.load("./assets/img/white_screen.png")
white_screen.convert()

ant1 = pygame.image.load("./assets/img/ant1.png")
ant1.convert()

ant2 = pygame.image.load("./assets/img/ant2.png")
ant2.convert()

about_screen = pygame.image.load("./assets/img/about_screen.png")

ladybug = pygame.image.load("./assets/img/ladybug.png")

tunel1 = pygame.image.load("./assets/map/tunnel_1.png")
tunel2 = pygame.image.load("./assets/map/tunnel_2.png")
tunel4 = pygame.image.load("./assets/map/tunnel_4.png")
tunel8 = pygame.image.load("./assets/map/tunnel_8.png")

red = (255, 0, 0)





def exit():
    #os.remove("./tmp/map.png")
    pygame.mixer.quit()
    pygame.quit()

    quit()
def constrain (value, min, max):
    if value < min:
        return float(min)
    elif value > max:
        return float(max)
    else:
        return value
def signum(x):
    return x / math.fabs(x)
def positionToDraw(x, y):
    draw_x = int(x * Board.box_size + 0.5 * Board.box_size)
    draw_y = int(y * Board.box_size + 0.5 * Board.box_size)
    return (draw_x, draw_y)
def drawPoints(currentMap):
    for i in range(len(currentMap.edgeList)):
        # currentMap.edgeList[i].pointList[j].pos

        if currentMap.edgeList[i].vertical == False:
            for j in range(len(currentMap.edgeList[i].pointList)):
                pygame.draw.circle(gameDisplay, (255,255,0), positionToDraw(currentMap.edgeList[i].pointList[j].pos,
                                                                    currentMap.edgeList[i].node1y), 3)


        else:
            for j in range(len(currentMap.edgeList[i].pointList)):
                pygame.draw.circle(gameDisplay, (255,255,0), positionToDraw(currentMap.edgeList[i].node1x,
                                                                    currentMap.edgeList[i].pointList[j].pos), 3)

    for i in range(len(currentMap.nodeList)):
        if currentMap.nodeList[i].pointSlot != -1:
            pygame.draw.circle(gameDisplay, (255,255,0), positionToDraw(currentMap.nodeList[i].x, currentMap.nodeList[i].y), 5)
def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def draw_rampage_pills(currentMap):
    for i in range(len(currentMap.rampage_pill)):
        pygame.draw.circle(gameDisplay, (255, 0, 0),positionToDraw(currentMap.nodeList[currentMap.rampage_pill[i]].x, currentMap.nodeList[currentMap.rampage_pill[i]].y), 6)


def draw_hearts(_lives):
    hearts = pygame.image.load("./assets/img/lives_" + str(_lives) + ".png")
    gameDisplay.blit(hearts, (0,0))

def spawn_ghosts(currentMap, ghost_number):
    for i in range(ghost_number):
        rnd = int(random.randrange(len(currentMap.nodeList)))
        ghosts.append(Ghost(currentMap, rnd))


def change_highscore(total_score):
    file = open("./mapFiles/highscore.txt", "r")

    line = file.read()
    file.close()
    if int(line) <= total_score:
        file = open("./mapFiles/highscore.txt", "w")
        file.write(str(total_score))
        file.close()
        return True
    else:
        return False





coin = pygame.mixer.Sound('./assets/sound/coin.wav')
coin.set_volume(0.5)


ant_death = pygame.mixer.Sound('./assets/sound/ant_death.wav')

bug_death = pygame.mixer.Sound('./assets/sound/bug_death.wav')