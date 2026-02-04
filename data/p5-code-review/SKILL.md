---
name: p5-code-review
description: Reviews p5.js tower defense game code for architecture patterns, manager responsibilities, performance issues, and code quality. Use when reviewing enemies, towers, managers, renderers, or asking for code review.
allowed-tools: Read, Grep, LSP
---

# p5.js Game Code Review

## Reference Documentation

- **Architecture Patterns:** @~.claude/docs/architectural_patterns.md
- **Design Document:** @~design_doc.md

## Review Checklist

### 1. Architecture Compliance

**Manager Pattern:**
- ✓ Each manager has ONE clear responsibility
- ✓ Managers don't render (delegate to Renderers)
- ✓ Managers don't hold duplicate state
- ✗ Manager performing multiple unrelated tasks
- ✗ Rendering logic inside manager

**Singleton Pattern:**
- ✓ Game.js uses singleton (`if (Game.instance) return Game.instance`)
- ✓ Global managers accessible via `game.managerName`
- ✗ Multiple Game instances created

**State Machine Pattern:**
- ✓ Clear states (MENU, PLAY, DIALOGUE, GAMEOVER, PAUSED)
- ✓ State transitions explicit (`setState(GameState.PLAY)`)
- ✓ Enemy states clear (SPAWNING, WALK, DYING)
- ✗ Implicit state changes
- ✗ Missing state transition validation

### 2. Performance

**Object Pooling:**
```javascript
// ✓ Good - Reuses objects
particlePool.push(particle);
let particle = particlePool.pop();

// ✗ Bad - Creates new objects every frame
particles.push(new Particle());
```

**Off-Screen Culling:**
```javascript
// ✓ Good - Only draw visible entities
if (e.x >= visibleLeft && e.x <= visibleRight) {
    e.draw();
}

// ✗ Bad - Draw everything
for (let e of enemies) {
    e.draw();
}
```

**Event-Driven Updates:**
```javascript
// ✓ Good - Update only when needed
onTowerPlaced() {
    recalculateBufferNetworks();
}

// ✗ Bad - Update every frame
if (frameCount % 30 === 0) {
    calculateNetwork();
}
```

**Array Cleanup:**
```javascript
// ✓ Good - Remove inactive entities
this.enemies = this.enemies.filter(e => e.active);

// ✗ Bad - Array grows forever
this.enemies.push(newEnemy); // Never removes dead ones
```

### 3. p5.js Best Practices

**Global Conflicts:**
```javascript
// ✗ Bad - Shadows p5.js globals
let text = "Hello";
let color = 255;
let image = loadImage("path");

// ✓ Good - Use descriptive names
let textContent = "Hello";
let fillColor = 255;
let enemyImage = loadImage("path");
```

**Scope Management:**
```javascript
// ✓ Good - Use push/pop for isolated transforms
push();
translate(x, y);
rotate(angle);
// ... draw stuff
pop();

// ✗ Bad - Transforms leak to other draws
translate(x, y);
rect(0, 0, 50, 50);
// Next rect is also translated!
```

**Performance:**
```javascript
// ✓ Good - Calculate once per frame
let offset = grid.getGridOffset();
for (enemy of enemies) {
    enemy.draw(offset);
}

// ✗ Bad - Recalculate for every entity
for (enemy of enemies) {
    let offset = grid.getGridOffset(); // Wasteful!
    enemy.draw(offset);
}
```

### 4. Code Organization

**Separation of Concerns:**
```javascript
// ✓ Good - Logic in update, rendering in draw
update() {
    this.health -= damage;
    if (this.health <= 0) this.state = 'DYING';
}
draw() {
    fill(this.color);
    ellipse(this.x, this.y, 32);
}

// ✗ Bad - Mixed logic and rendering
draw() {
    this.health -= damage; // Logic in draw!
    fill(this.color);
    ellipse(this.x, this.y, 32);
}
```

**Clear Responsibilities:**
```javascript
// ✓ Good - Tower focuses on targeting
class Tower {
    findTarget() { /* ... */ }
    shoot() { /* ... */ }
}

// ✗ Bad - Tower handles particles, UI, economy
class Tower {
    findTarget() { /* ... */ }
    createParticles() { /* Should be ParticleManager */ }
    drawUI() { /* Should be Renderer */ }
    addGold() { /* Should be EconomyManager */ }
}
```

### 5. Error Handling

**Null Safety:**
```javascript
// ✓ Good - Check before accessing
if (this.target && this.target.active) {
    this.target.takeDamage(this.damage);
}

// ✗ Bad - Crashes if target is null
this.target.takeDamage(this.damage);
```

**Asset Loading:**
```javascript
// ✓ Good - Fallback rendering
let img = Assets.getImage(key);
if (img) {
    image(img, x, y);
} else {
    fill(255, 0, 255); // Magenta = missing
    rect(x, y, w, h);
}

// ✗ Bad - Crashes if asset missing
image(Assets.getImage(key), x, y);
```

