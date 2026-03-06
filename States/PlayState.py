from States.GameState import GameState
import pygame
import RocketGame

class PlayState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.game = RocketGame.Game(manager.screen)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from States.PauseState import PauseState
                background = self.manager.screen.copy()
                self.manager.set_state(PauseState(self.manager, self, background_surface=background))
                return

        self.game.update(events)

        if getattr(self.game, 'level_completed', False):
            from States.LevelCompleteState import LevelCompleteState
            self.manager.set_state(LevelCompleteState(self.manager))
            return

        player_hp = int(getattr(self.game.player, 'health', 0)) if self.game.player is not None else 0
        if player_hp <= 0 or not self.game.running:
            from States.GameOverState import GameOverState
            self.manager.set_state(GameOverState(self.manager))
            return

    def draw(self, screen):
        self.game.draw(screen)