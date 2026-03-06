from States.GameState import GameState
import RocketGame

class PlayState(GameState):
    def __init__(self, manager):
        super().__init__(manager)
        self.game = RocketGame.Game(manager.screen)

    def update(self, events):
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