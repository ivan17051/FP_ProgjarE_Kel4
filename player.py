import pygame

class Player():
    def __init__(self, name,x, y, width, height,image):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x,y,width,height)
        self.vel = 3
        self.image = image
        self.ready = False
        self.obsRect = (0,0,0,0)

    def draw(self, win):
        win.blit(self.image, self.rect)
        # pygame.draw.rect(win, self.color, self.rect)

    def getRect(self):
        return self.rect

    def movement(self,enemy):
        keys = pygame.key.get_pressed()
        # up,bottom,left,right
        way = [True,True,True,True]

        collision = [False] * 8
        collision[0] = enemy.collidepoint(pygame.Rect(self.rect).topleft)
        collision[1] = enemy.collidepoint(pygame.Rect(self.rect).topright)
        collision[2] = enemy.collidepoint(pygame.Rect(self.rect).bottomleft)
        collision[3] = enemy.collidepoint(pygame.Rect(self.rect).bottomright)

        collision[4] = enemy.collidepoint(pygame.Rect(self.rect).midleft)
        collision[5] = enemy.collidepoint(pygame.Rect(self.rect).midright)
        collision[6] = enemy.collidepoint(pygame.Rect(self.rect).midtop)
        collision[7] = enemy.collidepoint(pygame.Rect(self.rect).midbottom)

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
            
        # print(way)
        if keys[pygame.K_LEFT] and way[2] == True:
            self.x -= self.vel

        if keys[pygame.K_RIGHT] and way[3] == True:
            self.x += self.vel

        if keys[pygame.K_UP] and way[0] == True:
            self.y -= self.vel

        if keys[pygame.K_DOWN] and way[1] == True:
            self.y += self.vel

        self.update()

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)