import random
import pygame
from PIL import Image

import Board
import os
import math
import time

red = (255,0,0)


random.seed(time.time())

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
    draw_x = int(x * Board.box_size - Board.box_size / 2 + background_x)
    draw_y = int(y * Board.box_size - Board.box_size / 2 + background_y)
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

class Ghost:

    def __init__(self,_currentNode, _type = 0):

        self.type = _type
        self.speed = 0.03
        self.target_dir_x = 0
        self.target_dir_y = 0

        self.x_vel = 0.0
        self.y_vel = 0.0
        self.currentNode = _currentNode
        self.currentEdge = 0
        self.x = float(currentMap.nodeList[_currentNode].x)
        self.y = float(currentMap.nodeList[_currentNode].y)
        self.target_dir = -1

    def show(self):
        pygame.draw.circle(gameDisplay, (0, 0, 255), positionToDraw(self.x, self.y), 13)


    def update(self):
        if self.currentNode != -1:
            # siedzimy na wezle

            if currentMap.nodeList[self.currentNode].linkedTunelID != -1:
                self.currentNode = currentMap.nodeList[self.currentNode].linkedTunelID
                self.x = currentMap.nodeList[self.currentNode].x
                self.y = currentMap.nodeList[self.currentNode].y

                if currentMap.nodeList[self.currentNode].right != -1:  # Go right
                    self.x_vel = float(self.speed)
                    self.y_vel = 0
                    self.currentEdge = currentMap.nodeList[self.currentNode].right
                    self.currentNode = -1

                elif currentMap.nodeList[self.currentNode].left != -1:  # Go left
                    self.x_vel = float(-1 * self.speed)
                    self.y_vel = 0
                    self.currentEdge = currentMap.nodeList[self.currentNode].left
                    self.currentNode = -1

                elif currentMap.nodeList[self.currentNode].down != -1:  # Go down
                    self.x_vel = 0
                    self.y_vel = self.speed
                    self.currentEdge = currentMap.nodeList[self.currentNode].down
                    self.currentNode = -1

                elif currentMap.nodeList[self.currentNode].up != -1:  # Go up
                    self.x_vel = 0
                    self.y_vel = -self.speed
                    self.currentEdge = currentMap.nodeList[self.currentNode].up
                    self.currentNode = -1

                self.target_dir_x = 0
                self.target_dir_y = 0
                self.x += self.x_vel
                self.y += self.y_vel
                return

            self.target_dir_x = player.x - self.x
            self.target_dir_y = player.y - self.y

            direction_list = []
            direction_list.append(-self.target_dir_y)
            direction_list.append(self.target_dir_x)
            direction_list.append(self.target_dir_y)
            direction_list.append(-self.target_dir_x)


            currentNode = currentMap.nodeList[self.currentNode]

            if currentNode.up == -1:
                direction_list[0] = -100
            if currentNode.right == -1:
                direction_list[1] = -100
            if currentNode.down == -1:
                direction_list[2] = -100
            if currentNode.left == -1:
                direction_list[3] = -100


            # zabronienie zawracania
            # if direction_list.count(-100) < 3:
            #     direction_list[(self.target_dir + 2) % 4] = -100

            self.target_dir = direction_list.index(max(direction_list))




            if self.target_dir == 0:
                self.target_dir_x = 0
                self.target_dir_y = -1
            elif self.target_dir == 1:
                self.target_dir_x = 1
                self.target_dir_y = 0
            elif self.target_dir == 2:
                self.target_dir_x = 0
                self.target_dir_y = 1
            elif self.target_dir == 3:
                self.target_dir_x = -1
                self.target_dir_y = 0









            if self.target_dir_x > 0 and currentMap.nodeList[self.currentNode].right != -1:  # Go right
                self.x_vel = self.speed
                self.y_vel = 0
                self.currentEdge = currentMap.nodeList[self.currentNode].right
                self.currentNode = -1

            elif self.target_dir_x < 0 and currentMap.nodeList[self.currentNode].left != -1:  # Go left
                self.x_vel = -self.speed
                self.y_vel = 0
                self.currentEdge = currentMap.nodeList[self.currentNode].left
                self.currentNode = -1

            elif self.target_dir_y > 0 and currentMap.nodeList[self.currentNode].down != -1:  # Go down
                self.x_vel = 0
                self.y_vel = self.speed
                self.currentEdge = currentMap.nodeList[self.currentNode].down
                self.currentNode = -1

            elif self.target_dir_y < 0 and currentMap.nodeList[self.currentNode].up != -1:  # Go up
                self.x_vel = 0
                self.y_vel = -self.speed
                self.currentEdge = currentMap.nodeList[self.currentNode].up
                self.currentNode = -1




        elif self.currentEdge != -1:

            self.x = round(self.x + self.x_vel, 5)
            self.y = round(self.y + self.y_vel, 5)
            self.x = float(constrain(self.x, currentMap.edgeList[self.currentEdge].minX,
                                     currentMap.edgeList[self.currentEdge].maxX))
            self.y = float(constrain(self.y, currentMap.edgeList[self.currentEdge].minY,
                                     currentMap.edgeList[self.currentEdge].maxY))

            if currentMap.edgeList[self.currentEdge].vertical and self.target_dir_y != 0:
                self.y_vel = self.target_dir_y * self.speed
            elif currentMap.edgeList[self.currentEdge].vertical == False and self.target_dir_x != 0:
                self.x_vel = self.target_dir_x * self.speed

            if self.atNode1():

                self.currentNode = currentMap.edgeList[self.currentEdge].nodeID_1
                self.currentEdge = -1
            elif self.atNode2():

                self.currentNode = currentMap.edgeList[self.currentEdge].nodeID_2
                self.currentEdge = -1

    def atNode1(self):  # if player reached node 1
        return currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_1].x == self.x and currentMap.nodeList[
            currentMap.edgeList[self.currentEdge].nodeID_1].y == self.y

    def atNode2(self):  # if plater reached node 2
        return currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_2].x == self.x and \
               currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_2].y == self.y


