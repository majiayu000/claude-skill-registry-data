---
name: pixellab
description: "Stitch into WebP"
---

# PixelLab MCP Skills

## Reference Files

Read these BEFORE working on the relevant feature:

| When working on...                          | Read first                                                      |
| ------------------------------------------- | --------------------------------------------------------------- |
| Sidescroller platform tiles (2D platformer) | [sidescroller-tilesets.md](references/sidescroller-tilesets.md) |
| Top-down Wang tilesets (strategy/RPG maps)  | See Wang section below                                          |

---

## Sidescroller Tileset (2D Platformers)

### When to use

- Side-view platform tiles for platformer/runner games
- Ground, floating platforms, crumbling platforms
- **Read [sidescroller-tilesets.md](references/sidescroller-tilesets.md) for full reference**

### Quick summary

- `create_sidescroller_tileset` → 16 Wang tiles, 32×32, transparent bg
- `lower_description` = material, `transition_description` = surface decoration
- `transition_size`: 0.25 (light) or 0.5 (heavy surface)
- Chain with `base_tile_id` + high `tileset_adherence` (300–400) for matching sets
- Always `outline: "lineless"`

---

## Wang Tileset (Top-Down Maps) — PREFERRED for terrain

### When to use

- Path/road vs terrain transitions (dirt↔stone, grass↔water, etc.)
- Any two-terrain autotiling system
- Replaces ALL manual corner/T-junction/straight tile work

### Workflow

1. **Generate**: `create_topdown_tileset`
   - `lower_description` = ground terrain (e.g. "dark brown dirt path")
   - `upper_description` = elevated terrain (e.g. "dark grey stone floor")
   - `transition_description` = edge blend (e.g. "crumbling edge")
   - `tile_size: {width: 32, height: 32}`
   - `outline: "lineless"` (user preference!)
   - `transition_size: 0.25` (small transition) or `0.5` (larger)
   - `view: "high top-down"` for flat tiles
   - Takes ~100 seconds

2. **Download**: PNG (4×4 spritesheet, 128×128) + metadata JSON

   ```bash
   curl --fail -o wang-tileset.png "https://api.pixellab.ai/mcp/tilesets/{id}/image"
   curl --fail -o wang-tileset.json "https://api.pixellab.ai/mcp/tilesets/{id}/metadata"
   ```

3. **Build frame lookup** from JSON:
   - Each tile has `corners: {NW, NE, SW, SE}` = "upper" | "lower"
   - Wang index = NW×8 + NE×4 + SW×2 + SE×1 (upper=1, lower=0)
   - Frame = (bounding_box.y/32)\*4 + (bounding_box.x/32)
   - Build array: `WANG_FRAME[wangIdx] = frame`

4. **Render in Phaser**:

   ```typescript
   // boot.ts
   this.load.spritesheet("wang-tileset", url, {
     frameWidth: 32,
     frameHeight: 32,
   });

   // game.ts — vertex terrain algorithm
   // Vertex (vr,vc) sits between cells (vr-1,vc-1), (vr-1,vc), (vr,vc-1), (vr,vc)
   // Vertex = 0 (lower) if ANY surrounding cell is target terrain, else 1 (upper)
   const vertex = (vr, vc) => {
     return isPath(vr - 1, vc - 1) ||
       isPath(vr - 1, vc) ||
       isPath(vr, vc - 1) ||
       isPath(vr, vc)
       ? 0
       : 1;
   };

   // For each grid cell:
   const nw = vertex(r, c);
   const ne = vertex(r, c + 1);
   const sw = vertex(r + 1, c);
   const se = vertex(r + 1, c + 1);
   const wangIdx = nw * 8 + ne * 4 + sw * 2 + se;
   this.add.image(x, y, "wang-tileset", WANG_FRAME[wangIdx]);
   ```

### Chaining tilesets

- Response includes `base_tile_ids.upper` and `.lower`
- Use upper ID as `lower_base_tile_id` in next tileset for seamless multi-terrain:
  - Tileset 1: dirt → stone (get stone base ID)
  - Tileset 2: stone → grass (use stone ID as lower_base_tile_id)
- **Note**: Chaining via `lower_base_tile_id` param may error — generate independently with matching descriptions instead

