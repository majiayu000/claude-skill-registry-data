---
name: Writing Phaser 3 Games
description: Provides battle-tested patterns, best practices, and code examples for building Phaser 3 games. Use when writing game code, implementing game mechanics, setting up scenes, handling physics, animations, input, or any Phaser-related development. Covers architecture, performance, algorithms, and common pitfalls.
---

# Phaser 3 Game Development Skill

## Quick Start

### Most Common Patterns

**Multi-Scene Flow**
```javascript
const config = {
    scene: [ Boot, Preloader, MainMenu, Game, GameOver ]
};
// Boot → Preloader → MainMenu → Game → GameOver
```

**Object Pooling**
```javascript
create() {
    this.projectiles = this.physics.add.group({
        classType: Projectile,
        frameQuantity: 20,
        active: false,
        visible: false
    });
}

fire() {
    const projectile = this.projectiles.getFirstDead(false);
    if (projectile) projectile.fire(x, y);
}
```

**Global Animations**
```javascript
// In Preloader.js create()
this.anims.create({
    key: 'walk',
    frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }),
    frameRate: 10,
    repeat: -1
});
```

**JustDown Input**
```javascript
if (Phaser.Input.Keyboard.JustDown(this.spacebar)) {
    this.jump();
}
```

## Navigation Guide

### How to Use This Skill

This skill provides access to 18 comprehensive pattern files covering all aspects of Phaser 3 development. Each file contains detailed patterns, code examples, and best practices.

**To find specific patterns:**

```bash
# Read a specific topic
Read knowledgebase/06-input-handling.md

# Search for a pattern across all files
grep -r "object pooling" knowledgebase/

# Find patterns by keyword
grep -i "animation" knowledgebase/*.md
grep -i "collision" knowledgebase/*.md
```

**Quick lookup by number:**
- 01 = Scene Architecture
- 02 = Asset Management
- 03 = Physics & Collision
- 04 = Movement Patterns
- 05 = Animation System
- 06 = Input Handling
- 07 = State Management
- 08 = Object Pooling & Memory
- 09 = Grid Systems
- 10 = Custom Game Objects
- 11 = UI/HUD Patterns
- 12 = Tween & Visual Effects
- 13 = Audio Integration
- 14 = Game Loop Patterns
- 15 = Algorithm Implementations
- 16 = Performance Optimization
- 17 = Code Organization
- 18 = Development Philosophy

## Table of Contents

### 1. Scene Architecture
[knowledgebase/01-scene-architecture.md](knowledgebase/01-scene-architecture.md)

Multi-scene flow, parallel scenes for UI overlays, scene transitions with effects, data passing between scenes.

**Key Patterns:**
- Boot → Preloader → MainMenu → Game → GameOver flow
- Parallel UI scene with `scene.launch()`
- Camera fade transitions
- Scene data passing via `init(data)`

### 2. Asset Management
[knowledgebase/02-asset-management.md](knowledgebase/02-asset-management.md)

Two-stage loading, texture atlases, multi-format audio, font synchronization.

**Key Patterns:**
- Bootstrap assets in Boot, full assets in Preloader
- Texture atlas for multiple sprites
- Multi-format audio for browser compatibility
- WebFont loading synchronization

### 3. Physics & Collision
[knowledgebase/03-physics-collision.md](knowledgebase/03-physics-collision.md)

Physics configuration, collision vs overlap, dynamic responses, state-gated collision.

**Key Patterns:**
- Collider for physical blocking, overlap for triggers
- Position-based dynamic response (paddle hits)
- State-gated collision checks
- Per-track/layer collision isolation

### 4. Movement Patterns
[knowledgebase/04-movement-patterns.md](knowledgebase/04-movement-patterns.md)

Velocity-based, time-based discrete, timer-based, pursuit, direction validation, screen wrapping.

**Key Patterns:**
- Velocity-based for continuous action games
- Time-based discrete for grid games
- Timer-based for turn-based games
- Direction validation (prevent 180° turns)

### 5. Animation System
[knowledgebase/05-animation-system.md](knowledgebase/05-animation-system.md)

Global animation creation, reverse animations, animation-driven logic, state-based control.

