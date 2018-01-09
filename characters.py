from settings import *
# from gameState import *

import random

ghosts = []


class Ghost:

    def __init__(self, currentMap, _currentNode, _type=0):

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

    def positionToDraw(self):

        draw_x = int(self.x * Board.box_size + 0.5 * Board.box_size - 10)
        draw_y = int(self.y * Board.box_size + 0.5 * Board.box_size - 15)
        return (draw_x, draw_y)

    def show(self):

        rotated = pygame.Surface((1, 1))
        # pygame.draw.circle(gameDisplay, (255, 255, 0), positionToDraw(self.x, self.y), 12)
        if self.x_vel > 0:
            rotated = pygame.transform.rotate(ladybug, -90)
        if self.x_vel < 0:
            rotated = pygame.transform.rotate(ladybug, 90)
        if self.y_vel < 0 or (self.x_vel == 0 and self.y_vel == 0):
            rotated = ladybug
        if self.y_vel > 0:
            rotated = pygame.transform.rotate(ladybug, 180)

        gameDisplay.blit(rotated, self.positionToDraw())

    def update(self, currentMap, player, rampage_mode, scatter_mode):
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

            currentNode = currentMap.nodeList[self.currentNode]




            if currentMap.nodeList[self.currentNode].ghostHouse == 1 and currentNode.up != -1:
                self.x_vel = 0
                self.y_vel = -self.speed
                self.currentEdge = currentMap.nodeList[self.currentNode].up
                self.currentNode = -1
                self.target_dir_x = 0
                self.target_dir_y = 0
                self.x += self.x_vel
                self.y += self.y_vel
                return






            direction_list = []

            if not rampage_mode and scatter_mode:

                for i in range (4):
                    direction_list.append(random.randrange(20))



            else:


                direction_list.append(-self.target_dir_y)
                direction_list.append(self.target_dir_x)
                direction_list.append(self.target_dir_y)
                direction_list.append(-self.target_dir_x)





                if(rampage_mode):
                    for i in range(len(direction_list)):
                        direction_list[i] *= -1


            if currentNode.up == -1:
                direction_list[0] = -100
            if currentNode.right == -1:
                direction_list[1] = -100
            if currentNode.down == -1:
                direction_list[2] = -100
            if currentNode.left == -1:
                direction_list[3] = -100

            # zabronienie zawracania
            if direction_list.count(-100) < 3:
                direction_list[(self.target_dir + 2) % 4] = -100

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

            if self.atNode1(currentMap):

                self.currentNode = currentMap.edgeList[self.currentEdge].nodeID_1
                self.currentEdge = -1
            elif self.atNode2(currentMap):

                self.currentNode = currentMap.edgeList[self.currentEdge].nodeID_2
                self.currentEdge = -1

    def atNode1(self, currentMap):  # if player reached node 1
        return currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_1].x == self.x and currentMap.nodeList[
            currentMap.edgeList[self.currentEdge].nodeID_1].y == self.y

    def atNode2(self, currentMap):  # if plater reached node 2
        return currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_2].x == self.x and \
               currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_2].y == self.y

    def respawn(self, currentMap):
        rnd = random.randrange(2)
        self.currentNode = currentMap.ghostHouseList[rnd]
        self.x = float(currentMap.nodeList[currentMap.ghostHouseList[rnd]].x)
        self.y = float(currentMap.nodeList[currentMap.ghostHouseList[rnd]].y)


