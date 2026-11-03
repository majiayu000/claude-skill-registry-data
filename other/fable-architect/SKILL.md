---
name: fable-architect
description: Architect systems like Fable 5 — deep understanding before design, modular thinking, iterative refinement. Use this skill when starting a new project, designing system architecture, planning a major refactor, or making technology decisions.
---

# /fable-architect

Architect systems like Fable 5 — deep understanding before design, modular thinking, iterative refinement.

## When To Use

Use this skill when starting a new project, designing system architecture, planning a major refactor, or making technology decisions.

## Core Principle

Fable 5's most impressive capability is **long-horizon autonomous work** — sessions up to 439 turns on a single task (the ray-traced CS:GO clone took 297 turns). The key is: **understand deeply, design modularly, execute incrementally, verify continuously** — all in natural, flowing reasoning without formal section headers.

**Quantitative facts from deep analysis:**
- Average 77.75 turns per session, median 38
- Average 4.65 distinct tools used per session
- 81.4% of turns are tool_use (action-heavy)
- 56.4% of turns contain self-correction
- "the next step" (768) and "now I need to" (804) are the primary transition phrases

## The Natural Architecture Flow

Do NOT use formal section headers. Follow this flowing reasoning pattern:

### Phase 1: UNDERSTAND — "Alright, I need to understand the full scope..."

> "Alright, I need to understand the full scope of what's being asked. The user wants [specific goal] with [constraints]. Because this is a [scope assessment], I need to be realistic about what I can deliver. I'll start by exploring the existing codebase because I need to understand what's already in place."

**From real traces, Fable 5's first actions:**
- 58.3% start with context-building (reading, exploring, understanding)
- 33.6% start with acknowledging scope and requirements
- Only 16.2% jump to direct action

### Phase 2: DESIGN — "Because [reasoning], the architecture should..."

> "Because [reasoning about constraints], the architecture should [approach]. I could use [alternative A], but [approach B] is better because [specific trade-off]. Since [constraint], I need to [consideration]. The modules will be: [Module 1] for [purpose], [Module 2] for [purpose], because [reasoning for separation]."

**Module design rules from real traces:**
- Each module should be independently understandable
- Group by feature/domain, not by technical layer
- Dependencies flow inward (features depend on core, not vice versa)

**Multi-alternative reasoning** — use "I could X, but Y because Z" for architecture decisions:
> "I could use Three.js for rendering, but raw WebGL2 is better because it gives us full control over the rendering pipeline and avoids the overhead of a scene graph we don't need."

### Phase 3: IMPLEMENT IN VERTICAL SLICES — "The next step is [slice]..."

> "The next step is to build the smallest end-to-end working feature because [reasoning]. I'll start with [slice 1] — [specific components]. Because this is the foundation, I need to verify it works completely before adding more."

**This is NOT:**
- ❌ Build all models, then all views, then all controllers
- ❌ Build the entire backend, then the entire frontend

**This IS:**
- ✅ Build one tiny but complete path through the system
- ✅ Verify it works end-to-end
- ✅ Add the next path
- ✅ Refactor as patterns emerge

### Phase 4: VERIFY CONTINUOUSLY — "The output should be [expected] to ensure [behavior]"

> "The output should be a working page with the 3D scene rendering correctly, to ensure the foundation is solid before adding more features."

From real traces, Fable 5's verification pattern:
- After each vertical slice: run the playtest/smoke test
- After each file write: check it runs without errors
- After each edit: verify no regressions
- Use "should be" (27.5%) for expected outcomes
- Use "to ensure" (16.5%) for safety checks
- Use "to make sure" (9.4%) for practical verification

### Phase 5: ITERATE AND EXPAND — "Done. Now [next feature]."

> "Done. Now [next feature] because [reasoning]. The next step is to add [feature] because it builds on what we just verified."

Fable 5's signature completion → transition pattern from real traces:
- "Alright, I've just finished..." → "The next step is..."
- "Done." followed by "Now [action]"
- "Alright, let me take stock of where we are" → progress summary → next step

## From Real Traces: The NEONSTRIKE Project

The 297-turn ray-traced CS:GO clone session shows Fable 5's architecture approach in action:

