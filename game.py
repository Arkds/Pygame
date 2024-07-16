import pygame
import os
import sys
import cv2
import random

class Note:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join('assets', 'notes.png'))
        self.image = pygame.transform.scale(self.image, (80, 80))  # Ajustar tamaño de la nota
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hit = False

    def update(self):
        self.rect.y += 20  # Velocidad de la nota

    def draw(self, screen):
        if not self.hit:
            screen.blit(self.image, self.rect.topleft)

class Game:
    def __init__(self, level, difficulty, main_menu, song):
        self.level = level
        self.difficulty = difficulty  # Agregado
        self.main_menu = main_menu
        self.song = song
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Rhythm Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.load_assets()
        self.reset_game_state()
        self.font = pygame.font.Font(None, 36)
        self.cap = cv2.VideoCapture(self.background)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.delay = int(1000 / self.fps)  # Corregido a 1000 / self.fps para ms por frame

    def load_assets(self):
        assets_path = os.path.join(os.path.dirname(__file__), 'assets')
        self.background = os.path.join(assets_path, f'{self.song.lower().replace(" ", "_")}.mp4')
        if not os.path.exists(self.background):
            print(f"Error: El archivo de video de fondo {self.background} no se encontró.")
            sys.exit()
        self.music = os.path.join(assets_path, f'{self.song.lower().replace(" ", "_")}.mp3')
        if not os.path.exists(self.music):
            print(f"Error: El archivo de música {self.song} no se encontró.")
            sys.exit()

    def reset_game_state(self):
        self.notes = []
        self.note_timings = self.load_note_timings()
        self.current_note_index = 0
        self.score = 0
        self.life = 8  # Número de fallos permitidos
        self.max_life = 8  # Máxima vida
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(0)  # Reproducir una vez
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Configurar evento al terminar la música

    def load_note_timings(self):
        timings_path = os.path.join(os.path.dirname(__file__), 'assets', f'patterns{self.level}_{self.difficulty}_{self.song}.txt')
        if not os.path.exists(timings_path):
            print(f"Error: El archivo de patrones {timings_path} no se encontró.")
            sys.exit()
        with open(timings_path, 'r') as file:
            timings = [int(line.strip()) for line in file]
        return timings

    def run(self):
        self.reset_game_state()  # Restablecer el estado del juego al iniciar
        pygame.time.wait(0)  # Esperar 0 segundos antes de iniciar
        start_ticks = pygame.time.get_ticks()  # Guardar el tiempo de inicio
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update(start_ticks)  # Pasar el tiempo de inicio a update
            self.draw()
            self.clock.tick(60)  # Limitar a 60 FPS
        self.cap.release()
        self.main_menu.run()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Tecla para "golpear" la nota
                    self.hit_note()
                if event.key == pygame.K_p:  # Tecla para pausar
                    self.paused = not self.paused
                if event.key == pygame.K_ESCAPE:  # Tecla para salir
                    pygame.mixer.music.stop()
                    self.running = False
            if event.type == pygame.USEREVENT:  # Evento cuando la música termina
                self.running = False

    def hit_note(self):
        hit = False
        for note in self.notes:
            if note.rect.bottom >= 550 and note.rect.top <= 550:
                note.hit = True
                self.score += 1
                hit = True
                print(f"Score: {self.score}")
        if hit:
            self.life = min(self.max_life, self.life + 1)  # Aumentar vida si acierta
        else:
            self.life -= 1  # Disminuir vida si falla
            print(f"Life: {self.life}")
            if self.life <= 0:
                self.running = False
                print("Game Over")

    def update(self, start_ticks):
        current_time = pygame.time.get_ticks() - start_ticks  # Tiempo desde el inicio del juego
        if self.current_note_index < len(self.note_timings):
            if current_time >= self.note_timings[self.current_note_index]:
                x_position = random.randint(0, 950)  # Generar una posición x aleatoria
                self.notes.append(Note(x_position, 0))
                self.current_note_index += 1

        for note in self.notes:
            note.update()
            if note.rect.top > 600:  # Nota pasó la línea indicadora
                if not note.hit:
                    self.life -= 1
                    print(f"Life: {self.life}")
                    if self.life <= 0:
                        self.running = False
                        print("Game Over")
                self.notes.remove(note)  # Eliminar la nota que pasó

    def draw(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotar el frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (600, 1000))  # Ajustar tamaño manteniendo proporción
        frame_surface = pygame.surfarray.make_surface(frame)
        self.screen.blit(frame_surface, (0, 0))
        for note in self.notes:
            note.draw(self.screen)
        pygame.draw.line(self.screen, (255, 0, 0), (0, 550), (1000, 550), 5)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        life_ratio = self.life / self.max_life
        pygame.draw.rect(self.screen, (255, 0, 0), (10, 50, 980 * life_ratio, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 50, 980, 20), 2)
        pygame.display.flip()
        pygame.time.delay(self.delay)

if __name__ == "__main__":
    pygame.init()
    main_menu = MainMenu()
    main_menu.run()
    pygame.quit()
