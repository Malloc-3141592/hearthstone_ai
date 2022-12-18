import random
import pygame as pg
import sys
import gym
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.initializers import RandomUniform
from collections import deque

class DQN(tf.keras.Model):
    def __init__(self, action_size):
        super(DQN, self).__init__()
        self.fc1 = Dense(24, activation='relu')
        self.fc2 = Dense(24, activation='relu')
        self.fc_out = Dense(action_size, kernel_intializer=RandomUniform(-1e-3, 1e-3))

    def call(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        q = self.fc_out(x)
        return q

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.render=False

        self.state_size=state_size
        self.action_size=action_size

        self.discount_factor=0.99
        self.learning_rate=0.001
        self.epsilon=1.0
        self.epsilon_decay=0.999
        self.epsilon_min=0.01
        self.batch_size=64
        self.train_start=1000

        self.memory=deque(maxlen=2000)

        self.model=DQN(action_size)
        self.target_model=DQN(action_size)
        self.optimizer=Adam(lr=self.learning_rate)

        self.update_target_model()

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            q_value=self.model(state)
            return np.argmax(q_value[0])

    def append_sample(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_model(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon*=self.epsilon_decay


if __name__=='__main__':
    state_size=80 # 골드, 상점레벨, 상점카드(최대 5개), 전장 카드(최대 7개)
    action_size=10
    done=False
    while not done:
        action=0
        gameData=open('gamedata.txt', 'r')
        gold=int(gameData.readline())
        level=int(gameData.readline())
        buyCard=gameData.readline().split()
        playerCard=[]
        for i in range(7):
            playerCard.append([list(map(int, gameData.readline()))])
        gameData.close()

        gameAction=open('gameaction.txt', 'w')
        gameAction.write(action)
        gameAction.close()