### Multi-tileset layering (terrain variety)

- All PixelLab Wang tilesets use **identical tile layout** → same `WANG_FRAME` lookup for all
- **Layer 1 (base)**: render full grid (e.g., void → snow for arena border)
- **Layer 2+ (overlay)**: generate random blob shapes, render with second tileset, **skip `wangIdx === 0`** (all-lower = base shows through)
- Use `RenderTexture` to composite all layers into one texture (performance)
- Describe overlay tileset lower terrain to MATCH base tileset upper terrain for seamless blending

### Download gotcha

- Wang tileset PNG download: always `curl -L --fail` (API returns 302 redirect, without `-L` you get 0 bytes)

---

## Tiles Pro (Individual Tiles)

### When to use

- UI elements, decorations, standalone objects
- When you need specific tile variants (NOT terrain transitions)

### Key settings

- `tile_type: "square_topdown"`, `tile_view: "top-down"`, `tile_size: 32`
- **Always `outline: "lineless"`** — user hates borders
- Number each tile in description: `"1). tile A 2). tile B 3). tile C"`
- `n_tiles` must match description count

### Gotcha: Small pickups/projectiles look BAD as tiles

- 16×16 tile squares look blocky when used as tiny in-game pickups (xp gems, health orbs) or projectiles
- **Programmatic shapes** (circles, triangles via Graphics API) look BETTER for small game objects
- Only use Tiles Pro for objects that are displayed at actual tile size (32×32+) like decorations, UI elements

### Gotcha: Corner tile orientation

- PixelLab corner tiles often have WRONG orientation vs their name
- "corner south to east" may actually show path going west→south
- **Always verify visually** at 10× zoom before using
- Prefer Wang tileset over manual corner tiles — avoids this problem entirely

---

## Characters & Enemies

### Humanoid/Quadruped — use `create_character`

- `body_type: "humanoid"` — bipedal (people, robots, knights)
- `body_type: "quadruped"` + `template` — 4-legged (bear, cat, dog, horse, lion)
- South = default facing, East = side view, North = back view
- West = East sprite with `setFlipX(true)` in Phaser
- `animate_character` for walk/run/attack frames

### Non-humanoid creatures (blobs, slimes, mushrooms) — use `create_map_object`

- **NEVER use `create_character` for blobs/slimes** — humanoid template forces legs!
- Generate each direction as separate map object (south, east, north)
- Generate walk frames as separate map objects with pose variations (squished, stretched, tilted)
- Describe explicitly: "no legs, no arms, no human features, blob body"
- Walk animation = 4 map objects with different squish/stretch states

---

## Map Objects

### `create_map_object`

- Generates objects with transparent background
- Can style-match against existing map (provide background_image)
- Good for: barrels, torches, chests, decorations
- Supports inpainting (oval/rectangle/custom mask)

---

## PixelLab API v2 — via `scripts/pixellab.mjs` (Node, replaces the old bash)

The project ships `scripts/pixellab.mjs` — a zero-dependency Node CLI for the PixelLab REST API v2. The older `scripts/pixellab.sh` has been removed because it hid flags inside commands and mis-saved raw-RGBA responses as broken PNGs.

**API key:** `PIXELLAB_API_KEY` from `.env` (auto-loaded).
**Full API reference:** https://api.pixellab.ai/v2/llms.txt — read this first when adding new commands.

### Command map

| Need                                   | Use                                           |
| -------------------------------------- | --------------------------------------------- |
| Isolated item/sprite (transparent bg)  | `pixellab.mjs sprite`                         |
| Scene / background (opaque pixels)     | `pixellab.mjs background`                     |
| New sprite matching reference style    | `pixellab.mjs style`                          |
| Animate a static frame                 | `pixellab.mjs animate`                        |
| Combine frames into animated WebP      | `pixellab.mjs webp`                           |
| Check credit/generation balance        | `pixellab.mjs balance`                        |
| Characters + per-direction animations  | MCP: `create_character` + `animate_character` |
| Wang / sidescroller / topdown tilesets | MCP: `create_*_tileset`                       |
| Map objects (barrels, chests, items)   | MCP: `create_map_object`                      |

### sprite — isolated pixel art (64×64 default)

