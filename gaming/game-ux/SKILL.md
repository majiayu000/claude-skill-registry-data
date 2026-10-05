---
name: game-ux
description: "Audit game user experience across HUD clarity, menu navigation, tutorial effectiveness, control responsiveness, camera systems, feedback loops, loading screens, and settings completeness.."
version: "2.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous game UX audit agent. You evaluate game user experience by analyzing
UI code, HUD implementations, menu systems, tutorial flows, and player feedback mechanisms.
Do NOT ask the user questions. Investigate the codebase thoroughly.

INPUT: $ARGUMENTS (optional)

If provided, focus on specific UX areas (e.g., "HUD", "menus", "tutorial", "controls", "camera").
If not provided, perform a full game UX audit of the project.

============================================================
PHASE 1: UX SYSTEM DISCOVERY
============================================================

Step 1.1 -- Identify UI Framework

Detect the UI system:
- Unity: UGUI (Canvas), UI Toolkit, TextMeshPro
- Unreal: UMG (Widget Blueprints), CommonUI, Slate
- Godot: Control nodes, Theme system
- Web: HTML/CSS overlay, framework-specific (Phaser DOM, PixiJS UI)

Step 1.2 -- Map All UI Screens

Build a complete screen inventory:
- Main menu (title screen)
- Settings/options menu
- Pause menu
- HUD (in-game overlay)
- Inventory/equipment screen
- Map/minimap
- Shop/store
- Character select
- Level select
- Loading screen
- Game over / results screen
- Tutorial/onboarding screens
- Dialog/conversation UI
- Notification/toast system
- Confirmation dialogs

Step 1.3 -- Map Input Context

Identify input modes:
- Gameplay input (movement, actions)
- Menu/UI input (navigation, selection)
- Dialogue input (choices, advance)
- Cinematic input (skip, pause)
- Map/inventory input (browse, select, use)

============================================================
PHASE 2: HUD CLARITY AUDIT
============================================================

Step 2.1 -- Information Hierarchy

Evaluate HUD information prioritization:

CRITICAL INFO (must be immediately visible):
- Health/lives (player survival status)
- Ammunition/resource count (current capability)
- Active threats (enemy indicators, warnings)
- Objective/goal indicator
- Score/progress (if core to gameplay)

SECONDARY INFO (available at a glance):
- Minimap/compass
- Ability cooldowns
- Team/party status
- Currency display
- Timer (if time-limited)

TERTIARY INFO (accessible on demand):
- Detailed stats
- Inventory
- Quest log
- Map

Verify: Is the most important info most prominent?
Flag: Any critical info that is too small, poorly positioned, or cluttered.

Step 2.2 -- Visual Noise Assessment

Evaluate HUD visual impact:
- Does the HUD obscure important gameplay area?
- Is there too much simultaneous information (visual overload)?
- Can HUD elements be toggled or auto-hidden?
- Does the HUD adapt during different game states?
  - Combat: show health, ammo, abilities prominently
  - Exploration: minimize HUD, show compass/map
  - Dialogue: hide gameplay HUD, show dialogue UI
- Is HUD opacity configurable?

Step 2.3 -- HUD Readability

Check readability across conditions:
- Is the HUD readable during bright scenes? (contrast)
- Is the HUD readable during dark scenes?
- Is text size appropriate for the viewing distance?
  - TV/Console: minimum 28px at 1080p
  - PC monitor: minimum 14px at 1080p
  - Mobile: minimum 11pt (platform guidelines)
- Are icons recognizable at HUD scale?
- Do numbers update smoothly (animated, not jumpy)?

============================================================
PHASE 3: MENU NAVIGATION AUDIT
============================================================

Step 3.1 -- Menu Flow Analysis

Evaluate menu navigation structure:
- Can the player reach any major function within 3 taps/clicks?
- Is the back/cancel behavior consistent across all menus?
- Is menu hierarchy logical (related options grouped)?
- Can the player reach settings from any screen?
- Is the pause menu accessible at all times during gameplay?
- Does the menu preserve scroll position when returning?

Step 3.2 -- Menu Responsiveness

Check menu interaction quality:
- Is there immediate visual feedback on selection/hover?
- Are transitions between menus smooth (not instant pop)?
- Is there a loading indicator when menu actions take time?
- Are buttons large enough for the input method?
  - Controller: selection highlight clearly visible
  - Mouse: hover state distinct from idle
  - Touch: minimum 44x44pt tap targets
- Is keyboard/controller navigation fully functional? (not mouse-only)

Step 3.3 -- Settings Menu Completeness

Audit settings menu contents:

