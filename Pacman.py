import pygame
import main
import Board


class Pacman:


    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y



    def show2 (self):
        pygame.draw.circle(main.gameDisplay,(0,255,255),(self.x*Board.box_size+main.background_x, self.y*Board.box_size)+main.background_y,20);
        print(self.x*Board.box_size+main.background_x)