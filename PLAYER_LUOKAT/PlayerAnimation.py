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
                os.path.join(project_root, 'alukset', self.ship_name),
                os.path.join(project_root, 'alukset', f"{self.ship_name}-SPRITES"),
                os.path.join(project_root, 'alukset', f"{self.ship_name}_SPRITES"),
                os.path.join(project_root, 'images', f"{self.ship_name}_sprites"),
                os.path.join(project_root, 'images', self.ship_name),
            ]

            # Add matching folders under /alukset (e.g. FIGHTER-SPRITES).
            alukset_root = os.path.join(project_root, 'alukset')
            if os.path.isdir(alukset_root):
                for cand in sorted(os.listdir(alukset_root)):
                    if self.ship_name.lower() in cand.lower():
                        candidates.append(os.path.join(alukset_root, cand))

        base_folders = []
        seen = set()
        for cand in candidates:
            if not cand or not os.path.isdir(cand):
                continue
            key = os.path.normcase(os.path.abspath(cand))
            if key in seen:
                continue
            seen.add(key)
            base_folders.append(cand)

        frames = []

        # 1) check for Destroyed/ subfolder in any candidate base folder
        for base_folder in base_folders:
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

        # 2) if no subfolder, find files in base folders that start with Destroyed_
        for base_folder in base_folders:
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