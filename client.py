import pygame
from network import Network
from player import Player
import os

# State: "menu", "start", "game"
state = "menu"

width = 854
height = 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fligo")
pygame.font.init()
font = pygame.font.Font(os.getcwd() + '\\Resources\\fonts\\SnesItalic-vmAPZ.ttf', 128)
font2 = pygame.font.Font(os.getcwd() + '\\Resources\\fonts\\Alice-Regular.ttf', 128)

bg = pygame.image.load(os.getcwd() + '\\Resources\\img\\bg.png').convert()

red = (255,0,0)
bright_red = (150,0,0)

white = (255,255,255)

def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

def button(msg, x, y, wid, hei, ac, ic, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + wid > mouse[0] > x and y + hei > mouse[1] > y:
        pygame.draw.rect(win, ac,(x,y,wid,hei))
        if click[0] == 1 and action != None:
            if action == "play":
                game()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(win, ic,(x,y,wid,hei))

    font3 = pygame.font.Font(os.getcwd() + '\\Resources\\SnesItalic-vmAPZ.ttf', 30)
    smallText = font3.render(msg, True, white)
    textRect2 = smallText.get_rect()
    textRect2.center = (x + (wid/2), y + (hei/2))
    win.blit(smallText, textRect2)

def main_menu():
    menu = True
    # clock = pygame.time.Clock()
    bgX = 0
    bgX2 = bg.get_width()
    while menu:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
        
        # main menu
        win.fill((255,255,255))
        

        #scolling background
        bgX -= 0.5  # Move both background images back
        bgX2 -= 0.5

        if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
            bgX = bg.get_width()

        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()


        win.blit(bg, (bgX, 0))  # draws our first bg image
        win.blit(bg, (bgX2, 0))  # draws the seconf bg image

        # Button dan Text
        # Title
        text = font.render('4. FLIGO', True, red) 
        textRect = text.get_rect()

        textRect.center = (width // 2, (height // 2) - 100)
        win.blit(text, textRect)

        # Button
        button("Start", ((width // 2)-100), (height // 2), 200, 50, bright_red, red, "play")
        button("Quit", ((width // 2)-100), ((height // 2)+75), 200, 50, bright_red, red, "quit")
        # pygame.draw.rect(win, red,((width // 2)-100,(height // 2),200,50),3)
        # pygame.draw.rect(win, red,((width // 2)-100,(height // 2)+75,200,50),3)

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