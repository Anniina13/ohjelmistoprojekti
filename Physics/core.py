"""
Physics/core.py - Base RigidBody class for physics-enabled entities

Provides unified physics simulation for all game objects (player, enemies, projectiles).
Each entity maintains position, velocity, acceleration, mass, and can have forces applied.
"""

import pygame
import math


class RigidBody:
    """
    Base class for all physics-enabled objects in the game.
    
    Handles:
    - Position and velocity tracking
    - Force accumulation and application
    - Velocity constraints (max speed)
    - Integration: forces -> acceleration -> velocity -> position
    
    Attributes:
        pos (pygame.Vector2): Position in world space
        vel (pygame.Vector2): Velocity vector (pixels/second)
        acc (pygame.Vector2): Accumulated acceleration (cleared each frame)
        mass (float): Physical mass (kg equivalent)
        inv_mass (float): Cached 1/mass for optimization
        collision_radius (float): Radius for collision detection
        max_speed (float|None): Optional maximum speed constraint
        forces (list): List of Force objects to apply each frame
        is_dynamic (bool): Can this body be affected by forces?
    """
    
    def __init__(self, x=0, y=0, mass=1.0):
        """
        Initialize a physics body.
        
        Args:
            x (float): Initial X position
            y (float): Initial Y position
            mass (float): Physical mass (default 1.0)
        
        Raises:
            ValueError: If mass is zero or negative
        """
        if mass <= 0:
            raise ValueError("Mass must be positive")
            
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        
        self.mass = float(mass)
        self.inv_mass = 1.0 / self.mass
        
        self.collision_radius = 1.0
        self.max_speed = None  # No limit by default
        
        self.forces = []
        self.is_dynamic = True
    
    def add_force(self, force):
        """
        Add a force to be applied during next update().
        
        Args:
            force (Force): A Force object with get_force(body, dt) method
        """
        if force is not None:
            self.forces.append(force)
    
    def apply_forces(self, dt):
        """
        Sum all forces and convert to acceleration.
        
        F = ma => a = F/m (sum of all forces divided by mass)
        Clears force list after application.
        
        Args:
            dt (float): Delta time in seconds
        """
        self.acc = pygame.Vector2(0, 0)
        
        for force in self.forces:
            try:
                f = force.get_force(self, dt)
                if f is not None:
                    self.acc += f * self.inv_mass
            except Exception:
                # Silently skip invalid forces
                pass
        
        self.forces = []  # Clear for next frame
    
    def apply_velocity_constraints(self):
        """
        Apply maximum speed constraint if set.
        
        Clamps velocity to max_speed by scaling velocity vector.
        """
        if self.max_speed is not None and self.max_speed > 0:
            speed = self.vel.length()
            if speed > self.max_speed:
                self.vel.scale_to_length(self.max_speed)
    
    def update_velocity(self, dt):
        """
        Update velocity from acceleration: v += a*dt
        
        Then apply velocity constraints.
        
        Args:
            dt (float): Delta time in seconds
        """
        self.vel += self.acc * dt
        self.apply_velocity_constraints()
    
    def update_position(self, dt):
        """
        Update position from velocity: pos += v*dt
        
        Args:
            dt (float): Delta time in seconds
        """
        self.pos += self.vel * dt
    
    def update(self, dt):
        """
        Perform complete physics step:
        1. Apply forces -> acceleration
        2. Update velocity with acceleration
        3. Update position with velocity
        
        Args:
            dt (float): Delta time in seconds
        """
        if not self.is_dynamic:
            return
            
        self.apply_forces(dt)
        self.update_velocity(dt)
        self.update_position(dt)
    
    def set_velocity(self, vx, vy):
        """Set velocity directly."""
        self.vel = pygame.Vector2(vx, vy)
        self.apply_velocity_constraints()
    
    def get_speed(self):
        """Get current speed magnitude."""
        return self.vel.length()
    
    def __repr__(self):
        return (f"RigidBody(pos={self.pos}, vel={self.vel}, "
                f"mass={self.mass}, speed={self.get_speed():.1f})")
