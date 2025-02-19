import random
from typing import Tuple, List
from .constants import GRID_WIDTH, GRID_HEIGHT

class Food:
    """
    Yem sınıfı: Oyundaki yemlerin konumunu ve davranışını yönetir
    """
    def __init__(self):
        """
        Yem nesnesini başlatır
        İlk yem rastgele bir konumda oluşturulur
        """
        self.position = self._generate_position()

    def _generate_position(self) -> Tuple[int, int]:
        """
        Yem için rastgele bir konum oluşturur
        Returns:
            Tuple[int, int]: Yemin yeni konumu (x, y)
        """
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)

    def spawn(self, snake_body: List[Tuple[int, int]]):
        """
        Yeni bir yem oluşturur
        Yemin yılanın vücudunda olmadığından emin olur
        Args:
            snake_body (List[Tuple[int, int]]): Yılanın vücut koordinatları
        """
        while True:
            new_position = self._generate_position()
            # Yem yılanın vücudunda değilse kabul et
            if new_position not in snake_body:
                self.position = new_position
                break

    def get_position(self) -> Tuple[int, int]:
        """
        Yemin mevcut konumunu döndürür
        Returns:
            Tuple[int, int]: Yemin konumu (x, y)
        """
        return self.position