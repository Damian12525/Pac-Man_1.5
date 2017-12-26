import pygame
from PIL import Image
import math
import Board
import os

displayWidth = 1360
displayHeight = 960
ghost_number = 3

currentMap = Board.Map("./mapFiles/map6.txt")



pygame.init()
pygame.display.set_caption('Return of the PAC-ANT')


logo = pygame.image.load("./assets/img/logo2.png")
logo2 = pygame.image.load("./assets/img/logo4.png")

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Fipps", 40)
text = font.render("Press Enter", True, (255,255 , 0))
press_prompt = pygame.Surface((400,100))
press_prompt.blit(text,(0,0))

start_screen = pygame.image.load("./assets/img/start_screen2.png")
start_screen = pygame.transform.scale(start_screen, (displayWidth, displayHeight))

im = Image.new('RGB', (displayWidth, displayHeight), (0, 0, 0))
im.save("./assets/img/black_screen.png")
black_screen = pygame.image.load("./assets/img/black_screen.png")
black_screen.convert()

im = Image.new('RGB', (displayWidth, displayHeight), (255, 255, 255))
im.save("./assets/img/white_screen.png")
white_screen = pygame.image.load("./assets/img/white_screen.png")
white_screen.convert()

red = (255, 0, 0)



def exit():
    os.remove("./tmp/map.png")
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
    draw_x = int(x * Board.box_size - 0.5 * Board.box_size)
    draw_y = int(y * Board.box_size + 0.5 * Board.box_size)
    return (draw_x, draw_y)
def drawPoints():
    for i in range(len(currentMap.edgeList)):
        # currentMap.edgeList[i].pointList[j].pos

        if currentMap.edgeList[i].vertical == False:
            for j in range(len(currentMap.edgeList[i].pointList)):
                pygame.draw.circle(gameDisplay, red, positionToDraw(currentMap.edgeList[i].pointList[j].pos,
                                                                    currentMap.edgeList[i].node1y), 3)


        else:
            for j in range(len(currentMap.edgeList[i].pointList)):
                pygame.draw.circle(gameDisplay, red, positionToDraw(currentMap.edgeList[i].node1x,
                                                                    currentMap.edgeList[i].pointList[j].pos), 3)

    for i in range(len(currentMap.nodeList)):
        if currentMap.nodeList[i].pointSlot != -1:
            pygame.draw.circle(gameDisplay, red, positionToDraw(currentMap.nodeList[i].x, currentMap.nodeList[i].y), 5)
def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)


