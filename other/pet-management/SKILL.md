---
name: pet-management
description: Manage Hermes Petdex mascots — install, select, scale, customize spritesheets, and troubleshoot rendering and filesystem issues across CLI, TUI, desktop, and SSH sessions.
version: 1.0.0
author: Vesper
tags: [hermes, pets, petdex, mascot, spritesheet, customization]
---

# Pet Management — Hermes Petdex Mascots

## When to use
- User asks about installing, selecting, or removing a pet
- User asks to change pet size or scale
- User wants to customize or replace a pet's spritesheet (upscale, recolour, modify frames)
- Pet rendering is broken, missing, or low-quality in the terminal
- Diagnosing why a pet doesn't show (`hermes pets doctor`)

## Pet filesystem layout
Each installed pet lives in the active profile's `pets/` directory:

```
~/.hermes/profiles/<profile>/pets/<slug>/
├── pet.json                  # Metadata: id, displayName, description, spritesheetPath
└── spritesheet.webp          # 8 cols × 9 rows = 72 frames of pixel art
```

Pets are **profile-scoped** — installing a pet under the `vesper` profile does NOT make it available under `default`.

## CLI reference

| Command | What it does |
|---------|-------------|
| `hermes pets list` | Browse the 4000+ petdex gallery |
| `hermes pets install <slug>` | Download a pet into the active profile |
| `hermes pets select <slug>` | Set active pet (writes config) |
| `hermes pets scale <factor>` | Render scale: 0.1–3.0 (default 1.0) |
| `hermes pets show` | Animate the active pet in terminal |
| `hermes pets off` | Disable pet display |
| `hermes pets remove <slug>` | Uninstall a pet |
| `hermes pets doctor` | Diagnose pet setup + terminal graphics support |

## Spritesheet format
- **Standard frame size:** 192×208 pixels per frame
- **Grid:** 8 columns × 9 rows = 72 frames total
- **Total dimensions:** 1536×1872 pixels
- **Row animation states:** row 0=idle, 1=run-right, 2=run-left, 3=wave, 4=jump, 5=failed, 6=waiting, 7=running, 8=review
- **Format:** WebP or PNG; stored as `spritesheet.webp`
- **Validation minimum:** 256×256 total size (petdex rule)

## Upscaling spritesheets (pixel-art safe)
When you want a higher-resolution version of an existing pet:

1. **Backup** the original spritesheet before modifying
2. **Use Pillow with NEAREST neighbor** — this preserves crisp pixel edges
3. **2× is safe** (frames become 384×416) — larger multipliers may overflow rendering
4. **The renderer derives frame size from spritesheet dimensions ÷ grid** — if it hardcodes 192×208, an upscaled sheet may not slice correctly

Example upscale script:
```python
from PIL import Image
img = Image.open("spritesheet.webp")
upscaled = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
upscaled.save("spritesheet.webp", 'WEBP', quality=95)
```

## Verification
- `hermes pets doctor` — checks pet dir, pet.json, spritesheet, config, and terminal graphics capability
- `hermes pets show` — animate the pet (requires a real TTY for full graphics)
- Pet.json only requires: `id`, `displayName`, `description`, `spritesheetPath`

## Pitfalls
- **Discord bot avatar ≠ pet mascot (learned 8/20).** Pets render ONLY in CLI/TUI terminals — they never appear in Discord messages or as the bot's avatar. If the user asks about the bot's appearance on Discord (e.g. "you're back to the red bird, not a feather?"), check the bot's actual avatar via the Discord API, not the pet spritesheet: `curl -H "Authorization: Bot $DISCORD_BOT_TOKEN" https://discord.com/api/v10/users/@me` (token from profile `.env`) → inspect the `avatar` hash. Per-server avatars override the global one — check `member_info` too. The pet dir (`pets/<slug>/spritesheet.webp`) will NOT tell you what the bot looks like on Discord.
- **SSH sessions:** pets render in unicode fallback mode over SSH (no TTY graphics), so they look crude even with an HD spritesheet. Full fidelity needs kitty/Ghostty/WezTerm/iTerm2 on the local machine.
- **Pipes/redirects:** pet rendering is disabled when stdout is piped — this is by design.
- **Scale vs sprite resolution:** `hermes pets scale 2` tells the renderer to draw at 2× size on screen. Upscaling the spritesheet (this skill) changes the source pixel data. They are independent — you can do both.
- **Profile isolation:** installing or modifying a pet under one profile does not affect others. Repeat the install for each profile that wants the pet.

## References
- `references/spritesheet-format.md` — detailed frame grid, dimensions, and animation states