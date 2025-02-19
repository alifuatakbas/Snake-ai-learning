import numpy as np
from .agent import DQNAgent
from ..game.game_state import GameState
from ..game.snake import Direction


class Trainer:
    def __init__(self):
        self.game_state = GameState()
        self.width = 40
        self.height = 30
        self.state_size = 11
        self.action_size = 4
        self.episodes = 1000
        self.agent = DQNAgent(self.state_size, self.action_size)
        self.scores = []
        self.mean_scores = []

    def _get_right_direction(self, direction):
        """Verilen yönün sağındaki yönü döndürür"""
        if direction == Direction.UP:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.LEFT
        return Direction.UP

    def _get_left_direction(self, direction):
        """Verilen yönün solundaki yönü döndürür"""
        if direction == Direction.UP:
            return Direction.LEFT
        elif direction == Direction.LEFT:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.RIGHT
        return Direction.UP

    def _is_direction_dangerous(self, game_state, direction):
        """Belirli bir yönün tehlikeli olup olmadığını kontrol eder"""
        snake = game_state.snake
        head = snake.get_head()
        next_pos = (
            head[0] + direction.value[0],
            head[1] + direction.value[1]
        )

        # Duvar kontrolü
        if (next_pos[0] < 0 or next_pos[0] >= self.width or
                next_pos[1] < 0 or next_pos[1] >= self.height):
            return True

        # Kuyruk kontrolü
        if next_pos in snake.body[1:]:
            return True

        return False

    def get_state(self, game_state):
        """Oyun durumunu AI'ın anlayabileceği formata çevirir"""
        snake = game_state.snake
        food = game_state.food
        head = snake.get_head()

        # Tehlike kontrolü
        danger_straight = self._is_direction_dangerous(game_state, snake.direction)
        danger_right = self._is_direction_dangerous(game_state, self._get_right_direction(snake.direction))
        danger_left = self._is_direction_dangerous(game_state, self._get_left_direction(snake.direction))

        # Yem yönü
        food_left = food.position[0] < head[0]
        food_right = food.position[0] > head[0]
        food_up = food.position[1] < head[1]
        food_down = food.position[1] > head[1]

        return np.array([
            danger_straight,
            danger_right,
            danger_left,
            snake.direction == Direction.UP,
            snake.direction == Direction.DOWN,
            snake.direction == Direction.LEFT,
            snake.direction == Direction.RIGHT,
            food_left,
            food_right,
            food_up,
            food_down
        ], dtype=int)


    def train(self):
        """AI'ı eğitir"""
        from ..ui.game_window import GameWindow
        from ..game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, BLACK, GREEN, RED, WHITE
        import pygame
        import time

        # Pencere boyutunu yan panel için genişlet
        PANEL_WIDTH = 200
        total_width = WINDOW_WIDTH + PANEL_WIDTH
        screen = pygame.display.set_mode((total_width, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake AI Training")
        clock = pygame.time.Clock()
        BACKGROUND_COLOR = (10, 10, 10)

        # Font ayarları
        font = pygame.font.Font(None, 24)

        # Hız kontrolü için değişkenler
        speeds = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        speed_index = 0
        current_speed = speeds[speed_index]
        base_fps = 30  # Temel FPS değeri
        paused = False


        def draw_panel():
            """Yan paneli çizer"""
            # Panel arkaplanı
            panel_rect = pygame.Rect(WINDOW_WIDTH, 0, PANEL_WIDTH, WINDOW_HEIGHT)
            pygame.draw.rect(screen, (30, 30, 30), panel_rect)
            pygame.draw.line(screen, (50, 50, 50), (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT), 2)

            # Bilgileri yazdır
            y_pos = 20
            line_height = 30
            texts = [
                f"Episode: {episode}",
                f"Score: {score}",
                f"High Score: {max(self.scores) if self.scores else 0}",
                f"Mean Score: {self.mean_scores[-1]:.1f}" if self.mean_scores else "Mean Score: 0",
                "",
                f"Speed: {current_speed}x",
                f"Epsilon: {self.agent.epsilon:.4f}",
                f"Batch Size: {self.agent.batch_size}",
                f"Memory Size: {len(self.agent.memory)}",
                "",
                "Controls:",
                "↑/↓: Change Speed",
                "Space: Pause",
                "Esc: Menu"
            ]

            for text in texts:
                text_surface = font.render(text, True, WHITE)
                screen.blit(text_surface, (WINDOW_WIDTH + 10, y_pos))
                y_pos += line_height

        action_to_direction = {
            0: Direction.UP,
            1: Direction.DOWN,
            2: Direction.LEFT,
            3: Direction.RIGHT
        }

        try:
            for episode in range(self.episodes):
                game_state = GameState()
                state = self.get_state(game_state)
                done = False
                score = 0
                prev_length = len(game_state.snake.body)

                while not done:
                    # Sabit FPS kontrolü
                    clock.tick(base_fps)
                    # Pygame eventlerini kontrol et
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_UP:
                                speed_index = min(speed_index + 1, len(speeds) - 1)
                                current_speed = speeds[speed_index]
                                print(f"Hız artırıldı: {current_speed}x")
                            elif event.key == pygame.K_DOWN:
                                speed_index = max(speed_index - 1, 0)
                                current_speed = speeds[speed_index]
                                print(f"Hız azaltıldı: {current_speed}x")
                            elif event.key == pygame.K_SPACE:
                                paused = not paused
                            elif event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                return "menu"

                    # Episode içindeki döngüde
                    if not paused:
                        for _ in range(current_speed):  # Bu döngü her adımda birden fazla güncelleme yapıyor
                            action = self.agent.act(state)
                            direction = action_to_direction[action]
                            game_state.change_direction(direction)

                            if not game_state.update():
                                reward = -10
                                done = True
                                break
                            else:
                                current_length = len(game_state.snake.body)
                                if current_length > prev_length:
                                    reward = 10
                                    score += 1
                                    prev_length = current_length
                                else:
                                    reward = 0

                            next_state = self.get_state(game_state)
                            self.agent.remember(state, action, reward, next_state, done)
                            self.agent.replay()  # Her adımda epsilon güncelleniyor!
                            state = next_state# Episode sonunda epsilon güncellenir

                    screen.fill(BACKGROUND_COLOR)

                    # Grid çiz
                    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
                        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
                    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
                        pygame.draw.line(screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

                    # Yılanı çiz
                    for segment in game_state.snake.body:
                        pygame.draw.rect(screen, GREEN,
                                         (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                                          GRID_SIZE - 1, GRID_SIZE - 1))

                    # Yemi çiz
                    food_pos = game_state.food.position
                    pygame.draw.rect(screen, RED,
                                     (food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE,
                                      GRID_SIZE - 1, GRID_SIZE - 1))

                    # Yan paneli çiz
                    draw_panel()

                    if paused:
                        pause_text = font.render("PAUSED", True, WHITE)
                        text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                        screen.blit(pause_text, text_rect)

                    pygame.display.flip()
                 # FPS'i hıza göre ayarla

                self.scores.append(score)
                mean_score = np.mean(self.scores[-100:])
                self.mean_scores.append(mean_score)
                self.agent.end_episode()  # Episode sonunda epsilon güncelle

                if episode % 100 == 0:
                    print(
                        f'Episode: {episode}, Score: {score}, Average Score: {mean_score:.2f}, Epsilon: {self.agent.epsilon:.2f}')

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
        finally:
            pygame.quit()
            return "menu"