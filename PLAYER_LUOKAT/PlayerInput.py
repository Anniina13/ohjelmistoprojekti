import pygame

class PlayerInput:
    def __init__(self):
        self.moveUp = False
        self.moveDown = False
        self.turnLeft = False
        self.turnRight = False
        # shoot1 = L, shoot2 = P. Säilytetään myös `shoot` alias yhteensopivuuden vuoksi (shoot -> shoot1)
        self.shoot = False
        self.shoot1 = False
        self.shoot2 = False
        self.hit = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.moveUp = keys[pygame.K_w]
        self.moveDown = keys[pygame.K_s]
        self.turnLeft = keys[pygame.K_d]
        self.turnRight = keys[pygame.K_a]
        # Asetetaan shoot1 ja shoot2 erillisinä nappeina: P = Shot1, L = Shot2
        self.shoot1 = keys[pygame.K_p]
        self.shoot2 = keys[pygame.K_l]
        # säilytä shoot alias vanhalle koodille (ottaa arvon shoot1)
        self.shoot = self.shoot1
        self.hit = keys[pygame.K_h]