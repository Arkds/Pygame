import pygame
from game import Game

class DifficultyMenu:
    def __init__(self, main_menu, song):
        self.main_menu = main_menu
        self.song = song
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Select Difficulty")
        self.font = pygame.font.Font(None, 36)
        self.running = True

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
                if 400 <= x <= 600:
                    if 100 <= y <= 150:
                        game = Game(level=1, difficulty='easy', main_menu=self.main_menu, song=self.song)  # Nivel fijo como 1 para ejemplo
                        game.run()
                    elif 200 <= y <= 250:
                        game = Game(level=1, difficulty='medium', main_menu=self.main_menu, song=self.song)
                        game.run()
                    elif 300 <= y <= 350:
                        game = Game(level=1, difficulty='hard', main_menu=self.main_menu, song=self.song)
                        game.run()
                    elif 400 <= y <= 450:
                        game = Game(level=1, difficulty='expert', main_menu=self.main_menu, song=self.song)
                        game.run()
                if 10 <= x <= 110 and 10 <= y <= 60:  # Botón "Atrás"
                    self.running = False

    def draw(self):
        self.screen.fill((250, 0, 0))
        easy_text = self.font.render("Easy", True, (255, 255, 255))
        self.screen.blit(easy_text, (450, 100))
        medium_text = self.font.render("Medium", True, (255, 255, 255))
        self.screen.blit(medium_text, (450, 200))
        hard_text = self.font.render("Hard", True, (255, 255, 255))
        self.screen.blit(hard_text, (450, 300))
        expert_text = self.font.render("Expert", True, (255, 255, 255))
        self.screen.blit(expert_text, (450, 400))
        back_text = self.font.render("Back", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, 100, 50), 2)
        self.screen.blit(back_text, (20, 20))
