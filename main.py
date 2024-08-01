import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 480, 640
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dora Jump")
clock = pygame.time.Clock()
bg = pygame.image.load("images\\background7.png")


class Dora(pygame.sprite.Sprite):

    def __init__(self, x = WIDTH // 2, y = HEIGHT - 200, speed = 5, xSize = 75, ySize = 45):

        self.speed = speed
        self.lives = 8
        self.max_lives = 8
        self.velocity_y = 0
        self.gravity = 0.35
        self.jump_strength = -12
        self.on_ground = False
        self.x = x
        self.y = y
        self.width = xSize
        self.height = ySize

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images\\dora.svg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (xSize, ySize))  # Изменение размера робособаки
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        # Обработка столкновений с самолетами
        self.on_ground = False
        
        for plane in planes:
            if self.rect.colliderect(plane):
                if self.velocity_y > 0:
                    self.y = plane.y - self.height
                    self.velocity_y = 0
                    self.on_ground = True
                # else:
                #     self.y -= self.velocity_y
                #     self.velocity_y  = 0

        # Управление игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

        # Применение гравитации
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Ограничение движений игрока по границам экрана 
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
        if self.y > HEIGHT - self.height: # выпадает за границы мира
            print("Game Over!")
            pygame.quit()
            sys.exit()
        global dY
        if self.y <= HEIGHT // 2:
            self.y = HEIGHT // 2
            dY = self.velocity_y
        else:
            dY = 0
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect.topleft)

class Plane(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0, xSize = 83, ySize = 25):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images\\plane.png')
        self.image = pygame.transform.scale(self.image, (xSize, ySize))  # Изменение размера самолета
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
    def update(self):
        self.y -= round(dY)
        if self.y > HEIGHT:
            self.y -=  HEIGHT * 2
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect.topleft)

planes = pygame.sprite.Group()    
planes.add(Plane(WIDTH//2, HEIGHT - 100))
planes.add(Plane(WIDTH - 83, HEIGHT - 100))
for i in range(2, 14):
    planes.add(Plane(random.randint(0, WIDTH - 83), HEIGHT - i * 100))




dY = 0

font = pygame.font.Font(None, 36)

all_sprites = pygame.sprite.Group()
dora = Dora()
all_sprites.add(dora)

screen.blit(bg, (0, 0))
# Игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


            

    # Отрисовка фона
    screen.blit(bg, (0, 0))

    planes.update()
    all_sprites.update()

    pygame.display.flip()
    clock.tick(FPS)
