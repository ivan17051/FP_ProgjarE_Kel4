import pygame

class Player():
    def __init__(self, x, y, width, height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x,y,width,height)
        self.vel = 3
        self.image = image
        # self.players

    def draw(self, win):
        win.blit(self.image, self.rect)
        # pygame.draw.rect(win, self.color, self.rect)

    def getRect(self):
        return self.rect

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