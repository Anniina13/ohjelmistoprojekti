import pygame
import math


class Player(pygame.sprite.Sprite):
    """
    Player-luokka:
    - `frames`: lista pygame.Surface -objekteja animaation kehyksiksi
    - `rect` kertoo pelaajan sijainnin maailmassa (maailman koordinaatit)
    - update(dt) hoitaa animaation vaihtamisen
    - move(dx, dy, world_w, world_h) siirtää pelaajaa ja rajoittaa maailmaan
    - draw(screen, cam_x, cam_y) piirtää pelaajan ruudulle ottaen kameran offsetin huomioon
    """

    def __init__(self, frames, x, y, boost_frames=None):
        super().__init__()
        # tukee erillisiä animaatioita: move ja boost
        self.animations = {
            'move': frames or [pygame.Surface((32, 32), pygame.SRCALPHA)],
            'boost': boost_frames or []
        }
        self.frame_index = 0
        self.current_anim = 'move'
        # säilytä aktiivinen kuva
        self.image = self.animations[self.current_anim][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))
        # Käytetään liikkeessä tarkempaa kelluvaa sijaintia
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.angle = 0.0  # asteina
        self.turn_speed = 180.0  # astetta per sekunti
        self.accel = 300.0  # pikseleitä per sekunti^2
        self.max_speed = 400.0  # pikseleitä per sekunti
        self.brake_decel = 500.0  # jarrutusvoima (px/s^2)
        self.anim_timer = 0
        self.anim_speed = 100  # ms per frame
        self.moveUp = False
        self.moveDown = False
        self.turnLeft = False
        self.turnRight = False

    def update(self, dt):
        """Päivitä animaatioaika (dt millisekunteina)."""
        # valitse aktiivinen animaatio (boost kun w painetaan ja boost-kehyksiä löytyy)
        keys = pygame.key.get_pressed()
        self.moveUp = keys[pygame.K_w]
        self.moveDown = keys[pygame.K_s]
        
        self.turnLeft = keys[pygame.K_d]
        self.turnRight = keys[pygame.K_a]


        # tähän lisätään uusia animaatioita tarpeen mukaan.
        # valitaan tarvitaanko lista,array tai dict rakenteita
        # new_anim määritellään painikkeiden perusteella
        # w = boost, muuten move
        # ctrl = attack1, Alt Gr = attack2 jne.
        # space = rockets jne.
        new_anim = 'boost' if (self.moveUp and self.animations.get('boost')) else 'move'
        if new_anim != self.current_anim:
            self.current_anim = new_anim
            self.frame_index = 0
            self.anim_timer = 0

        frames = self.animations.get(self.current_anim, [])
        if frames:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer -= self.anim_speed
                self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]

        # aikamuunnos
        dt_s = dt / 1000.0

        # kääntö
        if self.turnLeft:
            self.angle += self.turn_speed * dt_s
        if self.turnRight:
            self.angle -= self.turn_speed * dt_s

        # eteenpäin (thrust)
        if self.moveUp:
            rad = math.radians(self.angle)
            thrust = pygame.math.Vector2(math.cos(rad), math.sin(rad)) * self.accel * dt_s
            self.vel += thrust
            # rajoitus maksiminopeuteen
            if self.vel.length() > self.max_speed:
                self.vel.scale_to_length(self.max_speed)

        # jarru (paina s)
        if self.moveDown:
            speed = self.vel.length()
            if speed > 0:
                dec = self.brake_decel * dt_s
                new_speed = max(0.0, speed - dec)
                if new_speed == 0:
                    self.vel = pygame.math.Vector2(0, 0)
                else:
                    self.vel.scale_to_length(new_speed)

        # päivitä sijainti
        self.pos += self.vel * dt_s
        # päivitä rect-keskikohta
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        # Liike on jo laskettu self.vel/self.pos: älä muuta rect:ia suoraan täällä.

    def move(self, dx, dy, world_w, world_h):
        """Siirrä pelaajaa ja rajoita maailman reunoihin."""
        # move kutsutaan pääsilmukasta mahdollisesti rajoitusten asettamiseksi
        self.rect.x += dx
        self.rect.y += dy
        # synkronoi myös pos-muuttuja, jotta seuraavat päivitykset säilyttävät koordinaatit
        self.pos.x = self.rect.centerx
        self.pos.y = self.rect.centery
        # Rajoita olio maailmaan
        self.rect.x = max(0, min(self.rect.x, world_w - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, world_h - self.rect.height))
        # pidä pos yhteneväisenä rajauksen jälkeen
        self.pos.x = self.rect.centerx
        self.pos.y = self.rect.centery
        



    def draw(self, screen, cam_x, cam_y):
        """Piirrä pelaaja ruudulle kameran offsetilla."""
        # Kierrä aktiivista kehystä ja piirrä sen keskipisteellä
        base = self.image
        rotated = pygame.transform.rotate(base, -self.angle)
        rot_rect = rotated.get_rect(center=(self.pos.x - cam_x, self.pos.y - cam_y))
        screen.blit(rotated, rot_rect.topleft)