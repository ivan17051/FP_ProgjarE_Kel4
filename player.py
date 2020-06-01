import pygame

class Player():
    def __init__(self, name,x, y, width, height,image):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x,y,width,height)
        self.vel = 7
        self.image = image
        self.ready = False
        self.obsRect = (-200,0,0,0,0)
        self.dead = False
        self.emot = 0

    def draw(self, win):
        win.blit(self.image, self.rect)
        # pygame.draw.rect(win, self.color, self.rect)

    def getRect(self):
        return self.rect

    def Obstacle(self,obs):
        col = [False] * 8
        col[0] = obs.collidepoint(pygame.Rect(self.rect).topleft)
        col[1] = obs.collidepoint(pygame.Rect(self.rect).topright)
        col[2] = obs.collidepoint(pygame.Rect(self.rect).bottomleft)
        col[3] = obs.collidepoint(pygame.Rect(self.rect).bottomright)

        col[4] = obs.collidepoint(pygame.Rect(self.rect).midleft)
        col[5] = obs.collidepoint(pygame.Rect(self.rect).midright)
        col[6] = obs.collidepoint(pygame.Rect(self.rect).midtop)
        col[7] = obs.collidepoint(pygame.Rect(self.rect).midbottom)

        if col[0] or col[1] or col[2] or col[3] or col[4] or col[5] or col[6] or col[7]:
            self.dead = True

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