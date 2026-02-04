
# Pohjat otettu: https://www.youtube.com/watch?v=2iyx8_elcYg
import pygame
pygame.init()


SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1700

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

def draw_text(text, font, text_col, x, y):
    img =font.render(text, True, text_col)
    screen.blit(img, (x,y))

#game loop
run = True
while run:

    screen.fill((52,78,91))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()    