**Key Patterns:**
- Create animations once in Preloader, use everywhere
- Animation events for gameplay synchronization
- State-based animation control with caching
- External animation JSON data

### 6. Input Handling
[knowledgebase/06-input-handling.md](knowledgebase/06-input-handling.md)

Keyboard, pointer, touch, JustDown pattern, dual input support, input gating, cleanup.

**Key Patterns:**
- JustDown for single-press detection
- Dual keyboard + pointer support
- Input gating during animations
- Event-driven pointer movement
- One-time input with `once()`

### 7. State Management
[knowledgebase/07-state-management.md](knowledgebase/07-state-management.md)

Scene-level state, registry for persistence, localStorage, GameObject data component, state machines.

**Key Patterns:**
- Constructor for config, init() for resettable state
- Registry for cross-scene data
- GameObject data component for custom properties
- Boolean flags vs state machines

### 8. Object Pooling & Memory
[knowledgebase/08-object-pooling-memory.md](knowledgebase/08-object-pooling-memory.md)

Group-based pooling, enable/disable pattern, object reuse, dynamic texture cleanup.

**Key Patterns:**
- Pre-create with `frameQuantity`, recycle with `getFirstDead()`
- Enable/disable instead of create/destroy
- Reset pattern for reusable objects
- Dynamic texture cleanup prevention

### 9. Grid Systems
[knowledgebase/09-grid-systems.md](knowledgebase/09-grid-systems.md)

Dual coordinates, 2D arrays, adjacency helpers, grid alignment, visualization.

**Key Patterns:**
- Separate grid coordinates from pixel coordinates
- 2D array with bounds checking
- Adjacency helpers (8-direction, 4-direction)
- Grid-aligned group creation

### 10. Custom Game Objects
[knowledgebase/10-custom-game-objects.md](knowledgebase/10-custom-game-objects.md)

Extending Sprite/Image, composition pattern, extending groups, self-registration.

**Key Patterns:**
- Extend Sprite when physics + animations needed
- Extend Image for static sprites with physics
- Composition for non-visual managers
- Must call `super.preUpdate()` for animations

### 11. UI/HUD Patterns
[knowledgebase/11-ui-hud-patterns.md](knowledgebase/11-ui-hud-patterns.md)

Text styling, positioning, dynamic updates, bitmap fonts, icon counters, layering.

**Key Patterns:**
- Text origin for positioning (top-left, center, etc.)
- Animated counters with tweens
- Icon-based counters (hearts, lives)
- Depth/z-ordering for layered UI

### 12. Tween & Visual Effects
[knowledgebase/12-tween-visual-effects.md](knowledgebase/12-tween-visual-effects.md)

Basic tweens, staggered animations, choreographed sequences, camera effects, particles.

**Key Patterns:**
- Tween callbacks for sequencing
- Staggered grid animations
- Choreographed sequences with accumulating delays
- Camera shake, flash, fade
- Particle emitters

### 13. Audio Integration
[knowledgebase/13-audio-integration.md](knowledgebase/13-audio-integration.md)

Sound management, audio lock handling, centralized audio, delayed/sequenced audio.

**Key Patterns:**
- Multi-format audio loading
- Audio lock detection and handling
- Centralized audio management in UI scene
- Persistent music across scenes

### 14. Game Loop Patterns
[knowledgebase/14-game-loop-patterns.md](knowledgebase/14-game-loop-patterns.md)

Standard update, minimal event-driven, preUpdate for custom objects, delegation, timers.

**Key Patterns:**
- Early exit guards in update()
- Event-driven for turn-based games
- Timer-based recurring/one-shot events
- Update delegation to managers

### 15. Algorithm Implementations
[knowledgebase/15-algorithm-implementations.md](knowledgebase/15-algorithm-implementations.md)

Flood fill, smart random placement, solvable puzzle generation, proximity calculation, following chains, AI.

**Key Patterns:**
- Recursive flood fill with 4-direction spread
- Valid position collection for guaranteed placement
- Walker algorithm for solvable puzzles
- Following chain with ShiftPosition

### 16. Performance Optimization
[knowledgebase/16-performance-optimization.md](knowledgebase/16-performance-optimization.md)

Object pooling, texture caching, minimize update logic, event-driven, static groups.

