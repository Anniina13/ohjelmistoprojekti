"""Taso 4 wave-rakenne RocketGame.Game:lle.

Sisältää wave 1-4 vihollisaallot ja boss-wave (wave 4).
Voit muokata tätä omilta enemy-kombinaatioilta.
"""

import pygame
import random

def spawn_wave_taso4(
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
	zigzag_enemy_cls=None,
    chase_enemy_cls=None,
):
	"""Spawn Level 4 enemies for the requested wave.

	Returns:
		bool: True if wave was handled by this level module, else False.
	"""
	# TODO: Implement Level 4 unique enemy compositions