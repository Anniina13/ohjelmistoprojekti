import pygame


def _set_enemy_hp(enemy, hp=2):
    """Aseta viholliselle elämät."""
    enemy.hp = hp
    enemy.max_hp = hp
    return enemy


def spawn_wave_taso2(
    game,
    wave_num,
    apply_hitbox,
    hitbox_enemy,
    hitbox_boss,
    straight_enemy_cls,
    circle_enemy_cls,
    boss_enemy_cls,
    down_enemy_cls,
    up_enemy_cls,
    zigzag_enemy_cls,
    chase_enemy_cls,
):
    """Spawn Level 2 enemies for the requested wave.

    Returns:
        bool: True if wave was handled by this level module, else False.
    """
    w = game.tausta_leveys
    h = game.tausta_korkeus

    if wave_num == 1:
        spawns = [
            (120, 120),
            (w - 120, 120),
            (120, h - 120),
            (w - 120, h - 120),
        ]

        velocities = [
            pygame.Vector2(1, 1),
            pygame.Vector2(-1, 1),
            pygame.Vector2(1, -1),
            pygame.Vector2(-1, -1),
        ]

        speed = 290

        for i, ((x, y), v) in enumerate(zip(spawns, velocities)):
            enemy = straight_enemy_cls(
                game.enemy_imgs[i % len(game.enemy_imgs)],
                x,
                y,
                speed=speed,
            )

            if v.length_squared() > 0:
                v = v.normalize() * speed
                enemy.vx = v.x
                enemy.vy = v.y

            _set_enemy_hp(enemy, 4)
            apply_hitbox(enemy, hitbox_enemy)
            game.enemies.append(enemy)

        return True

    if wave_num == 2:
        if zigzag_enemy_cls is None or chase_enemy_cls is None:
            return False

        e1 = zigzag_enemy_cls(
            game.enemy_imgs[0],
            w // 4,
            40,
            speed=250,
            amplitude=120,
            frequency=4.0,
            hp=4,
        )
        e2 = zigzag_enemy_cls(
            game.enemy_imgs[1],
            3 * w // 4,
            40,
            speed=250,
            amplitude=120,
            frequency=4.5,
            hp=4,
        )

        e3 = chase_enemy_cls(
            game.enemy_imgs[2],
            120,
            h // 2,
            speed=200,
            hp=4,
        )
        e4 = chase_enemy_cls(
            game.enemy_imgs[3],
            w - 120,
            h // 2,
            speed=200,
            hp=4,
        )

        for enemy in (e1, e2, e3, e4):
            _set_enemy_hp(enemy, 4)
            apply_hitbox(enemy, hitbox_enemy)
            game.enemies.append(enemy)

        return True

    if wave_num == 3:
        top_x = [w // 6, w // 2, 5 * w // 6]
        bottom_x = [w // 4, w // 2, 3 * w // 4]

        for i, x in enumerate(top_x):
            enemy = down_enemy_cls(
                game.enemy_imgs[i % len(game.enemy_imgs)],
                x,
                40,
                speed=330,
            )
            _set_enemy_hp(enemy, 4)
            apply_hitbox(enemy, hitbox_enemy)
            game.enemies.append(enemy)

        for i, x in enumerate(bottom_x):
            enemy = up_enemy_cls(
                game.enemy_imgs[(i + 3) % len(game.enemy_imgs)],
                x,
                h - 40,
                speed=340,
            )
            _set_enemy_hp(enemy, 4)
            apply_hitbox(enemy, hitbox_enemy)
            game.enemies.append(enemy)

        if zigzag_enemy_cls is not None:
            mid = zigzag_enemy_cls(
                game.enemy_imgs[0],
                w // 2,
                60,
                speed=260,
                amplitude=160,
                frequency=3.5,
                hp=5,
            )
            _set_enemy_hp(mid, 5)
            apply_hitbox(mid, hitbox_enemy)
            game.enemies.append(mid)

        return True

    if wave_num == 4:
        game.boss = boss_enemy_cls(
            game.boss_image,
            pygame.Rect(0, 0, w, h),
            hp=25,
            enter_speed=360,
            move_speed=410,
            hitbox_size=hitbox_boss,
            hitbox_offset=(0, 0),
        )
        apply_hitbox(game.boss, hitbox_boss)
        game.enemies.append(game.boss)
        return True

    return False