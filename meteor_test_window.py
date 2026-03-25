"""Standalone meteor preview window for quick visual testing.

Temporary utility file: remove after test use if no longer needed.
"""

import pygame

from Meteor.meteor_helpers import spawn_moving_meteor


class MeteorPreviewGame:
    def __init__(self, width=1280, height=720):
        self.tausta_leveys = width
        self.tausta_korkeus = height
        self.meteors = []


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Meteor Preview")
    clock = pygame.time.Clock()

    game = MeteorPreviewGame(1280, 720)

    spawn_timer = 0.0
    spawn_interval = 0.9
    running = True

    while running:
        dt = clock.tick(60)
        dt_s = dt / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        spawn_timer += dt_s
        if spawn_timer >= spawn_interval and len(game.meteors) < 6:
            spawn_timer = 0.0
            spawn_moving_meteor(game, speed=140)

        for meteor in list(game.meteors):
            meteor.update(dt)
            if meteor.dead:
                game.meteors.remove(meteor)

        screen.fill((10, 16, 26))
        for meteor in game.meteors:
            meteor.draw(screen, 0, 0)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
