"""
Physics/animation.py - Physics-based animation for oscillations

Provides DampedOscillator for collision bounces and other physics-driven animations.
Uses exponential damping + sinusoidal oscillation for natural-looking motion.
"""

import pygame
import math


class DampedOscillator:
    """
    Damped harmonic oscillator for physics-based animations.
    
    Models bounces and vibrations as:
        position = base + initial_displacement * exp(-damping*t/T) * cos(omega*t)
    
    This creates natural-looking physics: initial bounce that gradually settles.
    Used to replace collision_bounce_* logic from Enemy class.
    
    Attributes:
        base (pygame.Vector2): Rest position to converge toward
        initial_disp (pygame.Vector2): Starting displacement from base
        duration (float): Total animation duration in seconds
        oscillations (float): Number of oscillation cycles during duration
        damping (float): Damping factor (higher = faster decay)
        active (bool): Is oscillation currently running?
        timer (float): Time remaining in this oscillation
    """
    
    def __init__(self, base_pos, initial_displacement, duration=2.0, 
                 oscillations=2.0, damping=2.2):
        """
        Initialize a damped oscillator.
        
        Args:
            base_pos (tuple|pygame.Vector2): Center/rest position
            initial_displacement (tuple|pygame.Vector2): Starting offset from base
            duration (float): Total animation time in seconds (default 2.0)
            oscillations (float): Number of cycles (default 2.0)
            damping (float): Exponential decay factor (default 2.2)
        
        Example:
            # Bounce an enemy 30 pixels for 1 second with 2 oscillations
            osc = DampedOscillator((100, 100), (30, 0), duration=1.0, oscillations=2.0)
        """
        self.base = pygame.Vector2(base_pos)
        self.initial_disp = pygame.Vector2(initial_displacement)
        self.duration = max(0.01, float(duration))
        self.oscillations = float(oscillations)
        self.damping = float(damping)
        
        self.timer = self.duration
        self.active = True
    
    def update(self, dt):
        """
        Update oscillator and return current position.
        
        Position decays exponentially while oscillating sinusoidally.
        When timer expires, oscillator becomes inactive and returns base position.
        
        Args:
            dt (float): Delta time in seconds
        
        Returns:
            pygame.Vector2: Current position in this frame
        """
        self.timer -= dt
        
        # Animation complete
        if self.timer <= 0:
            self.active = False
            return self.base
        
        # Calculate elapsed time
        elapsed = self.duration - self.timer
        T = self.duration
        
        # Oscillation frequency: omega = 2*pi * (oscillations / duration)
        omega = 2.0 * math.pi * (self.oscillations / T)
        
        # Exponential envelope: e^(-damping * t / T)
        # Decays to ~0.1 at t=T with damping=2.2
        envelope = math.exp(-(self.damping * elapsed) / T)
        
        # Cosine oscillation: starts at 1, oscillates
        osc = math.cos(omega * elapsed)
        
        # Final position: base + initial_disp * envelope * oscillation
        displacement = self.initial_disp * (envelope * osc)
        
        return self.base + displacement
    
    def is_active(self):
        """Check if oscillation is still in progress."""
        return self.active
    
    def __repr__(self):
        return (f"DampedOscillator(base={self.base}, "
                f"remaining={self.timer:.2f}s, active={self.active})")


class BounceAnimator:
    """
    Manager for multiple simultaneous damped oscillators.
    
    Useful when an entity needs multiple bounce points (e.g., different body parts).
    Tracks all active oscillators and provides single update interface.
    """
    
    def __init__(self):
        """Initialize empty bounce animator."""
        self.oscillators = {}
    
    def add_oscillation(self, name, base_pos, initial_disp, duration=2.0,
                       oscillations=2.0, damping=2.2):
        """
        Add a new oscillator.
        
        Args:
            name (str): Unique identifier for this oscillation
            base_pos (tuple|pygame.Vector2): Rest position
            initial_disp (tuple|pygame.Vector2): Starting offset
            duration (float): Animation duration
            oscillations (float): Number of cycles
            damping (float): Decay rate
        """
        self.oscillators[name] = DampedOscillator(
            base_pos, initial_disp, duration, oscillations, damping
        )
    
    def update(self, dt):
        """
        Update all active oscillators, removing inactive ones.
        
        Args:
            dt (float): Delta time in seconds
        
        Returns:
            dict: {name: current_position} for all active oscillators
        """
        result = {}
        
        # Update and filter inactive
        names_to_remove = []
        for name, osc in self.oscillators.items():
            pos = osc.update(dt)
            if osc.is_active():
                result[name] = pos
            else:
                names_to_remove.append(name)
        
        # Remove inactive
        for name in names_to_remove:
            del self.oscillators[name]
        
        return result
    
    def has_active(self):
        """Check if any oscillators are still active."""
        return any(osc.is_active() for osc in self.oscillators.values())
    
    def clear(self):
        """Clear all oscillators."""
        self.oscillators.clear()
