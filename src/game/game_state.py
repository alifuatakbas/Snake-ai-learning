from typing import Tuple, Optional
from .snake import Snake, Direction
from .food import Food
from .constants import GRID_WIDTH, GRID_HEIGHT


class GameState:
    """
    Oyun durumunu yöneten sınıf
    Snake ve Food sınıflarını koordine eder ve oyun mantığını yönetir
    """

    def __init__(self):
        """
        Oyun durumunu başlatır
        - Yılanı oluşturur
        - Yemi oluşturur
        - Skor ve oyun durumu değişkenlerini ayarlar
        """
        # Yılanı grid'in ortasında başlat
        initial_position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = Snake(initial_position)

        # Yemi oluştur
        self.food = Food()
        # Yılanın olmadığı bir konumda yem oluştur
        self.food.spawn(self.snake.body)

        # Oyun değişkenleri
        self.score = 0
        self.game_over = False
        self.collision_point = None
        self.collision_type = None

    def update(self) -> bool:
        """
        Oyun durumunu günceller
        - Yılanı hareket ettirir
        - Yem yeme kontrolü yapar
        - Skor günceller
        Returns:
            bool: Oyun devam ediyorsa True, bittiyse False
        """
        if self.game_over:
            return False

            # Yılanın yeni pozisyonunu hesapla
        new_head = (
            self.snake.body[0][0] + self.snake.direction.value[0],
            self.snake.body[0][1] + self.snake.direction.value[1]
        )

        # Duvar çarpışması kontrolü
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.collision_point = self.snake.body[0]
            self.collision_type = "wall"
            self.game_over = True
            return False

        # Kuyruk çarpışması kontrolü
        if new_head in self.snake.body[1:]:
            self.collision_point = new_head
            self.collision_type = "tail"
            self.game_over = True
            return False

        # Yılanı hareket ettir
        if not self.snake.move():
            self.game_over = True
            return False

        # Yem yeme kontrolü
        if self.snake.get_head() == self.food.get_position():
            # Yılanı büyüt
            self.snake.grow()
            # Skoru artır
            self.score += 1
            # Yeni yem oluştur
            self.food.spawn(self.snake.body)

        return True

    def change_direction(self, direction: Direction):
        """
        Yılanın yönünü değiştirir
        Args:
            direction (Direction): Yeni yön
        """
        self.snake.change_direction(direction)

    def get_state(self) -> dict:
        """
        Mevcut oyun durumunu döndürür
        Returns:
            dict: Oyun durumu bilgileri
        """
        return {
            'snake_body': self.snake.body,
            'food_position': self.food.get_position(),
            'score': self.score,
            'game_over': self.game_over
        }

    def is_game_over(self) -> bool:
        """
        Oyunun bitip bitmediğini kontrol eder
        Returns:
            bool: Oyun bittiyse True
        """
        return self.game_over

    def get_score(self) -> int:
        """
        Mevcut skoru döndürür
        Returns:
            int: Oyun skoru
        """
        return self.score

    def get_collision_point(self):
        """
        Çarpışma noktasını döndürür
        """
        return self.collision_point

    def get_collision_type(self):
        """
        Çarpışma tipini döndürür (wall/tail)
        """
        return self.collision_type