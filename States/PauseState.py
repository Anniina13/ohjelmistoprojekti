from States.GameState import GameState
from Valikot.PauseMenu import PauseMenu


class PauseState(GameState):

	def __init__(self, manager, previous_state, background_surface=None):
		super().__init__(manager)
		self.previous_state = previous_state
		self.background_surface = background_surface
		self.pause_menu = PauseMenu(screen=manager.screen)

	def update(self, events):
		action = self.pause_menu.handle_events_from(events)
		result = self.pause_menu.resolve_action(action)

		if result == "continue":
			self.manager.set_state(self.previous_state)
			return

		if result == "quit":
			self.manager.running = False
			return

	def draw(self, screen):
		if self.background_surface is None and self.previous_state is not None:
			self.previous_state.draw(screen)
		self.pause_menu.draw(self.background_surface)
