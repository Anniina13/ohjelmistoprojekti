from States.GameState import GameState
from Valikot.MainMenu import MainMenu


class MainMenuState(GameState):

    def __init__(self, manager=None):
        super().__init__(manager)
        self.menu = MainMenu()

    def update(self, events):

        action = self.menu.handle_events(events)

        if action == "start":
            try:
                from States.PlayState import PlayState
                self.manager.set_state(PlayState(self.manager))
            except Exception as exc:
                # Keep the menu active if gameplay state is not yet wired.
                print(f"Could not start PlayState: {exc}")

        elif action == "settings":
            try:
                from Valikot.SettingsMenu import main as settings_menu_main

                settings_menu_main()
            except Exception as exc:
                print(f"Could not open settings menu: {exc}")

        elif action == "quit":
            self.manager.running = False

    def draw(self, screen):
        self.menu.draw(screen)