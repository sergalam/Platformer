import pygame 

pygame.init()
# okno
screen_W, screen_H = 900, 700
background = (44, 200, 100)
screen = pygame.display.set_mode((screen_W, screen_H))
pygame.display.set_caption('Платформер')

# таймер
clock = pygame.time.Clock()
FPS = 60

# классы
class Player(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))
        self.color=(0, 0, 255)
        self.surface.fill(self.color)

        self.x_vel = 5
        self.y_vel = 0
        self.fall_count = 0 

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.x_vel
        if keys[pygame.K_d] and self.rect.x < screen_W - 50:
            self.rect.x += self.x_vel

        #гравитация
        self.y_vel += min(1, (self.fall_count / FPS) * self.GRAVITY)
        self.rect.y += self.y_vel
        self.fall_count += 1

    def draw(self):
        screen.blit(self.surface, (self.rect.x, self.rect.y))


# игровые обьекты
player = Player(100, 100, 50, 50)
# Игровой цикл
run_game = True
while run_game:
    screen.fill(background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
    player.move()
    # отрисовка
    player.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()