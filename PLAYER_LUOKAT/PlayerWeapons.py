import pygame
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Ammus import Ammus

class PlayerWeapons:
    def __init__(self, scale_factor):
        self.scale_factor = scale_factor
        # Find a default bullet image from available ship folders instead of hardcoding a single ship
        def find_bullet_image():
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            # check both alukset/alus and alukset root for candidate ship folders
            candidates_bases = [os.path.join(project_root, 'alukset', 'alus'), os.path.join(project_root, 'alukset')]
            for base in candidates_bases:
                if os.path.isdir(base):
                    for candidate in sorted(os.listdir(base)):
                        charge_dir = os.path.join(base, candidate, 'Charge_1')
                        if os.path.isdir(charge_dir):
                            for fn in sorted(os.listdir(charge_dir)):
                                if fn.lower().endswith('.png'):
                                    return os.path.join(charge_dir, fn)
            # fallback: try images folders
            images_dir = os.path.join(project_root, 'images')
            if os.path.isdir(images_dir):
                for root, _, files in os.walk(images_dir):
                    for fn in sorted(files):
                        if fn.lower().endswith('.png') and 'charge' in fn.lower():
                            return os.path.join(root, fn)
            return None

        bullet_path = find_bullet_image()
        if bullet_path and os.path.exists(bullet_path):
            self.bullet_img = pygame.image.load(bullet_path).convert_alpha()
            w = max(1, int(self.bullet_img.get_width() * self.scale_factor))
            h = max(1, int(self.bullet_img.get_height() * self.scale_factor))
            self.bullet_img = pygame.transform.scale(self.bullet_img, (w, h))
        else:
            # create a tiny placeholder surface if no image found
            self.bullet_img = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(self.bullet_img, (255, 255, 0), (2, 2), 2)
        self.bullets = pygame.sprite.Group()
        self.shoot_cooldown = 300
        self.shoot_timer = 0
        # Per-preset cooldown timers (ms). Keys are preset names like 'ammus1','ammus2'
        self.preset_timers = {}

    def shoot(self, pos, angle):
        if self.shoot_timer <= 0:
            side_offset = 15 # asetettu 0.5 scalefactorille. RocketGame.py(scale_factor=0.5) -> 10px
            forward_offset = 20
            rad = math.radians(angle)
            perp_rad = rad + math.pi/2
            x1 = pos.x + math.cos(rad) * forward_offset + math.cos(perp_rad) * side_offset
            y1 = pos.y + math.sin(rad) * forward_offset + math.sin(perp_rad) * side_offset
            x2 = pos.x + math.cos(rad) * forward_offset - math.cos(perp_rad) * side_offset
            y2 = pos.y + math.sin(rad) * forward_offset - math.sin(perp_rad) * side_offset
            self.bullets.add(Ammus(x1, y1, angle, self.bullet_img))
            self.bullets.add(Ammus(x2, y2, angle, self.bullet_img))

    def shoot_with(self, pos, angle, img, *, preset_kind=None, speed=None, damage=None, size=None, offset=None, count=None):
        """Shoot using a specific image and optional preset/overrides.

        - `preset_kind`: if provided, uses `Ammus.from_preset(preset_kind, ...)`
        - other kwargs override preset values.
        """
        # If a preset is used and it has an active cooldown, do nothing.
        if preset_kind and self.preset_timers.get(preset_kind, 0) > 0:
            return

        if self.shoot_timer <= 0:

            # Resolve preset parameters (if any) into a param dict we can modify per-bullet
            preset_params = {}
            if preset_kind:
                preset_params = dict(Ammus.PRESETS.get(preset_kind, {}))
            # apply explicit overrides
            if speed is not None:
                preset_params['speed'] = speed
            if damage is not None:
                preset_params['damage'] = damage
            if size is not None:
                preset_params['size'] = size
            if offset is not None:
                # offset here is a (forward, side) base; we will vary the side per-bullet
                preset_params['offset'] = offset
            if count is not None:
                preset_params['count'] = count

            # Determine fire interval (ms) from preset rps if provided,
            # otherwise fall back to global `shoot_cooldown`.
            rps = None
            if 'rps' in preset_params:
                try:
                    rps = float(preset_params.get('rps'))
                except Exception:
                    rps = None
            if rps and rps > 0:
                fire_interval = int(max(1, 1000.0 / rps))
            else:
                fire_interval = int(self.shoot_cooldown)
            self.shoot_timer = fire_interval

            # determine count (total bullets to spawn)
            total = int(preset_params.get('count', 1))

            # Forward and base side offsets
            forward_offset = float(preset_params.get('offset', (20, 15))[0])
            base_side = float(preset_params.get('offset', (20, 15))[1])

            rad = math.radians(angle)
            forward_vec = (math.cos(rad), math.sin(rad))
            right_vec = (math.cos(rad + math.pi/2), math.sin(rad + math.pi/2))

            # compute side offsets for `total` bullets, symmetric around center
            side_positions = []
            if total <= 1:
                side_positions = [0.0]
            else:
                # spacing multiplier (use base_side as step)
                step = base_side
                mid = (total - 1) / 2.0
                for i in range(total):
                    side_positions.append((i - mid) * step)

            # spawn bullets at computed offsets
            for side in side_positions:
                world_x = pos.x + forward_vec[0] * forward_offset + right_vec[0] * side
                world_y = pos.y + forward_vec[1] * forward_offset + right_vec[1] * side
                # prepare per-bullet params
                per_params = dict(preset_params)
                per_params['offset'] = (forward_offset, side)
                # create Ammus instance
                if preset_kind:
                    a = Ammus.from_preset(preset_kind, world_x, world_y, angle, img, **{k: v for k, v in per_params.items() if v is not None})
                else:
                    a = Ammus(world_x, world_y, angle, img,
                              speed=per_params.get('speed', None),
                              damage=per_params.get('damage', 1),
                              size=per_params.get('size', None),
                              offset=per_params.get('offset', (forward_offset, side)),
                              count=1)
                self.bullets.add(a)
            # If preset defines a cooldown, set it now so the preset cannot be used
            # again until the cooldown expires.
            if preset_kind:
                cd = int(preset_params.get('cooldown', 0))
                if cd > 0:
                    self.preset_timers[preset_kind] = cd

    def update(self, dt):
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
        # decrement preset timers
        if self.preset_timers:
            for k in list(self.preset_timers.keys()):
                self.preset_timers[k] -= dt
                if self.preset_timers[k] <= 0:
                    del self.preset_timers[k]
        self.bullets.update(dt)