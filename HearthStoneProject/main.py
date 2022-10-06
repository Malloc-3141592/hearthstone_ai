import random as rd
import pygame as pg  # pygame library
import time
from pygame.locals import *
import threading
import copy
import sys
input=sys.stdin.readline

class Card:
    def __init__(self):
        self.name = 0
        self.attack = 0
        self.health = 0
        self.fighthealth = 0
        self.tribe = 0
        self.img = 0
        self.level = 0
        self.ability = 0
        self.goldenHealth = 0
        self.goldenAttack = 0
        self.goldenAbility = 0


pg.init()
screen = pg.display.set_mode((1280, 720))
pg.display.set_caption('HearthStone_Beta')
stop = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,255,0)
sec = 1
Round = 0
end_time = 20
playerCard = []  # 플레이어가 들고 있는 카드
playerGoldenCard = []  # 플레이어가 들고 있는 황금 카드
cardImg = []
goldencardImg = []
cardList = []
playerGround = []  # 플레이어 전장
opponentGround = []  # 상대 전장
tempGround =[]
p2Ground = []
p3Ground = []
p4Ground = []
buyList = []  # 선술집 목록
shopCard_number = [3, 4, 4, 5, 5, 6]  # 선술집에서 나오는 카드 수
shopLevel_cost = [5, 7, 8, 9, 11]
shopLevel = 1
freezed = False  # check if freezed
upgraded = False  # check if upgraded this turn
upgrade_cost = 5
gold = 0
max_gold = 0
cardLimit = [18, 15, 13, 11, 9, 7]  # 등급별 총 복사본 개수(근데 이거 4명이서 하면 바꿔야함)
cardCount = []
cardBound = [6, 15]
font30 = pg.font.Font('NanumGothic.ttf', 30)
font20 = pg.font.Font('NanumGothic.ttf', 20)
rrButton=pg.image.load('reroll.png')
upButton=pg.image.load('upgrade.png')
freezeButton=pg.image.load('freeze.png')
rrButton=pg.transform.scale(rrButton, (50,50))
upButton=pg.transform.scale(upButton, (50,50))
freezeButton=pg.transform.scale(freezeButton, (50,50))


'''
cardStats -> <Level> <Attack> <Health> <Ability> <Tribe>
goldencardStats -> <Attack> <Health> <Ability>

Effect numbers:
Battlecry - 1           전투의 함성
Deathrattle - 2         죽음의 메아리
Divine Shield - 3       천상의 보호막
Taunt - 4               도발

Tribe numbers:
Dragon - 1              용족
Mech - 2                기계
Murloc - 3              멀록
'''


def startTimer():
    global sec
    printText()
    sec += 1
    timer = threading.Timer(1, startTimer)
    timer.start()
    if sec > end_time:
        timer.cancel()
    pg.display.flip()


def printText():
    global freezed
    screen.fill(BLACK)

    text1 = 'Time: ' + str(sec)
    timerimg = font30.render(text1, True, WHITE)
    screen.blit(timerimg, (20, 305))

    for i in range(len(buyList)):
        tmp = cardList.index(buyList[i])
        screen.blit(cardImg[tmp], (i * 130, 40))
    if freezed == True:
        text1 = 'Freezed'
        freezedimg = font30.render(text1, True, WHITE)
        screen.blit(freezedimg, (10, 300))
    for i in range(len(playerCard)):
        tmp = cardList.index(playerCard[i])
        screen.blit(cardImg[tmp], (i * 130 + 300, 120))
    for i in range(len(playerGoldenCard)):
        tmp = cardList.index(playerGoldenCard[i])
        screen.blit(goldencardImg[tmp], (i * 130 + 300, 250))

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
    text2 = 'F key: Freeze // U key: Upgrade // R key: Reroll'
    manualimg = font20.render(text2, True, WHITE)
    screen.blit(manualimg, (20, 400))
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
                if cardCount[tmp] < cardLimit[0]: done = True
            elif tmp <= cardBound[1]:
                if cardCount[tmp] < cardLimit[1]: done = True
            # 카드 등급 더 많아지면 추가할 것
            if done:
                buyList.append(cardList[tmp])
    printText()


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
    printText()


