---
name: tower-visuals
description: Provides rules and patterns for drawing machine-based tower visuals using p5.js primitives. Use when designing or modifying tower rendering to use geometric shapes instead of sprites.
allowed-tools: Read, Edit, Write
---

# Tower Visuals - Machine Design Rules

## Design Philosophy

Towers should be **geometric machines** built from layered p5.js primitives (rectangles, circles, arcs). Each tower type should have a distinct silhouette and visual identity that communicates its function at a glance.

## Core Principles

### 1. Layered Construction
Build towers from bottom-up layers:
1. **Base/Platform** - Foundation (darker, grounded)
2. **Body** - Main structure (primary color)
3. **Turret/Barrel** - Weapon system (rotates with `this.angle`)
4. **Details** - Accents, vents, lights (smaller features)

### 2. Rounded Squares Philosophy
- Use `rect(x, y, w, h, radius)` with rounded corners for industrial look
- Prefer **rounded rectangles** over perfect circles for body/housing
- Perfect circles reserved for: barrels, energy cores, lights
- Corner radius typically: 4-8px for large shapes, 2-4px for details

### 3. Color Palette
```javascript
// Base colors (from tower type)
let baseColor = this.color; // Tower's primary color

// Derived palette
let darkBase = color(red(baseColor) * 0.6, green(baseColor) * 0.6, blue(baseColor) * 0.6);
let lightBase = color(red(baseColor) * 1.2, green(baseColor) * 1.2, blue(baseColor) * 1.2);
let metalGrey = color(80, 85, 90);
let darkMetal = color(40, 45, 50);
```

### 4. Visual Hierarchy
- **Largest shapes** (40-50px) - Main body
- **Medium shapes** (20-30px) - Turret, barrel
- **Small details** (5-15px) - Vents, lights, casings
- **Tiny accents** (2-5px) - Rivets, indicators

## Tower Type Guidelines

### Cannon/Gunner Tower
**Identity:** Single-barrel ballistic weapon
**Key Features:**
- Wide, stable base (rounded rectangle)
- Cylindrical barrel (long rectangle, rotates)
- Ammo casing/magazine visible
- Muzzle flash point (small circle at barrel end)

```javascript
draw(x, y, size) {
    let cx = x + size / 2;
    let cy = y + size / 2;

    push();
    translate(cx, cy);

    // 1. Base platform
    fill(60, 55, 50);
    noStroke();
    rect(-20, 8, 40, 16, 4);

    // 2. Body housing
    fill(this.color);
    stroke(0);
    strokeWeight(2);
    rect(-18, -10, 36, 20, 6);

    // 3. Rotating turret
    push();
    rotate(this.angle);

    // Barrel
    fill(70);
    rect(0, -4, 25, 8, 2);

    // Muzzle
    fill(40);
    ellipse(25, 0, 6, 6);

    pop();

    // 4. Details (vents, lights)
    fill(100, 200, 255);
    ellipse(-10, 0, 4, 4);
    ellipse(10, 0, 4, 4);

    pop();
}
```

### Double Cannon/Ranger
**Identity:** Dual-barrel rapid-fire system
**Key Features:**
- Twin parallel barrels
- Compact, aggressive stance
- Feed systems/ammo belts visible
- Wider base for stability

```javascript
// Twin barrels at offset Y positions
rect(5, -8, 20, 5, 2);  // Upper barrel
rect(5, 3, 20, 5, 2);   // Lower barrel

// Ammo feed boxes
rect(-5, -10, 8, 8, 2);
rect(-5, 2, 8, 8, 2);
```

### Flamethrower/Pyro
**Identity:** Fuel-based incendiary weapon
**Key Features:**
- Wide nozzle (cone/truncated triangle)
- Fuel tanks visible (cylinders)
- Pilot light indicator (glowing orange)
- Heat vents/cooling fins