class Pacman:
    speed = 0.08
    
    total_score = -5

    def __init__(self, currentMap, _currentNode):

        self.x_vel = 0.0
        self.y_vel = 0.0
        self.currentNode = _currentNode
        self.currentEdge = 0
        self.x = float(currentMap.nodeList[_currentNode].x)
        self.y = float(currentMap.nodeList[_currentNode].y)

        self.target_dir_x = 0
        self.target_dir_y = 0
        self.last_rampage_pill = -100000
        self.score = -5

    def positionToDraw(self):
        draw_x = 0
        draw_y = 0
        if self.x_vel > 0:
            draw_x = int(self.x * Board.box_size + 0.5 * Board.box_size - 20)
            draw_y = int(self.y * Board.box_size + 0.5 * Board.box_size - 15)
        if self.x_vel < 0:
            draw_x = int(self.x * Board.box_size + 0.5 * Board.box_size - 15)
            draw_y = int(self.y * Board.box_size + 0.5 * Board.box_size - 15)
        if self.y_vel < 0 or (self.x_vel == 0 and self.y_vel == 0):
            draw_x = int(self.x * Board.box_size + 0.5 * Board.box_size - 15)
            draw_y = int(self.y * Board.box_size + 0.5 * Board.box_size - 15)
        if self.y_vel > 0:
            draw_x = int(self.x * Board.box_size + 0.5 * Board.box_size - 15)
            draw_y = int(self.y * Board.box_size + 0.5 * Board.box_size - 20)

        return (draw_x, draw_y)

    def show(self):

        if pygame.time.get_ticks() % 200 < 100:
            ant = ant1
        else:
            ant = ant2

        rotated = pygame.Surface((1, 1))
        # pygame.draw.circle(gameDisplay, (255, 255, 0), positionToDraw(self.x, self.y), 12)
        if self.x_vel > 0:
            rotated = pygame.transform.rotate(ant, -90)
        if self.x_vel < 0:
            rotated = pygame.transform.rotate(ant, 90)
        if self.y_vel < 0 or (self.x_vel == 0 and self.y_vel == 0):
            rotated = ant
        if self.y_vel > 0:
            rotated = pygame.transform.rotate(ant, 180)

        gameDisplay.blit(rotated, self.positionToDraw())

    def control(self, dirX, dirY):
        # gets x and y direction as a argument

        self.target_dir_x = dirX
        self.target_dir_y = dirY

    def update(self, currentMap):

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
                self.score += currentMap.nodeList[self.currentNode].pointSlot.value
                Pacman.total_score += currentMap.nodeList[self.currentNode].pointSlot.value
                
                coin.play()
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

            if self.atNode1(currentMap):

                self.currentNode = currentMap.edgeList[self.currentEdge].nodeID_1
                self.currentEdge = -1
            elif self.atNode2(currentMap):

                self.currentNode = currentMap.edgeList[self.currentEdge].nodeID_2
                self.currentEdge = -1

    def atNode1(self, currentMap):  # if player reached node 1
        return currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_1].x == self.x and currentMap.nodeList[
            currentMap.edgeList[self.currentEdge].nodeID_1].y == self.y

    def atNode2(self, currentMap):  # if plater reached node 2
        return currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_2].x == self.x and \
               currentMap.nodeList[currentMap.edgeList[self.currentEdge].nodeID_2].y == self.y

    def eat(self, currentMap):
        if currentMap.edgeList[self.currentEdge].vertical == False:
            for j in range(len(currentMap.edgeList[self.currentEdge].pointList)):
                if abs(currentMap.edgeList[self.currentEdge].pointList[j].pos - self.x) <= 0.08:
                    currentMap.edgeList[self.currentEdge].pointList[j].eaten = True
                    self.score += currentMap.edgeList[self.currentEdge].pointList[j].value
                    Pacman.total_score += currentMap.edgeList[self.currentEdge].pointList[j].value
                    coin.play()


        else:
            for j in range(len(currentMap.edgeList[self.currentEdge].pointList)):
                if abs(currentMap.edgeList[self.currentEdge].pointList[j].pos - self.y) <= 0.08:
                    currentMap.edgeList[self.currentEdge].pointList[j].eaten = True
                    coin.play()

                    self.score += currentMap.edgeList[self.currentEdge].pointList[j].value
                    Pacman.total_score += currentMap.edgeList[self.currentEdge].pointList[j].value

        for j in range(len(currentMap.edgeList[self.currentEdge].pointList)):
            if currentMap.edgeList[self.currentEdge].pointList[j].eaten == True:
                currentMap.edgeList[self.currentEdge].pointList.pop(j)
                break

    def contact(self, _rampage_mode, currentMap, ghosts):
        for i in range(len(ghosts)):
            if distance(self.x, self.y, ghosts[i].x, ghosts[i].y) < 0.09:
                if _rampage_mode:
                    ghosts[i].respawn(currentMap)

                else:
                    self.respawn(currentMap)
                    return -1
        return 0

    def check_if_won(self, currentMap):
        if self.score >= currentMap.pointCount:
            return True
        else:
            return False

    def eat_rampage_pill(self, currentMap):
        for i in range(len(currentMap.rampage_pill)):
            if currentMap.rampage_pill[i] == self.currentNode:
                currentMap.rampage_pill.pop(i)
                self.last_rampage_pill = pygame.time.get_ticks()
                break

    def check_if_rampage(self):
        if (pygame.time.get_ticks() - self.last_rampage_pill) / 1000 <= 5:
            return True
        else:
            return False

    def respawn(self, currentMap):
        self.currentNode = currentMap.start_node
        self.x = float(currentMap.nodeList[self.currentNode].x)
        self.y = float(currentMap.nodeList[self.currentNode].y)
        self.target_dir_x = 0
        self.target_dir_y = 0
        self.x_vel = 0
        self.y_vel = 0
