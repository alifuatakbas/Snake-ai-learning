import pygame
from typing import Tuple
from ..game.game_state import GameState
from ..game.snake import Direction
from ..game.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    BLACK, WHITE, RED, GREEN
)


class GameWindow:
    """
    Oyunun görsel arayüzünü yöneten sınıf
    Pygame kullanarak oyunu ekrana çizer
    """

    def __init__(self):
        """
        Pygame penceresini ve gerekli değişkenleri başlatır
        """
        # Pygame'i başlat
        pygame.init()

        # Pencereyi oluştur
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")

        # Saat oluştur (FPS kontrolü için)
        self.clock = pygame.time.Clock()

        # Oyun durumunu başlat
        self.game_state = GameState()

        # Font oluştur
        self.font = pygame.font.Font(None, 36)
        self.reset_button = None  # Reset butonu için rect
        self.collision_frame = 0  # Çarpışma animasyonu için frame sayacı
        self.collision_point = None
        self.collision_type = None

    def _create_button(self, text: str, center_pos: Tuple[int, int]) -> Tuple[pygame.Surface, pygame.Rect]:
        """
        Özel bir buton oluşturur
        """
        # Buton renkleri
        button_color = (34, 139, 34)  # Koyu yeşil
        text_color = (255, 255, 255)  # Beyaz

        # Buton metni
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect()

        # Buton boyutları
        padding = 20
        button_width = text_rect.width + padding * 2
        button_height = text_rect.height + padding

        # Buton pozisyonu
        button_rect = pygame.Rect(0, 0, button_width, button_height)
        button_rect.center = center_pos

        return (text_surface, button_rect)

    def _draw_grid(self):
        """
        Oyun gridini yarı şeffaf çizer
        """
        # Yarı şeffaf grid rengi (RGB + Alpha)
        grid_color = (255, 255, 255, 30)  # Beyaz renk, düşük alpha değeri

        # Yarı şeffaf çizim için surface oluştur
        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        # Dikey çizgiler
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(grid_surface, grid_color, (x, 0), (x, WINDOW_HEIGHT), 1)

        # Yatay çizgiler
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(grid_surface, grid_color, (0, y), (WINDOW_WIDTH, y), 1)

        # Yarı şeffaf grid'i ana ekrana blit et
        self.screen.blit(grid_surface, (0, 0))

    def _draw_snake(self, snake_body: list):
        """
        Yılanı gelişmiş grafiklerle çizer
        """
        for i, segment in enumerate(snake_body):
            center = (
                segment[0] * GRID_SIZE + GRID_SIZE // 2,
                segment[1] * GRID_SIZE + GRID_SIZE // 2
            )

            # Yılan kafası
            if i == 0:
                # Ana daire (kafa)
                pygame.draw.circle(self.screen, (50, 205, 50), center, GRID_SIZE // 2 - 2)

                # Gözler
                eye_color = (255, 255, 255)  # Beyaz
                eye_radius = 3

                # Göz pozisyonları (yönüne göre)
                if self.game_state.snake.direction == Direction.RIGHT:
                    eye_pos1 = (center[0] + 3, center[1] - 5)
                    eye_pos2 = (center[0] + 3, center[1] + 5)
                elif self.game_state.snake.direction == Direction.LEFT:
                    eye_pos1 = (center[0] - 3, center[1] - 5)
                    eye_pos2 = (center[0] - 3, center[1] + 5)
                elif self.game_state.snake.direction == Direction.UP:
                    eye_pos1 = (center[0] - 5, center[1] - 3)
                    eye_pos2 = (center[0] + 5, center[1] - 3)
                else:  # DOWN
                    eye_pos1 = (center[0] - 5, center[1] + 3)
                    eye_pos2 = (center[0] + 5, center[1] + 3)

                # Gözleri çiz
                pygame.draw.circle(self.screen, eye_color, eye_pos1, eye_radius)
                pygame.draw.circle(self.screen, eye_color, eye_pos2, eye_radius)

                # Göz bebekleri (siyah)
                pupil_color = (0, 0, 0)
                pupil_radius = 1.5
                pygame.draw.circle(self.screen, pupil_color, eye_pos1, pupil_radius)
                pygame.draw.circle(self.screen, pupil_color, eye_pos2, pupil_radius)

            # Vücut parçaları
            else:
                # Gölge efekti
                shadow_offset = 2
                pygame.draw.circle(
                    self.screen,
                    (20, 20, 20),
                    (center[0] + shadow_offset, center[1] + shadow_offset),
                    GRID_SIZE // 2 - 4
                )

                # Vücut parçası (koyudan açığa geçiş)
                color_ratio = 1 - (i / len(snake_body))  # 0 ile 1 arası değer
                green_value = int(155 * color_ratio + 100)  # 100 ile 255 arası
                body_color = (34, green_value, 34)
                pygame.draw.circle(self.screen, body_color, center, GRID_SIZE // 2 - 4)

    def _draw_food(self, position: Tuple[int, int]):
        """
        Yemi daire şeklinde çizer
        """
        center = (
            position[0] * GRID_SIZE + GRID_SIZE // 2,
            position[1] * GRID_SIZE + GRID_SIZE // 2
        )
        pygame.draw.circle(self.screen, RED, center, GRID_SIZE // 2 - 4)

    def _draw_score(self, score: int):
        """
        Skoru ekrana çizer
        Args:
            score (int): Güncel skor
        """
        score_text = self.font.render(f'Score: {score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def _handle_input(self):
        """
        Kullanıcı girdilerini işler
        Returns:
            bool: Oyun devam ediyorsa True, çıkış istendiyse False
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game_state.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.game_state.change_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.game_state.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.game_state.change_direction(Direction.RIGHT)
        return True

    def _draw_collision_effect(self):
        """
        Çarpışma efektini çizer
        """
        if self.collision_point and self.collision_frame < 10:  # 10 frame'lik animasyon
            # Büyüyen kırmızı daire efekti
            radius = (self.collision_frame + 1) * 3
            center = (
                self.collision_point[0] * GRID_SIZE + GRID_SIZE // 2,
                self.collision_point[1] * GRID_SIZE + GRID_SIZE // 2
            )

            # Yanıp sönen efekt için alpha değeri
            alpha = 255 - (self.collision_frame * 25)

            # Yarı saydam surface
            effect_surface = pygame.Surface((GRID_SIZE * 4, GRID_SIZE * 4), pygame.SRCALPHA)

            # Çarpışma tipine göre renk seç
            if self.collision_type == "wall":
                color = (255, 0, 0, alpha)  # Kırmızı (duvar çarpışması)
            else:
                color = (255, 165, 0, alpha)  # Turuncu (kuyruk çarpışması)

            # Efekti çiz
            pygame.draw.circle(effect_surface, color,
                               (GRID_SIZE * 2, GRID_SIZE * 2), radius)

            # Efekti ekrana blit et
            self.screen.blit(effect_surface,
                             (center[0] - GRID_SIZE * 2, center[1] - GRID_SIZE * 2))

            self.collision_frame += 1

    def run(self):
        """
        Ana oyun döngüsü
        Returns:
            str: "menu" (ana menüye dön) veya "quit" (çık)
        """
        running = True
        BACKGROUND_COLOR = (10, 10, 10)

        while running:
            running = self._handle_input()

            # Oyun durumunu güncelle
            if not self.game_state.update():
                if self.game_state.is_game_over():
                    # Çarpışma noktasını ve tipini al
                    self.collision_point = self.game_state.get_collision_point()
                    self.collision_type = self.game_state.get_collision_type()

                    # Çarpışma animasyonunu göster
                    while self.collision_frame < 10:
                        self.screen.fill(BACKGROUND_COLOR)
                        state = self.game_state.get_state()

                        self._draw_grid()
                        self._draw_snake(state['snake_body'])
                        self._draw_food(state['food_position'])
                        self._draw_score(state['score'])
                        self._draw_collision_effect()

                        pygame.display.flip()
                        pygame.time.wait(50)

                    # Game Over ekranını göster
                    result = self._show_game_over()
                    if result == "retry":
                        # Oyunu sıfırla
                        self.game_state = GameState()
                        self.collision_frame = 0
                        self.collision_point = None
                        continue
                    elif result == "menu":
                        return "menu"
                    else:  # quit
                        return "quit"

            self.screen.fill(BACKGROUND_COLOR)
            state = self.game_state.get_state()

            self._draw_grid()
            self._draw_snake(state['snake_body'])
            self._draw_food(state['food_position'])
            self._draw_score(state['score'])

            pygame.display.flip()
            self.clock.tick(10)

        return "quit"
    def _show_game_over(self):
        """
        Oyun sonu ekranını gösterir ve buton tıklamasını bekler
        Returns:
            str: "retry" (tekrar dene), "menu" (ana menüye dön) veya "quit" (çık)
        """
        # Game Over yazısı
        text = self.font.render('Game Over!', True, WHITE)
        score_text = self.font.render(
            f'Final Score: {self.game_state.get_score()}',
            True, WHITE
        )

        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Butonlar
        retry_text, retry_rect = self._create_button(
            "Tekrar Dene",
            (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 + 50)
        )

        menu_text, menu_rect = self._create_button(
            "Ana Menü",
            (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2 + 50)
        )

        waiting = True
        while waiting:
            # Event kontrolü
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(event.pos):
                        return "retry"
                    if menu_rect.collidepoint(event.pos):
                        return "menu"

            # Ekranı temizle
            self.screen.fill(BLACK)

            # Game Over ekranını çiz
            self.screen.blit(text, text_rect)
            self.screen.blit(score_text, score_rect)

            # Butonları çiz
            for button_text, button_rect in [(retry_text, retry_rect), (menu_text, menu_rect)]:
                # Buton arkaplanı
                pygame.draw.rect(self.screen, (34, 139, 34), button_rect)

                # Mouse butonun üzerindeyse highlight efekti
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (50, 205, 50), button_rect, 3)
                else:
                    pygame.draw.rect(self.screen, (0, 100, 0), button_rect, 3)

                # Buton metnini ortala
                text_rect = button_text.get_rect(center=button_rect.center)
                self.screen.blit(button_text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

        return "quit"