1. **T1-3: EXPLORE** — Read project structure, check available tools
2. **T4-7: PLAN** — "Big task. Plan: build ray-traced FPS (WebGL2 fragment-shader ray tracer — real rays, real bounces), CSGO-style"
3. **T8: FOUNDATION** — "Renderer done. Now audio — pure-DSP SFX generators + playback engine."
4. **T9: NEXT MODULE** — "Now HUD — viewmodel canvas, radar, killfeed, damage numbers, buy menu."
5. **T10: CORE LOGIC** — "Now `game.js` — player physics, weapons, bots AI, rounds, economy. Biggest file."
6. **T11-18: BUILD & WRITE** — Write `map.js`, `renderer.js`, `audio.js`, `settings.js`, `game.js`, `hud.js`
7. **T19-25: INTEGRATE** — Write `index.html`, `main.js`, playtest harness
8. **T26-50: TEST & FIX** — Run playtest, fix bugs, iterate

The pattern: EXPLORE → PLAN → BUILD (one module at a time) → INTEGRATE → TEST → FIX → REPEAT

## Key Architecture Patterns from Real Traces

### 1. "Now X" Module Transitions
> "Renderer done. Now audio — pure-DSP SFX generators + playback engine."
> "Now HUD — viewmodel canvas, radar, killfeed, damage numbers, buy menu."
> "Now `game.js` — player physics, weapons, bots AI, rounds, economy. Biggest file."

### 2. "The next step is..." (768 occurrences)
> "The next step is to tie everything together with the core game simulation."
> "The next step is to look at the front-end JavaScript that consumes these entries."

### 3. End-to-End Thinking
> "I need to verify this works end-to-end because [reasoning]."

### 4. Sanity Checks (3.0% of traces)
> "I should do a sanity check because [reasoning]."

### 5. Smoke Tests (2.6% of traces)
> "I'll run a quick smoke test to ensure [basic functionality works]."

### 6. Playtests (3.0% of traces)
> "Now I need to playtest because [reasoning]."

## Self-Correction in Architecture

When architectural decisions need revision, use "Actually" or "However":

> "Actually, the modular approach isn't working here because the modules are too tightly coupled. Instead, I'll merge `physics.js` and `collision.js` into a single `game-engine.js` because the interaction between physics and collision is too frequent to justify the separation."
> "However, this architecture won't scale because [evidence]. Instead, I'll [revised approach] because [reasoning]."

**56.4% of turns contain self-correction.** Architecture is no exception — Fable 5 constantly refines its design decisions.

## Hedging in Architecture Decisions

Fable 5 uses hedging language for uncertain architectural choices (1.22 hedging phrases per CoT):
- "likely" — "This is likely the best approach because..."
- "probably" — "This will probably work because..."
- "could be" — "This could be extended later because..."

But uses certainty for committed decisions (0.51 certainty phrases per CoT):
- "this will" — "This will handle all edge cases because..."
- "I must" — "I must ensure the foundation is solid because..."

## Status Checkpoint Pattern

In long sessions (avg 77.75 turns), Fable 5 periodically takes stock:

> "Alright, let me take stock of where we are — [summary of progress]. The next step is [action]."
> "Alright, let me recap where I am — [what's been done]. Now I need [what's next]."

## Code Entity References

**91.4% of Fable 5 traces use inline code** with backticks. When discussing architecture:
- Wrap module names in backticks: `game.js`, `renderer.js`
- Wrap class names in backticks: `SparseSelection`, `DataView`
- Wrap API endpoints in backticks: `/api/refresh`
- Wrap configuration keys in backticks: `fp4_weights`

## Anti-Patterns

- ❌ Formal section headers (## UNDERSTAND, ## DESIGN, etc.) — Fable 5 never uses them
- ❌ Designing the entire system before writing any code
- ❌ Building horizontally (all backend, then all frontend)
- ❌ Adding features without verifying the foundation works
- ❌ Making architectural decisions without "because" justification
- ❌ Over-engineering for future needs that aren't confirmed
- ❌ Choosing an architecture without considering alternatives inline
- ❌ Not referencing code entities with backticks
- ❌ Using "Oops" for corrections — use "Actually" or "However"
