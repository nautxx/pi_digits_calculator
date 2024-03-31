from PIL import Image
import pygame
import sys

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

class Block:
    def __init__(self, x, w, m, v, xc):
        self.x = x
        self.y = height - w
        self.w = w
        self.v = v
        self.m = m
        self.xConstraint = xc

    def hit_wall(self):
        return self.x <= 0

    def reverse(self):
        self.v *= -1

    def collide(self, other):
        return not (self.x + self.w < other.x or self.x > other.x + other.w)

    def bounce(self, other):
        sum_m = self.m + other.m
        new_v = (self.m - other.m) / sum_m * self.v
        new_v += (2 * other.m / sum_m) * other.v
        return new_v

    def update(self):
        self.x += self.v

    def show(self):
        x = constrain(self.x, self.xConstraint, width)
        screen.blit(block_img, (x, self.y, self.w, self.w))

pygame.init()

# Set up the screen
width = 800
height = 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blocks Simulation")

# Load images and sound
block_img = pygame.image.load('data/block.png')
clack = pygame.mixer.Sound('data/clack.wav')

count = 0
digits = 7
time_steps = 10 ** (digits - 1)

block1 = Block(100, 20, 1, 0, 0)
m2 = pow(100, digits - 1)
block2 = Block(300, 100, m2, -1 / time_steps, 20)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((200, 200, 200))

    clack_sound = False

    for i in range(time_steps):
        if block1.collide(block2):
            v1 = block1.bounce(block2)
            v2 = block2.bounce(block1)
            block1.v = v1
            block2.v = v2
            clack_sound = True
            count += 1

        if block1.hit_wall():
            block1.reverse()
            clack_sound = True
            count += 1

        block1.update()
        block2.update()

    if clack_sound:
        clack.play()

    block1.show()
    block2.show()

    pygame.display.update()