**Key Patterns:**
- Object pooling eliminates GC pauses
- Static groups for immovable objects
- Event-driven over polling in update()
- Texture atlas for rendering performance

### 17. Code Organization
[knowledgebase/17-code-organization.md](knowledgebase/17-code-organization.md)

File structure, ES6 modules, constants management, separation of concerns.

**Key Patterns:**
- Scenes, gameobjects, managers, utils, constants folders
- ES6 module imports
- Constant files for sprite/animation/audio keys
- Clear initialization order in create()

### 18. Development Philosophy
[knowledgebase/18-development-philosophy.md](knowledgebase/18-development-philosophy.md)

Architecture principles, when to use physics, scene decisions, update vs events, progressive difficulty.

**Key Patterns:**
- When to use physics vs manual logic
- Single vs multi vs parallel scenes
- Update() vs event-driven approaches
- Progressive difficulty patterns

## Core Patterns Reference

### Scene Setup

```javascript
export default class Game extends Phaser.Scene {
    constructor() {
        super('Game');
        // Configuration constants
        this.GRID_SIZE = 32;
    }

    init() {
        // Reset resettable state
        this.score = 0;
        this.gameOver = false;
    }

    create() {
        // Initialize objects
        this.player = new Player(this);
        this.enemies = this.physics.add.group();

        // Setup collisions
        this.physics.add.collider(this.player, this.enemies, this.onHit, null, this);
    }

    update(time, delta) {
        if (this.gameOver) return;
        // Game logic
    }
}
```

### Custom Game Object

```javascript
export default class Player extends Phaser.Physics.Arcade.Sprite {
    constructor(scene, x, y) {
        super(scene, x, y, 'player');

        // Self-register
        scene.add.existing(this);
        scene.physics.add.existing(this);

        // Configuration
        this.setCollideWorldBounds(true);
        this.isAlive = true;
    }

    preUpdate(time, delta) {
        super.preUpdate(time, delta);  // ESSENTIAL for animations

        if (!this.isAlive) return;
        this.handleMovement();
    }
}
```

### Grid System

```javascript
// Dual coordinate system
this.gridX = 5;
this.gridY = 3;
this.sprite.x = this.gridX * TILE_SIZE;
this.sprite.y = this.gridY * TILE_SIZE;

// 2D array with bounds checking
getCellXY(x, y) {
    if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
        return null;
    }
    return this.grid[y][x];
}
```

### Collision Handling

```javascript
// Physical collision
this.physics.add.collider(player, platforms);

// Trigger-based overlap
this.physics.add.overlap(player, coins, this.collectCoin, null, this);

// Collision with state gates
onHit(player, enemy) {
    if (!player.isAlive) return;
    if (player.invincible) return;
    if (enemy.alpha < 1) return;

    this.handleDamage(player, enemy);
}
```

### Input Patterns

```javascript
create() {
    // Cursor keys
    this.cursors = this.input.keyboard.createCursorKeys();

    // Specific key
    this.spacebar = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

    // Pointer/touch
    this.input.on('pointerdown', this.handleClick, this);
}

update() {
    // Continuous input
    if (this.cursors.left.isDown) {
        this.player.setVelocityX(-160);
    }

    // Single-press input
    if (Phaser.Input.Keyboard.JustDown(this.spacebar)) {
        this.jump();
    }
}
```

### Animation Setup

```javascript
// In Preloader create() - global animations
this.anims.create({
    key: 'player-walk',
    frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }),
    frameRate: 10,
    repeat: -1
});

// In Game create() - use animations
this.player.play('player-walk');

// Animation events
this.player.on('animationcomplete-attack', this.spawnProjectile, this);
```

### State Management

```javascript
// Scene-level state
init() {
    this.score = 0;
    this.lives = 3;
    this.gameOver = false;
}

// Registry for cross-scene data
this.registry.set('highscore', this.score);
const highscore = this.registry.get('highscore');

// GameObject data
sprite.setData({ gridX: 5, gridY: 3, type: 'enemy' });
const gridX = sprite.data.values.gridX;
```

## Common Pitfalls

**Critical mistakes to avoid:**

1. **Forgetting `super.preUpdate(time, delta)` in custom sprites**
   - Animations won't work without this
   - Always call first thing in preUpdate()

