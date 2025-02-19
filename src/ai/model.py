import tensorflow as tf
import numpy as np


class DQNModel:
    def __init__(self, state_size, action_size):
        """
        Deep Q-Network (DQN) modelini oluşturur

        Args:
            state_size (int): Giriş katmanının boyutu (durum vektörünün uzunluğu)
            action_size (int): Çıkış katmanının boyutu (olası hareket sayısı)
        """
        self.state_size = state_size  # Durumun boyutu (giriş)
        self.action_size = action_size  # Aksiyonların sayısı (çıkış)
        self.model = self._build_model()

    def _build_model(self):
        """
        Sinir ağı modelini oluşturur
        """
        model = tf.keras.Sequential([
            # Giriş katmanı
            tf.keras.layers.Dense(64, input_dim=self.state_size, activation='relu'),

            # Gizli katman
            tf.keras.layers.Dense(64, activation='relu'),

            # Çıkış katmanı
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])

        # Modeli derle
        model.compile(
            loss='mse',  # Mean Squared Error kayıp fonksiyonu
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001)  # Adam optimizasyon
        )

        return model

    def predict(self, state):
        """
        Verilen durum için Q-değerlerini tahmin eder
        """
        return self.model.predict(state, verbose=0)

    def train(self, states, targets):
        """
        Modeli verilen veri ile eğitir
        """
        return self.model.fit(states, targets, epochs=1, verbose=0)