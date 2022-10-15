import random as rd
import pygame as pg
from pygame.locals import *
import time
import threading
import sys

class Card:
    def __init__(self):
        self.name = 0
        self.attack = 0
        self.health = 0
        self.fighthealth = 0
        self.tribe = 0
        self.level = 0
        self.ability = 0
        self.goldenHealth = 0
        self.goldenAttack = 0
        self.goldenAbility = 0
        self.golden=False

# General
sec=0
turn=1

# Variables for buy turn
upgrade_cost=5
gold=3
shopLevel=1
cardList=[]     # All Cards
cardImg=[]     # All Cards Image
gcardImg=[]    # All Golden Cards Image
playerCard=[]     # All Player Cards (object)
buyList = []
cardLimit = [18, 15, 13, 11, 9, 7]
cardBound = [6, 15]
cardCount = []

# Variables for fight turn
playerGround=[]
opponentGround=[]

# Pygame Setting
pg.init()
screen = pg.display.set_mode((1280,720))
pg.display.set_caption('Hearthstone Beta')
font30 = pg.font.Font('NanumGothic.ttf', 30)
font20 = pg.font.Font('NanumGothic.ttf', 20)
rrButton=pg.image.load('reroll.png')
upButton=pg.image.load('upgrade.png')
freezeButton=pg.image.load('freeze.png')
rrButton=pg.transform.scale(rrButton, (50,50))
upButton=pg.transform.scale(upButton, (50,50))
freezeButton=pg.transform.scale(freezeButton, (50,50))
cardName_file = open('cardName.txt')
cardStats_file = open('cardStats.txt')
goldencardStats_file = open('goldencardStats.txt')
opponentGround_file = open('op1.txt')
i=0
while True:
    tmp = cardName_file.readline().strip()
    tmp2 = cardStats_file.readline().strip().split()
    tmp3 = goldencardStats_file.readline().strip().split()
    tmp4 = opponentGround_file.readline()
    if not tmp: break
    cardList[i].name = tmp
    cardImg[i] = pg.image.load('image/' + tmp + '.png')
    cardImg[i] = pg.transform.scale(cardImg[i], (200, 240))
    if i < 6:
        gcardImg.append(pg.image.load('goldenimage/' + tmp + '.png'))
        gcardImg[i] = pg.transform.scale(gcardImg[i], (200, 240))

    # Card Stats
    cardList[i].level = tmp2[0]
    cardList[i].attack = tmp2[1]
    cardList[i].health = tmp2[2]
    cardList[i].fighthealth = tmp2[2]
    cardList[i].ability = tmp2[3]

    cardList[i].goldenAttack = tmp3[0]
    cardList[i].goldenHealth = tmp3[1]
    cardList[i].goldenAbility = tmp3[2]
    cardCount.append(0)
    i += 1

cardName_file.close()
cardStats_file.close()
goldencardStats_file.close()

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)

shopCard_number = [3, 4, 4, 5, 5, 6]  # 선술집에서 나오는 카드 수
shopLevel_cost = [5, 7, 8, 9, 11]
shopLevel = 1
freezed = False  # check if freezed
upgraded = False  # check if upgraded this turn

def startTimer():
    global sec
    printUI()
    sec += 1
    timer = threading.Timer(1, startTimer)
    timer.start()
    if sec > 20:
        timer.cancel()
    pg.display.flip()

def printUI():
    global freezed
    screen.fill(BLACK)

    text1 = 'Time: ' + str(sec)
    timerimg = font30.render(text1, True, WHITE)
    screen.blit(timerimg, (20, 305))
    text1 = 'Buy List'
    buylistimg = font30.render(text1, True, WHITE)
    screen.blit(buylistimg, (20, 0))

    for i in range(len(buyList)):
        tmp = cardList.index(buyList[i])
        screen.blit(cardImg[tmp], (i * 200, 40))
    if freezed == True:
        text1 = 'Freezed'
        freezedimg = font30.render(text1, True, WHITE)
        screen.blit(freezedimg, (20, 350))
    for i in range(len(playerCard)):
        tmp = cardList.index(playerCard[i])
        if playerCard.golden:
            screen.blit(gcardImg[tmp], (i*200+300,250))
        else:
            screen.blit(cardImg[tmp], (i * 200 + 300, 250))

    text1 = 'Buy List'
    buylistimg = font30.render(text1, True, WHITE)
    screen.blit(buylistimg, (20, 0))
    text1 = 'Gold: ' + str(gold)
    goldimg = font30.render(text1, True, WHITE)
    screen.blit(goldimg, (20, 200))
    text2 = 'Level: ' + str(shopLevel)
    levelimg = font30.render(text2, True, WHITE)
    screen.blit(levelimg, (20, 235))
    text1 = 'Upgrade Cost: ' + str(upgrade_cost)
    upgrade_costimg = font30.render(text1, True, WHITE)
    screen.blit(upgrade_costimg, (20, 270))

    screen.blit(rrButton, (150, 0))
    screen.blit(upButton, (210, 0))
    screen.blit(freezeButton, (270, 0))
    pg.display.flip()

def reset():  # 전장 새로고침
    screen.fill(BLACK)
    buyList.clear()
    for i in range(shopCard_number[shopLevel - 1]):
        done = False
        while not done:
            tmp = rd.randrange(0, cardBound[shopLevel - 1] - 1)
            if tmp <= cardBound[0]:
                if cardCount[] < cardLimit[0]: done = True
            elif tmp <= cardBound[1]:
                if cardCount[] < cardLimit[1]: done = True
            # 카드 등급 더 많아지면 추가할 것
            if done:
                buyList.append(cardList[tmp])
    printUI()

def freeze():  # 전장 빙결
    global freezed
    freezed = not freezed

def upgrade():  # 선술집 강화
    global gold, upgrade_cost, shopLevel, upgraded
    if gold - upgrade_cost >= 0:
        if shopLevel < 6:
            gold -= upgrade_cost
            shopLevel += 1
            upgrade_cost = shopLevel_cost[shopLevel - 1]
            upgraded = True
    printUI()

def buy(buyCard):  # 하수인 고용
    global gold
    if 3 <= gold:
        gold -= 3
        playerCard.append(buyCard)
        if playerCard.count(buyCard) == 3:
            for i in range(3):
                playerCard.remove(buyCard)
                putDown(buyCard)
            playerCard.append(buyCard)
            tmp=len(playerCard)-1
            playerCard[tmp].golden=True
            playerCard[tmp].health=playerCard[tmp].goldenHealth
            playerCard[tmp].attack=playerCard[tmp].goldenAttack
            playerCard[tmp].fighthealth=playerCard[tmp].health
            playerCard[tmp].fightattack=playerCard[tmp].attack
        buyList.remove(buyCard)
        printText()
    else:
        print('error')

def putDown(downCard):      # 추후 위치 조정 가능하게 수정
    playerGround.append(downCard)

def startGame():
    global gold
    gold=3
    turn=1


if __name__ == '__main__':
    startGame()