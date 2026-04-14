"""
Ammus.py projectile presets and behavior

Missä ammusten tiedot määritellään:
- Kaikki oletusarvot ja esiasetukset löytyvät Ammus.PRESETS-sanakirjasta
    alla tässä tiedostossa. Muokkaa sitä muuttaaksesi ammusten nopeutta,
    cooldownia (ms).

Miten pelaajan ammusten spawn-logiikka toimii:
- PlayerWeapons.shoot()` on yleinen kahden-luodin pikalaukaisu, joka käyttää globaalisti määritettyä `shoot_cooldown`-arvoa.
- PlayerWeapons.shoot_with(kind)` käyttää `Ammus.PRESETS[kind]`-presettiä ja kunnioittaa presetin asetuksia kuten `count`, `rps` (rounds/sec) ja `cooldown`.


- P (normaali ase, sininen) käyttää presetiä `Shot2` — oletusasetus ampuu kaksi ammusta nopealla tahdilla, ilman per-preset cooldownia (vain globaalin cooldownin rajoittama).
- L (spesiaali / teho-ammus, vihreä) käyttää presetiä `Shot1` — voimakkaampi,
    hitaampi ja sillä on preset-kohtainen cooldown (esim. 3000 ms).

Käyttö esimerkkeinä:
- Ammus.PRESETS['Shot2']['count'] = 2`  # P ampuu tuplan (sininen)
- Ammus.PRESETS['Shot1']['cooldown'] = 3000`  # L voi ampua kerran 3s (vihreä)

Huomaa:
- `Ammus.from_preset(kind, ...)` palauttaa `Ammus`-instanssin. Mahdolliset
    avaimet kuten `cooldown` eivät ole Ammuksen konstruktorin parametreja —
    ne käsitellään erikseen (esim. `PlayerWeapons` käyttää `cooldown`-kenttää).
"""

import pygame
import math

# Centralized default spawn offsets (pixels at scale_factor == 1)
# - `DEFAULT_FORWARD_OFFSET`: how far in front of the ship the projectile spawns
# - `DEFAULT_SIDE_OFFSET`: lateral separation step used when spawning multiple
#   projectiles (used to compute symmetric positions when `count` > 1)
# Adjust these values here to change spawn geometry globally.
DEFAULT_FORWARD_OFFSET = 20
DEFAULT_SIDE_OFFSET = 15

class Ammus(pygame.sprite.Sprite):
    # Built-in presets for common projectile types. Keys: 'Shot1', 'Shot2'
    PRESETS = {
        # Shot2: normaali ase (P) — tupla-ammus
        'Shot2': {
            'speed': 1000.0,
            'damage': 1,
            'size': 5,        # integer 1..10 -> scale multiplier
            'offset': (40, 6), # spawn offset (forward, side) in pixels at scale_factor=1; scaled by PlayerWeapons
            'count': 2,       # P ampuu kaksi ammusta
            'cooldown': 0,    # ms additional per-preset cooldown (0 = none)
            'rps': 6.0,       # rounds per second for this preset (P = rapid)
        },
        # Shot1: teho-ammus (L) — hitaampi mutta voimakkaampi
        'Shot1': {
            'speed': 300.0,
            'damage': 4,
            'size': 5,
            'offset': (30, 2),
            'count': 2,       # L ampuu yhden ammuksen
            'cooldown': 3000,  # 3000 ms = 3 s viive käytön jälkeen
            'rps': 0.3333333,  # ~0.333 rounds/sec = 1 shot per 3s (matches cooldown)
        }
    }

    @classmethod
    def from_preset(cls, kind, x, y, angle, image, **overrides):
        """Factory: create an `Ammus` using a named preset merged with overrides.
        Example: `Ammus.from_preset('Shot1', x, y, angle, img, speed=900)`
        """
        preset = cls.PRESETS.get(kind, {})
        params = dict(preset)
        params.update(overrides)
        # Only pass kwargs that `Ammus.__init__` accepts.
        allowed = ('speed', 'damage', 'size', 'offset', 'count')
        init_kwargs = {k: params[k] for k in allowed if k in params}
        return cls(x, y, angle, image, **init_kwargs)

    def __init__(self, x, y, angle, image, *, speed=None, damage=1, size=None, offset=(0, 0), count=1):
        """Projectile sprite.

        Backwards-compatible: old callers use (x,y,angle,image).

        New optional keyword-only parameters:
        - speed: pixels/sec (default 700)
        - damage: integer damage value
        - size: either a (w,h) tuple or a scaling float to resize the image
        - offset: (forward, side) local offsets in pixels applied relative to ship facing
        - count: kept as metadata for callers that spawn multiple projectiles
        """
        super().__init__()

        # store metadata
        self.count = int(count)
        self.damage = damage

        # determine speed
        self.speed = float(speed) if speed is not None else 700.0

        # apply size if requested
        # Accepts:
        # - integer 1..10: mapped to a scale multiplier (size/5.0 -> 1=>0.2, 5=>1.0, 10=>2.0)
        # - float: treated as scale multiplier
        # - (w,h) tuple: absolute pixel size
        img = image
        if size is not None:
            if isinstance(size, int) and 1 <= size <= 10:
                scale_mul = float(size) / 5.0
                w = max(1, int(img.get_width() * scale_mul))
                h = max(1, int(img.get_height() * scale_mul))
                img = pygame.transform.scale(img, (w, h))
            elif isinstance(size, (int, float)):
                # treat as direct multiplier
                scale_mul = float(size)
                w = max(1, int(img.get_width() * scale_mul))
                h = max(1, int(img.get_height() * scale_mul))
                img = pygame.transform.scale(img, (w, h))
            elif isinstance(size, (tuple, list)) and len(size) == 2:
                w = max(1, int(size[0]))
                h = max(1, int(size[1]))
                img = pygame.transform.scale(img, (w, h))

        # compute world-space offset from local (forward, side) offset
        ox, oy = offset if offset is not None else (0, 0)
        rad = math.radians(angle)
        forward = pygame.math.Vector2(math.cos(rad), math.sin(rad))
        right = pygame.math.Vector2(math.cos(rad + math.pi / 2), math.sin(rad + math.pi / 2))
        world_offset = forward * ox + right * oy

        # rotate image to angle
        self.image = pygame.transform.rotate(img, -angle)

        # initial position adds rotated offset
        init_x = x + world_offset.x
        init_y = y + world_offset.y
        self.rect = self.image.get_rect(center=(init_x, init_y))
        self.pos = pygame.math.Vector2(init_x, init_y)
        self.angle = angle

        # velocity vector based on speed and angle
        self.vel = pygame.math.Vector2(math.cos(rad), math.sin(rad)) * self.speed

    def update(self, dt):
        dt_s = dt / 1000.0
        self.pos += self.vel * dt_s
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def set_speed(self, speed):
        """Update projectile speed and velocity vector."""
        self.speed = float(speed)
        rad = math.radians(self.angle)
        self.vel = pygame.math.Vector2(math.cos(rad), math.sin(rad)) * self.speed

    def set_damage(self, dmg):
        self.damage = int(dmg)
