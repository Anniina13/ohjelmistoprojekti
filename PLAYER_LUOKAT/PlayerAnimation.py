import pygame
import os

class PlayerAnimation:
    def __init__(self, scale_factor, ship_name=None):
        self.scale_factor = scale_factor
        self.ship_name = ship_name

    def load_destroyed_sprites(self):
        """Load destroyed animation frames.

        Prefer dynamic ship-specific folders (like Player2):
        - alukset/alus/<ship_name>/Destroyed/
        - images/<ship_name>_sprites/ (files prefixed with Destroyed_*)
        - images/<ship_name>/ (files prefixed with Destroyed_*)

        No legacy hardcoded ship fallback is used.
        """
        def find_project_root(start_path):
            d = os.path.dirname(os.path.abspath(start_path))
            while True:
                if os.path.isdir(os.path.join(d, 'alukset')):
                    return d
                parent = os.path.dirname(d)
                if parent == d:
                    return os.path.dirname(os.path.abspath(start_path))
                d = parent

        project_root = find_project_root(__file__)

        candidates = []
        if self.ship_name:
            candidates = [
                os.path.join(project_root, 'alukset', 'alus', self.ship_name),
                os.path.join(project_root, 'images', f"{self.ship_name}_sprites"),
                os.path.join(project_root, 'images', self.ship_name),
            ]

        def first_exist(paths):
            for p in paths:
                if p and os.path.isdir(p):
                    return p
            return None

        base_folder = first_exist(candidates) if candidates else None

        frames = []

        # 1) check for Destroyed/ subfolder in base_folder
        if base_folder:
            destroyed_folder = os.path.join(base_folder, 'Destroyed')
            if os.path.isdir(destroyed_folder):
                files = [f for f in sorted(os.listdir(destroyed_folder)) if f.lower().endswith('.png')]
                for fname in files:
                    path = os.path.join(destroyed_folder, fname)
                    img = pygame.image.load(path).convert_alpha()
                    w = max(1, int(img.get_width() * self.scale_factor))
                    h = max(1, int(img.get_height() * self.scale_factor))
                    frames.append(pygame.transform.scale(img, (w, h)))
                if frames:
                    return frames

            # 2) if no subfolder, find files in base_folder that start with Destroyed_
            candidates_files = []
            for fname in sorted(os.listdir(base_folder)):
                low = fname.lower()
                if low.endswith('.png') and (low.startswith('destroyed_') or low == 'destroyed.png'):
                    candidates_files.append(fname)

            if candidates_files:
                import re

                def sort_key(fn):
                    mm = re.search(r"(\d+)", fn)
                    if mm:
                        return int(mm.group(1))
                    return fn

                for fname in sorted(candidates_files, key=sort_key):
                    path = os.path.join(base_folder, fname)
                    img = pygame.image.load(path).convert_alpha()
                    w = max(1, int(img.get_width() * self.scale_factor))
                    h = max(1, int(img.get_height() * self.scale_factor))
                    frames.append(pygame.transform.scale(img, (w, h)))
                if frames:
                    return frames

        # 3) No legacy hardcoded-ship fallback any more. If nothing found, return empty list.
        return frames


    def scale_frames(self, frames):
        if not frames:
            return []
        scaled = []
        for f in frames:
            w = max(1, int(f.get_width() * self.scale_factor))
            h = max(1, int(f.get_height() * self.scale_factor))
            scaled.append(pygame.transform.scale(f, (w, h)))
        return scaled