"""
Physics/forces.py - Force hierarchy for RigidBody physics

Provides common force types:
- Gravity: Attractive force toward point
- Drag: Velocity-dependent resistance
- Magnetism: Directional attraction (for AI)
- Thrust: Directed acceleration (for player movement)
"""

import pygame
import math


class Force:
    """
    Base force class.
    
    Override get_force() to implement custom force behavior.
    All forces return a pygame.Vector2 representing the force vector (Newtons equivalent).
    """
    
    def get_force(self, body, dt):
        """
        Calculate force for this frame.
        
        Args:
            body (RigidBody): The body this force is applied to
            dt (float): Delta time in seconds
        
        Returns:
            pygame.Vector2: Force vector in pixels/second^2 units
        """
        return pygame.Vector2(0, 0)


class Gravity(Force):
    """
    Radial gravitational attraction toward a center point.
    
    Uses simplified inverse-square law: F = strength / distance^2
    
    Attributes:
        center (pygame.Vector2): Point of attraction
        strength (float): Gravitational strength parameter
    """
    
    def __init__(self, center, strength=500):
        """
        Initialize gravity field.
        
        Args:
            center (tuple|pygame.Vector2): Center of gravitational field
            strength (float): Higher = stronger attraction (default 500)
        """
        self.center = pygame.Vector2(center)
        self.strength = float(strength)
    
    def get_force(self, body, dt):
        """
        Calculate gravitational force: F = strength / distance^2
        
        Returns:
            pygame.Vector2: Force toward center point
        """
        direction = self.center - body.pos
        distance = max(1, direction.length())
        
        # Inverse-square law approximation
        force_magnitude = self.strength / (distance * distance)
        
        try:
            return direction.normalize() * force_magnitude
        except ValueError:
            return pygame.Vector2(0, 0)


class Drag(Force):
    """
    Linear velocity-dependent air resistance.
    
    Opposes motion: F = -coefficient * velocity
    Creates natural deceleration and speed damping.
    
    Attributes:
        coefficient (float): Drag coefficient (0-1 range typical)
    """
    
    def __init__(self, coefficient=0.1):
        """
        Initialize drag force.
        
        Args:
            coefficient (float): Drag strength (0.0-1.0, higher = more drag)
        """
        self.coefficient = float(coefficient)
    
    def get_force(self, body, dt):
        """
        Calculate drag force opposing velocity.
        
        Returns:
            pygame.Vector2: Force opposite to velocity direction
        """
        return -body.vel * self.coefficient


class Magnetism(Force):
    """
    Attraction force toward a target (typically the player).
    
    Used for enemy AI to create "homing" behavior.
    Strength scales with distance for more dynamic movement.
    
    Attributes:
        target (RigidBody): Target to attract toward
        strength (float): Base attraction strength
        min_distance (float): Minimum distance before force applies
    """
    
    def __init__(self, target, strength=200, min_distance=50):
        """
        Initialize magnetism force toward target.
        
        Args:
            target (RigidBody): Target entity (usually player)
            strength (float): Attraction strength (default 200)
            min_distance (float): Min distance to start attracting (default 50)
        """
        self.target = target
        self.strength = float(strength)
        self.min_distance = float(min_distance)
    
    def get_force(self, body, dt):
        """
        Calculate attraction force toward target.
        
        Scales with distance for more realistic behavior.
        
        Returns:
            pygame.Vector2: Force toward target
        """
        if self.target is None:
            return pygame.Vector2(0, 0)
        
        direction = self.target.pos - body.pos
        distance = direction.length()
        
        if distance < self.min_distance:
            return pygame.Vector2(0, 0)
        
        # Scale force with distance (closer = stronger)
        force_magnitude = self.strength * (distance / 500.0)
        
        try:
            return direction.normalize() * force_magnitude
        except ValueError:
            return pygame.Vector2(0, 0)


class Thrust(Force):
    """
    Directed acceleration force.
    
    Used for player propulsion and enemy movement.
    Applies constant force in specified direction.
    
    Attributes:
        direction (pygame.Vector2): Normalized direction vector
        magnitude (float): Force strength
    """
    
    def __init__(self, direction, magnitude):
        """
        Initialize thrust force in specific direction.
        
        Args:
            direction (tuple|pygame.Vector2): Direction to apply force
            magnitude (float): Force strength (pixels/second^2)
        """
        dir_vec = pygame.Vector2(direction)
        try:
            self.direction = dir_vec.normalize()
        except ValueError:
            self.direction = pygame.Vector2(1, 0)
        self.magnitude = float(magnitude)
    
    def get_force(self, body, dt):
        """
        Return constant thrust force in direction.
        
        Returns:
            pygame.Vector2: Force in specified direction
        """
        return self.direction * self.magnitude


class Spring(Force):
    """
    Spring-like restoring force.
    
    Pulls entity toward anchor point: F = -k * displacement
    Useful for oscillations and orbits.
    
    Attributes:
        anchor (pygame.Vector2): Rest position
        stiffness (float): Spring constant (higher = stiffer)
        damping (float): Damping coefficient (stabilizes oscillation)
    """
    
    def __init__(self, anchor, stiffness=100, damping=0.1):
        """
        Initialize spring force.
        
        Args:
            anchor (tuple|pygame.Vector2): Rest position
            stiffness (float): Spring constant (default 100)
            damping (float): Energy loss per step (default 0.1)
        """
        self.anchor = pygame.Vector2(anchor)
        self.stiffness = float(stiffness)
        self.damping = float(damping)
    
    def get_force(self, body, dt):
        """
        Calculate spring force: F = -k*x - b*v
        
        Returns:
            pygame.Vector2: Restoring force toward anchor
        """
        displacement = self.anchor - body.pos
        spring_force = displacement * self.stiffness
        damping_force = body.vel * (-self.damping)
        return spring_force + damping_force
