import random
from pgzero.actor import Actor
from pygame import Rect

TILE_SIZE = 32
MAP_PATH = "map.txt"
SOLID_CHARS = {"1"}


def load_level(path):
    with open(path, "r", encoding="utf-8") as source:
        lines = [line.rstrip("\n") for line in source if line.strip("\n")]
    if not lines:
        raise ValueError("Map file is empty.")
    width = len(lines[0])
    for line in lines:
        if len(line) != width:
            raise ValueError("All rows in the map must have the same length.")

    def make_tile_run(start_x, end_x, row):
        run_width = (end_x - start_x) * TILE_SIZE
        return Rect((start_x * TILE_SIZE, row * TILE_SIZE, run_width, TILE_SIZE))

    solids = []
    solid_tiles = []
    hero_spawn = None
    enemy_tiles = []

    for y, row in enumerate(lines):
        run_start = None
        for x, char in enumerate(row):
            if char in SOLID_CHARS:
                solid_tiles.append((x, y))
                if run_start is None:
                    run_start = x
            else:
                if run_start is not None:
                    solids.append(make_tile_run(run_start, x, y))
                    run_start = None
                if char == "P":
                    hero_spawn = ((x + 0.5) * TILE_SIZE, (y + 1) * TILE_SIZE)
                elif char == "E":
                    base_y = y
                    while base_y + 1 < len(lines) and lines[base_y + 1][x] == ".":
                        base_y += 1
                    enemy_tiles.append((x, base_y))
        if run_start is not None:
            solids.append(make_tile_run(run_start, width, y))

    if hero_spawn is None:
        hero_spawn = ((width / 2) * TILE_SIZE, (len(lines) - 1) * TILE_SIZE)

    top_segments = []
    for y, row in enumerate(lines):
        mask = [
            row[x] in SOLID_CHARS and (y == 0 or lines[y - 1][x] not in SOLID_CHARS)
            for x in range(width)
        ]
        x = 0
        while x < width:
            if mask[x]:
                start = x
                while x < width and mask[x]:
                    x += 1
                length = x - start
                if length >= 2:
                    rect = make_tile_run(start, start + length, y)
                    top_segments.append(
                        {"row": y, "start": start, "length": length, "rect": rect}
                    )
            else:
                x += 1

    if not enemy_tiles:
        for segment in top_segments:
            row = segment["row"]
            if row == 0 or row == len(lines) - 1:
                continue
            center_tile = segment["start"] + segment["length"] // 2
            enemy_tiles.append((center_tile, row))
            if len(enemy_tiles) >= 3:
                break

    enemy_spawns = []
    full_width_px = width * TILE_SIZE
    for tile_x, tile_y in enemy_tiles:
        territory = None
        for segment in top_segments:
            if (
                segment["row"] == tile_y
                and segment["start"] <= tile_x < segment["start"] + segment["length"]
            ):
                territory = segment["rect"]
                break
        if territory is None:
            left = max(0, (tile_x - 1) * TILE_SIZE)
            width_px = min(full_width_px - left, TILE_SIZE * 3)
            territory = Rect((left, tile_y * TILE_SIZE, width_px, TILE_SIZE))
        spawn_pos = ((tile_x + 0.5) * TILE_SIZE, (tile_y + 1) * TILE_SIZE)
        enemy_spawns.append({"territory": territory, "spawn": spawn_pos})

    return {
        "cols": width,
        "rows": len(lines),
        "solids": solids,
        "solid_tiles": solid_tiles,
        "hero_spawn": hero_spawn,
        "enemy_spawns": enemy_spawns,
    }


LEVEL_DATA = load_level(MAP_PATH)

WIDTH = LEVEL_DATA["cols"] * TILE_SIZE
HEIGHT = LEVEL_DATA["rows"] * TILE_SIZE
TITLE = "Skybound Ruins"

STATE_MENU = "MENU"
STATE_PLAY = "PLAYING"
STATE_VICTORY = "VICTORY"
STATE_GAME_OVER = "GAME_OVER"
STATE_EXIT = "EXITING"

