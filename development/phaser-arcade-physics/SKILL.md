---
name: phaser-arcade-physics
description: >
  Use Phaser 4 Arcade Physics: enable the world, give sprites bodies, set
  velocity/acceleration/gravity, and resolve collisions with colliders, overlaps,
  groups, and world bounds. Use when a Phaser game needs movement or collisions —
  when the user mentions Arcade Physics, this.physics, setVelocity, collider,
  overlap, gravity, onFloor, or a platformer/top-down controller. For game config,
  scenes, and the loader use phaser-core.
---

# Phaser 4 Arcade Physics

Add movement and collision to a Phaser game with the lightweight **Arcade
Physics** engine (AABB rectangles and circles only). Targets **Phaser 4.2** for
new projects; inspect the installed major before editing an existing project.

## When to use

- Use for top-down or platformer movement, velocity/acceleration/gravity, bouncing,
  world bounds, and collision/overlap resolution between sprites, groups, and tiles.
- Use when the scene enables `physics: { default: 'arcade' }` and code calls
  `this.physics.add.*`, `body.setVelocity`, or `this.physics.add.collider`.

**When *not* to use:** the `Game` config, scene structure, asset loading, or
cameras → use `phaser-core`. Hinges, springs, complex polygons, or stacking
rigid bodies → use Matter physics (a different engine; Arcade and Matter bodies
do not interact). For engine-agnostic feel tuning see `physics-tuning`.

## Core workflow

1. **Enable the world.** Set `physics: { default: 'arcade', arcade: { gravity:
   {...}, debug: true } }` in the game or scene config. Turn `debug` on while
   building to see body outlines and velocity vectors.
2. **Give a sprite a body.** Create it with `this.physics.add.sprite(...)` (dynamic)
   or `this.physics.add.staticImage(...)` (static), or attach to an existing object
   with `this.physics.add.existing(obj)`.
3. **Drive it through the body, not by setting `x`/`y`.** Use `setVelocity`,
   `setAcceleration`, gravity, `setBounce`, and `setCollideWorldBounds`. The engine
   integrates position from velocity each step (already frame-rate independent).
4. **Resolve interactions.** `this.physics.add.collider(a, b)` separates bodies;
   `this.physics.add.overlap(a, b, cb)` detects without separating (pickups,
   triggers). Pass a callback to react.
5. **Group many objects.** Use `this.physics.add.group()` (dynamic) or
   `staticGroup()` (platforms) so one collider call handles all members.
6. **Check ground contact** with `body.onFloor()` / `body.blocked.down` before
   jumping. Run with `debug: true` and confirm bodies, contacts, and bounds.

## Patterns

### 1. Enable Arcade Physics (game config)

```js
const config = {
  type: Phaser.AUTO,
  width: 800, height: 600,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 600 },  // top-down? use { x: 0, y: 0 }
      debug: false                // true to draw bodies + velocity while building
    }
  },
  scene: [PlayScene]
};
new Phaser.Game(config);
```

### 2. Top-down movement (velocity from input)

```js
create() {
  this.player = this.physics.add.sprite(400, 300, 'player');
  this.player.setCollideWorldBounds(true);
  this.cursors = this.input.keyboard.createCursorKeys();
}

update() {
  const speed = 220;
  const body = this.player.body;
  body.setVelocity(0);                              // reset each frame
  if (this.cursors.left.isDown)  body.setVelocityX(-speed);
  if (this.cursors.right.isDown) body.setVelocityX(speed);
  if (this.cursors.up.isDown)    body.setVelocityY(-speed);
  if (this.cursors.down.isDown)  body.setVelocityY(speed);
  body.velocity.normalize().scale(speed);           // keep diagonals same speed
}
```

### 3. Platformer jump (gravity + ground check)

```js
create() {
  this.player = this.physics.add.sprite(100, 450, 'player');
  this.player.setCollideWorldBounds(true);

  // Static platforms: one body each, never moved by collisions.
  this.platforms = this.physics.add.staticGroup();
  this.platforms.create(400, 568, 'ground');
  this.physics.add.collider(this.player, this.platforms);

  this.cursors = this.input.keyboard.createCursorKeys();
}

update() {
  const onGround = this.player.body.blocked.down; // or this.player.body.onFloor()
  if (this.cursors.left.isDown)  this.player.setVelocityX(-160);
  else if (this.cursors.right.isDown) this.player.setVelocityX(160);
  else this.player.setVelocityX(0);

  if (this.cursors.up.isDown && onGround) this.player.setVelocityY(-450);
}
```

### 4. Colliders vs overlaps (separate vs detect)

```js
// Push apart and react: player vs enemies.
this.physics.add.collider(this.player, this.enemies, (player, enemy) => {
  this.handleHit(player, enemy);
});

// Detect without pushing: collect coins. The 4th arg is an optional
// process callback returning a boolean to filter pairs before the main callback.
this.physics.add.overlap(this.player, this.coins, (player, coin) => {
  coin.disableBody(true, true);              // deactivate + hide
  this.registry.inc('score', 10);
});
```

### 5. A group of moving objects

```js
this.bullets = this.physics.add.group({
  defaultKey: 'bullet',
  maxSize: 30                  // pool size; reuse instead of allocating
});

fire(x, y) {
  const bullet = this.bullets.get(x, y);     // reuses a dead bullet if available
  if (!bullet) return;
  bullet.enableBody(true, x, y, true, true);
  bullet.setVelocityY(-500);
}
```

## Pitfalls

- **Sprite ignores physics** → it was added with `this.add.sprite` instead of
  `this.physics.add.sprite` (or `this.physics.add.existing(obj)`), so it has no body.
- **Setting `sprite.x` directly fights the engine** → move dynamic bodies with
  `setVelocity`/`setAcceleration`. Direct position writes can tunnel through colliders.
- **Diagonal movement is faster** → independent X and Y velocities add up; normalise
  the velocity vector and rescale to the intended speed.
- **Platforms get pushed by the player** → use a `staticGroup`, or set
  `body.setImmovable(true)` on a dynamic platform.
- **`onFloor()` is always false** → the body needs something to collide with; add the
  `collider` against the ground/platforms before checking, and ensure gravity is on.
- **Moved a static body but collisions are stale** → static bodies don't auto-sync;
  call `body.updateFromGameObject()` (or `refreshBody()` on the game object).
- **Collider added every frame** → register `collider`/`overlap` once in `create`,
  not in `update`.

## References

- For body anatomy and tuning (drag, bounce, max velocity, custom `setSize`/
  `setCircle`/`setOffset` hitboxes, collision categories/masks, and `worldbounds`
  events), read `references/bodies-and-collision.md`.

## Related skills

- `phaser-core` — game config, scenes, loader, cameras (the prerequisite setup).
- `physics-tuning` — engine-agnostic feel (fixed timestep, tunneling, jitter).
- `platformer` / `tower-defense` — genres that compose this skill.
- `level-design` — laying out tile/platform geometry these bodies collide with.
