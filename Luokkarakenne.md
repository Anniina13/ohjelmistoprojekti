# Peliprojektin luokkajako ja vastuualueet

Tämä dokumentti kuvaa peliprojektin (Python + Pygame) luokkajaon siten, että työ on helppo jakaa usean koodaajan kesken. Jako pohjautuu annettuun vaatimusmäärittelyyn.

---

## Osa 1: Pelin runko ja pelitilat

**Luokat:**

* `Main`
* `StartGame`
* `GameOver`

**Vastuu:**

* Pelin käynnistys ja pääsilmukka
* FPS:n hallinta
* Pelitilojen vaihto (aloitus, peli, game over)
* Yhteys muihin järjestelmiin (UI, pelaaja, tasot)

---

## Osa 2: Käyttöliittymä ja valikot

**Luokat:**

* `Menu`
* `HUD`

**Vastuu:**

* Päävalikko (aloita peli, ohjeet, lopeta)
* Taukovalikko
* Pisteiden ja elämien näyttäminen
* Tekstien ja kieliresurssien käsittely

---

## Osa 3: Pelaaja ja ammukset

**Luokat:**

* `Player`
* `Weapon`
* (valinnainen) `ShipType` / `Character`

**Vastuu:**

* Pelaajan liikkuminen
* Ampuminen (ammusten luonti ja hallinta)
* Hahmon valinta
* Power-upien vaikutukset

> Huom: `Projectile`-luokkaa ei ole erillisenä, vaan ammukset käsitellään osana pelaajan ja aseen logiikkaa.

---

## Osa 4: Viholliset

**Luokat:**

* `Enemy` (yläluokka)
* `EnemyTypeA`
* `EnemyTypeB`
* `EnemyTypeC`
* (valinnainen) `BossEnemy`

**Vastuu:**

* Vihollisten liike ja käyttäytyminen
* Kestävyys ja osumien käsittely
* Vihollisten ampuminen myöhemmillä tasoilla

---

## Osa 5: Törmäykset ja vahingot

**Luokat:**

* `CollisionManager`

**Vastuu:**

* Pelaajan ja vihollisten törmäykset
* Ammusten osumat
* Elämien vähentäminen ja kuolemat

---

## Osa 6: Tasot ja vihollisten ilmestyminen

**Luokat:**

* `Level`
* `EnemySpawner`

**Vastuu:**

* Tasokohtaiset säännöt
* Vihollisten määrä ja tyypit
* Pistetavoitteet ja päävihollisen ilmestyminen

---

## Osa 7: Pisteytys ja tallennus

**Luokat:**

* `ScoreManager`
* `SettingsManager`

**Vastuu:**

* Pisteiden laskeminen
* High score -tallennus
* Ääni- ja ohjausasetusten tallennus

---

## Osa 8: Äänet ja efektit

**Luokat:**

* `SoundManager`

**Vastuu:**

* Taustamusiikki
* Äänitehosteet
* Äänien mykistys ja huomiointi asetuksissa

---

## Yhteenveto

* Luokat on jaettu modulaarisesti
* Jokainen osa voidaan toteuttaa itsenäisesti
* Rakenne tukee laajennettavuutta ja huollettavuutta
