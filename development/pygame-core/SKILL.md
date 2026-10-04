---
name: pygame-core
description: >
  Structure a pygame (pygame-ce) game in Python: the init/event/update/draw loop,
  delta-time movement, Surface/Rect blitting, keyboard/mouse input, and
  Sprite/Group management with collision. Use when building or debugging a pygame
  game — when the user mentions pygame, pygame-ce, the game loop, blit, Surface,
  Rect, sprite groups, or clock.tick. Targets pygame-ce.
---

# pygame Core

Build the foundation of a pygame game in Python: the main loop, delta-time
movement, drawing with `Surface`/`Rect`, input, and `Sprite`/`Group` management.
Targets **pygame-ce 2.5.8** (the actively maintained community fork; same
`import pygame`).

## When to use

- Use when starting a pygame game, fixing the loop, frame-rate-dependent speed,
  input handling, blitting, or sprite/group collision.
- Use when code does `import pygame` and the project depends on `pygame-ce`
  (or `pygame`).

**When *not* to use:** Python language questions unrelated to pygame. 3D rendering
(pygame is 2D). For cross-engine save/load use `save-systems`; for rebindable input
architecture see `input-systems`.

## Core workflow

1. **Install pygame-ce, not legacy pygame.** `pip install pygame-ce` — it's the
   maintained fork and imports as `pygame`. Don't install both in one environment.
2. **Init and open a window.** `pygame.init()`, `screen =
   pygame.display.set_mode((w, h))`, `clock = pygame.time.Clock()`.
3. **Run one loop: events → update → draw → flip.** Pump the event queue every
   frame (`for event in pygame.event.get()`), update state, redraw, then
   `pygame.display.flip()`.
4. **Make it frame-rate independent.** Get `dt = clock.tick(60) / 1000` (seconds)
   and scale all motion by `dt`. Keep positions as floats; blit at integer rects.
5. **Handle input two ways:** event-based (`KEYDOWN`/`MOUSEBUTTONDOWN`, for discrete
   actions) and polled (`pygame.key.get_pressed()`, for held movement).
6. **Organise objects with `Sprite` + `Group`.** Subclass `pygame.sprite.Sprite`
   with `image`/`rect`; `group.update(dt)` and `group.draw(screen)` handle the
   batch. Run it and watch the window before assuming it works.

## Patterns

### 1. Minimal game loop (the skeleton)

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60) / 1000          # cap at 60 FPS; dt = seconds since last frame
    for event in pygame.event.get():    # MUST drain the queue or the OS thinks it hung
        if event.type == pygame.QUIT:
            running = False

    # update game state here, scaled by dt ...

    screen.fill((18, 18, 28))           # clear each frame
    # draw everything here ...
    pygame.display.flip()               # present the frame

pygame.quit()
```

### 2. Delta-time movement (frame-rate independent)

```python
from pygame.math import Vector2

pos = Vector2(100, 100)        # keep position as floats
speed = 220                    # PIXELS PER SECOND, not per frame

# inside the loop, after computing dt:
keys = pygame.key.get_pressed()
direction = Vector2(
    keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
    keys[pygame.K_DOWN]  - keys[pygame.K_UP],
)
if direction.length_squared() > 0:
    direction = direction.normalize()      # equal speed on diagonals
pos += direction * speed * dt              # RIGHT: dt-scaled
screen.blit(player_img, (round(pos.x), round(pos.y)))  # blit at integer pixels
```

### 3. Input: events vs polling

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:        # discrete press: jump, menu, pause
        if event.key == pygame.K_SPACE:
            jump()
        elif event.key == pygame.K_ESCAPE:
            running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        shoot_at(event.pos)                   # event.pos = (x, y)

# Polled state (read once per frame) for continuous/held input:
keys = pygame.key.get_pressed()
if keys[pygame.K_a]:
    move_left(dt)
```

### 4. A Sprite subclass + a Group

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # convert() once at load makes blits much faster; _alpha keeps transparency.
        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 240

    def update(self, dt):                      # Group.update(dt) calls this per sprite
        keys = pygame.key.get_pressed()
        self.pos.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

all_sprites = pygame.sprite.Group()
all_sprites.add(Player(400, 300))

# in the loop:
all_sprites.update(dt)        # calls each sprite's update(dt)
all_sprites.draw(screen)      # blits each sprite at its rect
```

### 5. Collision detection

```python
# Sprite vs group: e.g. player picking up coins (True = remove collided coins).
collected = pygame.sprite.spritecollide(player, coins, dokill=True)
score += len(collected)

# Group vs group: bullets vs enemies (kill both on hit).
hits = pygame.sprite.groupcollide(bullets, enemies, True, True)

# Plain rect overlap (no sprites needed):
if player.rect.colliderect(door_rect):
    open_door()
```

## Pitfalls

- **Window freezes / "not responding"** → you didn't pump the event queue. Call
  `pygame.event.get()` (or `pygame.event.pump()`) every frame.
- **Speed differs on faster machines** → you moved by a fixed amount per frame.
  Scale by `dt = clock.tick(fps) / 1000` and use pixels-per-second values.
- **Sub-pixel movement snaps/jitters** → `rect` coordinates are integers; store the
  true position as a `Vector2` of floats and assign `rect.center = round(...)` each
  frame.
- **Blits are slow / framerate drops** → call `.convert()` (opaque) or
  `.convert_alpha()` (transparent) on loaded images once; un-converted surfaces blit
  far slower.
- **Nothing appears** → you forgot `pygame.display.flip()` (or `update()`), or you
  drew before `screen.fill(...)` so it was cleared away.
- **Wrong draw order** → pygame uses painter's order; later blits cover earlier ones.
  Draw background first, sprites last.
- **`pip install pygame` got the old one** → for the maintained fork use
  `pip install pygame-ce`; having both installed causes import conflicts.
- **Diagonal movement is faster** → normalise the direction vector before scaling by
  speed.

## References

- For `Group` variants (`GroupSingle`, `LayeredUpdates` for z-order), pixel-perfect
  collision with `mask`, slicing a spritesheet, simple animation, sound/music, and
  text rendering, read `references/sprites-and-collision.md`.

## Related skills

- `love2d-core` — the same loop concepts in LÖVE/Lua.
- `bevy-ecs` — a heavier ECS engine when a project outgrows pygame.
- `input-systems` / `save-systems` — engine-agnostic input and persistence.
- `platformer` / `roguelike` — genre templates that pair with pygame.
