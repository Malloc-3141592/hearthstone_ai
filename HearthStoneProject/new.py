import sys
import numpy as np
import matplotlib.pyplot as plt
import os

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def main():
    x=[]
    y1=[]
    y2=[]
    y3=[]
    for i in range(1, 87):  # 트리 개수에 따라 변경
        j=1
        createDirectory('analyze')
        f2 = open('analyze/' + 'tree' + str(i) + '.txt', 'w')
        buy=0
        upgrade=0
        reroll=0
        plus, minus=0,0
        plus_t, minus_t=0,0
        while True:
            try:
                f1 = open('tree' + str(i) + '/' + 'node_' + str(j) + '.txt', 'r')
                state=f1.readline()
                f1.readline()
                f1.readline()
                plus, minus = map(int, f1.readline().strip().split())
                action = list(map(int, f1.readline().strip().split()))
                f1.close()
                if j==1:
                    plus_t, minus_t=plus, minus
                    x.append(plus-minus)
                if action[0] == 1:
                    buy += 1
                elif action[0] == 2:
                    upgrade += 1
                elif action[0] == 3:
                    reroll += 1
            except:
                break
        f2.write('buy : ' + str(buy) + '\n')
        f2.write('upgrade : ' + str(upgrade) + '\n')
        f2.write('reroll : ' + str(reroll) + '\n\n')
        y1.append(buy)
        y2.append(upgrade)
        y3.append(reroll)
        f2.write(str(plus_t)+' - '+str(minus_t)+' = '+str(plus_t-minus_t))
        f2.close()

main()