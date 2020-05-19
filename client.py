import pygame
from network import Network
from player import Player
import os
import socket

class Done(Exception): pass

# State: "menu", "start", "game"
state = "game"

width = 1280
height = 720
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fligo")
pygame.font.init()

baseFont = pygame.font.Font(None, 35)
font = pygame.font.Font(os.getcwd() + '\\Resources\\fonts\\SnesItalic-vmAPZ.ttf', 128)
font2 = pygame.font.Font(os.getcwd() + '\\Resources\\fonts\\Alice-Regular.ttf', 128)

bg = pygame.image.load(os.getcwd() + '\\Resources\\img\\bg.png').convert()

red = (255,0,0)
bright_red = (150,0,0)
white = (255,255,255)
black = (0,0,0)

def doRectsOverlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.left, a.top, b)) or (isPointInsideRect(a.left, a.bottom, b)) or (isPointInsideRect(a.right, a.top, b)) or (isPointInsideRect(a.right, a.bottom, b))):
            return True
    return False

def isPointInsideRect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

def redrawWindow(win,player, player2):
    win.fill((255,255,255))
    # player.draw(win)
    # player2.draw(win)
    pygame.display.update()

def button(msg, x, y, wid, hei, ac, ic, action=None):
    global state
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + wid > mouse[0] > x and y + hei > mouse[1] > y:
        pygame.draw.rect(win, ac,(x,y,wid,hei))
        if click[0] == 1 and action != None:
            if action == "main":
                state = "main"
                raise Done
            elif action == "create":
                state = "create"
                raise Done
            elif action == "join":
                state = "join"
                raise Done
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(win, ic,(x,y,wid,hei))

    font3 = pygame.font.Font(os.getcwd() + '\\Resources\\fonts\\SnesItalic-vmAPZ.ttf', 30)
    smallText = font3.render(msg, True, white)
    textRect2 = smallText.get_rect()
    textRect2.center = (x + (wid/2), y + (hei/2))
    win.blit(smallText, textRect2)

def main_menu():
    menu = True
    # clock = pygame.time.Clock()
    bgX = 0
    bgX2 = bg.get_width()
    try:
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
            button("Create Game", ((width // 2)-100), (height // 2), 200, 50, bright_red, red, "create")
            button("Join Game", ((width // 2)-100), ((height // 2)+75), 200, 50, bright_red, red, "join")
            button("Quit", ((width // 2)-100), ((height // 2)+150), 200, 50, bright_red, red, "quit")
            # pygame.draw.rect(win, red,((width // 2)-100,(height // 2),200,50),3)
            # pygame.draw.rect(win, red,((width // 2)-100,(height // 2)+75,200,50),3)

            pygame.display.update()
    except Done:
        pass

def create_menu():
    start = True
    # clock = pygame.time.Clock()
    bgX = 0
    bgX2 = bg.get_width()
    try:
        while start:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
            
            # main menu
            win.fill((0,255,255))

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
            button("Back", ((width // 2)-100), (height // 2), 200, 50, bright_red, red, "main")
            pygame.display.update()
    except Done:
        pass

def join_menu():
    start = True
    # clock = pygame.time.Clock()
    ip_server = ''
    bgX = 0
    bgX2 = bg.get_width()
    try:
        while start:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        ip_server = ip_server[:-1]
                    else:
                        ip_server += event.unicode
            
            # main menu
            win.fill((0,255,255))

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
            input_rect = pygame.Rect(((width // 2)-100), (height // 2)-50, 200, 50)
            pygame.draw.rect(win, white, input_rect)

            text_surface = baseFont.render(ip_server, True, black)
            win.blit(text_surface, (input_rect.x + 5, input_rect.y + 15))
            button("Back", ((width // 2)-100), (height // 2)+25, 200, 50, bright_red, red, "main")

            pygame.display.update()
    except Done:
        pass

def game():
    game = True
    bgX = 0
    bgX2 = bg.get_width()

    n = Network()
    p = n.getP()
    p2 = n.send(p)

    p_img = pygame.image.load(p.image)
    p2_img = pygame.image.load(p2.image)


    # print(p.rect)
    # p_rect = p.rect
    # print(p.rect)
    # clock = pygame.time.Clock()

    while game:  
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()

        
        # if(doRectsOverlap(p.rect,p2.rect)):
            # p.move()
        # if p_rect.colliderect(p2.rect):
        p.move()

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
        
        win.blit(p_img, p.rect)
        win.blit(p2_img, p2.rect)
        pygame.display.update()


def main():
    run = True
    print(socket.gethostbyname(socket.gethostname()))
    while run:  
        # clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if state == "main":
            main_menu()
        if state == "create":
            create_menu()
        if state == "join":
            join_menu()
        if state == "game":
            game()
        # print(state)

clock = pygame.time.Clock()
main()