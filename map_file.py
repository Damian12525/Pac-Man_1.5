from characters import *
from settings import *


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


            gameDisplay.blit(tunel, positionToDraw(currentMap.nodeList[i].x - 0.5 , currentMap.nodeList[i].y - 0.5))

