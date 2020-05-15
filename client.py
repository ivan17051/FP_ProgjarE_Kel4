import pygame
from network import Network
from player import Player
import os

# State: "menu", "start", "game"
state = "menu"

width = 1280
height = 720
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fligo")
pygame.font.init()
font = pygame.font.Font(os.getcwd() + '\\Resources\\SnesItalic-vmAPZ.ttf', 128)
font2 = pygame.font.Font(os.getcwd() + '\\Resources\\Alice-Regular.ttf', 128)

def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

def main_menu():
    menu = True
    # clock = pygame.time.Clock()

    while menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
        
        # main menu
        win.fill((255,255,255))
        mouse = pygame.mouse.get_pos()

        # Button dan Text
        # Title
        text = font.render('4. FLIGO', True, (255,0,0)) 
        textRect = text.get_rect()

        textRect.center = (width // 2, (height // 2) - 100)
        win.blit(text, textRect)

        # Button
        pygame.draw.rect(win, (255,0,0),((width // 2)-100,(height // 2),200,50),3)
        pygame.draw.rect(win, (255,0,0),((width // 2)-100,(height // 2)+75,200,50),3)

        pygame.display.update()

def start_menu():
    start = True
    # clock = pygame.time.Clock()

    while start:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
        
        # main menu
        win.fill((0,255,255))
        # Button dan Text
        pygame.display.update()

def game():
    game = True
    n = Network()
    p = n.getP()
    # clock = pygame.time.Clock()

    while game:  
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()

        p.move()
        redrawWindow(win, p, p2)


def main():
    run = True

    while run:  
        # clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if state == "menu":
            main_menu()
        if state == "start":
            start_menu()
        if state == "game":
            game()

clock = pygame.time.Clock()
main()