BG_COLOR = (18, 22, 32)
TEXT_COLOR = (240, 240, 255)

PLAYER_SIZE = (32, 48)
MAX_HEALTH = 100
PLAYER_HIT_DAMAGE = 25

HERO_FRAMES = {
    "idle": [f"hero_idle_{i}" for i in range(6)],
    "move": [f"hero_walk_{i}" for i in range(8)],
    "attack": [f"hero_attack_{i}" for i in range(3)],
    "hit": ["hero_hit_0", "hero_hit_1"],
}
ENEMY_FRAMES = {
    "idle": [f"enemy_idle_{i}" for i in range(6)],
    "move": [f"enemy_walk_{i}" for i in range(6)],
    "attack": [f"enemy_attack_{i}" for i in range(5)],
}

MOVE_SPEED = 220
ATTACK_DURATION = 0.38
ATTACK_COOLDOWN = 0.45
ATTACK_ACTIVE_START = 0.12
ATTACK_ACTIVE_END = 0.30
ATTACK_WIDTH = 96
ATTACK_HEIGHT = 48
INVINCIBLE_TIME = 1.2

ENEMY_SPEED = 120
ENEMY_ATTACK_DURATION = 0.5
ENEMY_ATTACK_COOLDOWN = 1.1
ENEMY_ATTACK_ACTIVE_START = 0.15
ENEMY_ATTACK_ACTIVE_END = 0.32
ENEMY_ATTACK_RANGE = 60
ENEMY_SIZE = (32, 44)
ENEMY_ATTACK_SIZE = (52, 40)

MUSIC_TRACK = "music_theme"
SFX_CLICK = "click"
SFX_HIT = "hit"

SOLID_RECTS = LEVEL_DATA["solids"]
SOLID_TILE_COORDS = LEVEL_DATA["solid_tiles"]
HERO_SPAWN = LEVEL_DATA["hero_spawn"]
ENEMY_SPAWN_INFO = LEVEL_DATA["enemy_spawns"]
ENEMY_TERRITORIES = [info["territory"] for info in ENEMY_SPAWN_INFO]

