import pygame

class Player:
    def __init__(self, position: tuple[int,int]):
        self.__xPos, self.__yPos = position
        self.__speed = 10

    @property
    def xPos(self):
        return self.__xPos

    @property
    def yPos(self):
        return self.__yPos

    def move_up(self):
        self.__yPos -= self.__speed

    def move_down(self):
        self.__yPos += self.__speed

    def move_left(self):
        self.__xPos -= self.__speed

    def move_right(self):
        self.__xPos += self.__speed

class Block:
    def __init__(self, position: tuple[int,int], color: str = "brown"):
        self.__width = 60
        self.__xPos = position[0] - self.__width // 2
        self.__yPos = position[1] - self.__width // 2
        self.__color = color
        self.__rect = pygame.Rect(self.__xPos, self.__yPos,
                                  self.__width, self.__width)

    @property
    def xPos(self):
        return self.__xPos

    @property
    def yPos(self):
        return self.__yPos

    @property
    def rect(self):
        return self.__rect

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
SCREEN_CENTER: tuple[int,int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player = Player(SCREEN_CENTER)
block = Block(SCREEN_CENTER)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill screen with color to wipe last frame
    screen.fill("blue")

    # render
    pygame.draw.circle(screen, "red", (player.xPos, player.yPos) , 40)
    start = (SCREEN_CENTER[0] - 180, SCREEN_CENTER[1])
    for i in range(0, 7):
        new_block = Block(start)
        pygame.draw.rect(screen, "brown", new_block.rect)
        start = (start[0] + 60, start[1])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        player.move_up()
    if keys[pygame.K_d]:
        player.move_down()
    if keys[pygame.K_s]:
        player.move_left()
    if keys[pygame.K_f]:
        player.move_right()

    # flip display to screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

