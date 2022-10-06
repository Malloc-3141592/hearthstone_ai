import pygame as pg
from pygame.locals import *
import sys

input=sys.stdin.readline

pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption('HearthStone_Beta')
font30 = pg.font.Font('NanumGothic.ttf', 30)
font20 = pg.font.Font('NanumGothic.ttf', 20)
BLACK=(0,0,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
done = False
cardName_file = open('cardName.txt')
cardImg=[]
i=0
while True:
    tmp = cardName_file.readline()
    if not tmp: break
    tmp = tmp.strip()  # cardName.txt
    cardImg.append(pg.image.load('image/' + tmp + '.png'))
    cardImg[i] = pg.transform.scale(cardImg[i], (100, 120))
    i+=1

screen.fill(BLACK)
text1 = 'Time: 1'
timerimg = font30.render(text1, True, WHITE)
screen.blit(timerimg, (20, 305))

text1='Buy List'
buylistimg=font30.render(text1, True, WHITE)
screen.blit(buylistimg, (20,0))

screen.blit(cardImg[0], (0, 40))
screen.blit(cardImg[1], (130, 40))
screen.blit(cardImg[2], (260, 40))
text1 = 'Freezed'
freezedimg = font30.render(text1, True, YELLOW)
screen.blit(freezedimg, (20, 350))
screen.blit(cardImg[4], (300, 500))     # i*130+300, 500
screen.blit(cardImg[5], (430, 500))
screen.blit(cardImg[6], (560, 500))

text1 = 'Gold: 30'
goldimg = font30.render(text1, True, WHITE)
screen.blit(goldimg, (20, 200))
text2 = 'Level: 4'
levelimg = font30.render(text2, True, WHITE)
screen.blit(levelimg, (20, 235))
text1 = 'Upgrade Cost: 5'
upgrade_costimg = font30.render(text1, True, WHITE)
screen.blit(upgrade_costimg, (20, 270))
text2 = 'F key: Freeze // U key: Upgrade // R key: Reroll'
manualimg = font20.render(text2, True, WHITE)
screen.blit(manualimg, (20, 400))
pg.display.flip()

while not done:
    for event in pg.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            col=event.pos[0]
            row=event.pos[1]
            print(col, row)
    pg.display.flip()