def buy(boughtNumber):  # 하수인 고용
    global gold
    buyCard = buyList[boughtNumber]
    if 3 <= gold:
        gold -= 3
        playerCard.append(buyCard)
        playerGround.append(buyCard)
        if playerCard.count(buyCard) == 3:
            for i in range(3):
                playerCard.remove(buyCard)
                putDown(buyCard)
            playerGoldenCard.append(buyCard)
        buyList.remove(buyCard)
        printText()
    else:
        print('error')

def putDown(cardNum):
    if len(playerGround)!=7:
        playerGround.append(cardList[cardNum])

def attack(attackerNum, whoTurn):  # 공격(공격하는 유닛, 플레이어)
    global playerGround, opponentGround
    tauntArr = []  # taunted enemy list
    if whoTurn == "player":
        for i in range(len(opponentGround)):
            if opponentGround[i].ability == 4:
                tauntArr.append(i)
        if len(tauntArr) != 0:
            tmp = rd.randint(0, len(tauntArr))
            opponentGround[tauntArr[tmp]].fighthealth -= playerGround[attackerNum].attack
            playerGround[attackerNum].fighthealth -= opponentGround[tauntArr[tmp]].attack
        else:
            tmp = rd.randint(0, len(opponentGround))
            opponentGround[tauntArr[tmp]].fighthealth -= playerGround[attackerNum].attack
            playerGround[attackerNum].fighthealth -= opponentGround[tauntArr[tmp]].attack

    elif whoTurn == "opponent":
        for i in range(len(playerGround)):
            if playerGround[i].ability == 4:
                tauntArr.append(i)
        if len(tauntArr) != 0:
            tmp = rd.randint(0, len(tauntArr))
            playerGround[tauntArr[tmp]].fighthealth -= opponentGround[attackerNum].attack
            opponentGround[attackerNum].fighthealth -= playerGround[tauntArr[tmp]].attack
        else:
            tmp = rd.randint(0, len(opponentGround))
            playerGround[tauntArr[tmp]].fighthealth -= opponentGround[attackerNum].attack
            opponentGround[attackerNum].fighthealth -= playerGround[tauntArr[tmp]].attack


def heroAbility(heroNumber): # 우두머리 능력
    global gold
    if gold > 1:
        pass

def fightTurn():  # 전투 단계
    screen.fill(BLACK)
    global playerGround, opponentGround, p2Ground, p3Ground, p4Ground
    tmp = rd.randint(1, 4)  # 어떤 상대와 싸우는지 정함
    first = 0  # first=1이면 내가 선공, 0이면 상대가 선공
    #if tmp == 1:
    #    opponentGround = copy.deepcopy(p2Ground)
    #elif tmp == 2:
    #    opponentGround = copy.deepcopy(p3Ground)
    #elif tmp == 3:
    #    opponentGround = copy.deepcopy(p4Ground)
    print(len(opponentGround))
    if len(opponentGround) > len(playerGround):
        first = "player"
    elif len(opponentGround) == len(playerGround):
        tmp = rd.randint(0, 2)
        if tmp == 0:
            first = "player"
        elif tmp == 1:
            first = "opponent"
    else:
        first = "opponent"
    for i in range(len(playerGround)):
        screen.blit(playerGround[i].img,(i*130, 300))
    for i in range(len(opponentGround)):
        screen.blit(opponentGround[i].img, (i*130,0))


    # 여기까지 선공 정하기 구현
    if first == "player":
        for i in range(0, 7, 1):
            if i > len(opponentGround) - 1:
                if i > len(playerGround) - 1:
                    break
                else:
                    attack(i, "player")
            else:
                attack(i, "opponent")
                if i > len(playerGround) - 1:
                    continue
                else:
                    attack(i, "player")
    else:
        for i in range(0, 7, 1):
            if i > len(playerGround) - 1:
                if i > len(opponentGround) - 1:
                    break
                else:
                    attack(i, "opponent")
            else:
                attack(i, "player")
                if i > len(opponentGround) - 1:
                    continue
                else:
                    attack(i, "opponent")

