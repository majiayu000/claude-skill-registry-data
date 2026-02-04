---
name: Game Sprint Executor (AILANG)
description: Execute approved sprint plans for Stapledons Voyage using AILANG. ALL game logic must be AILANG - engine is rendering only. Use when user says "execute sprint", "start implementation", or wants to begin an approved sprint plan.
---

# Game Sprint Executor (AILANG-Only)

Execute an approved sprint plan with **AILANG as the primary implementation language**. All game logic, state machines, and gameplay code goes in `sim/*.ail` - the Go engine only renders DrawCmd output.

## MANDATORY: Sprint JSON Tracking

**Every sprint MUST have a tracking JSON file:**

```bash
# Location: sprints/sprint_<sprint-id>.json
# Example: sprints/sprint_view-system-v1.json
```

**Two formats supported:**

### Features-Based (Preferred for new sprints)
```json
{
  "sprint_id": "<sprint-id>",
  "created": "YYYY-MM-DDTHH:MM:SSZ",
  "status": "in_progress",
  "design_doc": "design_docs/planned/next/<feature>.md",
  "features": [
    {
      "id": "feature-id",
      "description": "What this feature does",
      "estimated_loc": 300,
      "actual_loc": null,
      "dependencies": [],
      "acceptance_criteria": ["Criterion 1", "Criterion 2"],
      "passes": null,
      "started": null,
      "completed": null,
      "notes": null
    }
  ],
  "velocity": { "target_loc_per_day": 275, "actual_loc_per_day": 0 },
  "ailang_issues": [],
  "dx_issues_discovered": [],
  "lessons_learned": [],
  "last_updated": "YYYY-MM-DDTHH:MM:SSZ"
}
```

### Phases/Tasks-Based (Legacy)
```json
{
  "sprint_id": "<sprint-id>",
  "name": "Sprint Name",
  "status": "in_progress",
  "type": "ailang",
  "started": "YYYY-MM-DD",
  "design_doc": "design_docs/planned/next/<feature>.md",
  "phases": [
    {
      "id": "phase1",
      "name": "Phase Name",
      "status": "in_progress",
      "tasks": [
        {"id": "1.1", "name": "Task Name", "status": "pending", "notes": ""}
      ]
    }
  ],
  "ailang_issues": [],
  "dx_issues_discovered": [],
  "lessons_learned": [],
  "notes": []
}
```

**AILANG sprints MUST include these sections** (added to standard format):
- `ailang_issues` - Bugs/features reported to AILANG team
- `dx_issues_discovered` - DX friction discovered during sprint
- `lessons_learned` - What to do differently next time

**Update this JSON:**
- Mark milestones as `completed` immediately after finishing
- Add notes with workarounds used
- Document ALL DX issues as you discover them
- Add lessons learned in real-time, not at sprint end

## Pre-Sprint DX Checklist

Before writing any code, verify these items:

