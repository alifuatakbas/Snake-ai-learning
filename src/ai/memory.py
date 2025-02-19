import numpy as np
from collections import deque
import random


class ReplayMemory:
    def __init__(self, max_size=2000):
        """
        Deneyim tekrarı için bellek yapısı

        Args:
            max_size: Maksimum deneyim sayısı (varsayılan: 2000)
        """
        self.buffer = deque(maxlen=max_size)

    def add(self, state, action, reward, next_state, done):
        """
        Yeni bir deneyimi belleğe ekler

        Args:
            state: Mevcut durum
            action: Yapılan hareket
            reward: Alınan ödül
            next_state: Sonraki durum
            done: Oyun bitti mi
        """
        experience = (state, action, reward, next_state, done)
        self.buffer.append(experience)

    def sample(self, batch_size=32):
        """
        Bellekten rastgele deneyimler örnekler

        Args:
            batch_size: Örneklenecek deneyim sayısı
        Returns:
            states, actions, rewards, next_states, dones
        """
        if batch_size > len(self.buffer):
            batch_size = len(self.buffer)

        batch = random.sample(self.buffer, batch_size)

        states = np.array([experience[0] for experience in batch])
        actions = np.array([experience[1] for experience in batch])
        rewards = np.array([experience[2] for experience in batch])
        next_states = np.array([experience[3] for experience in batch])
        dones = np.array([experience[4] for experience in batch])

        return states, actions, rewards, next_states, dones

    def __len__(self):
        """
        Bellekteki deneyim sayısını döndürür
        """
        return len(self.buffer)