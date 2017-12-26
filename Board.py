from PIL import Image
import math
import random



def signum(x):
    return x / math.fabs(x)



box_size = 80






class Node:

    def __init__(self, _x, _y, _nodeID, _linkedTunelID = -1, _ghostHouse = -1):
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
        self.ghostHouse = _ghostHouse





class Map:
    mapCount = 0


    def addEdge(self, _node1ID, _node2ID, _withPoints = 1):
        newEdge = Edge(int( _node1ID), int(_node2ID), len(self.edgeList), _withPoints)
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

        self.pointCount += newEdge.placePoints()

        self.edgeList.append(newEdge)






    def __init__(self, file_path):
        Map.mapCount += 1
        self.mapID = Map.mapCount
        self.nodeList = []
        self.edgeList = []
        self.size_x = int(0)
        self.size_y = int(0)
        self.pointCount = -5
        self.ghostHouseList = []

        self.rampage_pill = []

        file = open(file_path, "r")

        lines = file.readlines()

        for i in range(len(lines)):
            # odczytujemy linia po lini

            currentLine = lines[i]
            currentLine = currentLine.split()

            if currentLine[0] == 'n':
                newNode = Node(int(currentLine[1]), int(currentLine[2]), len(self.nodeList))
                self.nodeList.append(newNode)
                self.pointCount += 5
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


            elif currentLine[0] == 'e':
                if len(currentLine) == 4:
                    self.addEdge(int(currentLine[1]), int(currentLine[2]), int(currentLine[3]))
                else:
                    self.addEdge(int(currentLine[1]), int(currentLine[2]))


            elif currentLine[0] == 'g':
                middleNode = Node(int(currentLine[1]), int(currentLine[2]), len(self.nodeList), -1,1)
                middleNode.pointSlot = -1

                self.ghostHouseList.append(len(self.nodeList))
                self.nodeList.append(middleNode)

                if int(currentLine[2]) > int(self.size_y):
                    self.size_y = currentLine[2]


                leftNode = Node(int(middleNode.x -1 ),middleNode.y, len(self.nodeList),-1,1)
                leftNode.pointSlot = -1
                self.ghostHouseList.append(len(self.nodeList))
                self.nodeList.append(leftNode)


                rightNode = Node(int(middleNode.x +1), middleNode.y, len(self.nodeList),-1,1)
                rightNode.pointSlot = -1
                self.ghostHouseList.append(len(self.nodeList))
                self.nodeList.append(rightNode)
                if int(currentLine[1]) + 1 > int(self.size_x):
                    self.size_x = rightNode.x



                self.addEdge(middleNode.nodeID, leftNode.nodeID, 0)
                self.addEdge(middleNode.nodeID, rightNode.nodeID, 0)






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

        self.generateIMG()

    def generateIMG(self):

        img_res_x = int(self.size_x) * box_size
        img_res_y = int(self.size_y) * box_size
        color = (255, 255, 255)
        # im = Image.frombytes('L', (img_res_x, img_res_y), bytes([0] * img_res_x * img_res_y))
        im = Image.new('RGB', (img_res_x, img_res_y), color)
        background = Image.open("./assets/map/background.png", "r")
        for x in range(int(self.size_x)):
            for y in range(int(self.size_y)):
                im.paste(background, ((x  * box_size), (y * box_size)))





        for i in range(len(self.nodeList)):
            if self.nodeList[i].ghostHouse == -1:
                nodeImgPath = "./assets/map/node_" + str(self.nodeList[i].type) + ".png"

                node = Image.open(nodeImgPath, "r")
            else:
                if self.nodeList[i].up != -1:
                    node = Image.open("./assets/map/ghouse_middle.png","r")
                elif self.nodeList[i].right != -1:
                    node = Image.open("./assets/map/ghouse_left.png", "r")
                elif self.nodeList[i].left != -1:
                    node = Image.open("./assets/map/ghouse_right.png", "r")

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
        back = Image.open("./assets/img/back.png")
        back.paste(im, (0,box_size))
        back.save("./tmp/map.png")


    def spawn_rampage_pill(self):
        while len(self.rampage_pill) < 4:
            rnd = -1
            while rnd == -1 and self.rampage_pill.count(rnd) != 0:
                rnd = random.randrange(len(self.nodeList))

            self.rampage_pill.append(rnd)




class Edge:

    def __init__(self, _nodeID_1, _nodeID_2, _edgeID, _withPoints = 1):

        self.edgeID = _edgeID
        self.nodeID_1 = _nodeID_1
        self.nodeID_2 = _nodeID_2
        self.vertical = False
        self.length = 0
        self.withPoints = _withPoints
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
        count = 0
        amount = int(self.length * Point.density)
        separation_distance = self.length / (amount + 1)
        if self.withPoints:
            if self.vertical == False:
                sign = signum(self.node1x - self.node2x)

                for i in range(amount):
                    self.pointList.append(Point(self.node1x - sign * (i + 1) * separation_distance))
                    count += 1


            else:
                sign = signum(self.node1y - self.node2y)

                for i in range(amount):
                    self.pointList.append(Point(self.node1y - sign * (i + 1) * separation_distance))
                    count += 1
        return count


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