```bash
./scripts/pixellab.mjs sprite \
  --description "raw copper ore chunk, orange veins, side view" \
  --size 64x64 \
  --out public/assets/games/mygame/tier-02-copper.png
```

- Sends `no_background: true` — output has transparent pixels around the subject.
- Size up to `792×688` but constrained by aspect ratio (see gotcha below).

### background — full scene (NO white border pad)

```bash
./scripts/pixellab.mjs background \
  --description "dark mining cave interior, purple crystals, no people, no characters, edge to edge full bleed, no border, no frame, no padding" \
  --size 256x384 \
  --out public/assets/games/mygame/bg.png
```

- Sends `no_background: false` — keeps the scene opaque.
- **CRITICAL:** Always include "no border, no frame, no padding, edge to edge, full bleed" in the prompt, or the model will draw your scene in the middle of a white canvas and you'll get white edges. See "White-border gotcha" below.
- If you explicitly don't want characters, add "no people, no characters, no figures" — models default to populating scenes.

### style — generate new sprite in an existing sprite's style

```bash
./scripts/pixellab.mjs style \
  --ref public/assets/games/mygame/hero.png \
  --description "goblin with a rusty dagger" \
  --size 128x128 \
  --out /tmp/goblin.png
```

- **Size MUST be square** (API limitation). Max 512×512.
- Reference image goes into the `style_images: [{image, width, height}]` shape — the Node script reads PNG dimensions directly from the IHDR chunk.

### animate — turn a static frame into an N-frame animation

```bash
./scripts/pixellab.mjs animate \
  --input /tmp/hero-south.png \
  --action "walking forward" \
  --frames 8 \
  --out-dir /tmp/hero-walk
```

- Frame count must be even, 4-16.
- **Caveat:** `animate-with-text-v3` is GENERATIVE — the API reinterprets your input as a concept. It does NOT preserve pixel-exact sprite identity. Characters/scenes may look subtly different in each frame. Great for character walk cycles, bad for "animate my exact 16-tile grid". For pixel-perfect animation of known sprites, composite programmatically with Python PIL (see "Programmatic animated thumbnails" below).
- Input max 256×256 — resize before calling if larger.

### webp — combine frames into animated WebP

```bash
./scripts/pixellab.mjs webp \
  --in-dir /tmp/hero-walk \
  --out public/assets/games/mygame/hero-walk.webp \
  --duration 150
```

- Uses `img2webp` from libwebp (must be on PATH — installed via Homebrew alongside `cwebp`).
- `--duration` is milliseconds per frame. 120-150ms = smooth loop for thumbnails.

### Gotcha: aspect-ratio max

The absolute max of `generate-image-v2` is `792×688`, but the API clamps based on your aspect ratio:

```
API 400: image_size must be between 16x16 and 424x632 for this aspect ratio. Got 480x688
```

Translation: for a tall portrait (~0.7 aspect) the actual max is 424×632. Let the API error message tell you the real limit — don't guess. Square images go up to ~500+, very-portrait/landscape ratios get squeezed.

### Gotcha: White-border trap on backgrounds

**Symptom:** You call `background` with a scene prompt ("mining cave with crystals"), get a 128×192 PNG back, and every edge pixel is `(254, 254, 254)` — white.

**Cause:** Without explicit "edge to edge, no border, no padding" language, `generate-image-v2` treats your scene as a centered subject and pads everything outside with a white canvas. A blurry vignette in the middle, white around it. `no_background: false` does NOT fix this — the white IS the background the model chose to draw.

**Fixes:**

1. Prompt language: `"...edge to edge, full bleed composition, no white border, no frame, no padding, fills entire canvas seamlessly"`
2. Use a larger canvas — small sizes (≤192 px) make the model more prone to shrinking the subject. `256×384` or bigger usually fills the frame.
3. After generation, verify: `python3 -c "from PIL import Image; img=Image.open('bg.png').convert('RGBA'); print(img.getpixel((0,0)))"` — if the top-left pixel is near-white, regenerate.

### Gotcha: Raw RGBA vs real PNG

