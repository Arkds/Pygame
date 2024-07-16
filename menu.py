import pygame
import os
from difficulty_menu import DifficultyMenu

class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Main Menu")
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.songs = ["Song 1", "Song 2", "Song 3"]
        self.current_song_index = 0
        self.show_instructions = False
        self.load_assets()

    def load_assets(self):
        assets_path = os.path.join(os.path.dirname(__file__), 'assets')
        self.background = pygame.image.load(os.path.join(assets_path, 'menu.png'))  # Ajusta el nombre de la imagen según sea necesario
        self.background = pygame.transform.scale(self.background, (1000, 600))  # Redimensiona la imagen al tamaño de la pantalla

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if not self.show_instructions:
                    if 400 <= x <= 600:
                        if 300 <= y <= 350:
                            difficulty_menu = DifficultyMenu(self, self.songs[self.current_song_index])
                            difficulty_menu.run()
                        elif 400 <= y <= 450:
                            self.show_instructions = True
                    elif 350 <= x <= 400 and 500 <= y <= 550:
                        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
                    elif 700 <= x <= 750 and 500 <= y <= 550:
                        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
                else:
                    if 450 <= x <= 550 and 500 <= y <= 550:
                        self.show_instructions = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))  # Dibujar la imagen de fondo
        if not self.show_instructions:
            title_text = self.font.render("Rhythm Game", True, (255, 255, 255))
            self.screen.blit(title_text, (630, 170))
            start_text = self.font.render("Start Game", True, (255, 255, 255))
            self.screen.blit(start_text, (450, 300))
            how_to_play_text = self.font.render("How to Play", True, (255, 255, 255))
            self.screen.blit(how_to_play_text, (450, 400))
            song_text = self.font.render(f"Song: {self.songs[self.current_song_index]}", True, (255, 255, 255))
            self.screen.blit(song_text, (450, 500))
            left_arrow_text = self.font.render("<", True, (255, 255, 255))
            self.screen.blit(left_arrow_text, (350, 500))
            right_arrow_text = self.font.render(">", True, (255, 255, 255))
            self.screen.blit(right_arrow_text, (700, 500))
        else:
            instructions_title_text = self.font.render("Cómo jugar:", True, (255, 255, 255))
            self.screen.blit(instructions_title_text, (450, 100))
            instructions_text = [
                "1. Las notas caen desde la parte superior de la pantalla.",
                "2. Presiona la tecla espacio cuando la nota llegue a la línea roja.",
                "3. No dejes que las notas pasen sin presionar la tecla.",
                "4. La barra de vida disminuye con cada nota fallada y aumenta con cada nota acertada."
            ]
            for i, line in enumerate(instructions_text):
                line_text = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(line_text, (100, 200 + i * 50))
            back_text = self.font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (450, 500))

if __name__ == "__main__":
    pygame.init()
    main_menu = MainMenu()
    main_menu.run()
    pygame.quit()
