from src.ui.menu import Menu
import pygame

def main():
    """
    Oyunu başlatan ana fonksiyon
    """
    try:
        menu = Menu()
        menu.run()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        print("Oyun kapatılıyor...")
        pygame.quit()

if __name__ == "__main__":
    main()