BACKGROUND_BANDS = [
    (0, (12, 16, 28)),
    (HEIGHT // 2, (16, 20, 34)),
    (HEIGHT * 3 // 4, (18, 22, 36)),
]
BACKGROUND_COLUMNS = [
    (Rect((TILE_SIZE * 2, 0, TILE_SIZE * 2, HEIGHT - TILE_SIZE * 4)), (40, 52, 86)),
    (
        Rect((WIDTH - TILE_SIZE * 4, 0, TILE_SIZE * 2, HEIGHT - TILE_SIZE * 4)),
        (44, 58, 96),
    ),
]
BACKGROUND_STARS = [
    (random.randint(0, WIDTH), random.randint(40, HEIGHT // 2), random.randint(1, 2))
    for _ in range(36)
]

GRAVITY = 900
JUMP_SPEED = 420
MAX_FALL_SPEED = 780

state = STATE_MENU
audio_enabled = True
menu_buttons = []
overlay_message = ""
overlay_button = Rect(
    (WIDTH // 2 - 160, HEIGHT // 2 + 60),
    (320, 70),
)


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def draw_text(text, **kwargs):
    kwargs.setdefault("color", TEXT_COLOR)
    kwargs.setdefault("owidth", 1)
    kwargs.setdefault("ocolor", "black")
    screen.draw.text(text, **kwargs)


def draw_background_layers():
    screen.fill(BG_COLOR)
    for start_y, color in BACKGROUND_BANDS:
        height = HEIGHT - start_y
        screen.draw.filled_rect(Rect((0, start_y, WIDTH, height)), color)
    for x, y, radius in BACKGROUND_STARS:
        screen.draw.filled_circle((x, y), radius, (200, 210, 255))
    for column, color in BACKGROUND_COLUMNS:
        screen.draw.filled_rect(column, color)
        outline = (
            min(color[0] + 20, 255),
            min(color[1] + 20, 255),
            min(color[2] + 20, 255),
        )
        screen.draw.rect(column, outline)


def draw_tiles():
    base_color = (68, 80, 120)
    top_color = (188, 204, 236)
    edge_color = (28, 36, 54)
    for tile_x, tile_y in SOLID_TILE_COORDS:
        left = tile_x * TILE_SIZE
        top = tile_y * TILE_SIZE
        tile_rect = Rect((left, top, TILE_SIZE, TILE_SIZE))
        screen.draw.filled_rect(tile_rect, base_color)
        screen.draw.rect(tile_rect, edge_color)
        top_rect = Rect((left, top, TILE_SIZE, 6))
        screen.draw.filled_rect(top_rect, top_color)


def play_sound(name, force=False):
    if not (audio_enabled or force):
        return
    sound_obj = getattr(sounds, name, None)
    if sound_obj is None:
        print(f"[audio] Missing sound asset: {name}")
        return
    try:
        sound_obj.play()
    except Exception as exc:
        print(f"[audio] Failed to play '{name}': {exc}")


def start_music():
    if not audio_enabled:
        return
    for candidate in (MUSIC_TRACK, f"{MUSIC_TRACK}.wav"):
        try:
            music.play(candidate)
            break
        except Exception:
            continue


def stop_music():
    if hasattr(music, "stop"):
        music.stop()


class SpriteAnimator:
    def __init__(self, actor, frames, loop_states=None, interval=0.12):
        self.actor = actor
        self.frames = frames
        self.loop_states = loop_states or set()
        self.interval = interval
        self.state = "idle"
        self.timer = 0.0
        self.index = 0
        self.finished = False
        self.actor.image = frames[self.state][0]

    def set_state(self, state):
        if state == self.state and not self.finished:
            return
        self.state = state
        self.timer = 0.0
        self.index = 0
        self.finished = False
        self.actor.image = self.frames[self.state][0]

    def update(self, dt):
        frames = self.frames[self.state]
        if len(frames) < 2 or (self.finished and self.state not in self.loop_states):
            return
        self.timer += dt
        if self.timer < self.interval:
            return
        self.timer -= self.interval
        self.index = (self.index + 1) % len(frames)
        self.actor.image = frames[self.index]
        if self.state not in self.loop_states and self.index == len(frames) - 1:
            self.finished = True


class Character:
    def __init__(self, pos, frames, speed, loop_states=None):
        self.actor = Actor(frames["idle"][0], pos, anchor=("center", "bottom"))
        self.animator = SpriteAnimator(self.actor, frames, loop_states)
        self.speed = speed


class Hero(Character):
    def __init__(self, pos):
        super().__init__(pos, HERO_FRAMES, MOVE_SPEED, loop_states={"idle", "move"})
        self.spawn = pos
        self.lives = 3
        self.facing = 1
        self.reset(reset_lives=False)

    def reset(self, reset_lives=True):
        if reset_lives:
            self.lives = 3
        self.health = MAX_HEALTH
        self.actor.pos = self.spawn
        self.invulnerable = 0.0
        self.attack_timer = 0.0
        self.attack_cooldown = 0.0
        self.attack_used = True
        self.velocity = [0.0, 0.0]
        self.on_ground = False
        self.jump_request = False
        self.safe_pos = self.spawn
        self.max_jumps = 2
        self.jumps_used = 0
        self.animator.set_state("idle")

    def request_jump(self):
        self.jump_request = True

    def update(self, dt, solids):
        move_left = bool(keyboard.left or keyboard.a)
        move_right = bool(keyboard.right or keyboard.d)
        horizontal = int(move_right) - int(move_left)
        if horizontal:
            self.facing = 1 if horizontal > 0 else -1

        vx = horizontal * self.speed
        vy = self.velocity[1]
        if self.jump_request and self.jumps_used < self.max_jumps:
            vy = -JUMP_SPEED
            self.on_ground = False
            self.jumps_used += 1
        self.jump_request = False

        vy = min(vy + GRAVITY * dt, MAX_FALL_SPEED)

        width, height = PLAYER_SIZE
        half_width = width / 2
        pos_x = self.actor.x + vx * dt
        bottom = self.actor.y
        top = bottom - height
        left = pos_x - half_width
        right = pos_x + half_width

        if vx:
            for tile in solids:
                if bottom > tile.top and top < tile.bottom:
                    if vx > 0 and right > tile.left and left < tile.left:
                        pos_x = tile.left - half_width
                        vx = 0.0
                        break
                    if vx < 0 and left < tile.right and right > tile.right:
                        pos_x = tile.right + half_width
                        vx = 0.0
                        break
            left = pos_x - half_width
            right = pos_x + half_width

        bottom += vy * dt
        top = bottom - height
        self.on_ground = False
        if vy > 0:
            for tile in solids:
                if (
                    right > tile.left
                    and left < tile.right
                    and bottom > tile.top
                    and top < tile.top
                ):
                    bottom = tile.top
                    top = bottom - height
                    self.on_ground = True
                    vy = 0.0
                    break
        elif vy < 0:
            for tile in solids:
                if (
                    right > tile.left
                    and left < tile.right
                    and top < tile.bottom
                    and bottom > tile.bottom
                ):
                    top = tile.bottom
                    bottom = top + height
                    vy = 0.0
                    break

        boundary_left = 16 + half_width
        boundary_right = WIDTH - 16 - half_width
        clamped_x = clamp(pos_x, boundary_left, boundary_right)
        if clamped_x != pos_x:
            pos_x = clamped_x
            vx = 0.0

        self.actor.x = pos_x
        self.actor.y = bottom
        if self.on_ground:
            self.safe_pos = (self.actor.x, self.actor.y)
            self.jumps_used = 0

        self.velocity[0] = vx
        self.velocity[1] = vy

        self.invulnerable = max(0.0, self.invulnerable - dt)
        self.attack_timer = max(0.0, self.attack_timer - dt)
        self.attack_cooldown = max(0.0, self.attack_cooldown - dt)

        if self.animator.state == "hit" and self.animator.finished:
            self.animator.set_state("idle")
        if self.attack_timer > 0.0:
            self.animator.set_state("attack")
        elif self.animator.state != "hit":
            moving = horizontal != 0
            self.animator.set_state("move" if moving else "idle")

        if self.animator.state == "attack" and self.attack_timer == 0.0:
            self.attack_used = True
        self.animator.update(dt)
        self.actor.flip_x = self.facing < 0

    def attack(self):
        if self.attack_cooldown > 0.0 or self.lives <= 0:
            return False
        self.attack_timer = ATTACK_DURATION
        self.attack_cooldown = ATTACK_COOLDOWN
        self.attack_used = False
        self.animator.set_state("attack")
        return True

    def is_attack_active(self):
        if self.attack_timer <= 0.0:
            return False
        elapsed = ATTACK_DURATION - self.attack_timer
        return ATTACK_ACTIVE_START <= elapsed <= ATTACK_ACTIVE_END

    def attack_zone(self):
        if not self.is_attack_active():
            return None
        width, height = ATTACK_WIDTH, ATTACK_HEIGHT
        if self.facing >= 0:
            left = self.actor.x - 16
        else:
            left = self.actor.x - width + 16
        cy = self.actor.y - PLAYER_SIZE[1] / 2
        return Rect((int(left), int(cy - height / 2), width, height))

    def take_hit(self):
        if self.invulnerable > 0.0 or self.lives <= 0:
            return False, False
        self.invulnerable = INVINCIBLE_TIME
        self.attack_timer = 0.0
        self.attack_cooldown = 0.0
        self.attack_used = True
        self.animator.set_state("hit")
        self.velocity = [0.0, 0.0]
        self.on_ground = False
        self.jump_request = False

        self.health = max(0, self.health - PLAYER_HIT_DAMAGE)
        lost_life = False
        if self.health == 0:
            lost_life = True
            self.lives = max(0, self.lives - 1)
            self.health = MAX_HEALTH
            self.actor.x, self.actor.y = self.spawn
            self.safe_pos = self.spawn
        else:
            knockback = TILE_SIZE * 0.35
            proposed_x = clamp(self.actor.x - self.facing * knockback, 24, WIDTH - 24)
            original_y = self.actor.y
            self.actor.x = proposed_x
            hero_box = self.hitbox()
            for tile in SOLID_RECTS:
                if hero_box.colliderect(tile):
                    if self.facing >= 0:
                        self.actor.x = tile.left - PLAYER_SIZE[0] / 2 - 1
                    else:
                        self.actor.x = tile.right + PLAYER_SIZE[0] / 2 + 1
                    hero_box = self.hitbox()
                    break
            self.actor.y = original_y

        play_sound(SFX_HIT)
        return True, lost_life

    def hitbox(self):
        width, height = PLAYER_SIZE
        left = self.actor.x - width / 2
        top = self.actor.y - height
        return Rect((int(left), int(top), width, height))


class Enemy(Character):
    def __init__(self, territory, spawn_pos=None):
        if spawn_pos is None:
            spawn_pos = (territory.centerx, territory.bottom)
        half_width = ENEMY_SIZE[0] / 2
        left_bound = territory.left + half_width
        right_bound = territory.right - half_width
        if left_bound > right_bound:
            center_x = territory.centerx
            left_bound = right_bound = center_x
        spawn_x = clamp(spawn_pos[0], left_bound, right_bound)
        spawn_pos = (spawn_x, spawn_pos[1])
        super().__init__(
            spawn_pos, ENEMY_FRAMES, ENEMY_SPEED, loop_states={"idle", "move"}
        )
        self.territory = territory
        self.spawn_pos = spawn_pos
        self.surface_y = spawn_pos[1]
        self.half_width = half_width
        self.half_height = ENEMY_SIZE[1] / 2
        self.attack_offset = self.half_width + ENEMY_ATTACK_SIZE[0] / 2
        self.attack_half_height = ENEMY_ATTACK_SIZE[1] / 2
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.direction = random.choice([-1, 1])
        self.attack_timer = 0.0
        self.cooldown = 0.0
        self.alive = True
        self.actor.bottom = self.surface_y

    def reset(self):
        self.actor.x, self.actor.y = self.spawn_pos
        self.actor.bottom = self.surface_y
        self.direction = random.choice([-1, 1])
        self.attack_timer = 0.0
        self.cooldown = 0.0
        self.alive = True
        self.animator.set_state("idle")

    def take_hit(self):
        if not self.alive:
            return
        self.alive = False
        self.actor.pos = (-120, -120)

    def is_attack_active(self):
        if self.attack_timer <= 0.0:
            return False
        elapsed = ENEMY_ATTACK_DURATION - self.attack_timer
        return ENEMY_ATTACK_ACTIVE_START <= elapsed <= ENEMY_ATTACK_ACTIVE_END

    def attack_hitbox(self):
        if not self.is_attack_active():
            return None
        width, height = ENEMY_ATTACK_SIZE
        offset = self.attack_offset * (1 if self.direction > 0 else -1)
        x = self.actor.x + offset - width / 2
        y = self.actor.y - self.half_height - self.attack_half_height
        return Rect((int(x), int(y), width, height))

    def hitbox(self):
        width, height = ENEMY_SIZE
        left = self.actor.x - self.half_width
        top = self.actor.y - height
        return Rect((int(left), int(top), width, height))

    def update(self, dt, hero):
        if not self.alive:
            return

        self.cooldown = max(0.0, self.cooldown - dt)
        if self.attack_timer > 0.0:
            self.attack_timer = max(0.0, self.attack_timer - dt)
        else:
            self.actor.x += self.direction * self.speed * dt
            if self.actor.x <= self.left_bound:
                self.actor.x = self.left_bound
                self.direction = 1
            elif self.actor.x >= self.right_bound:
                self.actor.x = self.right_bound
                self.direction = -1

        if (
            hero
            and self.attack_timer == 0.0
            and self.cooldown == 0.0
            and abs(hero.actor.x - self.actor.x) <= ENEMY_ATTACK_RANGE
            and abs(hero.actor.y - self.actor.y) <= ENEMY_ATTACK_SIZE[1]
        ):
            self.direction = -1 if hero.actor.x < self.actor.x else 1
            self.attack_timer = ENEMY_ATTACK_DURATION
            self.cooldown = ENEMY_ATTACK_COOLDOWN
            self.animator.set_state("attack")

        if self.attack_timer == 0.0:
            if self.animator.state == "attack":
                self.animator.set_state("idle")
            else:
                moving = self.left_bound != self.right_bound
                self.animator.set_state("move" if moving else "idle")

        self.animator.update(dt)
        self.actor.flip_x = self.direction < 0
        self.actor.bottom = self.surface_y


hero = Hero(HERO_SPAWN)
enemies = [Enemy(info["territory"], info["spawn"]) for info in ENEMY_SPAWN_INFO]


def get_solid_rects():
    return SOLID_RECTS


def reset_world(full=True):
    hero.reset(reset_lives=full)
    for enemy in enemies:
        enemy.reset()
    global overlay_message
    overlay_message = ""


def enter_victory():
    global state, overlay_message
    overlay_message = "All pigs defeated!"
    state = STATE_VICTORY


def enter_game_over():
    global state, overlay_message
    overlay_message = "Game Over!"
    state = STATE_GAME_OVER


def create_menu_buttons():
    button_width = 320
    button_height = 64
    start_y = HEIGHT // 2 - 120
    actions = ["start", "sound", "exit"]
    buttons = []
    for index, action in enumerate(actions):
        rect = Rect(
            (
                WIDTH // 2 - button_width // 2,
                start_y + index * (button_height + 20),
            ),
            (button_width, button_height),
        )
        buttons.append({"rect": rect, "action": action, "label": ""})
    return buttons


def refresh_menu_labels():
    for entry in menu_buttons:
        action = entry["action"]
        if action == "start":
            entry["label"] = "Start Game"
        elif action == "sound":
            entry["label"] = f"Sound & Music: {'ON' if audio_enabled else 'OFF'}"
        else:
            entry["label"] = "Exit"


def start_game():
    global state
    reset_world(full=True)
    state = STATE_PLAY
    stop_music()


def toggle_audio():
    global audio_enabled
    audio_enabled = not audio_enabled
    if audio_enabled:
        if state == STATE_MENU:
            start_music()
    else:
        stop_music()
    refresh_menu_labels()


def return_to_menu():
    global state
    state = STATE_MENU
    reset_world(full=True)
    if audio_enabled:
        start_music()


def draw_menu():
    draw_background_layers()
    draw_tiles()
    draw_text("Skybound Ruins", midtop=(WIDTH // 2, HEIGHT // 5), fontsize=64)
    draw_text(
        "Arrow/WASD move • Up/W jump • Space/Z/X attack • Esc returns",
        midtop=(WIDTH // 2, HEIGHT // 5 + 60),
        fontsize=26,
        color=(210, 220, 255),
    )
    for entry in menu_buttons:
        rect = entry["rect"]
        screen.draw.filled_rect(rect, (58, 78, 128))
        screen.draw.rect(rect, (200, 220, 255))
        draw_text(entry["label"], center=rect.center, fontsize=30)


def draw_play():
    draw_background_layers()
    draw_tiles()
    draw_text(f"Lives: {hero.lives}", topleft=(20, 20), fontsize=30)
    draw_text(f"HP: {hero.health}/{MAX_HEALTH}", topleft=(20, 56), fontsize=26)
    draw_text(
        f"Sound: {'ON' if audio_enabled else 'OFF'}",
        topright=(WIDTH - 20, 20),
        fontsize=24,
    )
    hero.actor.draw()
    for enemy in enemies:
        if enemy.alive:
            enemy.actor.draw()


def draw_overlay(message):
    screen.draw.filled_rect(Rect((0, 0, WIDTH, HEIGHT)), (0, 0, 0))
    draw_text(message, center=(WIDTH // 2, HEIGHT // 2 - 40), fontsize=56)
    screen.draw.filled_rect(overlay_button, (60, 80, 130))
    screen.draw.rect(overlay_button, (200, 220, 255))
    draw_text("Restart", center=overlay_button.center, fontsize=34)


def draw_exit():
    screen.fill((0, 0, 0))
    draw_text("Thanks for playing!", center=(WIDTH // 2, HEIGHT // 2), fontsize=48)


def draw():
    if state == STATE_MENU:
        draw_menu()
    elif state == STATE_PLAY:
        draw_play()
    elif state == STATE_VICTORY:
        draw_play()
        draw_overlay(overlay_message or "Victory! All pigs defeated!")
    elif state == STATE_GAME_OVER:
        draw_play()
        draw_overlay(overlay_message or "Game Over")
    else:
        draw_exit()


def check_victory():
    if state != STATE_PLAY:
        return
    if all(not enemy.alive for enemy in enemies):
        enter_victory()


def hero_attack_check():
    if not hero.is_attack_active() or hero.attack_used:
        return
    zone = hero.attack_zone()
    if zone is None:
        return
    for enemy in enemies:
        if enemy.alive and enemy.hitbox().colliderect(zone):
            enemy.take_hit()
            hero.attack_used = True
            play_sound(SFX_HIT)
            check_victory()
            break


def hero_damage_check():
    hero_box = hero.hitbox()
    for enemy in enemies:
        if not enemy.alive:
            continue
        hitbox = enemy.attack_hitbox()
        if hitbox and hitbox.colliderect(hero_box):
            took, lost_life = hero.take_hit()
            if took and lost_life and hero.lives == 0:
                enter_game_over()
            return


def update(dt):
    if state != STATE_PLAY:
        return
    hero.update(dt, SOLID_RECTS)
    for enemy in enemies:
        enemy.update(dt, hero)
    hero_attack_check()
    hero_damage_check()
    if hero.actor.top > HEIGHT + 80:
        took, lost = hero.take_hit()
        if took and lost and hero.lives == 0:
            enter_game_over()


def on_mouse_down(pos, button):
    global state
    if state in {STATE_VICTORY, STATE_GAME_OVER}:
        if button == mouse.LEFT and overlay_button.collidepoint(pos):
            reset_world(full=True)
            state = STATE_PLAY
        return
    if state != STATE_MENU or button != mouse.LEFT:
        return
    for entry in menu_buttons:
        if entry["rect"].collidepoint(pos):
            play_sound(SFX_CLICK, force=True)
            if entry["action"] == "start":
                start_game()
            elif entry["action"] == "sound":
                toggle_audio()
            elif entry["action"] == "exit":
                state = STATE_EXIT
                stop_music()
                quit()
            break


def on_key_down(key):
    global state
    if state == STATE_MENU and key == keys.RETURN:
        play_sound(SFX_CLICK, force=True)
        start_game()
    elif state in {STATE_VICTORY, STATE_GAME_OVER}:
        if key == keys.RETURN:
            reset_world(full=True)
            state = STATE_PLAY
        elif key == keys.ESCAPE:
            return_to_menu()
    elif state == STATE_PLAY:
        if key == keys.ESCAPE:
            return_to_menu()
        if key in (keys.UP, keys.W):
            hero.request_jump()
        if key in (keys.SPACE, keys.Z, keys.X, keys.K):
            if hero.attack():
                play_sound(SFX_CLICK)


menu_buttons = create_menu_buttons()
refresh_menu_labels()
reset_world(full=True)
start_music()
