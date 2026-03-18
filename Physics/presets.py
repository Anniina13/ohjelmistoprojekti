"""
Physics/presets.py - Predefined physics profiles for enemy types

Centralizes enemy physics configuration: mass, max_speed, forces, etc.
Makes it easy to tune enemy difficulty and behavior globally.
"""

import pygame
from Physics.core import RigidBody
from Physics.forces import Drag


# Enemy physics presets - define mass, speed, and behavior for each enemy type
ENEMY_PRESETS = {
    'StraightEnemy': {
        'mass': 1.0,
        'max_speed': 220,
        'collision_radius': 24,
        'drag_coefficient': 0.05,
        'description': 'Light, fast, straight-line movement',
    },
    'CircleEnemy': {
        'mass': 1.2,
        'max_speed': 180,
        'collision_radius': 24,
        'drag_coefficient': 0.08,
        'description': 'Medium weight, circles around player',
    },
    'Figure8Enemy': {
        'mass': 0.8,
        'max_speed': 250,
        'collision_radius': 24,
        'drag_coefficient': 0.03,
        'description': 'Light, fast, figure-8 pattern',
    },
    'DownEnemy': {
        'mass': 1.0,
        'max_speed': 200,
        'collision_radius': 24,
        'drag_coefficient': 0.05,
        'description': 'Downward-moving straight enemy',
    },
    'UpEnemy': {
        'mass': 1.0,
        'max_speed': 200,
        'collision_radius': 24,
        'drag_coefficient': 0.05,
        'description': 'Upward-moving straight enemy',
    },
    'BossEnemy': {
        'mass': 5.0,
        'max_speed': 150,
        'collision_radius': 70,
        'drag_coefficient': 0.15,
        'description': 'Heavy, slow, powerful boss',
    },
    'ZigZagEnemy': {
        'mass': 0.9,
        'max_speed': 260,
        'collision_radius': 24,
        'drag_coefficient': 0.04,
        'description': 'Light, agile, zigzag pattern movement',
    },
    'ChaseEnemy': {
        'mass': 1.1,
        'max_speed': 220,
        'collision_radius': 24,
        'drag_coefficient': 0.06,
        'description': 'Medium, homing behavior toward player',
    },
}


def create_enemy_physics(enemy_type, x=0, y=0):
    """
    Factory method to create a RigidBody with preset physics.
    
    Args:
        enemy_type (str): Type of enemy (key from ENEMY_PRESETS)
        x (float): Initial X position
        y (float): Initial Y position
    
    Returns:
        RigidBody: Physics body with preset configuration
    
    Raises:
        KeyError: If enemy_type not in ENEMY_PRESETS
    
    Example:
        body = create_enemy_physics('CircleEnemy', 100, 50)
        body.add_force(Magnetism(player))
    """
    if enemy_type not in ENEMY_PRESETS:
        raise KeyError(f"Unknown enemy type: {enemy_type}. "
                      f"Valid types: {list(ENEMY_PRESETS.keys())}")
    
    preset = ENEMY_PRESETS[enemy_type]
    
    # Create RigidBody with preset mass
    body = RigidBody(x, y, mass=preset['mass'])
    
    # Apply constraints
    body.max_speed = preset['max_speed']
    body.collision_radius = preset['collision_radius']
    
    # Add default drag force
    drag_coef = preset.get('drag_coefficient', 0.05)
    body.add_force(Drag(coefficient=drag_coef))
    
    return body


def get_preset_info(enemy_type):
    """
    Get human-readable description of enemy preset.
    
    Args:
        enemy_type (str): Type of enemy
    
    Returns:
        dict: Preset configuration and description
    """
    return ENEMY_PRESETS.get(enemy_type, {})


def list_presets():
    """
    List all available enemy presets.
    
    Returns:
        list: Enemy type names
    """
    return list(ENEMY_PRESETS.keys())
