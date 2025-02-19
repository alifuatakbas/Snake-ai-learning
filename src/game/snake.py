from typing import List, Tuple  # Type hinting için
from enum import Enum  # Sabit değerler için
from .constants import GRID_WIDTH, GRID_HEIGHT  # Oyun sabitleri


class Direction(Enum):
    """
    Yılanın hareket yönlerini temsil eden enum sınıfı
    Her yön bir x,y koordinat çifti ile temsil edilir
    """
    RIGHT = (1, 0)  # x+1: sağa hareket
    LEFT = (-1, 0)  # x-1: sola hareket
    UP = (0, -1)  # y-1: yukarı hareket
    DOWN = (0, 1)  # y+1: aşağı hareket


class Snake:
    """
    Yılan sınıfı: Oyundaki yılanın tüm özelliklerini ve davranışlarını içerir
    """

    def __init__(self, initial_position: Tuple[int, int], initial_length: int = 3):
        """
        Yılan nesnesini başlatır
        Args:
            initial_position (Tuple[int, int]): Başlangıç pozisyonu (x, y)
            initial_length (int): Başlangıç uzunluğu (varsayılan: 3)
        """
        # Yılanın başlangıç yönü
        self.direction = Direction.RIGHT

        # Yılanın vücut parçalarını tutan liste
        # Her parça (x,y) koordinat çifti olarak saklanır
        self.body = []

        # Başlangıç pozisyonunu al
        x, y = initial_position

        # Yılanın başlangıç vücudunu oluştur
        # İlk parça (kafa) initial_position'da, diğerleri sola doğru uzanır
        for i in range(initial_length):
            self.body.append((x - i, y))

    def move(self) -> bool:
        """
        Yılanı mevcut yönde hareket ettirir
        Returns:
            bool: Hareket başarılı ise True, çarpışma varsa False
        """
        # Yeni kafa pozisyonu
        new_head = (
            self.body[0][0] + self.direction.value[0],
            self.body[0][1] + self.direction.value[1]
        )

        # Duvara çarpma kontrolü
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False

        # Kendine çarpma kontrolü
        if new_head in self.body[1:]:
            return False

        self.body.insert(0, new_head)
        self.body.pop()
        return True
    def grow(self):
        """
        Yılanı bir birim büyütür
        Yem yediğinde çağrılır
        """
        # Kuyruğun son pozisyonunu tekrarla
        # Bir sonraki move() çağrısında bu parça yeni pozisyona geçecek
        self.body.append(self.body[-1])

    def change_direction(self, new_direction: Direction):
        """
        Yılanın yönünü değiştirir
        Args:
            new_direction (Direction): Yeni yön
        """
        # Zıt yönlere anlık dönüşü engelle
        opposite_directions = {
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP
        }

        # Eğer yeni yön, mevcut yönün zıttı değilse yönü değiştir
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def get_head(self) -> Tuple[int, int]:
        """
        Yılanın kafa pozisyonunu döndürür
        Returns:
            Tuple[int, int]: Kafa pozisyonu (x, y)
        """
        return self.body[0]