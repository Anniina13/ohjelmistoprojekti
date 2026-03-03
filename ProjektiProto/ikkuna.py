# Pohjat otettu: https://www.youtube.com/watch?v=2iyx8_elcYg
# Avaruus-spriteja löytyy: https://www.freepik.com/free-photos-vectors/space-sprite#uuid=689f2d8e-f000-4f6c-be3f-d277040f2102
import pygame
import os
import random



currentWorkDir = os.getcwd()
print(currentWorkDir)

sourceFileDir = os.path.dirname(os.path.abspath(__file__))
print(sourceFileDir)


pygame.init()
Y = 800
X = 1600


screen = pygame.display.set_mode((X,Y))

# load, convert and scale background to window size
tausta = pygame.image.load(os.path.join(os.path.dirname(__file__),'img','avaruus.jpg')).convert()
tausta = pygame.transform.scale(tausta, (X, Y))
# Käytetään hallittua skaalausta (esim. 1.5x) jotta tausta on hieman suurempi kuin ikkuna
scale_factor = 1
tausta = pygame.transform.scale(tausta, (int(X * scale_factor), int(Y * scale_factor)))

# Lataa planeetat ja arvo niiden paikat ison taustan mukaan
planeetat = [
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice2.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice3.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice4.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice5.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice6.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice7.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice8.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice9.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("ProjektiProto/img/slice10.png"), (100, 100)),
]

tausta_leveys, tausta_korkeus = tausta.get_width(), tausta.get_height()
planeetta_paikat = []
for _ in range(len(planeetat)):
    x = random.randint(0, max(0, tausta_leveys - 300))
    y = random.randint(0, max(0, tausta_korkeus - 300))
    planeetta_paikat.append((x, y))

# -----------------------------
# Pelaajan (Player) lataus ja asetukset
# - Lataa pelaajan sprite-tiedostot tarvittaessa
# - Player-olio maailman keskelle
# -----------------------------
from player import Player

# Sprite loading removed; use project-specific ship folders instead
frames = []
boost_frames = []



# Luo pelaaja maailman keskelle
player_start_x = tausta_leveys // 2
player_start_y = tausta_korkeus // 2
player = Player(frames, player_start_x, player_start_y, boost_frames=boost_frames)

# Kello frameratea ja animaatiota varten
clock = pygame.time.Clock()

# Alusta kamera ennen silmukkaa
camera_x = 0
camera_y = 0
run = True
while run:
    # Tapahtumien käsittely
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # rajoita framerate ja hae dt (millisekunteina)
    dt = clock.tick(60)

    # Päivitä pelaaja (animaatio + näppäinliike)
    player.update(dt)
    # Varmista, että pelaaja pysyy taustan sisällä
    player.move(0, 0, tausta_leveys, tausta_korkeus)


    # Keskitetään kamera pelaajaan (kameran sijainti maailmassa)
    camera_x = player.rect.centerx - X // 2
    camera_y = player.rect.centery - Y // 2
    # Rajoita kamera taustan reunoihin
    camera_x = max(0, min(camera_x, tausta_leveys - X))
    camera_y = max(0, min(camera_y, tausta_korkeus - Y))

    # Piirrä tausta kameran kohdalta
    screen.blit(tausta, (0, 0), area=(camera_x, camera_y, X, Y))

    # Piirrä planeetat kameran offsetilla
    for kuva, (x, y) in zip(planeetat, planeetta_paikat):
        screen.blit(kuva, (x - camera_x, y - camera_y))

    # Piirrä pelaaja kameran suhteessa
    player.draw(screen, camera_x, camera_y)

    # Päivitä näyttö
    pygame.display.update()
    

pygame.quit()