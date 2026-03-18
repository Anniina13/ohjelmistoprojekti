"""
Physics module - Unified physics engine for RocketGame

Provides:
- RigidBody: Base physics class for all entities
- Forces: Gravity, Drag, Magnetism, Thrust
- Animations: DampedOscillator for collision bounces
- Presets: Predefined physics profiles for enemy types
"""

from Physics.core import RigidBody
from Physics.forces import Force, Gravity, Drag, Magnetism, Thrust
from Physics.animation import DampedOscillator
from Physics.presets import ENEMY_PRESETS, create_enemy_physics

__all__ = [
    'RigidBody',
    'Force',
    'Gravity',
    'Drag',
    'Magnetism',
    'Thrust',
    'DampedOscillator',
    'ENEMY_PRESETS',
    'create_enemy_physics',
]