class Pacman:
    speed = 0.04
    score = -5

    def __init__(self, _currentNode):

        self.x_vel = 0.0
        self.y_vel = 0.0
        self.currentNode = _currentNode
        self.currentEdge = 0
        self.x = float(currentMap.nodeList[_currentNode].x)
        self.y = float(currentMap.nodeList[_currentNode].y)

        self.target_dir_x = 0
        self.target_dir_y = 0

    def show(self):

        pygame.draw.circle(gameDisplay, (255, 255, 0), positionToDraw(self.x, self.y), 12)

    def control(self, dirX, dirY):
        # gets x and y direction as a argument

        self.target_dir_x = dirX
        self.target_dir_y = dirY

    def update(self):

        if self.currentNode != -1:
            # siedzimy na wezle

            if currentMap.nodeList[self.currentNode].linkedTunelID != -1:
                self.currentNode = currentMap.nodeList[self.currentNode].linkedTunelID
                self.x = currentMap.nodeList[self.currentNode].x
                self.y = currentMap.nodeList[self.currentNode].y

                if currentMap.nodeList[self.currentNode].right != -1:  # Go right
                    self.x_vel = float(Pacman.speed)
                    self.y_vel = 0
                    self.currentEdge = currentMap.nodeList[self.currentNode].right
                    self.currentNode = -1

                elif currentMap.nodeList[self.currentNode].left != -1:  # Go left
                    self.x_vel = float(-1 * Pacman.speed)
                    self.y_vel = 0
                    self.currentEdge = currentMap.nodeList[self.currentNode].left
                    self.currentNode = -1

                elif currentMap.nodeList[self.currentNode].down != -1:  # Go down
                    self.x_vel = 0
                    self.y_vel = Pacman.speed
                    self.currentEdge = currentMap.nodeList[self.currentNode].down
                    self.currentNode = -1

                elif currentMap.nodeList[self.currentNode].up != -1:  # Go up
                    self.x_vel = 0
                    self.y_vel = -Pacman.speed
                    self.currentEdge = currentMap.nodeList[self.currentNode].up
                    self.currentNode = -1

                self.target_dir_x = 0
                self.target_dir_y = 0
                self.x += self.x_vel
                self.y += self.y_vel
                return

            if currentMap.nodeList[self.currentNode].pointSlot != -1:
                Pacman.score += currentMap.nodeList[self.currentNode].pointSlot.value
                currentMap.nodeList[self.currentNode].pointSlot = -1

            if self.target_dir_x > 0 and currentMap.nodeList[self.currentNode].right != -1:  # Go right
                self.x_vel = self.target_dir_x * Pacman.speed
                self.y_vel = 0
                self.currentEdge = currentMap.nodeList[self.currentNode].right
                self.currentNode = -1

            elif self.target_dir_x < 0 and currentMap.nodeList[self.currentNode].left != -1:  # Go left
                self.x_vel = self.target_dir_x * Pacman.speed
                self.y_vel = 0
                self.currentEdge = currentMap.nodeList[self.currentNode].left
                self.currentNode = -1

            elif self.target_dir_y > 0 and currentMap.nodeList[self.currentNode].down != -1:  # Go down
                self.x_vel = 0
                self.y_vel = self.target_dir_y * Pacman.speed
                self.currentEdge = currentMap.nodeList[self.currentNode].down
                self.currentNode = -1

            elif self.target_dir_y < 0 and currentMap.nodeList[self.currentNode].up != -1:  # Go up
                self.x_vel = 0
                self.y_vel = self.target_dir_y * Pacman.speed
                self.currentEdge = currentMap.nodeList[self.currentNode].up
                self.currentNode = -1

            elif self.x_vel > 0 and currentMap.nodeList[self.currentNode].right != -1:  # Continue going right
                self.currentEdge = currentMap.nodeList[self.currentNode].right
                self.currentNode = -1

            elif self.x_vel < 0 and currentMap.nodeList[self.currentNode].left != -1:  # Continue going left

                self.currentEdge = currentMap.nodeList[self.currentNode].left
                self.currentNode = -1

            elif self.y_vel > 0 and currentMap.nodeList[self.currentNode].down != -1:  # Continue going down

                self.currentEdge = currentMap.nodeList[self.currentNode].down
                self.currentNode = -1

            elif self.y_vel < 0 and currentMap.nodeList[self.currentNode].up != -1:  # Continue going up

                self.currentEdge = currentMap.nodeList[self.currentNode].up
                self.currentNode = -1
            # self.control(0, 0)




        elif self.currentEdge != -1:

            self.x = round(self.x + self.x_vel, 5)
            self.y = round(self.y + self.y_vel, 5)
            self.x = float(constrain(self.x, currentMap.edgeList[self.currentEdge].minX, currentMap.edgeList[self.currentEdge].maxX))
            self.y = float(constrain(self.y, currentMap.edgeList[self.currentEdge].minY, currentMap.edgeList[self.currentEdge].maxY))


            if currentMap.edgeList[self.currentEdge].vertical and self.target_dir_y != 0:
                self.y_vel = self.target_dir_y * Pacman.speed
            elif currentMap.edgeList[self.currentEdge].vertical == False and self.target_dir_x != 0:
                self.x_vel = self.target_dir_x * Pacman.speed

            if self.atNode1():

                self.currentNode = currentMap.edgeList[self.currentEdge].nodeID_1
                self.currentEdge = -1
            elif self.atNode2():

                self.currentNode = currentMap.edgeList[self.currentEdge].nodeID_2
                self.currentEdge = -1

    def atNode1(self):  # if player reached node 1
        return currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_1].x == self.x and currentMap.nodeList[
            currentMap.edgeList[self.currentEdge].nodeID_1].y == self.y

    def atNode2(self):  # if plater reached node 2
        return currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_2].x == self.x and \
               currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_2].y == self.y

    def eat(self):
        if currentMap.edgeList[self.currentEdge].vertical == False:
            for j in range(len(currentMap.edgeList[self.currentEdge].pointList)):
                if currentMap.edgeList[self.currentEdge].pointList[j].pos == self.x:
                    currentMap.edgeList[self.currentEdge].pointList[j].eaten = True
                    Pacman.score += currentMap.edgeList[self.currentEdge].pointList[j].value


        else:
            for j in range(len(currentMap.edgeList[self.currentEdge].pointList)):
                if currentMap.edgeList[self.currentEdge].pointList[j].pos == self.y:
                    currentMap.edgeList[self.currentEdge].pointList[j].eaten = True

                    Pacman.score += currentMap.edgeList[self.currentEdge].pointList[j].value

        for j in range(len(currentMap.edgeList[self.currentEdge].pointList)):
            if currentMap.edgeList[self.currentEdge].pointList[j].eaten == True:
                currentMap.edgeList[self.currentEdge].pointList.pop(j)
                break

    def check_if_dead(self):
        for i in range(len(ghosts)):
            if distance(self.x,self.y,ghosts[i].x,ghosts[i].y) < 0.07:
                return True
        return False

    def check_if_won(self):
        if player.score == currentMap.pointCount:
            return True
        else:
            return False

