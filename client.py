import pygame
from network import Network
from player import Player
import os
import socket

class Done(Exception): pass

# State: "main", "start", "game"
state = "main"
server = ""
n = ""

width = 1280
height = 720
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fligo")
pygame.font.init()

baseFont = pygame.font.Font(None, 35)
font = pygame.font.Font(os.getcwd() + '\\Resources\\fonts\\SnesItalic-vmAPZ.ttf', 128)
font2 = pygame.font.Font(os.getcwd() + '\\Resources\\fonts\\Alice-Regular.ttf', 128)
FONT = pygame.font.Font(None, 50)

bg = pygame.image.load(os.getcwd() + '\\Resources\\img\\bg.png').convert()

red = (255,0,0)
bright_red = (150,0,0)
white = (255,255,255)
black = (0,0,0)

def convertTuple(tup): 
    str =  ''.join(tup) 
    return str

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = red
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = bright_red if self.active else red
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(300, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

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

def button(msg, x, y, wid, hei, ac, ic, action=None, *arg):
    global state
    global server
    global n
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + wid > mouse[0] > x and y + hei > mouse[1] > y:
        pygame.draw.rect(win, ac,(x,y,wid,hei))
        if click[0] == 1 and action != None:
            if action == "main":
                state = "main"
                raise Done
            if action == "joinmenu":
                state = "join"
                raise Done
            if action == "start":
                state = "game"
                raise Done
            if action == "join":
                state = "create"
                nserver = convertTuple(arg)
                server = nserver
                n = Network(server)
                raise Done
            if action == "quit":
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
    
    while menu:
        try:
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
            button("Join Game", ((width // 2)-100), (height // 2), 200, 50, bright_red, red, "joinmenu")
            # button("Create Game", ((width // 2)-100), ((height // 2)+75), 200, 50, bright_red, red, "create")
            button("Quit", ((width // 2)-100), ((height // 2)+75), 200, 50, bright_red, red, "quit")
            # pygame.draw.rect(win, red,((width // 2)-100,(height // 2),200,50),3)
            # pygame.draw.rect(win, red,((width // 2)-100,(height // 2)+75,200,50),3)

            pygame.display.update()
        except Done:
            break

def create_menu():
    start = True
    # clock = pygame.time.Clock()
    bgX = 0
    bgX2 = bg.get_width()

    p = n.getP()
    p2 = n.send(p)

    players = [p.name, p2.name]
    
    while start:
        try:
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
            text = FONT.render("Server: " + server, True, red) 
            textRect = text.get_rect()
            # textRect.w = 150
            # textRect.h = 30
            # textRect.center = (75,30)
            win.blit(text, textRect)

            pos = (100,50)
            for name in players:
                text = FONT.render(name, True, red) 
                textRect = text.get_rect()
                # textRect.w = 150
                # textRect.h = 30
                textRect.center = pos
                win.blit(text, textRect)

                t = list(pos)
                t[1]+=50
                pos = tuple(t) 

            button("Start", 1050, 10, 200, 50, bright_red, red, "start")
            button("Back", ((width // 2)-100), (height // 2)+100, 200, 50, bright_red, red, "main")
            pygame.display.update()
        except Done:
            break

def join_menu():
    start = True
    # clock = pygame.time.Clock()
    ip_server = ''
    bgX = 0
    bgX2 = bg.get_width()

    input_box1 = InputBox(((width // 2)-150), (height // 2)-50, 300, 50)
    input_boxes = [input_box1]
    
    while start:
        try:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    pygame.quit()
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_BACKSPACE:
                #         ip_server = ip_server[:-1]
                #     else:
                #         ip_server += event.unicode
                for box in input_boxes:
                    box.handle_event(event)
            
            # main 
            for box in input_boxes:
                box.update()

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

            # screen.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(win)

            # input_rect = pygame.Rect(((width // 2)-100), (height // 2)-50, 200, 50)
            # pygame.draw.rect(win, white, input_rect)

            # text_surface = baseFont.render(ip_server, True, black)
            # win.blit(text_surface, (input_rect.x + 5, input_rect.y + 15))
            button("Join", ((width // 2)-100), (height // 2)+25, 200, 50, bright_red, red, "join", input_boxes[0].text)
            button("Back", ((width // 2)-100), (height // 2)+100, 200, 50, bright_red, red, "main")

            pygame.display.update()
        except Done:
            break

def movement(p,rect,enemy):
    keys = pygame.key.get_pressed()
    # up,bottom,left,right
    way = [True,True,True,True]

    collision = [False] * 9
    collision[0] = enemy.collidepoint(rect.topleft)
    collision[1] = enemy.collidepoint(rect.topright)
    collision[2] = enemy.collidepoint(rect.bottomleft)
    collision[3] = enemy.collidepoint(rect.bottomright)

    collision[4] = enemy.collidepoint(rect.midleft)
    collision[5] = enemy.collidepoint(rect.midright)
    collision[6] = enemy.collidepoint(rect.midtop)
    collision[7] = enemy.collidepoint(rect.midbottom)

    collision[8] = rect.collidepoint(rect.center)

    if collision[0] or collision[2] or collision[4]:
        print ("left")
        way[2] = False
    if collision[1] or collision[3] or collision[5]:
        print ("right")
        way[3] = False
    if collision[0] or collision[1] or collision[6]:
        print ("top")
        way[0] = False
    if collision[2] or collision[3] or collision[7]:
        print ("bottom")
        way[1] = False

    if keys[pygame.K_LEFT] and way[2]:
        p.x -= p.vel
    if keys[pygame.K_RIGHT] and way[2]:
        p.x += p.vel
    if keys[pygame.K_UP] and way[2]:
        p.y -= p.vel
    if keys[pygame.K_DOWN] and way[2]:
        p.y += p.vel



def game():
    game = True
    bgX = 0
    bgX2 = bg.get_width()

    # n = Network()
    p = n.getP()
    p.ready = True
    p2 = n.send(p)

    p_img = pygame.image.load(p.image)
    p2_img = pygame.image.load(p2.image)

    p.players = [pygame.Rect(p2.rect)]
    # players = [pygame.Rect(p2.rect)]


    # print(p.rect)
    # p_rect = p.rect
    # print(p.rect)
    # clock = pygame.time.Clock()

    while game:  
        clock.tick(60)
        p2 = n.send(p)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()

        
        # if(doRectsOverlap(p.rect,p2.rect)):
            # p.move()
        # if p_rect.colliderect(p2.rect):
        # if pygame.Rect(p.rect).collidelist(p.players) >= 0:
        #     print("ga")

        # movement(p,pygame.Rect(p.rect), pygame.Rect(p2.rect))
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
            # pass
        elif state == "create":
            create_menu()
            # pass
        elif state == "join":
            join_menu()
            # pass
        elif state == "game":
            game()
            # pass
        print(state)

clock = pygame.time.Clock()
main()