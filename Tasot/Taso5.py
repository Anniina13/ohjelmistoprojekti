"""Taso 5 wave-rakenne RocketGame.Game:lle.

Sisältää wave 1-4 vihollisaallot ja boss-wave (wave 4).
Voit muokata tätä omilta enemy-kombinaatioilta.
"""

import pygame
import random

def spawn_wave_taso5(
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
	enemy_speeds=None,  # Dict with speed overrides
):
	"""Spawn Level 5 enemies for the requested wave.

	Args:
		enemy_speeds: Optional dict with enemy speed overrides.
			Keys: 'straight', 'circle', 'down', 'up', 'zigzag', 'chase', 'boss_enter', 'boss_move'
			Default speeds are used if not specified.

	Returns:
		bool: True if wave was handled by this level module, else False.
	"""
	# Setup default speeds and apply overrides
	if enemy_speeds is None:
		enemy_speeds = {}
	
	speeds = {
		'straight': enemy_speeds.get('straight', 170),
		'circle': enemy_speeds.get('circle', 2.7),
		'down': enemy_speeds.get('down', 140),
		'up': enemy_speeds.get('up', 140),
		'zigzag': enemy_speeds.get('zigzag', 130),
		'chase': enemy_speeds.get('chase', 190),
		'boss_enter': enemy_speeds.get('boss_enter', 200),
		'boss_move': enemy_speeds.get('boss_move', 250),
	}
	
	# TODO: Implement Level 5 unique enemy compositions