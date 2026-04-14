import os
import pygame

# ============================================================================
# PLANEETAN ANIMAATIO JA PIIRTÄMINEN
# ============================================================================
# LATAA PLANEETAN KUVIA, KIERTÄÄ NIITÄ TAI ANIMOI KUVARUUTSARJAA, JA PIIRTÄÄ
# NE RUUDULLE ERI ASEMIIN (KEHYKSEN YLÄ, RUUDUN KESKI, MAAILMAN KOORDINAATIT).

# KÄYTTÖLIITTYMÄ:
#   init_planet(project_root=None, filename=None, height=96, rot_speed_deg=36.0)
#   update_planet(dt_ms)
#   draw_planet_above_frame(screen, frame_x, frame_y, frame_w, frame_h, gap=6)

# ALKUPERÄINEN KUVA ENNEN MUUNNOKSIA (pygame.Surface TAI NONE)
_sprite_orig = None
# KUVA JONKA KIERRETÄÄN NÄYTÖLLÄ (pygame.Surface TAI NONE)
_sprite_base = None
# NYKYINEN KIERTOKULMA ASTEISSA (0-360)
_angle = 0.0
# KIERTONOPEUS ASTEISSA SEKUNNISSA
_rot_speed = 36.0
# KAIKKI KUVARUUDUT KUN KÄYTETÄÄN KUVARUUTSARJA-ANIMAATIOTA (LISTA pygame.Surface OBJEKTEJA)
_frames = []
# NYKYISEN KUVARUUDUN INDEKSI LISTASSA
_frame_index = 0
# KULUNUT AIKA NYKYISELLE KUVARUUDULLE MILLISEKUNTEISSA
_frame_time = 0.0
# KUINKA KAUAN YKSI KUVARUUTU NÄYTETÄÄN MILLISEKUNTEISSA
_frame_duration = 200.0
# TOIMINTATILA: 'rotate' = KIERTÄVÄ KUVA TAI 'frames' = KUVARUUTSARJA
_mode = 'rotate'


