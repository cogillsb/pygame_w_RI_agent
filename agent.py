# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 15:47:31 2023

@author: grace
"""

import numpy as np

import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.models import load_model
from collections import deque

class DQN:
    def __init__(self, env_dims, move_dims):
        self.env_dims = env_dims
        self.move_dims = move_dims
        self.memory  = deque(maxlen=2000)
        
        self.gamma = 0.85
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        #self.model        = self.create_model()
        #self.target_model = self.create_model()
        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model   = Sequential()
        model.add(Dense(24, input_dim=self.env_dims, activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.move_dims))
        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
         
            return np.random.randint(0,self.move_dims)
        return np.argmax(self.model(state)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 50
        #if len(self.memory) < batch_size: 
        #    return
        #print('batch full')
        if len(self.memory) < batch_size: return
        samples = random.sample(self.memory, batch_size)
        for m in self.memory:
            if (m[2] > 0) or (m[2] <-1):
                print (m[2])
                samples.append(m)       

        for i, sample in enumerate(samples):
            if i%10==0: print(i)
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state, verbose=0)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state, verbose=0)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

