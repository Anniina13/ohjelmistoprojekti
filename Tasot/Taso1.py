"""Taso 1 wave-rakenne RocketGame.Game:lle.

Sisaltaa wave 1-3 vihollisaallot ja boss-wave (wave 4).
"""

import pygame
import random


def spawn_wave_taso1(
	game,
	wave_num,
	apply_hitbox,
	hitbox_enemy,
	hitbox_boss,
	straight_enemy_cls,
	circle_enemy_cls,
	boss_enemy_cls,
	down_enemy_cls,
	up_enemy_cls,
):
	"""Spawn Level 1 enemies for the requested wave.

	Returns:
		bool: True if wave was handled by this level module, else False.
	"""
	if wave_num == 1:
		e1 = straight_enemy_cls(game.enemy_imgs[0], 200, 200, speed=220)
		e2 = circle_enemy_cls(
			game.enemy_imgs[1],
			game.tausta_leveys // 2 + 300,
			game.tausta_korkeus // 2,
			radius=180,
			angular_speed=2.2,
		)
		for enemy in (e1, e2):
			apply_hitbox(enemy, hitbox_enemy)
			game.enemies.append(enemy)
		return True

	if wave_num == 2:
		edges = ["right", "top", "left"]
		for i, edge in enumerate(edges):
			if edge == "left":
				x = 80
				y = random.randint(80, game.tausta_korkeus - 80)
			elif edge == "right":
				x = game.tausta_leveys - 80
				y = random.randint(80, game.tausta_korkeus - 80)
			elif edge == "top":
				x = random.randint(80, game.tausta_leveys - 80)
				y = 80
			else:
				x = random.randint(80, game.tausta_leveys - 80)
				y = random.randint(80, game.tausta_korkeus - 80)

			enemy = straight_enemy_cls(game.enemy_imgs[i % len(game.enemy_imgs)], x, y, speed=220)
			if hasattr(enemy, "vel"):
				v = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
				if v.length_squared() == 0:
					v = pygame.Vector2(1, 0)
				enemy.vel = v.normalize() * 220
			apply_hitbox(enemy, hitbox_enemy)
			game.enemies.append(enemy)
		return True

	if wave_num == 3:
		spacing = game.tausta_leveys // 6

		for i in range(3):
			x = spacing * (i + 1)
			y = 30
			enemy = down_enemy_cls(game.enemy_imgs[i % len(game.enemy_imgs)], x, y, speed=250)
			apply_hitbox(enemy, hitbox_enemy)
			game.enemies.append(enemy)

		for i in range(2):
			x = spacing * (i + 3.5)
			y = game.tausta_korkeus - 30
			enemy = up_enemy_cls(game.enemy_imgs[(i + 3) % len(game.enemy_imgs)], x, y, speed=250)
			apply_hitbox(enemy, hitbox_enemy)
			game.enemies.append(enemy)
		return True

	if wave_num == 4:
		game.boss = boss_enemy_cls(
			game.boss_image,
			pygame.Rect(0, 0, game.tausta_leveys, game.tausta_korkeus),
			hp=12,
			enter_speed=280,
			move_speed=320,
			hitbox_size=hitbox_boss,
			hitbox_offset=(0, 0),
		)
		apply_hitbox(game.boss, hitbox_boss)
		game.enemies.append(game.boss)
		return True

	return False
