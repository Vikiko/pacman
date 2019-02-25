import os
import random

import pygame

size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
gravity = 0.00000001

clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

screen_rect = (0, 0, 1000, 800)
screen_rect2 = (0, 0, 1000, 700)

class Bomb(pygame.sprite.Sprite):
    image = load_image("invader01.png")
    image_boom = load_image("boom.png")

    def __init__(self, all_sprites, dx=0, dy=1):
        super().__init__(all_sprites)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.topleft = ((random.randint(0, width - self.rect.width), random.randint(-600, height - self.rect.height - 600)))
        self.gravity = gravity
    def update(self):
        # применяем гравитационный эффект: 
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += 0
        self.rect.y += 1
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()
        if not self.rect.colliderect(screen_rect2):
            self.rect.x += 0
            self.rect.y += -1
            
    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            self.image = self.image_boom


all_sprites = pygame.sprite.Group()

for i in range(100):

    Bomb(all_sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in all_sprites:
                b.get_event(event)
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    all_sprites.update()    
    pygame.display.flip()

pygame.quit()