```javascript
// Fuel tanks (layered circles)
fill(150, 50, 50);
ellipse(-8, 5, 12, 16);
ellipse(8, 5, 12, 16);

// Wide nozzle (trapezoid)
beginShape();
vertex(10, -6);
vertex(25, -10);
vertex(25, 10);
vertex(10, 6);
endShape(CLOSE);

// Pilot light (pulsing)
let pulse = sin(frameCount * 0.2) * 0.3 + 0.7;
fill(255, 150, 0, 200 * pulse);
ellipse(0, 0, 6, 6);
```

### Lightning/Electrifier
**Identity:** Tesla coil energy weapon
**Key Features:**
- Vertical coils/spires
- Arcing electricity (animated)
- Energy core (pulsing glow)
- Capacitor banks visible

```javascript
// Energy core (pulsing)
let pulse = sin(frameCount * 0.15) * 0.2 + 0.8;
fill(0, 200, 255, 150 * pulse);
ellipse(0, 0, 20 * pulse, 20 * pulse);

// Tesla coils (vertical)
fill(80);
rect(-10, -20, 6, 30, 3);
rect(4, -20, 6, 30, 3);

// Arc tips (spheres)
fill(150, 200, 255);
ellipse(-7, -20, 8, 8);
ellipse(7, -20, 8, 8);

// Static arcs (draw in draw() if this.laserFrames > 0)
```

### Sniper Tower
**Identity:** Long-range precision railgun
**Key Features:**
- Extended barrel (2-3x normal length)
- Scope/targeting system
- Recoil dampeners (springs, hydraulics)
- Minimal profile (compact body)

```javascript
// Slim body
rect(-12, -6, 24, 12, 4);

// Extended barrel
push();
rotate(this.angle);
fill(60);
rect(0, -3, 45, 6, 2);  // Very long barrel

// Scope mount
fill(100, 255, 100);
rect(15, -8, 12, 4, 2);

// Recoil spring
stroke(120);
noFill();
for (let i = 0; i < 5; i++) {
    ellipse(-5 + i * 2, 0, 3, 6);
}
pop();
```

### Buffer Tower
**Identity:** Support beacon/relay station
**Key Features:**
- Central crystal/antenna
- Pulsing energy field
- Symmetrical design (not rotational)
- Connection nodes visible
- Network size indicator

```javascript
// Already well-designed in current code!
// Keep the diamond crystal + pulsing glow
// Add: Connection ports (small circles at cardinal directions)
fill(150);
ellipse(0, -20, 6, 6);  // Top port
ellipse(20, 0, 6, 6);   // Right port
ellipse(0, 20, 6, 6);   // Bottom port
ellipse(-20, 0, 6, 6);  // Left port
```

### Swap Tower
**Identity:** Teleporter/phase shifter
**Key Features:**
- Circular portal ring
- Rotating phase indicators
- Swap symbol (arrows)
- Energy swirl effect when ready

```javascript
// Portal ring
stroke(180, 80, 255);
strokeWeight(3);
noFill();
ellipse(0, 0, size * 0.6);

// Phase indicators (rotating particles)
for (let i = 0; i < 4; i++) {
    let angle = frameCount * 0.05 + (i * PI / 2);
    let px = cos(angle) * 18;
    let py = sin(angle) * 18;
    fill(200, 100, 255);
    ellipse(px, py, 6, 6);
}

// Weapon barrel (still attacks)
push();
rotate(this.angle);
fill(120, 60, 180);
rect(5, -3, 15, 6, 2);
pop();
```

## Animation Guidelines

### Rotating Elements
```javascript
push();
rotate(this.angle); // Tracks target
// Draw barrel, turret, weapon
pop();
```

### Pulsing Effects
```javascript
let pulse = sin(frameCount * speed) * amplitude + baseline;
// speed: 0.05-0.2 (slower = more menacing)
// amplitude: 0.2-0.3 (variation amount)
// baseline: 0.7-0.8 (minimum brightness)

fill(r * pulse, g * pulse, b * pulse);
```

