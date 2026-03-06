import pygame
from States.GameState import GameState
from States.MainMenuState import MainMenuState
from Valikot.NextLevel import NextLevel

class LevelCompleteState(GameState):

    def __init__(self, manager):
        super().__init__(manager)
        self.next_level_menu = NextLevel(
            current_level=1,
            max_level=1,
            display_current_level=1,
            display_next_level=2,
            screen=manager.screen,
        )

    def update(self, events):
        action = self.next_level_menu.handle_events_from(events)
        result = self.next_level_menu.resolve_action(action)

        if isinstance(result, int):
            from States.PlayState import PlayState
            self.manager.set_state(PlayState(self.manager))
            return

        if result == "game_completed":
            self.manager.set_state(MainMenuState(self.manager))
            return

        if result == "settings":
            try:
                from Valikot.SettingsMenu import main as settings_menu_main
                settings_menu_main()
            except Exception as exc:
                print(f"Could not open settings menu: {exc}")
            return

        if result == "quit":
            self.manager.running = False
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.manager.set_state(MainMenuState(self.manager))
                return

    def draw(self, screen):
        self.next_level_menu.draw(screen)