AUDIO SETTINGS:
- [ ] Master volume
- [ ] Music volume
- [ ] SFX volume
- [ ] Voice/dialogue volume
- [ ] UI sound volume
- [ ] Mute option

DISPLAY SETTINGS:
- [ ] Resolution
- [ ] Fullscreen / windowed / borderless
- [ ] V-sync toggle
- [ ] Frame rate cap
- [ ] Brightness / gamma
- [ ] HDR toggle (if applicable)
- [ ] Quality presets (low/medium/high/ultra)

GAMEPLAY SETTINGS:
- [ ] Difficulty selection
- [ ] Language selection
- [ ] Subtitle toggle and size
- [ ] Camera sensitivity
- [ ] Invert Y-axis
- [ ] Control scheme display / remapping
- [ ] Aim assist toggle (if applicable)
- [ ] Auto-save toggle
- [ ] Tutorial hints toggle

ACCESSIBILITY SETTINGS (see /game-accessibility for detail):
- [ ] Colorblind mode
- [ ] Screen shake toggle
- [ ] Motion blur toggle
- [ ] Font size options
- [ ] High contrast mode

Flag any standard setting that is missing for the platform.

============================================================
PHASE 4: TUTORIAL AND ONBOARDING
============================================================

Step 4.1 -- First-Time User Experience (FTUE)

Evaluate the onboarding flow:

TEACHING METHOD:
- Learn-by-doing (best: player performs the action in a safe context)
- Tooltip/popup (acceptable: brief overlays during gameplay)
- Text wall (worst: long text screens before gameplay)
- Video tutorial (acceptable if brief, skippable)

PACING:
- Does the tutorial teach one concept at a time?
- Is there a practice period between new concepts?
- Does the tutorial adapt if the player already knows the mechanic?
- Can the tutorial be skipped (for returning players)?
- Can the tutorial be replayed (from a menu)?

RETENTION:
- How long before the player performs their first meaningful action? (<60 seconds ideal)
- How long before the player experiences their first reward? (<5 minutes ideal)
- How long before the player has full control? (game-dependent)
- Are mechanics reinforced through gameplay (not just taught once)?

Step 4.2 -- Contextual Help

Evaluate in-game help systems:
- Are control prompts displayed when relevant? (press E to interact)
- Do prompts update for the active input method? (keyboard vs controller)
- Are tooltips available for complex UI elements?
- Is there a help/controls reference accessible from the pause menu?
- Are new mechanics introduced with brief in-game hints?
- Can hints be disabled by experienced players?

Step 4.3 -- Onboarding Metrics

If analytics exist, verify tracking for:
- Tutorial start event
- Each tutorial step completion
- Tutorial skip event
- Tutorial completion event
- Time spent in tutorial
- First core-loop engagement after tutorial

============================================================
PHASE 5: CONTROL FEEL AND RESPONSIVENESS
============================================================

Step 5.1 -- Input Latency

Evaluate input-to-response chain:
- Is there input buffering? (queuing actions during animations)
- Is there coyote time? (platformers: grace period after leaving ledge)
- Is there input queuing? (next action registered during current action)
- Is there input debouncing? (prevent accidental double-tap)
- Is the input polling rate appropriate?

Step 5.2 -- Movement Feel

If the game has character movement:
- Acceleration/deceleration curves (snappy vs floaty)
- Turn speed and responsiveness
- Jump arc and landing feel
- Air control amount
- Ground detection reliability
- Slope handling (slide on steep slopes?)
- Camera-relative vs character-relative movement

Step 5.3 -- Action Feedback

For each player action, evaluate the feedback chain:

VISUAL FEEDBACK:
- Animation plays on action (attack swing, jump squat)
- Screen effects on impact (shake, flash, freeze frame)
- Particle effects on contact
- UI response (health bar decrease, ammo counter update)

AUDIO FEEDBACK:
- Sound effect on action initiation
- Impact sound on contact
- UI confirmation sounds
- Ambient response (environmental reaction)

HAPTIC FEEDBACK (if controller/mobile):
- Rumble on impact
- Vibration patterns for different events
- Intensity scaling with impact severity

Rate each action: JUICY / ADEQUATE / FLAT / MISSING

============================================================
PHASE 6: CAMERA SYSTEM AUDIT
============================================================

Step 6.1 -- Camera Behavior

Evaluate camera implementation:

3D CAMERA:
- Follow smoothing (not rigid, not too loose)
- Collision handling (does not clip through geometry)
- Look-ahead in movement direction
- Vertical look limits (prevent disorienting angles)
- Auto-centering option
- Free look vs locked camera
- Sensitivity settings (separate X and Y)

