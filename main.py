import pygame
from menu import MainMenu

def main():
    pygame.init()
    main_menu = MainMenu()
    main_menu.run()
    pygame.quit()

if __name__ == "__main__":
    main()