### Muzzle Flash
```javascript
// In shoot() method, set this.muzzleFlash = 8;
// In draw():
if (this.muzzleFlash > 0) {
    this.muzzleFlash--;
    let alpha = map(this.muzzleFlash, 0, 8, 0, 255);

    push();
    rotate(this.angle);
    fill(255, 255, 150, alpha);
    ellipse(barrelEndX, barrelEndY, 15, 15);
    pop();
}
```

## Integration with Merge System

**Preserve existing merge shapes!** The Reuleaux polygon background should remain.

```javascript
draw(x, y, size) {
    let cx = x + size / 2;
    let cy = y + size / 2;

    push();
    translate(cx, cy);

    // KEEP THIS - Merge rank background
    this.drawMergeShapeBackground(0, 0, size);

    // Your machine tower on top
    // ... tower drawing code

    pop();
}
```

## Performance Considerations

**Optimization Rules:**
1. **Precalculate colors** - Don't call `color()` in draw loop
2. **Minimize state changes** - Group `fill()` and `stroke()` calls
3. **Avoid complex paths** - Use primitives over `beginShape()`
4. **Throttle animations** - Use `frameCount % N` for expensive effects

```javascript
// BAD - Recalculates every frame
draw() {
    fill(color(255, 0, 0));  // Creates new color object!
}

// GOOD - Cache in constructor
constructor() {
    this.fillColor = color(255, 0, 0);
}
draw() {
    fill(this.fillColor);
}
```

## Visual Identity Matrix

| Tower Type | Primary Shape | Secondary Shape | Accent | Rotation |
|------------|--------------|----------------|--------|----------|
| Cannon     | Rounded rect | Long barrel    | Lights | Yes - barrel |
| DoubleCannon | Compact rect | Twin barrels  | Ammo feed | Yes - both barrels |
| Flamethrower | Wide base | Cone nozzle   | Pilot light | Yes - nozzle |
| Electrifier | Compact square | Vertical coils | Arcs | No - omni-directional |
| Sniper | Slim rect | Extended barrel | Scope | Yes - entire turret |
| Buffer | Diamond | Crystal | Glow | No - support beacon |
| Swap | Portal ring | Phase particles | Arrows | Partial - particles spin |

## Common Mistakes to Avoid

❌ **Too many colors** - Stick to 3-4 colors per tower
❌ **No visual hierarchy** - Everything same size
❌ **Ignoring merge shape** - Should work with Reuleaux background
❌ **Static design** - No animation or rotation
❌ **Pixel-perfect alignment** - Over-engineering coordinates
❌ **Missing weapon identity** - Can't tell what it shoots

✅ **Clear silhouette** - Recognizable at small size
✅ **Functional design** - Form follows function
✅ **Consistent style** - All towers feel like same universe
✅ **Animated details** - Pulsing, rotating, glowing
✅ **Merge rank integration** - Background shapes visible

## Testing Checklist

Before finalizing tower visuals:
- [ ] Looks good at 64×64px tile size
- [ ] Silhouette distinct from other towers
- [ ] Merge rank background visible
- [ ] Rotation smooth when targeting
- [ ] Colors match tower type identity
- [ ] No performance impact (check FPS with 50+ towers)
- [ ] Weapon type clear (barrel, nozzle, coil, etc.)
- [ ] Works with all 7 merge ranks

## Reference Files

- **Tower.js:404-967** - Current tower draw() methods
- **Tower.js:320-401** - Merge shape background system
- **GameConstants.js** - Color definitions
- **design_doc.md** - Tower identity and roles

## Example: Full Tower Redesign

See inline code examples above for each tower type. When redesigning:

1. **Read current draw() method**
2. **Identify tower function** (single-shot, rapid-fire, area, support)
3. **Sketch machine concept** (what would this weapon look like?)
4. **Build from layers** (base → body → weapon → details)
5. **Test with merge ranks** (does it work with all 7 backgrounds?)
6. **Animate** (rotation, pulsing, effects)

Remember: **Form follows function**. A flamethrower should look wide and aggressive. A sniper should look sleek and precise. A buffer should look like a support beacon.
