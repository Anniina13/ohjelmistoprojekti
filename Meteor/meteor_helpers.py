"""Helper functions for spawning meteors in levels.

Provides convenience functions to spawn moving meteors.
"""

import random
from Meteor.meteor import Meteor


def spawn_moving_meteor(game, speed=80):
    """Spawn a meteor cluster with one large and a few smaller meteors.
    
    The meteor spawns above the play area and moves diagonally downward
    (down-left or down-right), then despawns after exiting.
    
    Args:
        game: The Game instance
        speed: Movement speed in pixels per second (default 80)
        
    Returns:
        The large lead Meteor instance
    """
    # Get screen bounds
    width = game.tausta_leveys
    height = game.tausta_korkeus
    spawn_margin = 140
    
    # Spawn above top edge and move diagonally downward.
    x = random.randint(80, max(80, width - 80))
    y = -spawn_margin
    dx = random.choice((-1, 1))
    vel = (dx * speed * 0.7071, speed * 0.7071)
    
    lead_meteor = Meteor(
        x, y,
        image=None,
        bounds=(width, height),
        speed=speed,
        velocity=vel,
        size_scale=1.0,
    )
    game.meteors.append(lead_meteor)

    # Add 2-4 smaller meteors around the lead meteor to form a cluster.
    small_count = random.randint(2, 4)
    for _ in range(small_count):
        offset_x = random.randint(-140, 140)
        offset_y = random.randint(-120, 30)
        size_scale = random.uniform(0.42, 0.68)
        speed_mul = random.uniform(1.02, 1.22)

        small_vel = (
            vel[0] * speed_mul + random.uniform(-12.0, 12.0),
            vel[1] * speed_mul + random.uniform(-10.0, 10.0),
        )

        small_meteor = Meteor(
            x + offset_x,
            y + offset_y,
            image=None,
            bounds=(width, height),
            speed=speed * speed_mul,
            velocity=small_vel,
            size_scale=size_scale,
        )
        game.meteors.append(small_meteor)

    return lead_meteor


def spawn_meteor(game, x, y, image=None):
    """Spawn a single meteor at a specific position with random direction.
    
    Args:
        game: The Game instance
        x: X position in pixels
        y: Y position in pixels
        image: Optional pre-loaded pygame Surface for the meteor
        
    Returns:
        The created Meteor instance
    """
    meteor = Meteor(
        x, y,
        image=image,
        bounds=(game.tausta_leveys, game.tausta_korkeus),
        speed=80
    )
    game.meteors.append(meteor)
    return meteor