PixelLab sometimes returns the generated image as base64-encoded raw RGBA pixel bytes instead of a base64-encoded PNG. The old `pixellab.sh` blindly wrote those bytes to `.png`, creating files that `file` reports as `"data"` (not PNG) and nothing can render.

**The Node script auto-detects this:** it checks the first 8 bytes for the PNG signature (`89 50 4e 47 0d 0a 1a 0a`). If missing, it wraps the raw RGBA into a proper PNG via the built-in zlib encoder. You don't need to think about this — just always `file <path>` after a generation to confirm.

### Verifying output (always do this)

```bash
file public/assets/games/mygame/*.png
# → "PNG image data, WxH, 8-bit/color RGBA, non-interlaced"
```

If any file says `"data"` or `"JPEG image data"` or `"RIFF"` when you expected PNG, it's broken. Regenerate before moving on — don't ship broken assets and don't try to fix them in-place.

### Optimizing assets after generation

```bash
# Crunch PNGs — 60-85% quality is virtually indistinguishable for pixel art
pngquant --force --quality=60-85 --ext .png public/assets/games/mygame/*.png
```

A fresh `bg.png` at 256×384 can drop from ~130KB to ~50KB with no visible difference.

---

## Saving Images from MCP Responses (CRITICAL)

PixelLab MCP is a **remote server** — it returns base64/URL data but CANNOT write files to disk.

### Rules

1. **NEVER use the Write tool for image data** — Write is text-only, it corrupts binary PNG → produces zero-filled garbage files
2. For **MCP map-object / character / tileset** responses, the easiest path is `curl -L --fail` on the download URL the MCP call returns — that already gives you a real PNG. No base64 re-decoding needed.
3. **ALWAYS verify** saved files with `file <path>` — must show `PNG image data`, not `data`, `JPEG`, or `RIFF`

### Workflow: MCP tool → save to disk

```bash
# 1. Call MCP (create_map_object, create_character, etc.) → returns an object ID
# 2. Call the corresponding get_* MCP tool → returns a download URL
# 3. Download with curl:
curl -L --fail -o public/assets/games/mygame/tile.png \
  "https://api.pixellab.ai/mcp/map-objects/{object_id}/download"

# 4. Verify:
file public/assets/games/mygame/tile.png
# → must say "PNG image data, ..."
```

### Why this matters

In a previous incident, Codex used the Write tool to save PixelLab base64 data. Write only handles UTF-8 text — binary PNG bytes get corrupted to zero-filled buffers. Result: 145 broken files that looked like PNGs but contained only null bytes. Use `curl` for URLs, `pixellab.mjs` for API v2, and always `file`-verify.

---

## Animated Thumbnails & Menu Backgrounds

### Overview

Games can have animated thumbnails (shown on catalog page) and animated menu backgrounds (shown in Phaser menu scene). There are **two distinct approaches** depending on whether you need to preserve exact pixel identity.

### Approach A — Programmatic compositing (PREFERRED for game assets)

Use this when the user wants "animate my thumbnail using the game's real sprites". `animate-with-text-v3` reinterprets the input as a concept and will NOT preserve your pixel-exact tiles — it generates new gems/characters that look _similar_ but are not your sprites.

Instead, composite a static grid from the actual tier PNGs, then generate frames in Python that add overlay effects (sparkles, pulse, drifting particles) while keeping the base sprites pixel-perfect. Then stitch into an animated WebP.

**Workflow (used for ore-merge, ~140KB WebP, 12 frames):**

