---
name: draw-sprite
description: Draw or edit sprites in Canvas 2D in client/Tools/sprites.js — stalls, counters, food dishes, NPC portraits, wearables, decorations, and UI frames. Use this skill whenever the user wants to draw or modify a sprite, says "vẽ hình", "vẽ quầy", "vẽ món", "thêm trang phục", "vẽ nón lá", "vẽ bàn ghế", "vẽ sprite", "vẽ portrait", or when Unity logs "Missing sprite...".
---

# Draw a Canvas 2D sprite

All game art outside the photorealistic street backdrop cuts is drawn programmatically in Canvas 2D in `client/Tools/sprites.js` and rendered to PNGs under `client/Assets/Resources/Sprites/`.

Scale: **200 px = 1 Unity unit** (`PPU = 200`). Outline color is dark chocolate brown: `const OUTLINE = '#3b2414'`.

## Canvas Drawing Helpers

`client/Tools/sprites.js` provides standard vector primitives:

| Helper | Signature | Description |
|---|---|---|
| `roundRect` | `(g, x, y, w, h, r)` | Rounded rectangle with radius `r` |
| `fill` | `(g, color, line = 4, outline = OUTLINE)` | Fills current path and strokes an outline |
| `ellipse` | `(g, x, y, rx, ry)` | Draws an ellipse centered at `(x, y)` |
| `poly` | `(g, [[x,y], ...])` | Polygon path connecting points |
| `gradient` | `(g, x0, y0, x1, y1, [[offset, color], ...])` | Linear gradient generator |
| `shade` | `(hex, k)` | Tint helper (`k > 0` lighter, `k < 0` darker) |
| `drawText` | `(g, text, x, y, size, color, outline, align)` | Centered bold text with outline |

## Standard Categories & Dimensions

### 1. Product Stall Counter (`counter_<productId>`)
* **Dimensions**: `380 x 190` px.
* **Pivot**: `[0.5, 0]` (bottom center).
* **Base table**: Call `table(g, woodColorHex)` which draws the standard wooden vendor cart.
* **Food topping**: Draw dishes, pots, or trays between `y = 20` and `y = 70`.
* **Sign**: Call `drawText(g, 'TÊN MÓN', 190, 116, 28, '#fff', OUTLINE)`.

```js
COUNTERS.pho = (g) => {
  table(g, '#a0652e');
  // Steaming bowl
  ellipse(g, 190, 50, 40, 22); fill(g, '#ffffff', 3);
  drawText(g, 'PHỞ BÒ', 190, 116, 28, '#fff', OUTLINE);
};
```

### 2. NPC Portrait (`npc_<id>`)
* **Dimensions**: `200 x 200` px.
* **Pivot**: `[0.5, 0]`.
* **Helper**: Use `portrait(name, skinColor, hairPathSvg, shirtColor, extraDrawFn)`.

```js
portrait('npc_guard', '#d9a273', 'M42 86C40 44 66 22 102 22C138 22 164 44 160 86Q100 64 42 86Z', '#2b4c7e', (g) => {
  // Draw guard cap or badge
  roundRect(g, 70, 20, 60, 20, 5); fill(g, '#1a365d', 2);
});
```

### 3. UI Frames & Buttons (9-Slice)
* Provide `border: [left, bottom, right, top]` in px.
* Unity will slice the sprite so borders stay crisp while the center stretches.

```js
add('ui_badge', 80, 80, (g) => {
  roundRect(g, 4, 4, 72, 72, 16); fill(g, '#ff922b', 4);
}, [0.5, 0.5], [20, 20, 20, 20]);
```

### 4. Street Decorations & Props
* Pivot is normally `[0.5, 0]` (feet on the ground / curb).
* Draw with clean bold strokes (`line = 3` or `4`).

## Export Pipeline

Once `sprites.js` is updated:
1. Run server: `node client/Tools/export-server.mjs`.
2. Open `http://localhost:5181/` in Chrome/Edge.
3. In browser console, run: `exportSprites()`.
4. In Unity, select: **Via He → Reimport Sprites**.

## Sync Skills

```bash
node tools/sync-skills.mjs
```