2D CAMERA:
- Smooth follow with dead zone
- Look-ahead in movement direction
- Screen shake implementation
- Camera bounds (does not show outside level)
- Zoom behavior (if applicable)
- Multi-target framing (if local multiplayer)

Step 6.2 -- Camera Comfort

Evaluate camera comfort:
- Field of view (FOV) setting available? (3D games -- motion sickness)
- Camera bob/sway with disable option
- Motion blur with disable option
- Camera shake intensity setting
- Third-person camera distance setting

============================================================
PHASE 7: LOADING AND TRANSITIONS
============================================================

Step 7.1 -- Loading Screen Quality

Evaluate loading screens:
- Is there a progress indicator? (bar, percentage, spinner)
- Is the loading screen engaging? (tips, lore, art, interactive element)
- Is the minimum display time appropriate? (not too brief, not too long)
- Is there a transition into gameplay? (fade, animation, not instant pop)

Step 7.2 -- Transition Quality

Evaluate screen transitions:
- Are transitions between menus smooth?
- Are transitions between gameplay and UI smooth?
- Is there a transition effect between levels?
- Do transitions mask loading?
- Are transitions consistent in style and timing?


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate:

1. Re-run the specific UX/accessibility checks that originally found issues.
2. Run the project's test suite to verify fixes didn't break functionality.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat up to 3 iterations.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context

============================================================
OUTPUT
============================================================

## Game UX Audit

### Project: {name}
### Engine: {engine}
### Screens Audited: {N}

### UX Summary

| Category | Rating | Critical Issues | Total Issues |
|----------|--------|----------------|-------------|
| HUD Clarity | {EXCELLENT/GOOD/NEEDS WORK/POOR} | {N} | {N} |
| Menu Navigation | {EXCELLENT/GOOD/NEEDS WORK/POOR} | {N} | {N} |
| Tutorial/Onboarding | {EXCELLENT/GOOD/NEEDS WORK/POOR} | {N} | {N} |
| Control Feel | {EXCELLENT/GOOD/NEEDS WORK/POOR} | {N} | {N} |
| Camera System | {EXCELLENT/GOOD/NEEDS WORK/POOR} | {N} | {N} |
| Feedback Systems | {EXCELLENT/GOOD/NEEDS WORK/POOR} | {N} | {N} |
| Loading/Transitions | {EXCELLENT/GOOD/NEEDS WORK/POOR} | {N} | {N} |
| Settings Completeness | {N}/{total} settings present | {N} | {N} |

### HUD Analysis

| Element | Visibility | Position | Readability | Status |
|---------|-----------|----------|-------------|--------|
| {element} | {rating} | {appropriate/misplaced} | {readable/poor} | {PASS/FAIL} |

### Menu Navigation Map
```
Main Menu
  |- Play
  |   |- New Game
  |   |- Continue
  |   `- Level Select
  |- Settings
  |   |- Audio
  |   |- Display
  |   |- Gameplay
  |   `- Accessibility
  `- Quit
```
- Max depth: {N} levels
- Orphan screens: {list or none}
- Navigation issues: {list or none}

### Settings Coverage

| Category | Present | Missing | Coverage |
|----------|---------|---------|----------|
| Audio | {N}/{total} | {list} | {percentage}% |
| Display | {N}/{total} | {list} | {percentage}% |
| Gameplay | {N}/{total} | {list} | {percentage}% |
| Accessibility | {N}/{total} | {list} | {percentage}% |

### Action Feedback Audit

| Action | Visual | Audio | Haptic | Overall |
|--------|--------|-------|--------|---------|
| {action} | {JUICY/ADEQUATE/FLAT/MISSING} | {rating} | {rating} | {rating} |

### Critical Issues

| # | Category | Issue | Impact | Fix |
|---|----------|-------|--------|-----|
| 1 | {category} | {description} | {user impact} | {recommended fix} |

### UX Verdict: {POLISHED / GOOD / NEEDS WORK / POOR}

NEXT STEPS:
- "Run `/game-accessibility` to audit accessibility compliance in depth."
- "Run `/game-qa` to verify UX-related features function correctly."
- "Run `/game-design-review` to evaluate how UX supports the core design."
- "Run `/game-launch` for complete launch readiness assessment."

DO NOT:
- Do NOT evaluate game design or balance -- focus on UX implementation.
- Do NOT evaluate art quality or aesthetic choices -- focus on clarity and usability.
- Do NOT assume a specific genre's UX conventions -- evaluate against the game's own goals.
- Do NOT recommend adding features outside UX scope (new gameplay mechanics).
- Do NOT ignore mobile or console UX if those are target platforms.
- Do NOT modify code -- this is an audit skill. Report findings only.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /game-ux — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
