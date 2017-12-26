import pygame
from settings import *
from PIL import Image
from main import gameDisplay

pygame.init()

font = pygame.font.SysFont("Fipps", 40)
text = font.render("Press Enter", True, (255,255 , 0))
press_prompt = pygame.Surface((400,100))
press_prompt.blit(text,(0,0))

background = pygame.image.load("./assets/img/start_screen2.png")
background = pygame.transform.scale(background, (displayWidth, displayHeight))

im = Image.new('RGB', (displayWidth, displayHeight), (0, 0, 0))
im.save("./assets/img/black_screen.png")
black_screen = pygame.image.load("./assets/img/black_screen.png")
black_screen.convert()

im = Image.new('RGB', (displayWidth, displayHeight), (255, 255, 255))
im.save("./assets/img/white_screen.png")
white_screen = pygame.image.load("./assets/img/white_screen.png")
white_screen.convert()

logo = pygame.image.load("./assets/img/logo2.png")


pygame.quit()