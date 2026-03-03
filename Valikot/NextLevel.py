import pygame

# Näytön asetukset
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

# Värit
WHITE = (255, 255, 255)
DARK_BLUE = (52, 78, 91)
LIGHT_BLUE = (100, 150, 200)
HOVER_COLOR = (150, 200, 255)

# Fontit
title_font = None
button_font = None
small_font = None


class Button:
	"""Nappi-luokka seuraavan tason valikolle"""

	def __init__(self, x, y, width, height, text, color, text_color, action=None):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.color = color
		self.text_color = text_color
		self.action = action
		self.is_hovered = False

	def draw(self, surface):
		current_color = HOVER_COLOR if self.is_hovered else self.color
		pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
		pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=10)

		text_surf = button_font.render(self.text, True, self.text_color)
		text_rect = text_surf.get_rect(center=self.rect.center)
		surface.blit(text_surf, text_rect)

	def is_clicked(self, pos):
		return self.rect.collidepoint(pos)

	def update(self, pos):
		self.is_hovered = self.rect.collidepoint(pos)


class NextLevel:
	"""Seuraavan tason valikon hallinta"""

	def __init__(self, current_level=1, max_level=None, display_current_level=None, display_next_level=None):
		global title_font, button_font, small_font

		if not pygame.get_init():
			pygame.init()
		if not pygame.display.get_init():
			pygame.display.init()

		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Rocket Game - Next Level")

		title_font = pygame.font.Font(None, 80)
		button_font = pygame.font.Font(None, 50)
		small_font = pygame.font.Font(None, 34)

		self.current_level = int(current_level)
		self.max_level = max_level
		self.next_level = self.current_level + 1
		self.display_current_level = self.current_level if display_current_level is None else int(display_current_level)
		self.display_next_level = self.next_level if display_next_level is None else int(display_next_level)

		self.buttons = [
			Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 80, "NEXT LEVEL", LIGHT_BLUE, WHITE, action="next_level"),
			Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20, 300, 80, "SETTINGS", LIGHT_BLUE, WHITE, action="settings"),
			Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 140, 300, 80, "QUIT", LIGHT_BLUE, WHITE, action="quit"),
		]
		self.clock = pygame.time.Clock()
		self.running = True

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				for button in self.buttons:
					if button.is_clicked(mouse_pos):
						return button.action

		return None

	def draw(self):
		self.screen.fill(DARK_BLUE)

		title_surf = title_font.render("LEVEL COMPLETE", True, WHITE)
		title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
		self.screen.blit(title_surf, title_rect)

		level_line = small_font.render(
			f"Current Level: {self.display_current_level}   Next Level: {self.display_next_level}",
			True,
			WHITE,
		)
		level_rect = level_line.get_rect(center=(SCREEN_WIDTH // 2, 180))
		self.screen.blit(level_line, level_rect)

		mouse_pos = pygame.mouse.get_pos()
		for button in self.buttons:
			button.update(mouse_pos)
			button.draw(self.screen)

		pygame.display.update()

	def run(self):
		while self.running:
			action = self.handle_events()

			if action == "next_level":
				if self.max_level is not None and self.next_level > self.max_level:
					return "game_completed"
				return self.next_level
			if action == "settings":
				return "settings"
			if action == "quit":
				return "quit"

			self.draw()
			self.clock.tick(60)

		return "quit"

