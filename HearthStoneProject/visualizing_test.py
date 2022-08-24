import pygame as pg
from pygame.locals import *
import sys

input=sys.stdin.readline

pg.init()
screen = pg.display.set_mode((640, 480))
pg.display.set_caption('HearthStone_Beta')
font30 = pg.font.Font('NanumGothic.ttf', 30)
font20 = pg.font.Font('NanumGothic.ttf', 20)

done = False
while not done:
    for event in pg.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            col=event.pos[0]
            row=event.pos[1]
            print(col, row)
    pg.display.flip()