pygame.init()
displayWidth = 1760
displayHeight = 990
currentMap = Board.Map("./mapFiles/map6.txt")
currentMap.generateIMG()
ghost_number = 3

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

pygame.display.set_caption('Return of the PAC-ANT')

clock = pygame.time.Clock()

pygame.mixer.init()


player = Pacman(1)
ghosts = []
for i in range (ghost_number):
    rnd = int(random.randrange(len(currentMap.nodeList)))
    ghosts.append(Ghost(rnd))

dead = False
want_to_exit = False
won = False
start = False

background = pygame.image.load("./assets/img/start_screen.png")
background = pygame.transform.scale(background, (displayWidth, displayHeight))

im = Image.new('RGB', (displayWidth, displayHeight), (0,0,0))
im.save("./assets/img/black_screen.png")
black_screen = pygame.image.load("./assets/img/black_screen.png")
black_screen.convert()

im = Image.new('RGB', (displayWidth, displayHeight), (255,255,255))
im.save("./assets/img/white_screen.png")
white_screen = pygame.image.load("./assets/img/white_screen.png")
white_screen.convert()

for i in range (225,0,-10):
    gameDisplay.blit(background, (0,0))
    black_screen.set_alpha(i)
    gameDisplay.blit(black_screen, (0,0))

    pygame.display.update()

# for i in range (0,100,20):
#     gameDisplay.blit(background, (0,0))
#     white_screen.set_alpha(i)
#     gameDisplay.blit(white_screen, (0,0))
#     pygame.display.update()

# for i in range (100,20,-20):
#     gameDisplay.blit(background, (0,0))
#     white_screen.set_alpha(i)
#     gameDisplay.blit(white_screen, (0,0))
#     pygame.display.update()

for i in range (0,255,40):
    gameDisplay.blit(background, (0,0))
    white_screen.set_alpha(i)
    gameDisplay.blit(white_screen, (0,0))
    pygame.display.update()


while not start and not want_to_exit:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 13:
                start = True
        if event.type == pygame.QUIT:
            want_to_exit = True

    gameDisplay.blit(background, (0, 0))
    pygame.display.update()




if want_to_exit:
    exit()


background = pygame.image.load("./tmp/map.png")
background_x = int((displayWidth - int(currentMap.size_x) * Board.box_size) / 2)
background_y = int((displayHeight - int(currentMap.size_y) * Board.box_size) / 2)





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
    dead = player.check_if_dead()
    won = player.check_if_won()

    gameDisplay.blit(background, (background_x, background_y))

    drawPoints()
    player.show()

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


