import pygame
import pygame.locals as pl
from network import Network
from player import Player
import os
import socket
import random

class Done(Exception): pass

# State: "main", "start", "game"
state = "main"
server = ""
n = ""

pygame.init()
width = 1280
height = 720
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fligo")
# pygame.font.init()

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
                    # menu = False
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
            win.blit(text, (50, 10, 200, 50))

            pos = ((width // 2),(height // 2))
            text = FONT.render(players[0], True, red) 
            textRect = text.get_rect()
            # textRect.w = 150
            # textRect.h = 30
            textRect.center = pos
            win.blit(text, textRect)

                # t = list(pos)
                # t[1]+=50
                # pos = tuple(t) 

            button("Start", 1050, 10, 200, 50, bright_red, red, "start")
            button("Back", ((width // 2)-100), (height // 2)+100, 200, 50, bright_red, red, "main")
            pygame.display.update()
        except Done:
            break

def join_menu():
    start = True
    # clock = pygame.time.Clock()
    bgX = 0
    bgX2 = bg.get_width()

    input_box1 = InputBox(((width // 2)-150), (height // 2)-50, 300, 50)
    input_boxes = [input_box1]
    
    while start:
        try:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # menu = False
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
    r = list(p2.obsRect)
    obs_startx = r[0]
    obs_starty = r[1]
    obs_width = r[2]
    obs_height = r[3]

    # obs_startx = width - 200
    # obs_starty = random.randrange(0, height)
    obs_speed = 9
    # obs_width = 100
    # obs_height = 100

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

        p.movement(pygame.Rect(p2.rect))
        # movement(p,pygame.Rect(p.rect), pygame.Rect(p2.rect))
        # p.move()

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

        # Obstacle
        if obs_startx < -200:
            r = list(p2.obsRect)
            obs_startx = r[0]
            obs_starty = r[1]
            obs_width = r[2]
            obs_height = r[3]
            # obs_startx = width
            # obs_starty = random.randrange(0, height)
            # obs_width = random.randrange(100, 200)
            # obs_height = random.randrange(100, 400)

        # obs_startx = r[0]
        # obs_starty = r[1]
        # obs_width = r[2]
        # obs_height = r[3]
        # print(str(obs_startx) +","+str(obs_starty) +","+str(obs_width) +","+str(obs_height))
        pygame.draw.rect(win, white,(obs_startx,obs_starty,obs_width,obs_height))
        obs_startx -= obs_speed

        p.Obstacle(pygame.Rect((obs_startx,obs_starty,obs_width,obs_height)))
        print(p.dead)

        # Chat
        pygame.draw.rect(win, white,((width-110),((height // 2)-160),70,370))
        button("1", (width-100), (height // 2)+150, 50, 50, bright_red, red,)
        button("2", (width-100), (height // 2)+75, 50, 50, bright_red, red,)
        button("3", (width-100), (height // 2), 50, 50, bright_red, red,)
        button("4", (width-100), (height // 2)-75, 50, 50, bright_red, red,)
        button("5", (width-100), (height // 2)-150, 50, 50, bright_red, red,)
        pygame.display.update()

class ChatInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, Home and End work as well.
    """
    def __init__(
            self,
            initial_string="",
            font_family="",
            font_size=35,
            antialias=True,
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 1),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            max_string_length=-1):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font
        :param text_color: Color of text
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param max_string_length: Allowed length of text
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.max_string_length = max_string_length
        self.input_string = initial_string  # Inputted text

        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)

        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:
                    self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == pl.K_RETURN:
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # Re-render text surface:
        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0

def main():
    run = True
    print(socket.gethostbyname(socket.gethostname()))
    while run:  
        # clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.K_RETURN:
                text_input = ChatInput()
                
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