def buyTurn():  # 고용 단계
    global gold, max_gold, upgrade_cost, max_gold, upgraded, freezed, shopCard_number, sec, Round, opponentGround, tempGround
    Round += 1

    start_time = time.time()
    end_time = 0
    gold = max_gold
    if not freezed:
        reset()
    if not upgraded:
        if upgrade_cost > 1:
            upgrade_cost -= 1
    if max_gold < 10:
        max_gold += 1
    printText()
    sec = 1
    startTimer()
    opponentGround=tempGround[Round-1].split()
    opponentGround=list(map(int,opponentGround))
    print(opponentGround[0])
    print(len(opponentGround))
    while end_time - start_time < 20:
        end_time = time.time()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                col = event.pos[0]
                row = event.pos[1]
                if col >= 150 and col <= 200 and row >= 0 and row <= 50: # reroll
                    if gold>0:
                        gold-=1
                        reset()
                elif col >= 210 and col <= 260 and row >= 0 and row <= 50: # upgrade
                    upgrade()
                elif col >= 270 and col <= 320 and row >= 0 and row <= 50: # freeze
                    freeze()
                print(col, row)
            elif event.type == KEYDOWN:
                if event.key == pg.K_1:
                    if len(buyList) > 0:
                        buy(0)
                elif event.key == pg.K_2:
                    if len(buyList) > 1:
                        buy(1)
                elif event.key == pg.K_3:
                    if len(buyList) > 2:
                        buy(2)
                elif event.key == pg.K_4:
                    if len(buyList) > 3:
                        buy(3)
                elif event.key == pg.K_5:
                    if len(buyList) > 4:
                        buy(4)
                elif event.key == pg.K_6:
                    if len(buyList) > 5:
                        buy(5)
    fightTurn()
    upgraded = False

def init():  # init
    global upgrade_cost, shopLevel_cost, freezed, upgraded, gold, max_gold
    cardName_file = open('cardName.txt')
    cardStats_file = open('cardStats.txt')
    goldencardStats_file = open('goldencardStats.txt')
    opponentGround_file = open('op1.txt')

    i = 0
    upgrade_cost = shopLevel_cost[0]
    freezed = False
    upgraded = True
    max_gold = 3
    gold = max_gold

    # 카드 이름 입력
    while True:
        tmp = cardName_file.readline()
        tmp2 = cardStats_file.readline()
        tmp3 = goldencardStats_file.readline()
        tmp4 = opponentGround_file.readline()
        if not tmp: break
        tmp = tmp.strip()  # cardName.txt
        tmp2 = tmp2.strip().split()  # cardStats.txt
        tmp3 = tmp3.strip().split()  # goldencardStats.txt
        tempGround.append(tmp4)
        cardList.append(Card())
        cardList[i].name = tmp
        cardImg.append(pg.image.load('image/' + tmp + '.png'))
        cardImg[i] = pg.transform.scale(cardImg[i], (100, 120))
        cardList[i].img=cardImg[i]
        if i < 6:
            goldencardImg.append(pg.image.load('goldenimage/' + tmp + '.png'))
            goldencardImg[i] = pg.transform.scale(goldencardImg[i], (100, 120))

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
    # 영웅은 고정으로 진행(일단)
    buyTurn()

init()
done = False
while not done:
    for event in pg.event.get():
        if event.type == QUIT:
            done = True
        # elif event.type == KEYDOWN:
        elif event.type == MOUSEBUTTONDOWN:
            clicked = True
            # event.pos[0]: cell size_column
            # event.pos[1]: cell size_row
    pg.display.flip()