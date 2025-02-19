import numpy as np
import random
from .model import DQNModel
from .memory import ReplayMemory


class DQNAgent:
    def __init__(self, state_size, action_size):
        """
        DQN ajanını başlatır

        Args:
            state_size: Durum vektörünün boyutu
            action_size: Olası hareket sayısı
        """
        self.state_size = state_size
        self.action_size = action_size

        # Öğrenme parametreleri
        self.gamma = 0.99  # Gelecek ödüllerin değer kaybı oranı
        self.epsilon = 1.0  # Keşif oranı
        self.epsilon_min = 0.0 # Minimum keşif oranı
        self.epsilon_decay = 0.99  # Keşif oranı azalma katsayısı
        self.batch_size = 64  # Eğitim için örnek sayısı
        self.episode_count = 0

        # Model ve bellek
        self.model = DQNModel(state_size, action_size)
        self.memory = ReplayMemory(10000)

    def act(self, state):
        """
        Mevcut duruma göre bir hareket seçer

        Args:
            state: Mevcut durum
        Returns:
            seçilen hareket
        """
        if random.random() <= self.epsilon:
            # Keşif: Rastgele hareket
            return random.randrange(self.action_size)

        # Sömürü: En iyi hareketi seç
        state = np.array([state])
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def remember(self, state, action, reward, next_state, done):
        """
        Deneyimi belleğe kaydeder
        """
        self.memory.add(state, action, reward, next_state, done)

    def replay(self):
        """Sadece eğitim yapar, epsilon güncellemez"""
        if len(self.memory) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)
        targets = self.model.predict(states)
        next_q_values = self.model.predict(next_states)

        for i in range(self.batch_size):
            if dones[i]:
                target = rewards[i]
            else:
                target = rewards[i] + self.gamma * np.amax(next_q_values[i])
            targets[i][actions[i]] = target

        self.model.train(states, targets)

    def end_episode(self):
        """Episode sonunda çağrılır"""
        self.episode_count += 1
        old_epsilon = self.epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        print(f"Episode {self.episode_count}: Epsilon {old_epsilon:.4f} -> {self.epsilon:.4f}")