import pygame
from typing import List, Tuple
from .game_window import GameWindow
from ..game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE
import matplotlib.pyplot as plt


class Menu:
    def __init__(self):
        """Menü penceresini başlatır"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Menu")

        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

        # Menü seçenekleri
        self.options = [
            "İnsan Oyuncusu",
            "AI Eğitimi",
            "Çıkış"
        ]

        # Arkaplan rengi
        self.bg_color = (10, 10, 10)

        # Buton renkleri
        self.button_colors = {
            'normal': (34, 139, 34),
            'hover': (50, 205, 50),
            'text': WHITE
        }

    def _create_button(self, text: str, center_pos: Tuple[int, int], selected: bool) -> Tuple[
        pygame.Surface, pygame.Rect]:
        """Özel bir buton oluşturur"""
        padding = 20
        text_surface = self.font.render(text, True, self.button_colors['text'])
        text_rect = text_surface.get_rect()

        button_width = text_rect.width + padding * 2
        button_height = text_rect.height + padding

        button_rect = pygame.Rect(0, 0, button_width, button_height)
        button_rect.center = center_pos

        return (text_surface, button_rect)

    def _show_game_instructions(self):
        """Oyun talimatlarını gösterir"""
        print("Snake Game başlatılıyor...")
        print("Kontroller:")
        print("- Ok tuşları ile yılanı yönlendir")
        print("- Pencereyi kapatmak için X tuşuna bas")

    def _show_training_progress(self, trainer):
        """Eğitim sonuçlarını gösterir"""
        plt.figure(figsize=(12, 5))
        plt.plot(trainer.scores, label='Score', alpha=0.4)
        plt.plot(trainer.mean_scores, label='Mean Score', color='red')
        plt.title('Training Progress')
        plt.xlabel('Episode')
        plt.ylabel('Score')
        plt.legend()
        plt.show()

    def run(self) -> None:
        """Menüyü çalıştırır ve seçilen opsiyonu işler"""
        running = True
        clock = pygame.time.Clock()

        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, option in enumerate(self.options):
                        button_pos = (WINDOW_WIDTH // 2, 200 + i * 100)
                        _, button_rect = self._create_button(option, button_pos, False)

                        if button_rect.collidepoint(mouse_pos):
                            if i == 0:  # İnsan Oyuncusu
                                self._show_game_instructions()
                                game = GameWindow()
                                result = game.run()

                                # Eğer menüye dönüş istendiyse
                                if result == "menu":
                                    # Ekranı yeniden oluştur
                                    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                                    pygame.display.set_caption("Snake Game - Menu")
                                    continue  # Menü döngüsüne devam et
                                elif result == "quit":
                                    running = False
                                    break

                            elif i == 1:  # AI Eğitimi
                                print("AI Eğitimi başlatılıyor...")
                                from ..ai.trainer import Trainer
                                trainer = Trainer()
                                trainer.train()
                                print("Eğitim tamamlandı!")
                                self._show_training_progress(trainer)

                                # Eğitim sonrası menüye dön
                                self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                                pygame.display.set_caption("Snake Game - Menu")
                                continue

                            else:  # Çıkış
                                running = False
                                break

            # Ekranı temizle
            self.screen.fill(self.bg_color)

            # Başlığı çiz
            title = self.font.render("Snake Game", True, WHITE)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)

            # Butonları çiz
            for i, option in enumerate(self.options):
                button_pos = (WINDOW_WIDTH // 2, 200 + i * 100)
                text_surface, button_rect = self._create_button(option, button_pos, False)

                # Mouse butonun üzerindeyse
                if button_rect.collidepoint(mouse_pos):
                    button_color = self.button_colors['hover']
                else:
                    button_color = self.button_colors['normal']

                pygame.draw.rect(self.screen, button_color, button_rect)
                pygame.draw.rect(self.screen, (0, 100, 0), button_rect, 3)

                text_rect = text_surface.get_rect(center=button_rect.center)
                self.screen.blit(text_surface, text_rect)

            # Alt bilgi
            info_text = self.small_font.render("Ok tuşları ile hareket et, ESC ile çık", True, WHITE)
            info_rect = info_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            self.screen.blit(info_text, info_rect)

            pygame.display.flip()
            clock.tick(60)