import pygame

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    QUIT
)

pygame.init()
pygame.mixer.init()

ballHitPlayer_Sound = pygame.mixer.Sound("soundEffects/playerHit.wav")
ballHitWall_Sound = pygame.mixer.Sound("soundEffects/wallHit.wav")

screenWidth = 1200
screenHeight = 800

playerHeight = 15
playerWidth = 70

enemyHeight = playerHeight
enemyWidth = playerWidth

ballRadius = 8

screen = pygame.display.set_mode((screenWidth, screenHeight))
screenBgColor = pygame.Color("#30323d")
pygame.display.set_caption("Pong Game")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surface = pygame.Surface((playerWidth, playerHeight))
        self.image = self.surface
        self.surface.fill(pygame.Color("#E8C547"))
        self.rect = self.surface.get_rect()
        self.rect.x = ((screenWidth / 2) - (playerWidth / 2))
        self.rect.y = (screenHeight - playerHeight) - 10

    def updatePlayer(self, pressedKeys):
        if pressedKeys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressedKeys[K_RIGHT]:
            self.rect.move_ip((2, 0))
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screenWidth:
            self.rect.right = screenWidth


player = Player()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surface = pygame.Surface((enemyWidth, enemyHeight))
        self.image = self.surface
        self.surface.fill(pygame.Color("#FF674D"))
        self.rect = self.surface.get_rect()
        self.rect.x = ((screenWidth / 2) - (playerWidth / 2))
        self.rect.y = enemyHeight - 10
        self.ball = None

    def setBall(self, ball):
        self.ball = ball

    def updateEnemy(self):
        if self.ball:
            ballCenter = self.ball.rect.centerx
            enemyCenter = self.rect.centerx
            if ballCenter < enemyCenter:
                self.rect.move_ip(-2, 0)
            elif ballCenter > enemyCenter:
                self.rect.move_ip(2, 0)
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > screenWidth:
                self.rect.right = screenWidth


enemy = Enemy()


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.ballRadius = ballRadius
        self.ballDiameter = ballRadius * 2
        self.surface = pygame.Surface((self.ballDiameter, self.ballDiameter), pygame.SRCALPHA)
        self.image = self.surface
        pygame.draw.circle(self.surface, pygame.Color("#F6F7EB"), (ballRadius, ballRadius), ballRadius)
        self.rect = self.surface.get_rect()
        self.rect.x = (screenWidth // 2) - ballRadius
        self.rect.y = (screenHeight // 2) - ballRadius
        self.speed = [1, 1]
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

    def updateBall(self):
        self.rect.move_ip(self.speed)
        if self.rect.left < 0 or self.rect.right > screenWidth:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > screenHeight:
            self.speed[1] = -self.speed[1]


ball = Ball()
enemy.setBall(ball)

allSprites = pygame.sprite.Group()
allSprites.add(player)
allSprites.add(enemy)
allSprites.add(ball)

gameRunning = True
while gameRunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameRunning = False

    screen.fill(screenBgColor)

    pressedKeys = pygame.key.get_pressed()
    player.updatePlayer(pressedKeys)
    screen.blit(ball.surface, ball.rect)

    ball.updateBall()
    enemy.updateEnemy()

    allSprites.draw(screen)

    pygame.display.flip()
    pygame.display.update()

pygame.quit()