### File Boundaries
- [ ] **sim_gen/*.go is GENERATED** - Never edit (OK to have game types - they come from AILANG)
- [ ] **engine/*.go is GENERIC** - Must work for ANY AILANG game (no deck names, planet names, crew roles)
- [ ] **game_views/*.go for game-specific** - Stapledon-specific rendering helpers go here
- [ ] **sim/*.ail is source** - Primary edit location for all game logic

### Engine Genericization Check
- [ ] **Before adding to engine/**, ask: Could a different game use this unchanged?
- [ ] **If NO** → Put in `game_views/` instead
- [ ] **sim_gen types OK in engine**: DrawCmd*, FrameInput, FrameOutput, Camera, Coord
- [ ] **sim_gen types NOT OK in engine**: World, DeckType, Planet, NPC, ArrivalState, DomeViewState

### For Visual Features
- [ ] **Screenshot testing ready** - Can run `go run ./cmd/game -screenshot N -output /tmp/test.png`
- [ ] **Test at multiple frames** - Don't declare rendering complete until tested
- [ ] **Use real assets from start** - No placeholder rectangles

### For Downloaded Assets
- [ ] **Verify with `file` command** - Catch HTML error pages masquerading as images
- [ ] **Check URLs still work** - NASA/external URLs may return 404

### DrawCmd Limitations
- [ ] **Color is INDEX not RGBA** - Use biomeColors[] indices or RectRGBA/CircleRGBA for custom colors
- [ ] **Renderer is isometric** - Use direct drawing for screen-space elements
- [ ] **Use RectRGBA/CircleRGBA for screen-space** - These bypass camera transforms and use packed 0xRRGGBBAA colors

### Screen Resolution
- [ ] **NEVER hardcode 640x480 or other fixed sizes** - Use `display.InternalWidth` and `display.InternalHeight`
- [ ] **Internal resolution is 1280x960** - All screen-space coordinates should be relative to this
- [ ] **Use percentages for positioning** - e.g., `screenW * 0.5` for center, not fixed `320`

### Physics/Shader Effects
- [ ] **Use artistic license on values** - Physically accurate may not be visually playable
- [ ] **Test SR blueshift >0.5c** - May wash out all content
- [ ] **Test GR at high intensity** - May render pure black

### Build & Test
- [ ] **Always use `make build`** - Detects sim_gen errors and enforces correct bug reporting
- [ ] **Use `make game` for executable** - Builds bin/game
- [ ] **Use `go run` for quick testing** - Compiles fresh each time
- [ ] **NEVER use direct `go build ./...`** - Won't detect AILANG codegen bugs
- [ ] **Run `voyage manifest`** - Validate all assets exist before starting

## CRITICAL: AILANG-First Architecture

**This project is ALL-IN on AILANG.** The architecture is:

| Layer | Language | Responsibility | Edit? |
|-------|----------|----------------|-------|
| `sim/*.ail` | AILANG | ALL game logic | ✅ Primary work |
| `sim_gen/*.go` | Generated | AILANG → Go output (OK to have game types) | ❌ Never edit |
| `game_views/*.go` | Go | Game-specific rendering helpers | ✅ For Stapledon-specific visuals |
| `engine/*.go` | Go | Generic rendering (reusable for ANY game) | ⚠️ Must be game-agnostic |

**If you're writing game logic in Go, STOP. Write it in AILANG.**

Mock-only mode was for early prototyping. We are past that phase.

### ⚠️ Engine Genericization Rule (IMPORTANT)

**The engine should work unchanged for a completely different AILANG game.**

Before writing Go code, ask: **Could a different game use this unchanged?**

| Answer | Where to Put It |
|--------|-----------------|
| YES - generic rendering | `engine/*.go` |
| NO - game-specific visual | `game_views/*.go` |
| NO - game logic/data | `sim/*.ail` (AILANG) |

**sim_gen/ is fine** - It's generated from AILANG. Game-specific types (World, DeckType, Planet) belong there because they come from AILANG.

**engine/ must be generic:**
- ✅ DrawCmd rendering (Sprite, Rect, Text, Circle, etc.)
- ✅ Asset loading (sprites, audio, fonts)
- ✅ Camera transforms, shaders, display
- ❌ Deck names (Core, Engineering, Bridge)
- ❌ Planet names (Saturn, Earth, Jupiter)
- ❌ Crew roles (pilot, comms, scientist)
- ❌ Game-specific state types (DomeViewState, ArrivalState)

**game_views/ for game-specific rendering:**
- DomeRenderer (solar system visualization)
- DeckStackRenderer (5-deck ship structure)
- DeckPreview (deck colors and names)
- Any code that references sim_gen game types beyond DrawCmd

**Example Violation (DO NOT DO):**
```go
// ❌ WRONG - in engine/render/draw.go
func getBridgeSpriteColor(id int64) color.RGBA {
    case id == 1200: return ... // pilot
    case id == 1201: return ... // comms  <- GAME CONCEPTS IN ENGINE!
}

// ✅ RIGHT - move to game_views/sprite_colors.go
// Or better: define colors in AILANG and pass via DrawCmd
```

## Quick Start

**Most common usage:**
```bash
# User says: "Execute the arrival sequence sprint"
# This skill will:
# 1. Check AILANG modules compile
# 2. Write new AILANG types and functions
# 3. Run ailang check after every change
# 4. Report AILANG issues immediately
# 5. Compile to Go and test in engine
```

## When to Use This Skill

Invoke this skill when:
- User says "execute sprint", "start sprint", "begin implementation"
- User has an approved sprint plan ready
- Implementing ANY game feature (it MUST be AILANG)

**Do NOT use this skill for:**
- Pure engine rendering changes (use dev-tools or direct edits)
- Asset pipeline work (use asset-manager skill)

## Core Principles

1. **AILANG-First**: ALL game logic in `sim/*.ail` - no exceptions
2. **Test-Driven**: Run `ailang check` after every change
3. **Feedback-First**: Report AILANG issues immediately
4. **Track Progress**: Use TodoWrite AND update sprint JSON
5. **Document Workarounds**: Record how you navigated limitations
6. **Physics Accuracy First**: Use exact formulas, document any approximations
7. **No Wrapper Files**: NEVER create Go wrapper files to work around AILANG codegen issues - report the bug and wait for a fix

## JSON Progress Tracking (IMPORTANT)

**Always update the sprint JSON file as you work.** This enables session continuity.

Sprint JSON files can use either **features-based** (preferred for new sprints) or **phases/tasks-based** (legacy) structure.

### Commands

```bash
# Location: sprints/sprint_<sprint-id>.json

# For feature-based sprints (preferred):
.claude/skills/sprint-executor/scripts/update_progress.sh \
  sprints/sprint_<sprint-id>.json feature <feature_id> in_progress

.claude/skills/sprint-executor/scripts/update_progress.sh \
  sprints/sprint_<sprint-id>.json feature <feature_id> completed [actual_loc]

# For phase/task-based sprints (legacy):
.claude/skills/sprint-executor/scripts/update_progress.sh \
  sprints/<sprint-id>.json task <task_id> completed

.claude/skills/sprint-executor/scripts/update_progress.sh \
  sprints/<sprint-id>.json phase <phase_id> completed

# Update overall sprint status (both formats):
.claude/skills/sprint-executor/scripts/update_progress.sh \
  <sprint-file>.json sprint in_progress

# Show current progress (auto-detects format):
.claude/skills/sprint-executor/scripts/update_progress.sh \
  <sprint-file>.json show
```

### Feature Command (for features-based sprints)

| Command | Effect |
|---------|--------|
| `feature <id> in_progress` | Sets `started` timestamp |
| `feature <id> completed` | Sets `completed` timestamp, `passes: true` |
| `feature <id> completed <loc>` | Also sets `actual_loc` |
| `feature <id> blocked` | Sets `passes: false` |
| `feature <id> pending` | Resets to initial state |

**Status values:** `pending` | `in_progress` | `completed` | `blocked`

### When to Update JSON
- Mark sprint as `in_progress` when starting
- Mark each feature/task `in_progress` before starting work
- Mark each feature/task `completed` immediately after finishing
- Mark sprint `completed` at the end

## Engine-Only Changes (Rare)

Most work should be AILANG. Engine changes are only needed for:
- Adding new DrawCmd rendering (e.g., new DrawCmd variant)
- Shader modifications (generic visual effects)
- Asset loading (generic loaders)

**STOP - Is this game-specific?**
- Game-specific rendering → `game_views/*.go`
- Generic rendering → `engine/*.go`

For engine-only work:
```bash
make engine       # Build engine only (skips sim_gen check)
make run          # Test rendering
```

**Remember:** Engine code should be "dumb" - it only renders what AILANG tells it via DrawCmd. It should work unchanged for ANY AILANG game.

## Game-Specific Views (game_views/)

For rendering helpers that reference game concepts:
- DomeRenderer, DeckStackRenderer, DeckPreview
- Any code using sim_gen types beyond DrawCmd/FrameInput/FrameOutput
- Code that knows about decks, planets, crew, etc.

```bash
# game_views imports both engine/ and sim_gen/
# engine/ should NOT import game_views/
```

## Execution Flow

### Phase 1: Initialize Sprint

1. **Check Status**
   ```bash
   # For AILANG sprints:
   for f in sim/*.ail; do ailang check "$f"; done
   ailang messages list --unread

   # For mock-only sprints:
   go test ./...
   make game-mock
   ```

2. **Initialize JSON Progress**
   ```bash
   .claude/skills/sprint-executor/scripts/update_progress.sh \
     sprints/<sprint-id>.json sprint in_progress
   ```

3. **Create Todo List**
   - Use TodoWrite for all milestones
   - Mark first milestone as in_progress

### Phase 2: Execute Milestones

**For each milestone:**

1. **Pre-Implementation**
   - Mark milestone as in_progress in TodoWrite
   - Re-read `ailang prompt` for syntax reference

2. **Implement AILANG Code**
   ```bash
   # After each file edit:
   ailang check sim/<file>.ail

   # If errors, fix immediately
   # If stuck, report to AILANG team
   ```

3. **Test with ailang run**
   ```bash
   # Test entry function
   ailang run --entry <function> sim/step.ail
   ```

4. **Report Issues Encountered**
   ```bash
   # For bugs
   ~/.claude/skills/ailang-feedback/scripts/send_feedback.sh bug \
     "Issue title" "Description" --from stapledons_voyage

   # For missing features
   ~/.claude/skills/ailang-feedback/scripts/send_feedback.sh feature \
     "Feature needed" "Why it would help" --from stapledons_voyage
   ```

5. **Update Progress (IMPORTANT)**
   ```bash
   # After each task
   .claude/skills/sprint-executor/scripts/update_progress.sh \
     sprints/<sprint-id>.json task <task_id> completed

   # After completing all tasks in a phase
   .claude/skills/sprint-executor/scripts/update_progress.sh \
     sprints/<sprint-id>.json phase <phase_id> completed
   ```
   - Note workarounds used
   - Update CLAUDE.md if new limitations found

6. **Pause for Review**
   - Show progress: `.../update_progress.sh sprints/<id>.json show`
   - Ask if ready to continue

### Phase 3: Engine Integration (if needed)

1. **Compile AILANG to Go**
   ```bash
   make sim   # Generates sim_gen/*.go
   ```

2. **Check Codegen Quality (MANDATORY)**
   ```bash
   # Run quality check on generated Go code
   .claude/skills/sprint-executor/scripts/check_codegen_quality.sh
   ```

   **What it checks:**
   - Excessive nesting (>20 chars indentation)
   - Too many closure wrappers (>10 consecutive)
   - Patterns that indicate AILANG codegen issues

   **If issues found:**
   - Report to AILANG via `ailang messages send user "..." --type bug --github`
   - Consider refactoring AILANG source to reduce nesting (helper functions)
   - Document workarounds in sprint JSON

3. **Test Game**
   ```bash
   make run   # Run with Ebiten
   ```

4. **Fix Integration Issues**
   - Check generated Go code
   - Update engine/ if needed

### Phase 4: Finalize Sprint

1. **Final Testing**
   ```bash
   # All AILANG modules
   for f in sim/*.ail; do ailang check "$f"; done

   # Game build
   make game
   ```

2. **AILANG Feedback Summary**
   - List all issues reported during sprint
   - Note any responses received

3. **Developer Experience (DX) Report** (AILANG sprints only)

   **Skip this for mock-only sprints** - the `ailang-feedback` skill is for AILANG language feedback, not general sprint completion.

   For sprints that involve AILANG code, send a DX feedback message reflecting on the overall experience:

   ```bash
   ~/.claude/skills/ailang-feedback/scripts/send_feedback.sh dx \
     "Sprint DX: <sprint-name>" \
     "<honest reflection on working with AILANG this sprint>" \
     --from stapledons_voyage
   ```

   **Include in your reflection:**
   - **Positives**: What worked well? What felt natural?
   - **Friction points**: Where did you get stuck? What was confusing?
   - **Productivity**: Could you express your intent easily?
   - **Error messages**: Were they helpful or cryptic?
   - **Documentation**: Did `ailang prompt` have what you needed?
   - **Overall sentiment**: Would you want to use AILANG again?

   **Be honest** - negative feedback is valuable. Examples:
   - "Pattern matching felt natural and expressive"
   - "Nested field access errors were frustrating to debug"
   - "The functional style made NPC updates clean"
   - "Had to fight the type system on record updates"

4. **Sprint Report**
   - Milestones completed
   - AILANG issues encountered (if any)
   - Workarounds used (if any)
   - DX rating (1-5 stars) - for AILANG sprints only

## Error Handling

### CRITICAL: Use `make build` - It Enforces Correct Behavior

**Always use `make build` instead of `go build`!**

`make build` automatically:
1. Detects if errors are in `sim_gen/` (AILANG codegen bug)
2. Prints instructions for reporting the bug
3. Prevents workaround attempts

```bash
# CORRECT - use this
make build

# WRONG - don't use direct go build
go build ./...   # Won't detect codegen bugs
```

**If `make build` shows "ERROR IN sim_gen/":**
1. Follow the printed instructions to report the bug
2. Mark the feature as BLOCKED in sprint tracking
3. STOP and wait for fix
4. DO NOT refactor AILANG to work around it
5. DO NOT edit sim_gen files

**If `make build` shows a normal error (not in sim_gen/):**
- Fix it in engine/*.go or cmd/*.go as usual

### AILANG Compilation Fails
1. Show error output
2. Check `ailang prompt` for correct syntax
3. If unclear error, report to AILANG team
4. Don't proceed until `ailang check` passes

### Recursion Depth Exceeded
1. Reduce data size for testing
2. Consider iterative workaround (if possible)
3. Report as feature request (tail recursion optimization)

### Module Import Fails
1. Duplicate type definitions locally
2. Document the duplication
3. Report import issue to AILANG team

### Feature Not Available
1. Design workaround
2. Document the workaround
3. Report as feature request

## Common AILANG Workarounds

Quick reference for known issues and their solutions:

| Problem | Error Message | Workaround |
|---------|---------------|------------|
| Nested field access | "cannot unify open record with TVar2" | Break `a.b.c` into `let b = a.b; b.c` |
| Record update with derived value | "cannot unify open record" on `{b \| pos: newPos}` | Use explicit construction: `{ field1: b.field1, pos: newPos }` |
| Module-level `let` in function | "undefined variable" | Inline constant or pass as parameter (intentional design) |
| Tuple destructuring | Parse error on `let (x, y) = pair` | Use `match pair { (x, y) => ... }` |
| ADT in inline tests | Test harness crashes | Only use primitive types in test inputs |
| DrawCmd uses color index not RGBA | N/A (works but limited) | Use direct Ebiten drawing in engine/ for custom colors. Feature requested from AILANG. |
| Go codegen wrong return types | Exported func returns `struct{}` but impl returns typed value | **DO NOT create wrapper files** - report bug via ailang-feedback and wait for fix |
| Go codegen unexported converters | `convertToDrawCmdSlice` is lowercase | **DO NOT create wrapper files** - report bug via ailang-feedback and wait for fix |
| **Editing sim_gen/*.go** | Changes overwritten | **NEVER edit sim_gen files**. Request features via ailang-feedback. |

### Maintaining This List (IMPORTANT)

**This project's purpose is to surface and fix AILANG issues.** Keep this workarounds table current:

**Scripts for tracking workarounds:**

```bash
# Check inbox and verify workarounds still needed
.claude/skills/sprint-executor/scripts/check_workarounds.sh

# Add a new workaround (updates both SKILL.md and CLAUDE.md)
.claude/skills/sprint-executor/scripts/add_workaround.sh \
  "Problem name" "Error message" "Workaround description"

# Mark an issue as fixed (moves to Fixed section)
.claude/skills/sprint-executor/scripts/mark_fixed.sh \
  "problem keyword" "v0.5.0"
```

**When you discover a new issue:**
1. Run `add_workaround.sh` with problem, error, and workaround
2. Report via `ailang-feedback` with detailed repro steps

**When AILANG fixes an issue:**
1. Check inbox: `ailang messages list --unread`
2. Verify fix: `ailang check sim/*.ail`
3. Run `mark_fixed.sh "<keyword>" "<version>"`
4. Remove workarounds from code where practical
5. Acknowledge: `ailang messages ack <msg-id>`

**At sprint start:**
```bash
# Full status check
.claude/skills/sprint-executor/scripts/check_workarounds.sh
```

### Record Update Pattern

When updating nested records, this pattern works:
```ailang
-- WORKS: newPos comes from parameter or fresh construction
pure func moveBox(b: Box, newPos: Point) -> Box {
    {b | pos: newPos}
}

-- FAILS: newPos derived from b.pos
pure func moveBoxBad(b: Box) -> Box {
    let oldPos = b.pos;
    let newPos = { x: oldPos.x + 1, y: oldPos.y };
    {b | pos: newPos}  -- ERROR!
}

-- WORKAROUND: explicit construction
pure func moveBoxFixed(b: Box) -> Box {
    let oldPos = b.pos;
    let newPos = { x: oldPos.x + 1, y: oldPos.y };
    { pos: newPos, size: b.size }  -- Explicit fields
}
```

## Quality Checkpoints

After each milestone:

```bash
# 1. All AILANG modules compile
for f in sim/*.ail; do ailang check "$f"; done

# 2. Entry functions run
ailang run --entry init_world sim/step.ail

# 3. Game builds (if engine changes)
make game
```

## Visual Verification (MANDATORY for Visual Features)

**For any milestone involving visual output, YOU MUST take and verify screenshots.**

### CRITICAL: Use In-Game Screenshots, NOT macOS screencapture

**NEVER use macOS `screencapture` command** - it captures the entire desktop at native resolution (5K+ on Retina), producing huge files that crash Claude.

**ALWAYS use the in-game screenshot functionality** - it captures the game's internal render buffer at 1280x960, producing consistent, small PNG files.

### Screenshot Helper Script (Recommended)

Use the dedicated screenshot helper for easy, reliable screenshots:

```bash
# Basic game screenshot at frame 30
.claude/skills/sprint-executor/scripts/take_screenshot.sh

# Bridge demo at frame 60
.claude/skills/sprint-executor/scripts/take_screenshot.sh -c demo-game-bridge -f 60

# Game with effects
.claude/skills/sprint-executor/scripts/take_screenshot.sh --effects bloom,sr_warp --velocity 0.5

# Arrival sequence at frame 120
.claude/skills/sprint-executor/scripts/take_screenshot.sh --arrival -f 120

# Custom output path
.claude/skills/sprint-executor/scripts/take_screenshot.sh -o out/screenshots/my-test.png
```

### Direct Command Usage

You can also use the screenshot flags directly on any game command:

```bash
# Main game
go run ./cmd/game --screenshot 30 --output out/screenshots/game.png

# Demo commands
go run ./cmd/demo-game-bridge --screenshot 30 --output out/screenshots/bridge.png
go run ./cmd/demo-saturn --screenshot 60 --output out/screenshots/saturn.png

# With effects
go run ./cmd/game --screenshot 60 --output out/test.png --effects bloom,sr_warp --velocity 0.5

# Arrival sequence
go run ./cmd/game --screenshot 120 --output out/arrival.png --arrival
```

### Why In-Game Screenshots?

| Method | Resolution | File Size | Works? |
|--------|------------|-----------|--------|
| `--screenshot` flag | 1280x960 | ~50-200KB | YES |
| macOS `screencapture` | 5120x2880+ | 5-20MB | NO (crashes) |

### Screenshot Workflow

1. **Take Screenshots at Key States**
   ```bash
   # Initial state
   .claude/skills/sprint-executor/scripts/take_screenshot.sh -f 30 -o out/screenshots/initial.png

   # Mid-animation (if applicable)
   .claude/skills/sprint-executor/scripts/take_screenshot.sh -f 60 -o out/screenshots/mid.png

   # Final state
   .claude/skills/sprint-executor/scripts/take_screenshot.sh -f 90 -o out/screenshots/final.png
   ```

2. **View Screenshots Using Read Tool**
   ```bash
   # Claude Code can view PNG images directly
   # Use Read tool on screenshot path to verify visuals
   ```

3. **Document What to Look For**
   - Visual elements positioned correctly
   - No rendering artifacts
   - Effects applied properly (if enabled)
   - UI elements visible and readable

### Screenshot Verification Checklist

For each visual feature:
- [ ] Screenshot captured at initial state
- [ ] Screenshot captured during any animations/transitions
- [ ] Screenshot captured at final state
- [ ] Screenshots viewed and verified correct
- [ ] Issues found documented in sprint JSON
- [ ] Visual artifacts investigated and fixed

### Available Commands for Screenshots

| Command | Description |
|---------|-------------|
| `game` | Main game (bridge view, NPC, etc.) |
| `demo-game-bridge` | Bridge interior only |
| `demo-saturn` | Saturn with rings |
| `demo-arrival` | Black hole arrival sequence |
| `demo-sr-flyby` | SR effects flyby demo |
| `demo-view` | View system demo |

## Output File Organization (MANDATORY)

**All generated output MUST go in the correct `out/` subdirectory.** See [out/README.md](../../../out/README.md) for full details.

### Directory Structure

```
out/
├── eval/           # Benchmarks, evaluation reports
├── generated/      # Final GIFs, videos, animations
├── scenarios/      # Scenario runner temp output
├── screenshots/    # Demo screenshots from sprints  ← USE THIS
└── test/           # Visual test golden files
```

### Where to Put Files

| Output Type | Location | Example |
|-------------|----------|---------|
| Demo screenshots | `out/screenshots/` | `out/screenshots/bridge-initial.png` |
| Sprint verification | `out/screenshots/<sprint>/` | `out/screenshots/arrival-v1/mid-transition.png` |
| Evaluation output | `out/eval/` | `out/eval/report.json` |
| Generated videos/GIFs | `out/generated/` | `out/generated/flyby-demo.gif` |
| Test scenario output | `out/test/<scenario>/` | `out/test/camera-pan/after-right.png` |

### Rules

1. **NEVER put files in `out/` root** - always use a subdirectory
2. **Clean up intermediate files** - frame sequences for video generation should be deleted after the final video is created
3. **Use descriptive names** - `bridge-initial.png` not `test1.png`
4. **Organize by sprint** - for multi-screenshot verification, use `out/screenshots/<sprint-name>/`

### Screenshot Commands

```bash
# Single screenshot
./bin/demo --screenshot 30 --output out/screenshots/initial.png

# Sprint with multiple screenshots
mkdir -p out/screenshots/arrival-v1
./bin/demo --screenshot 30 --output out/screenshots/arrival-v1/initial.png
./bin/demo --screenshot 60 --output out/screenshots/arrival-v1/mid.png
./bin/demo --screenshot 90 --output out/screenshots/arrival-v1/final.png
```

### Video/Animation Generation

```bash
# Generate frames to temp directory
mkdir -p /tmp/frames
./bin/demo --capture-frames /tmp/frames/

# Create final video
ffmpeg -i /tmp/frames/frame_%05d.png out/generated/demo.mp4

# Clean up intermediate frames
rm -rf /tmp/frames
```

**Do NOT leave frame directories in `out/`** - they can grow to hundreds of MB.

### Cleanup Command

If `out/` gets cluttered during development:
```bash
make clean  # Removes bin/, out/* but preserves structure
```

## Resources

### Engine & Physics Reference

**IMPORTANT:** Before implementing features, review these reference documents:

| Document | Contents | When to Use |
|----------|----------|-------------|
| [engine-capabilities.md](../../../design_docs/reference/engine-capabilities.md) | All DrawCmd types, effect handlers, assets, shaders, physics | Any sprint involving rendering or engine features |
| [game-capabilities.md](../../../design_docs/reference/game-capabilities.md) | AILANG game features (celestial, starmap, bridge, viewport) | Any sprint involving game logic in sim/*.ail |
| [ai-capabilities.md](../../../design_docs/reference/ai-capabilities.md) | AI text/image/TTS, 30 voices, SSML, style control | NPC dialogue, voice generation, AI-driven content |
| [demos.md](../../../design_docs/reference/demos.md) | Demo index (demo-engine-*, demo-game-*) | Creating or running feature demos |
| [gr-effects.md](../../../design_docs/implemented/v0_1_0/gr-effects.md) | GR physics formulas, shader uniforms, danger levels | Black hole/neutron star features |
| [ai-handler-system.md](../../../design_docs/implemented/v0_1_0/ai-handler-system.md) | AI effect, multimodal APIs, provider config | NPC dialogue, AI-driven decisions |

**Key Engine Capabilities:**

| Category | What's Available |
|----------|------------------|
| **DrawCmd** | Sprite, Rect, Text, IsoTile, IsoEntity, GalaxyBg, Star, Ui, Line, Circle, TextWrapped |
| **Effects** | Debug, Rand, Clock, AI (with Claude/Gemini/stub backends) |
| **Assets** | Sprites (animated), Audio (OGG/WAV), Fonts (TTF with scaling) |
| **Shaders** | SR warp (Doppler, aberration), GR warp (lensing, redshift), bloom, vignette, CRT |
| **Physics** | Lorentz factor, time dilation, gravitational redshift, Schwarzschild radius |

### Project Commands
- `make sim` - Compile AILANG to Go
- `make game` - Build game executable
- `make run` - Run game
- `make install` - Install voyage CLI globally

### Voyage CLI (Dev Tools)

The `voyage` CLI provides development tools. Install with `make install`.

```bash
# API documentation (always up-to-date via AST parsing)
voyage api                      # List all engine packages
voyage api tetra                # List types in package
voyage api tetra.Scene          # Show type details
voyage api tetra.Scene --methods # Show with method signatures
voyage api --search camera      # Search across all packages

# Demo runner (use instead of manual go run)
voyage demo              # Interactive selection menu
voyage demo bridge       # Run demo-game-bridge directly
voyage demo orbital      # Partial name matching works

# File watcher (auto-rebuild on changes)
voyage watch             # Watch sim/*.ail, run make sim on changes
voyage watch --test      # Also run ailang test after rebuild
voyage watch --run bridge # Rebuild and restart demo automatically

# Screenshot capture (use for visual verification)
voyage screenshot        # Capture main game (frame 60)
voyage screenshot bridge # Capture specific demo
voyage screenshot --all  # Capture all demos to out/screenshots/
voyage screenshot bridge -f 120 -o out/ # Custom frames/output

# Asset validation (run before sprints)
voyage manifest          # Validate all asset manifests exist
voyage manifest -v       # Verbose (show all files)
voyage manifest sprites  # Check specific manifest

# Other inspection tools
voyage world             # Inspect world state
voyage bench             # Run benchmarks
voyage ai                # Test AI handlers
```

**Use `voyage` commands for:**
- Engine API lookup (find correct signatures, constructors, methods)
- Quick demo switching during development
- Auto-rebuild while editing AILANG
- Screenshot capture for visual verification
- Asset validation before commits

### AILANG Commands
- `ailang check <file>` - Type-check
- `ailang run --entry <func> <file>` - Run with entry point
- `ailang prompt` - Syntax reference

### Feedback Commands
- `ailang messages list --unread` - Check unread messages
- `ailang messages ack <msg-id>` - Acknowledge message
- `ailang messages send <inbox> <msg>` - Send message
- `~/.claude/skills/ailang-feedback/scripts/send_feedback.sh` - Report issues

## Milestone Checklist Template

```markdown
## Milestone: [Name]

### Implementation
- [ ] AILANG types defined
- [ ] AILANG functions implemented
- [ ] `ailang check` passes
- [ ] `ailang run` works

### Testing
- [ ] Edge cases handled
- [ ] Error conditions covered

### Visual Verification (if visual feature)
- [ ] Screenshot captured at initial state
- [ ] Screenshot captured during animations/transitions
- [ ] Screenshot captured at final state
- [ ] Screenshots viewed and verified correct
- [ ] Visual issues fixed

### Feedback
- [ ] Issues reported: [list]
- [ ] Workarounds documented: [list]

### Status
- [ ] Complete and ready for next milestone
```

## Notes

- Every `ailang check` failure is a learning opportunity
- Report issues early, don't wait until sprint end
- Check inbox for AILANG team responses
- This project's purpose is testing AILANG, not just building a game
- Document everything - it helps AILANG improve
