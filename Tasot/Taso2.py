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
    enemy_speeds=None,  # Dict with speed overrides
):
    """Spawn Level 2 enemies for the requested wave.

    Args:
        enemy_speeds: Optional dict with enemy speed overrides.
            Keys: 'straight', 'circle', 'down', 'up', 'zigzag', 'chase', 'boss_enter', 'boss_move'
            Default speeds are used if not specified.

    Returns:
        bool: True if wave was handled by this level module, else False.
    """
    # Setup default speeds and apply overrides
    if enemy_speeds is None:
        enemy_speeds = {}
    
    speeds = {
        'straight': enemy_speeds.get('straight', 190),
        'circle': enemy_speeds.get('circle', 2.0),
        'down': enemy_speeds.get('down', 330),
        'up': enemy_speeds.get('up', 340),
        'zigzag': enemy_speeds.get('zigzag', 250),
        'chase': enemy_speeds.get('chase', 200),
        'boss_enter': enemy_speeds.get('boss_enter', 360),
        'boss_move': enemy_speeds.get('boss_move', 410),
    }
    
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

        speed = speeds['straight']

        for i, ((x, y), v) in enumerate(zip(spawns, velocities)):
            sprite_idx = i % len(game.enemy_imgs)
            enemy = straight_enemy_cls(
                game.enemy_imgs[sprite_idx],
                x,
                y,
                speed=speed,
                sprite_index=sprite_idx+1,
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
            speed=speeds['zigzag'],
            amplitude=120,
            frequency=4.0,
            hp=4,
            sprite_index=1,
        )
        e2 = zigzag_enemy_cls(
            game.enemy_imgs[1],
            3 * w // 4,
            40,
            speed=speeds['zigzag'],
            amplitude=120,
            frequency=4.5,
            hp=4,
            sprite_index=2,
        )

        e3 = chase_enemy_cls(
            game.enemy_imgs[2],
            120,
            h // 2,
            speed=speeds['chase'],
            hp=4,
            sprite_index=3,
        )
        e4 = chase_enemy_cls(
            game.enemy_imgs[3],
            w - 120,
            h // 2,
            speed=speeds['chase'],
            hp=4,
            sprite_index=4,
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
            sprite_idx = i % len(game.enemy_imgs)
            enemy = down_enemy_cls(
                game.enemy_imgs[sprite_idx],
                x,
                40,
                speed=speeds['down'],
                sprite_index=sprite_idx+1,
            )
            _set_enemy_hp(enemy, 4)
            apply_hitbox(enemy, hitbox_enemy)
            game.enemies.append(enemy)

        for i, x in enumerate(bottom_x):
            sprite_idx = (i + 3) % len(game.enemy_imgs)
            enemy = up_enemy_cls(
                game.enemy_imgs[sprite_idx],
                x,
                h - 40,
                speed=speeds['up'],
                sprite_index=sprite_idx+1,
            )
            _set_enemy_hp(enemy, 4)
            apply_hitbox(enemy, hitbox_enemy)
            game.enemies.append(enemy)

        if zigzag_enemy_cls is not None:
            mid = zigzag_enemy_cls(
                game.enemy_imgs[0],
                w // 2,
                60,
                speed=speeds['zigzag'],
                amplitude=160,
                frequency=3.5,
                hp=5,
                sprite_index=1,
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
            enter_speed=speeds['boss_enter'],
            move_speed=speeds['boss_move'],
            hitbox_size=hitbox_boss,
            hitbox_offset=(0, 0),
        )
        apply_hitbox(game.boss, hitbox_boss)
        game.enemies.append(game.boss)
        return True

    return False