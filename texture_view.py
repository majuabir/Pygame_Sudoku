import pygame

pygame.init()
pygame.display.set_caption("test")
screen = pygame.display.set_mode((200,200))
image = pygame.image.load("textures/numbers.png")
screen.fill((255,255,255))
screen.blit(image, (0,0), (60,0,30,30))
pygame.display.flip()

running = True

while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False