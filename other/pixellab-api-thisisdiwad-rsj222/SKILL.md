---
name: pixellab-api
description: "Recolor"
---

# PixelLab API v2 — Direct Pixel Art Generation

Generate pixel art assets via PixelLab REST API v2 — animations, UI elements, sprites, editing, and more.
Complements the PixelLab MCP server with endpoints not available through MCP.

## When to use this skill

| Need | Tool |
|------|------|
| Animate existing sprite (walk/attack/idle) | `pixellab.sh animate` |
| Generate UI elements (buttons, bars, frames) | `pixellab.sh generate-ui` |
| General pixel art from text description | `pixellab.sh generate` |
| Match style of existing game assets | `pixellab.sh style` |
| Edit/modify existing sprite with text | `pixellab.sh edit` |
| Remove sprite background | `pixellab.sh remove-bg` |
| Rotate sprite to different direction | `pixellab.sh rotate` |
| Smart pixel-art resize | `pixellab.sh resize` |

**Use PixelLab MCP instead for:** characters with directional views, Wang tilesets, sidescroller tilesets, map objects.

## Setup

1. Get API key from https://pixellab.ai/account
2. Add to project `.env`: `PIXELLAB_API_KEY=your-token`
3. Copy `tools/pixellab.sh` to your project's `scripts/` directory
4. Make executable: `chmod +x scripts/pixellab.sh`

## Reference Files

| Topic | Reference |
|-------|-----------|
| Full endpoint docs | [api-v2-endpoints.md](references/api-v2-endpoints.md) |
| Workflow examples | [workflows.md](references/workflows.md) |

---

## Tool: `scripts/pixellab.sh`

Helper script that wraps all PixelLab API v2 endpoints. Reads `PIXELLAB_API_KEY` from `.env`.
Handles base64 encoding, async job polling, and saves output PNGs automatically.

### Commands

```bash
# Animate a static sprite (SYNC — most useful for game dev)
./scripts/pixellab.sh animate <sprite.png> "<action>" [frame_count] [outdir]

# Generate pixel art from text (ASYNC — polls automatically)
./scripts/pixellab.sh generate "<description>" [WxH] [outdir]

# Generate UI elements (ASYNC)
./scripts/pixellab.sh generate-ui "<description>" [WxH] [palette] [outdir]

# Edit existing sprite (ASYNC)
./scripts/pixellab.sh edit <sprite.png> "<description>" [outdir]

# Generate matching style (ASYNC)
./scripts/pixellab.sh style <ref-sprite.png> "<description>" [WxH] [outdir]

# Rotate sprite direction (SYNC)
./scripts/pixellab.sh rotate <sprite.png> <from-dir> <to-dir> [outpath]

# Smart resize (SYNC)
./scripts/pixellab.sh resize <sprite.png> <WxH> [description] [outpath]

# Remove background (SYNC)
./scripts/pixellab.sh remove-bg <sprite.png> [outpath]

# Poll async job manually
./scripts/pixellab.sh poll <job-id> [outdir]
```

---

## Quick Examples

### Animate existing character sprite

```bash
# 8-frame walk animation from static south-facing sprite
./scripts/pixellab.sh animate public/assets/games/frost-hold/player-south.png \
  "walking forward" 8

# Attack animation
./scripts/pixellab.sh animate public/assets/games/frost-hold/player-south.png \
  "attacking with sword, slash animation" 8

# Casting spell
./scripts/pixellab.sh animate public/assets/games/frost-hold/player-south.png \
  "casting ice spell, magical frost blast" 8
```

Output: `public/assets/test-api/animate-player-south/frame-{0..7}.png`

### Generate UI elements

```bash
# Button states
./scripts/pixellab.sh generate-ui \
  "pixel art medieval stone button with gold trim, normal and pressed states side by side" \
  256x128 "brown and gold"

# Health bar frame
./scripts/pixellab.sh generate-ui \
  "pixel art health bar frame, ornate metal border, empty inside, horizontal" \
  256x64 "red and silver"

# Inventory slot
./scripts/pixellab.sh generate-ui \
  "pixel art inventory grid slot, dark stone background, subtle border" \
  64x64 "dark grey and brown"
```

### Generate game items / icons

```bash
# Multiple icon variants (64x64 generates 16 results)
./scripts/pixellab.sh generate "pixel art golden trophy cup, game achievement icon" 64x64

# Weapon sprites
./scripts/pixellab.sh generate "pixel art flaming sword, fantasy RPG weapon" 64x64
```

### Style-matched generation

```bash
# Generate new enemy matching existing game style
./scripts/pixellab.sh style \
  public/assets/games/frost-hold/player-south.png \
  "ice goblin enemy, aggressive stance" 48x48
```

### Rotate missing directions

```bash
# Generate east-facing from south-facing
./scripts/pixellab.sh rotate \
  public/assets/games/crystal-td/golem.png south east

# Generate north-facing
./scripts/pixellab.sh rotate \
  public/assets/games/crystal-td/golem.png south north
```

### Edit existing sprite

```bash
# Add equipment to character
./scripts/pixellab.sh edit player.png "add a red cape and iron helmet"

# Recolor
./scripts/pixellab.sh edit enemy.png "change color to ice blue, frost theme"
```

---

## Sync vs Async Endpoints

| Command | Type | Wait time |
|---------|------|-----------|
| `animate` | Sync | 10-30s (returns directly) |
| `rotate` | Sync | 5-15s |
| `resize` | Sync | 5-15s |
| `remove-bg` | Sync | 5-10s |
| `generate` | Async | 30-90s (auto-polls) |
| `generate-ui` | Async | 30-90s (auto-polls) |
| `edit` | Async | 30-90s (auto-polls) |
| `style` | Async | 30-90s (auto-polls) |

Async commands poll every 10s with a 120s timeout. Use `poll` command to resume if needed.

---

## Output Behavior

- **Sync commands**: save directly to output path
- **Async commands**: poll until complete, then save all result images
- **Default output**: `public/assets/test-api/<command>-<name>/`
- **Custom output**: pass outdir/outpath as last argument
- **Multiple results**: generate/generate-ui often return multiple variants (4-64 depending on size)

## Image Size → Result Count (generate/generate-ui)

| Max dimension | Results |
|---------------|---------|
| ≤42px | 64 images |
| 43-85px | 16 images |
| 86-170px | 4 images |
| >170px | 1 image |

## Animation Frame Guidelines

| Frames | Best for |
|--------|----------|
| 4 | Simple loops (idle breathing, bobbing) |
| 8 | Standard movement (walk, run) |
| 12-16 | Complex actions (attack combos, spell casting) |

Frame count must be even. Max 256x256 per frame. Pixel budget: width x height x frames ≤ 524,288.

---

## Tips

- **Describe actions, not poses**: "walking forward" > "left foot forward right foot back"
- **`no_background: true`** is always set by the helper — sprites come transparent
- **Seed parameter**: not exposed in helper yet — edit script if you need reproducibility
- **Asset format**: all output is PNG with transparency
- **Animate best practice**: use the "south" facing idle frame as first_frame for best results
- Always `outline: "lineless"` preference — matches PixelDen art style