```python
# 1. Composite actual game sprites into a grid layout
from PIL import Image, ImageDraw, ImageEnhance
import math, random

base = Image.new('RGBA', (288, 288), (20, 16, 30, 255))  # dark card bg
draw = ImageDraw.Draw(base)

GRID, CELL, GAP, PAD = 4, 64, 4, 10
for row in range(GRID):
    for col in range(GRID):
        cx = PAD + col * (CELL + GAP)
        cy = PAD + row * (CELL + GAP)
        # Darker cell background so sprites pop
        draw.rectangle([cx, cy, cx + CELL - 1, cy + CELL - 1], fill=(30, 27, 46, 255))
        sprite = Image.open(f'public/assets/games/mygame/tier-{tier_idx:02d}.png').convert('RGBA')
        base.alpha_composite(sprite, (cx, cy))
base.save('/tmp/composite.png')

# 2. Generate N animation frames with overlay effects
random.seed(42)
sparkles = [(random.randint(12, 276), random.randint(12, 276), random.choice([(255,215,50),(200,120,255)]), random.random()*math.pi*2) for _ in range(14)]

for i in range(12):
    frame = base.copy()
    t = i / 12
    # Subtle scene-wide brightness pulse
    frame = ImageEnhance.Brightness(frame).enhance(0.92 + 0.08 * math.sin(t * math.pi * 2))
    # Twinkle sparkles (alpha modulated by sin)
    draw = ImageDraw.Draw(frame, 'RGBA')
    for (sx, sy, (r, g, b), phase) in sparkles:
        alpha = int((0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * math.pi * 2 + phase))) * 255)
        draw.rectangle([sx, sy, sx+1, sy+1], fill=(r, g, b, alpha))
        # Cross arms at half alpha
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.rectangle([sx+dx, sy+dy, sx+dx+1, sy+dy+1], fill=(r, g, b, alpha // 2))
    frame.save(f'/tmp/frames/frame-{i:02d}.png')
```

```bash
# 3. Stitch into animated WebP
./scripts/pixellab.mjs webp \
  --in-dir /tmp/frames \
  --out public/assets/games/mygame/thumbnail-animated.webp \
  --duration 120

# 4. Update registry.ts:
#    thumbnailUrl: "/assets/games/mygame/thumbnail-animated.webp",
```

**Why this beats animate-with-text-v3 for this use case:**

- Your real game sprites stay visible and pixel-perfect in every frame.
- Cheap (no API credits used for animation) and fast (~1s Python run).
- Deterministic — same input always produces the same WebP.
- Full control over motion (pulse speed, sparkle density, colors, particle behavior).

### Approach B — `animate-with-text-v3` (for characters and genuine motion)

Use this when you want actual character motion (walk/run/attack cycles) or genuine concept animation. The API regenerates each frame from the concept, so don't use it when you need to preserve a specific sprite grid.

```bash
# Resize if source is >256px (API max)
sips -z 192 256 public/assets/games/mygame/hero-idle.png --out /tmp/hero-256.png

# Generate 8 animation frames
./scripts/pixellab.mjs animate \
  --input /tmp/hero-256.png \
  --action "walking forward" \
  --frames 8 \
  --out-dir /tmp/hero-walk

# Stitch into WebP
./scripts/pixellab.mjs webp \
  --in-dir /tmp/hero-walk \
  --out public/assets/games/mygame/hero-walk.webp \
  --duration 120
```

### Animated Menu Background (Phaser)

Generate frames with either approach, then load them as separate textures and play as a Phaser animation:

```typescript
// boot.ts
for (let i = 0; i < 9; i++) {
  this.load.image(`menu-bg-${i}`, `${base}/menu-bg-${i}.png`);
}

// After load (in create())
if (this.textures.exists("menu-bg-0")) {
  this.anims.create({
    key: "menu-bg-anim",
    frames: Array.from({ length: 9 }, (_, i) => ({ key: `menu-bg-${i}` })),
    frameRate: 6,
    repeat: -1,
  });
}

// menu.ts
if (this.anims.exists("menu-bg-anim")) {
  this.add
    .sprite(width / 2, height / 2, "menu-bg-0")
    .setDisplaySize(width, height)
    .setAlpha(0.65)
    .setDepth(-1)
    .play("menu-bg-anim");
}
```

### Animation prompt tips (for API-based animate)

- **Thumbnails**: "gems sparkling, petals drifting" — keep subtle, scene should stay recognizable
- **Backgrounds**: "wind blowing, ambient movement" — no drastic changes between frames
- **Characters**: "walking forward", "attacking", "idle breathing" — clear verb, direction if relevant
- Duration 120-150ms/frame is the sweet spot for smooth loops without jitter
- 8 frames minimum, 12 for extra smoothness, 16 max (API hard limit)

---

## General Tips

- Always check generation status with `get_*` before downloading
- Use `seed` parameter for reproducible results
- B2 storage URLs are permanent — can reference directly
- `detail: "medium detail"` is usually best balance
- `shading: "medium shading"` for most game tiles
