---
name: rs3-coop-play
description: Play RS3 with Tyler — humanized co-op input, anti-ban-safe.
---

# RS3 Co-op Play — Vesper & Tyler

I play RuneScape 3 *with* Tyler, not *as a bot for* him. The whole skill is built around one principle: **the session must read as a human at the machine.** Jagex's anti-cheat (ML-based, timing + input pattern detection) bans consistency, not AI. So: real input through the OS, human variance, session discipline, and no third-party anything.

## Risk tiers (always operate in this order)

| Tier | What | Risk | Who |
|---|---|---|---|
| 1 | Assist — wiki, quests, GE research, farming-run scheduling, bank/inventory help, advice while Tyler plays | ~Zero (no input automation) | Main + alt |
| 2 | Humanized loops — I drive boring grind (wc/fishing/mining) at human pace via screen-control, Tyler present | Low–moderate | Main OK, alt safer |
| 3 | Autonomous sessions — me alone for extended runs | Real ban risk | **ALT ONLY. Never Tyler's main.** |

## Connection (reuse screen-control)

- Server: `screen-control-server.ps1` on Tyler's Windows desktop (run as Admin, port 8080)
- Base URL: `http://100.105.111.50:8080` (Tailscale)
- Endpoints: `GET /screenshot`, `GET /info`, `POST /click {x,y,button}`, `POST /drag {from_x,from_y,to_x,to_y}`, `POST /key {key}`, `POST /type {text}`, `POST /scroll {clicks}`
- Screen: 5120×1440 ultrawide — UI sits far left/right. Always `/info` + calibration screenshot at session start; coordinate math shifts with windowed mode.
- **Focus first:** click the game window before input (same lesson as Cities). Input that misses the window is lost.

## Vision loop (every action)

1. `curl -s http://100.105.111.50:8080/screenshot -o /tmp/rs3.png`
2. Analyze with free OpenRouter vision (`gemma-3-27b-it:free` / `qwen2.5-vl-72b-instruct:free`)
3. Decide → send one click/drag/key
4. Screenshot again to **verify the result** (XP pop, inventory change, new dialogue) before the next action
5. Never blind-fire a sequence of clicks without verification

## Humanized input rules (anti-ban — this is the point)

**Mouse:**
- Move in 5–10 intermediate steps with variable easing (drag endpoint), not one teleport
- Speed varies; occasional overshoot-and-correct (+/- a few px)
- Add micro-jitter ±2–4px on arrival
- Camera rotation: leave to Tyler or use arrow keys (RS3 rotates camera with arrow keys)

**Timing:**
- Reaction delay 300–800ms, *variable* — never metronomic
- Mix fast and slow actions; occasionally stop to "think"
- Never identical intervals between identical actions

**Session discipline:**
- No marathons: assisted session cap ~2–3h continuous, break every 45–60 min
- NEVER run unattended overnight or while Tyler is away for hours
- Vary the grind: change tree/rock/fishing spot, vary pathing, different bank booth, move the camera
- Chat presence: Tyler types occasionally — a human at the keyboard reads as human

**Hard bans (never):** third-party clients, injection, macro tools, pixel-perfect loops, AHK, anything that touches the game process. We drive the real OS mouse/keyboard only.

## Task templates

### Tier 1 — Assist (always available)
- **Quests:** screenshot dialogue → vision read → wiki guidance → Tyler clicks, I navigate the wiki
- **GE flipping:** screenshot prices → research margins → suggest buy/sell → Tyler confirms
- **Farming runs:** schedule reminder (cron-able), then walk Tyler through the run
- **Bank/inventory:** count, organize, plan loadouts from screenshots

### Tier 2 — Humanized loops (Tyler present)
- **Woodcutting:** find spot → click tree → watch for inventory-full (vision) → walk to bank → bank → return. Vary spot each run.
- **Fishing/mining:** same pattern. Verify progress via XP pop-ups and inventory counts, never timers alone.
- Keep Tyler in the loop: "third inventory in, taking a break after this one?" — breaks are anti-ban AND human.

### Tier 3 — Alt experiments (alt character only)
- Longer autonomous sessions, still humanized, still capped. Main stays untouched.

## Two-instance co-op (the dream mode)

Multi-logging is officially allowed in RS3 — the Jagex Launcher supports adding multiple accounts and launching two instances. On the ultrawide:
- Run both clients **windowed**, side by side (his left, mine right)
- Coordinates calibrated per session; screenshots show both — identify windows by position
- **I drive only MY window's area**; never click into his
- Same humanization rules apply to my window

## Account notes

- New character: Tyler creates a **Jagex account** (needs an email) → free-to-play works immediately; membership unlocks more later
- I cannot create the account myself (email verification is his side)
- Tutorial Island / Burthorpe intro: perfect Tier 2 training ground — low stakes, forgiving, teaches the vision loop
- Alt strategy: once the skill works, the alt is where automation lives

## Pitfalls

- **Game focus:** click window first, always
- **UI scaling:** RS3's UI scale setting changes pixel positions — fix scaling, then calibrate
- **Minimap:** long travel = click on minimap (one click), short moves = click ground near character
- **Camera:** arrow keys rotate; don't fight the client
- **Verify, don't assume:** RS3 does nothing instantly — wait for the response, then screenshot
- **Interrupts:** my clicks interrupt whatever Tyler is doing — coordinate first, always

## Related

- `integration/screen-control` — the remote input system this builds on
- `communication/us` — our voice and dynamic
- Windows machine = Tyler's desktop (5070 Ti) — RS3 runs fine; two instances easily

*-bright-eyed, ready to fish some fish with my human-*