def init_planet(project_root=None, filename=None, height=96, rot_speed_deg=36.0, mode='rotate', frame_duration_ms=200.0):
    """
    ALUSTAA PLANEETAN KUVAN JA ANIMAATION ASETUKSET.
    
    LATAA PLANEETAN KUVATIEDOSTON MÄÄRITELLYSTÄ KANSIOSTA, MUOKKAA SEN KOKOA
    JA VALMISTELEE SEN PIIRTÄMISEEN JOKO KIERTÄVÄNÄ TAI KUVARUUTSARJANA.
    
    Parametrit:
        project_root (str): Projektin juuri. Jos None, käytetään tämän tiedoston sijaintia.
        filename (str): Kuvatiedoston nimi. Jos None, käytetään oletuksena Terrestrial_03-512x512.png tai ensimmäistä löydettyä.
        height (int): Kuvan näyttökorkeus pikseleissä (oletus 96).
        rot_speed_deg (float): Kiertonopeus asteissa sekunnissa (oletus 36).
        mode (str): Animaatiotila 'rotate' tai 'frames' (oletus 'rotate').
        frame_duration_ms (float): Kuvaruudun näyttöaika millisekunteissa (oletus 200).
    
    Palautus: Ei palautuksia. Asettaa globaalit muuttujat.
    """
    global _sprite_base, _sprite_orig, _rot_speed, _angle, _frames, _frame_index, _frame_time, _frame_duration, _mode
    _angle = 0.0
    _rot_speed = float(rot_speed_deg)
    _mode = mode or 'rotate'
    _frames = []
    _frame_index = 0
    _frame_time = 0.0
    _frame_duration = float(frame_duration_ms)
    try:
        # Planeetan kuvien kansion sijainti
        planet_dir = os.path.join(project_root, 'images', 'SBS - 2D Planet Pack 2 - Shaded 512x512',
                                  'Large Planets 512x512', 'Solid', 'Terrestrial')
        # Kun käytetään kuvaruutsarja-animaatiota, ladataan kaikki PNG-kuvat kansiosta
        if _mode == 'frames':
            # Kuvatiedostojen nimet
            names = []
            if filename:
                names = [filename]
            else:
                # Ladataan kaikki PNG-tiedostot kansiosta aakkosissa järjestyksessä
                names = sorted([n for n in os.listdir(planet_dir) if n.lower().endswith('.png')])
            if not names:
                _sprite_base = None
                _sprite_orig = None
                return

            # Käydään läpi jokainen tiedosto ja lisätään kuvaruudut listaan
            for n in names:
                path = os.path.join(planet_dir, n)
                surf = pygame.image.load(path).convert_alpha()
                try:
                    # Poistetaan tyhjä tila kuvan ympärillä
                    bbox = surf.get_bounding_rect()
                    cropped = surf.subsurface(bbox).copy() if bbox.width and bbox.height else surf
                except Exception:
                    cropped = surf
                # Skaalataan kuva haluttuun korkeuteen säilyttäen kuvasuhteen
                if cropped.get_height() != height:
                    pw = max(1, int(cropped.get_width() * (height / cropped.get_height())))
                    frame = pygame.transform.smoothscale(cropped, (pw, height))
                else:
                    frame = cropped
                _frames.append(frame)
            # Säilytetään ensimmäinen kuvaruutu yhteensopivuutta varten
            _sprite_orig = _frames[0].copy() if _frames else None
            _sprite_base = _sprite_orig
            return

        # Yksittäisen kuvan kierto-animaatio oletustavana
        if filename:
            path = os.path.join(planet_dir, filename)
        else:
            # Yritetään ensiksi oletusvaihtoehtoa
            preferred = os.path.join(planet_dir, 'Terrestrial_03-512x512.png')
            if os.path.exists(preferred):
                path = preferred
            else:
                # Jos oletusvaihtoehtoa ei ole, käytetään ensimmäistä löydettyä PNG:tä
                names = [n for n in os.listdir(planet_dir) if n.lower().endswith('.png')]
                if not names:
                    _sprite_base = None
                    _sprite_orig = None
                    return
                path = os.path.join(planet_dir, names[0])

        # Ladataan kuva
        surf = pygame.image.load(path).convert_alpha()
        try:
            # Poistetaan tyhjä tila kuvan ympärillä
            bbox = surf.get_bounding_rect()
            cropped = surf.subsurface(bbox).copy() if bbox.width and bbox.height else surf
        except Exception:
            cropped = surf
        _sprite_orig = cropped.copy()
        # Skaalataan kuva haluttuun korkeuteen säilyttäen kuvasuhteen
        if cropped.get_height() != height:
            pw = max(1, int(cropped.get_width() * (height / cropped.get_height())))
            base_surf = pygame.transform.smoothscale(cropped, (pw, height))
        else:
            base_surf = cropped
        _sprite_base = base_surf
    except Exception:
        _sprite_base = None
        _sprite_orig = None


