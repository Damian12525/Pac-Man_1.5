from PIL import Image
import math
import random

box_size = 80



def signum(x):
    return x / math.fabs(x)


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ^ 2 + (y1 - y2) ^ 2)


class Node:

    def __init__(self, _x, _y, _nodeID, _linkedTunelID=-1):
        self.x = _x
        self.y = _y
        self.type = 0
        self.nodeID = _nodeID

        self.pointSlot = Point(0, 5)

        # nodeType
        self.up = -1  # 1
        self.right = -1  # 2
        self.down = -1  # 4
        self.left = -1  # 8

        self.linkedTunelID = _linkedTunelID


class Map:
    mapCount = 0

    def __init__(self, file_path):
        Map.mapCount += 1
        self.mapID = Map.mapCount
        self.nodeList = []
        self.edgeList = []
        self.size_x = int(0)
        self.size_y = int(0)

        file = open(file_path, "r")

        lines = file.readlines()

        for i in range(len(lines)):
            # odczytujemy linia po lini

            currentLine = lines[i]
            currentLine = currentLine.split()

            if currentLine[0] == 'n':
                newNode = Node(int(currentLine[1]), int(currentLine[2]), len(self.nodeList))
                self.nodeList.append(newNode)
                if int(currentLine[1]) > int(self.size_x):
                    self.size_x = currentLine[1]
                if int(currentLine[2]) > int(self.size_y):
                    self.size_y = currentLine[2]

            elif currentLine[0] == 't':
                newNode = Node(int(currentLine[1]), int(currentLine[2]), len(self.nodeList), int(currentLine[3]))
                newNode.pointSlot = -1
                self.nodeList.append(newNode)
                if int(currentLine[1]) > int(self.size_x):
                    self.size_x = currentLine[1]
                if int(currentLine[2]) > int(self.size_y):
                    self.size_y = currentLine[2]


            else:
                newEdge = Edge(int(currentLine[1]), int(currentLine[2]), len(self.edgeList))
                newEdge.node1x = self.nodeList[newEdge.nodeID_1].x
                newEdge.node1y = self.nodeList[newEdge.nodeID_1].y
                newEdge.node2x = self.nodeList[newEdge.nodeID_2].x
                newEdge.node2y = self.nodeList[newEdge.nodeID_2].y

                if self.nodeList[newEdge.nodeID_1].x == self.nodeList[newEdge.nodeID_2].x:
                    newEdge.vertical = True
                else:
                    newEdge.vertical = False

                if newEdge.vertical == False:
                    newEdge.length = math.fabs(self.nodeList[newEdge.nodeID_1].x - self.nodeList[newEdge.nodeID_2].x)

                    if self.nodeList[newEdge.nodeID_1].x < self.nodeList[newEdge.nodeID_2].x:
                        self.nodeList[newEdge.nodeID_1].right = newEdge.edgeID
                        self.nodeList[newEdge.nodeID_2].left = newEdge.edgeID
                    else:
                        self.nodeList[newEdge.nodeID_1].left = newEdge.edgeID
                        self.nodeList[newEdge.nodeID_2].right = newEdge.edgeID

                else:
                    newEdge.length = math.fabs(
                        self.nodeList[newEdge.nodeID_1].y - self.nodeList[newEdge.nodeID_2].y)

                    if self.nodeList[newEdge.nodeID_1].y > self.nodeList[newEdge.nodeID_2].y:
                        self.nodeList[newEdge.nodeID_1].up = newEdge.edgeID
                        self.nodeList[newEdge.nodeID_2].down = newEdge.edgeID
                    else:
                        self.nodeList[newEdge.nodeID_1].down = newEdge.edgeID
                        self.nodeList[newEdge.nodeID_2].up = newEdge.edgeID

                if newEdge.vertical == False:
                    newEdge.minY = newEdge.node1y
                    newEdge.maxY = newEdge.node1y
                    if newEdge.node1x > newEdge.node2x:
                        newEdge.maxX = newEdge.node1x
                        newEdge.minX = newEdge.node2x
                    else:
                        newEdge.maxX = newEdge.node2x
                        newEdge.minX = newEdge.node1x

                else:
                    newEdge.minX = newEdge.node1x
                    newEdge.maxX = newEdge.node1x

                    if newEdge.node1y > newEdge.node2y:
                        newEdge.maxY = newEdge.node1y
                        newEdge.minY = newEdge.node2y
                    else:
                        newEdge.maxY = newEdge.node2y
                        newEdge.minY = newEdge.node1y


                newEdge.placePoints()

                self.edgeList.append(newEdge)

        # set type of all nodes
        for i in range(len(self.nodeList)):
            if self.nodeList[i].up != -1:
                self.nodeList[i].type += 1
            if self.nodeList[i].right != -1:
                self.nodeList[i].type += 2
            if self.nodeList[i].down != -1:
                self.nodeList[i].type += 4
            if self.nodeList[i].left != -1:
                self.nodeList[i].type += 8

    def generateIMG(self):

        img_res_x = int(self.size_x) * box_size
        img_res_y = int(self.size_y) * box_size
        color = (255, 255, 255)
        # im = Image.frombytes('L', (img_res_x, img_res_y), bytes([0] * img_res_x * img_res_y))
        im = Image.new('RGB', (img_res_x, img_res_y), color)
        for i in range(len(self.nodeList)):
            nodeImgPath = "./assets/map/node_" + str(self.nodeList[i].type) + ".png"

            node = Image.open(nodeImgPath, "r")
            im.paste(node, (((self.nodeList[i].x - 1) * box_size), ((self.nodeList[i].y - 1) * box_size)), mask=node)

        for i in range(len(self.edgeList)):

            x = self.nodeList[self.edgeList[i].nodeID_1].x
            y = self.nodeList[self.edgeList[i].nodeID_1].y

            if self.edgeList[i].vertical == False:

                sign = signum(self.nodeList[self.edgeList[i].nodeID_2].x - self.nodeList[self.edgeList[i].nodeID_1].x)
                edge = Image.open("./assets/map/hor.png", "r")

                while math.fabs(x - self.nodeList[self.edgeList[i].nodeID_2].x) > 1:
                    im.paste(edge, (int((x + sign - 1) * box_size), int((y - 1) * box_size)), mask=edge)
                    x += sign










            else:

                sign = signum(self.nodeList[self.edgeList[i].nodeID_2].y - self.nodeList[self.edgeList[i].nodeID_1].y)
                edge = Image.open("./assets/map/ver.png", "r")

                while math.fabs(y - self.nodeList[self.edgeList[i].nodeID_2].y) > 1:
                    im.paste(edge, (int((x - 1) * box_size), int((y + sign - 1) * box_size)), mask=edge)
                    y += sign

        # im.show()
        im.save("./tmp/map.png")


class Edge:

    def __init__(self, _nodeID_1, _nodeID_2, _edgeID):

        self.edgeID = _edgeID
        self.nodeID_1 = _nodeID_1
        self.nodeID_2 = _nodeID_2
        self.vertical = False
        self.length = 0
        self.pointList = []

        self.node1x = 0
        self.node1y = 0

        self.node2x = 0
        self.node2y = 0

        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0


    def placePoints(self):
        amount = int(self.length * Point.density)
        separation_distance = self.length / (amount + 1)
        if self.vertical == False:
            sign = signum(self.node1x - self.node2x)

            for i in range(amount):
                self.pointList.append(Point(self.node1x - sign * (i + 1) * separation_distance))


        else:
            sign = signum(self.node1y - self.node2y)

            for i in range(amount):
                self.pointList.append(Point(self.node1y - sign * (i + 1) * separation_distance))


def makeEven(x):
    x2 = round(x, 4)
    x2 *= 100

    x2 -= x2 % 4
    x2 = x2 / 100
    x2 = round(x2, 2)
    return x2


class Point:
    density = 2

    def __init__(self, _pos, _value=1):
        self.value = _value
        self.eaten = False

        self.pos = makeEven(_pos)
