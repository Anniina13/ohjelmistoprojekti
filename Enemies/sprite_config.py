"""
Sprite-specific rotation and orientation configuration for enemies.

Each sprite index has specific properties:
- rotation_enabled: Whether to apply display_angle rotation
- rotation_offset: Angle offset to apply (in radians, -π to π)
- min_angle: Minimum angle constraint (None = no limit)
- max_angle: Maximum angle constraint (None = no limit)
- description: Sprite orientation description
"""

import math

# Sprite configuration by index
SPRITE_CONFIG = {
    1: {
        'rotation_enabled': True,
        'rotation_offset': 0.0,  # Keula alas (default, 0° = oikealle, 90° = alas)
        'min_angle': None,
        'max_angle': None,
        'description': 'keula alas - rotaatio käytössä',
    },
    2: {
        'rotation_enabled': False,
        'rotation_offset': 0.0,
        'min_angle': None,
        'max_angle': None,
        'description': 'kiinteä, EI KIERTOA',
    },
    8: {
        'rotation_enabled': False,
        'rotation_offset': 0.0,
        'min_angle': None,
        'max_angle': None,
        'description': 'kiinteä, EI KIERTOA',
    },
    9: {
        'rotation_enabled': True,
        'rotation_offset': math.pi / 2,  # Keula oikealle: +90° offset
        'min_angle': None,
        'max_angle': None,
        'description': 'keula oikealle - rotaatio käytössä',
    },
    10: {
        'rotation_enabled': False,
        'rotation_offset': 0.0,
        'min_angle': None,
        'max_angle': None,
        'description': 'kiinteä, EI KIERTOA',
    },
    11: {
        'rotation_enabled': False,
        'rotation_offset': 0.0,
        'min_angle': None,
        'max_angle': None,
        'description': 'kiinteä, EI KIERTOA',
    },
    12: {
        'rotation_enabled': True,
        'rotation_offset': math.pi / 2,  # Keula oikealle: +90° offset
        'min_angle': 0.0,  # 0° = oikealle
        'max_angle': math.pi,  # 180° = vasemmalle (ei ylösalaisin)
        'description': 'keula oikealle - vain horisontaalinen rotaatio (0-180°)',
    },
    13: {
        'rotation_enabled': True,
        'rotation_offset': math.pi / 2,  # Keula oikealle: +90° offset
        'min_angle': 0.0,  # 0° = oikealle
        'max_angle': math.pi,  # 180° = vasemmalle (ei ylösalaisin)
        'description': 'keula oikealle - vain horisontaalinen rotaatio (0-180°)',
    },
}

# Default config for unknown sprites
DEFAULT_CONFIG = {
    'rotation_enabled': True,
    'rotation_offset': 0.0,
    'min_angle': None,
    'max_angle': None,
    'description': 'tuntematon sprite - oletus rotaatio käytössä',
}


def get_sprite_config(sprite_index):
    """Get configuration for a specific sprite index."""
    return SPRITE_CONFIG.get(sprite_index, DEFAULT_CONFIG).copy()


def apply_angle_constraints(angle, config):
    """Apply min/max angle constraints to an angle."""
    min_angle = config.get('min_angle')
    max_angle = config.get('max_angle')
    
    if min_angle is not None and angle < min_angle:
        angle = min_angle
    if max_angle is not None and angle > max_angle:
        angle = max_angle
    
    return angle