def update_planet(dt_ms):
    """
    PÄIVITTÄÄ PLANEETAN KIERTOKULMAA TAI KUVARUUTUA AJAN KULUMISEN MUKAISESTI.
    
    JOS KÄYTETÄÄN 'rotate'-TILAA, KIERRETÄÄN KUVAA. JOS KÄYTETÄÄN 'frames'-TILAA,
    SIIRRETÄÄN SEURAAVAAN KUVARUUTUUN MÄÄRITETYN AJAN KULUTTUA.
    
    Parametrit:
        dt_ms (float): Kulunut aika millisekunteissa edellisestä päivityksestä.
    
    Palautus: Ei palautuksia. Päivittää globaalit muuttujat (_angle, _frame_index).
    """
    global _angle, _frame_time, _frame_index
    # Muutetaan millisekunnit sekunneiksi
    dt = max(0.0, dt_ms) / 1000.0
    if _mode == 'frames' and _frames:
        # Kuvaruutsarja-animaatio: lasketaan nykyinen kuvaruutu kuluvan ajan perusteella
        total = _frame_time + max(0.0, dt_ms)
        if _frame_duration > 0:
            _frame_index = int(total // _frame_duration) % len(_frames)
            _frame_time = total % _frame_duration
        else:
            _frame_time = 0.0
    else:
        # Kierto-animaatio: päivitetään kiertokulma
        _angle = (_angle + _rot_speed * dt) % 360.0


def draw_planet_above_frame(screen, frame_x, frame_y, frame_w, frame_h, gap=6):
    import os
    import pygame

    # Simple planets helper: load a decorative planet sprite, handle rotation and drawing.
    # Public API:
    #   init_planet(project_root=None, filename=None, height=96, rot_speed_deg=36.0)
    #   update_planet(dt_ms)
    #   draw_planet_above_frame(screen, frame_x, frame_y, frame_w, frame_h, gap=6)

    _sprite_orig = None
    _sprite_base = None
    _angle = 0.0
    _rot_speed = 36.0


    def init_planet(project_root=None, filename=None, height=96, rot_speed_deg=36.0):
        global _sprite_base, _rot_speed, _angle
        _angle = 0.0
        _rot_speed = float(rot_speed_deg)
        if project_root is None:
            project_root = os.path.dirname(__file__)

        # default folder for terrestrial sprites
        planet_dir = os.path.join(project_root, 'images', 'SBS - 2D Planet Pack 2 - Shaded 512x512',
                                  'Large Planets 512x512', 'Solid', 'Terrestrial')
        try:
            if filename:
                path = os.path.join(planet_dir, filename)
            else:
                preferred = os.path.join(planet_dir, 'Terrestrial_03-512x512.png')
                if os.path.exists(preferred):
                    path = preferred
                else:
                    names = [n for n in os.listdir(planet_dir) if n.lower().endswith('.png')]
                    if not names:
                        _sprite_base = None
                        return
                    path = os.path.join(planet_dir, names[0])

            surf = pygame.image.load(path).convert_alpha()
            _sprite_orig = surf.copy()
            # scale to requested height preserving aspect
            if surf.get_height() != height:
                pw = max(1, int(surf.get_width() * (height / surf.get_height())))
                surf = pygame.transform.smoothscale(surf, (pw, height))
            _sprite_base = surf
        except Exception:
            _sprite_base = None


    def update_planet(dt_ms):
        global _angle
        dt = max(0.0, dt_ms) / 1000.0
        _angle = (_angle + _rot_speed * dt) % 360.0


    def draw_planet_above_frame(screen, frame_x, frame_y, frame_w, frame_h, gap=6):
        """Draw rotating planet centered horizontally above the given frame rect.
        If no sprite is loaded this does nothing.
        """
        if _sprite_base is None:
            return
        try:
            # rotate the base sprite by current angle (negate for pygame coordinates)
            surf = pygame.transform.rotozoom(_sprite_base, -_angle, 1.0)
            px = frame_x + (frame_w - surf.get_width()) // 2
            py = frame_y - surf.get_height() - gap
            screen.blit(surf, (px, py))
        except Exception:
            pass


    def draw_planet_screen(screen, screen_x, screen_y, height=320, gap=0):
        """Draw a large rotating planet at screen coordinates (screen_x, screen_y) as center.
        - `height` controls the display height in pixels (scales original image).
        - `screen_x, screen_y` are the center position in screen pixels.
        """
        if _sprite_orig is None:
            return
        try:
            # scale original to requested height preserving aspect
            base = _sprite_orig
            if base.get_height() != height:
                pw = max(1, int(base.get_width() * (height / base.get_height())))
                base = pygame.transform.smoothscale(base, (pw, height))
            surf = pygame.transform.rotozoom(base, -_angle, 1.0)
            r = surf.get_rect(center=(screen_x, screen_y - gap))
            screen.blit(surf, r.topleft)
        except Exception:
            pass


    def draw_planet_world(screen, camera_x, camera_y, world_x, world_y, height=320):
        """Draw planet at world coordinates (world_x, world_y). Converts to screen coords using camera.
        Centers the planet at the given world position.
        """
        if _sprite_orig is None:
            return
        try:
            base = _sprite_orig
            if base.get_height() != height:
                pw = max(1, int(base.get_width() * (height / base.get_height())))
                base = pygame.transform.smoothscale(base, (pw, height))
            surf = pygame.transform.rotozoom(base, -_angle, 1.0)
            screen_x = int(world_x - camera_x)
            screen_y = int(world_y - camera_y)
            r = surf.get_rect(center=(screen_x, screen_y))
            screen.blit(surf, r.topleft)
        except Exception:
            pass
    # center blit both frames with alpha blending