### 6. Game-Specific Patterns

**Enemy Classes:**
- ✓ Extend base Enemy class
- ✓ Override stats in constructor
- ✓ Use 8-directional sprite animations
- ✓ State machine (SPAWNING → WALK → DYING)
- ✗ Duplicate movement logic
- ✗ Hardcoded stats

**Tower Classes:**
- ✓ Extend base Tower class
- ✓ Override `shoot()` for custom behavior
- ✓ Respect range, damage, fireRate
- ✓ Create projectiles via ObjectManager
- ✗ Direct enemy manipulation (use projectiles)
- ✗ Drawing logic in Tower (use SpriteRenderer)

**Manager Responsibilities:**

| Manager | Responsibility | ✗ Should NOT Do |
|---------|---------------|-----------------|
| EconomyManager | Gold, lives, spending | Spawning enemies |
| WaveManager | Wave spawning, enemy factory | Tower placement |
| TowerManager | Tower placement, validation | Rendering |
| ObjectManager | Entity arrays, pooling | Pathfinding |
| InputManager | Mouse/keyboard | Game logic |

### 7. Constants vs Magic Numbers

```javascript
// ✗ Bad - Magic numbers
if (particles.length > 500) {
    particles.shift();
}
tower.range = 3;

// ✓ Good - Named constants
if (particles.length > PERFORMANCE_CONSTANTS.MAX_PARTICLES) {
    particles.shift();
}
tower.range = TOWER_STATS.GUNNER.range;
```

All tunable values should be in `GameConstants.js`.

### 8. Script Loading Order

**Critical:** Dependencies must load before dependents.

```html
<!-- ✓ Correct order -->
<script src="src/constants/GameConstants.js"></script>
<script src="src/Grid.js"></script>
<script src="src/Enemy.js"></script>
<script src="src/managers/WaveManager.js"></script> <!-- Uses Enemy -->

<!-- ✗ Wrong order -->
<script src="src/managers/WaveManager.js"></script> <!-- Uses Enemy -->
<script src="src/Enemy.js"></script> <!-- Not loaded yet! -->
```

See `index.html:14-62` for correct loading order.

---

## Review Process

When reviewing code:

### 1. Identify Component Type
- Manager? Check single responsibility
- Enemy/Tower? Check extends base class
- Renderer? Check no state mutation
- Utility? Check pure functions

### 2. Check Architecture Patterns
- Reference `.claude/docs/architectural_patterns.md`
- Verify correct pattern usage

### 3. Performance Scan
- Look for loops creating objects
- Check for unnecessary recalculations
- Verify cleanup of inactive entities

### 4. Security/Safety
- Null checks before accessing properties
- Bounds checking for arrays
- Fallbacks for asset loading

### 5. Code Style
- Descriptive variable names
- Comments for non-obvious logic
- Consistent naming conventions

---

## Output Format

Provide review as:

### ✓ Strengths
- List what's done well
- Reference specific patterns used correctly

### ✗ Issues
For each issue:
1. **File:Line** - Exact location
2. **Category** - Architecture/Performance/Style/Safety
3. **Problem** - What's wrong
4. **Fix** - Specific code change
5. **Impact** - Why it matters

### 💡 Suggestions
- Optional improvements
- Performance optimizations
- Architecture refinements

---

## Example Review

```
## Review: src/managers/WaveManager.js

### ✓ Strengths
- Clean enemy factory pattern (lines 170-192)
- Proper state machine for wave progression
- Event-driven wave start (not polling)

### ✗ Issues

**Issue 1: Performance**
- **File:Line** - WaveManager.js:85
- **Problem** - Spawning all enemies simultaneously
- **Fix:**
  ```javascript
  // Use staggered spawning
  spawnQueue.push(...enemies);
  spawnInterval = 30; // Spawn every 0.5s
  ```
- **Impact** - Prevents frame freeze on wave 15+ with 50+ enemies

**Issue 2: Architecture**
- **File:Line** - WaveManager.js:120
- **Problem** - Directly modifying EconomyManager.gold
- **Fix:**
  ```javascript
  // Use manager method
  game.economyManager.addGold(amount);
  ```
- **Impact** - Maintains single source of truth

### 💡 Suggestions
- Consider dynamic difficulty adjustment based on player performance
- Add wave preview UI before spawning
```

---

## Key Files

- **.claude/docs/architectural_patterns.md** - All patterns explained
- **design_doc.md** - Game design reference
- **GameConstants.js** - All tunable values
- **index.html:14-62** - Script loading order
- **PERFORMANCE_OPTIMIZATIONS.md** - Performance patterns

Always reference architectural_patterns.md when reviewing architecture!