2. **Not calling `refreshBody()` after scaling static groups**
   ```javascript
   this.platforms.create(x, y, 'platform')
       .setScale(2)
       .refreshBody();  // REQUIRED
   ```

3. **Creating objects in update() instead of pooling**
   - Causes GC pauses and poor performance
   - Pre-create pools, recycle with enable/disable

4. **Missing bounds checks on grid access**
   ```javascript
   if (x < 0 || x >= width || y < 0 || y >= height) return null;
   ```

5. **Not cleaning up listeners/timers**
   ```javascript
   shutdown() {
       this.input.off('pointerdown', this.handleClick);
       if (this.timer) this.timer.remove();
   }
   ```

6. **Using wrong collision method**
   - Use `collider` for physical blocking
   - Use `overlap` for triggers/pickups

7. **Polling in update() when events would work**
   - Use physics overlap instead of distance checks
   - Use pointer events instead of checking every frame

8. **Hard-coding values instead of constants**
   ```javascript
   // Bad: magic numbers
   sprite.x = 400;

   // Good: named constants
   const GRID_SIZE = 32;
   sprite.x = gridX * GRID_SIZE;
   ```

9. **Not resetting state in init()**
   - Scene restart won't work properly
   - Put all resettable state in init(), not constructor

10. **Ignoring context binding in callbacks**
    ```javascript
    // Use arrow functions or bind
    this.time.delayedCall(1000, () => this.start(), [], this);
    ```

## Performance Tips

- **Object pools** for frequently created/destroyed objects
- **Texture atlases** combine sprites into single image
- **Static groups** for immovable platforms/walls
- **Event-driven** over polling in update()
- **Minimal update logic** - only what's necessary each frame
- **Cache lookups** - don't search arrays every frame
- **Set depth once** - don't sort every frame

## When to Read Detailed Files

**Starting a new game?** → Read [01-scene-architecture.md](knowledgebase/01-scene-architecture.md)

**Performance issues?** → Read [16-performance-optimization.md](knowledgebase/16-performance-optimization.md)

**Grid-based game?** → Read [09-grid-systems.md](knowledgebase/09-grid-systems.md)

**Complex animations?** → Read [05-animation-system.md](knowledgebase/05-animation-system.md) and [12-tween-visual-effects.md](knowledgebase/12-tween-visual-effects.md)

**Input problems?** → Read [06-input-handling.md](knowledgebase/06-input-handling.md)

**Memory leaks?** → Read [08-object-pooling-memory.md](knowledgebase/08-object-pooling-memory.md)

**Implementing algorithms?** → Read [15-algorithm-implementations.md](knowledgebase/15-algorithm-implementations.md)

**Architecture decisions?** → Read [18-development-philosophy.md](knowledgebase/18-development-philosophy.md)

## Quick Reference Cheat Sheet

### Scene Flow
```javascript
Boot → Preloader → MainMenu → Game → GameOver
this.scene.start('NextScene', { score: this.score });
this.scene.launch('GameUI');  // Parallel scene
```

### Physics
```javascript
this.physics.add.collider(a, b);        // Physical blocking
this.physics.add.overlap(a, b, callback); // Trigger only
sprite.setCollideWorldBounds(true);
sprite.setImmovable(true);
```

### Groups & Pooling
```javascript
this.items = this.physics.add.group({ frameQuantity: 20 });
const item = this.items.getFirstDead(false);
item.enableBody(true, x, y, true, true);
item.disableBody(true, true);
```

### Input
```javascript
this.cursors = this.input.keyboard.createCursorKeys();
Phaser.Input.Keyboard.JustDown(key)
this.input.on('pointerdown', callback, this);
```

### Tweens
```javascript
this.tweens.add({
    targets: sprite,
    x: 400,
    duration: 1000,
    ease: 'Power2',
    onComplete: () => {}
});
```

### Camera
```javascript
this.cameras.main.shake(duration, intensity);
this.cameras.main.fadeOut(duration);
this.cameras.main.flash(duration, r, g, b);
```

This skill provides comprehensive Phaser 3 patterns. Read the detailed knowledgebase files for in-depth examples and advanced techniques.
