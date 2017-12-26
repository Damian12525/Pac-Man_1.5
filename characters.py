from settings import *
from gameState import *
import random


ghosts = []

class Ghost:

    def __init__(self, _currentNode, _type=0):

        self.type = _type
        self.speed = 0.07
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

    def respawn(self):
        rnd = random.randrange(2)
        self.currentNode = currentMap.ghostHouseList[rnd]
        self.x = float(currentMap.nodeList[currentMap.ghostHouseList[rnd]].x)
        self.y = float(currentMap.nodeList[currentMap.ghostHouseList[rnd]].y)





class Pacman:
    speed = 0.08
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
            self.x = float(constrain(self.x, currentMap.edgeList[self.currentEdge].minX,
                                               currentMap.edgeList[self.currentEdge].maxX))
            self.y = float(constrain(self.y, currentMap.edgeList[self.currentEdge].minY,
                                               currentMap.edgeList[self.currentEdge].maxY))

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
                if abs(currentMap.edgeList[self.currentEdge].pointList[j].pos - self.x) <= 0.08:
                    currentMap.edgeList[self.currentEdge].pointList[j].eaten = True
                    Pacman.score += currentMap.edgeList[self.currentEdge].pointList[j].value


        else:
            for j in range(len(currentMap.edgeList[self.currentEdge].pointList)):
                if abs(currentMap.edgeList[self.currentEdge].pointList[j].pos - self.y) <= 0.08:
                    currentMap.edgeList[self.currentEdge].pointList[j].eaten = True

                    Pacman.score += currentMap.edgeList[self.currentEdge].pointList[j].value

        for j in range(len(currentMap.edgeList[self.currentEdge].pointList)):
            if currentMap.edgeList[self.currentEdge].pointList[j].eaten == True:
                currentMap.edgeList[self.currentEdge].pointList.pop(j)
                break

    def contact(self):
        for i in range(len(ghosts)):
            if distance(self.x, self.y, ghosts[i].x, ghosts[i].y) < 0.09:
                if rampage_mode:
                    ghosts[i].respawn()

                else:
                    return True
        return False

    def check_if_won(self):
        if player.score == currentMap.pointCount:
            return True
        else:
            return False

player = Pacman(1)