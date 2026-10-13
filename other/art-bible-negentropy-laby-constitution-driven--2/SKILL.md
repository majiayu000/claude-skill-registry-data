---
name: art-bible
description: "Guided, section-by-section visual identity authoring. Game: Art Bible for asset production. Product: brand style guide for docs imagery, public visuals, and product-facing visual standards."
argument-hint: "[--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
---

## User Guide

- When to use: Guided, section-by-section visual identity authoring. Game: Art Bible for asset production. Product: brand style guide for docs imagery, public visuals, and product-facing visual standards.
- Inputs: Command arguments: `/art-bible [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Read `standards/technical-preferences.md`, existing scoped domain decisions,
and the substantive bodies of any `design/cdd/game-concept.md` and
`design/cdd/product-concept.md` before selecting a branch. Filenames, placeholder
or copied concept text and shared extensions do not establish a domain. Read
actual configured values in `Product Stack` or the populated legacy
`Language & Framework`, `Platform & Deployment`, and `Agent Routing` /
`File Extension Routing`
sections in their owning domain context; missing new sections or a concept do
not erase configured legacy Product facts. A placeholder Game concept does not
override a configured Product.

Resolve Game from consistent substantive Game concept/decision or actual
configured engine/domain and Game behavior evidence; resolve Product from
consistent substantive Product concept/decision or actual Product configuration.
Two substantive concepts, conflicting concept/configuration values or mixed scope
leave the affected branch **Unknown** until a scoped decision resolves the conflict.
With no consistent substantive concept/scoped decision or sufficient actual
configuration evidence, the domain is also Unknown; a valid concept alone can
establish the domain before stack configuration.
Record the supporting sections and values. For Unknown, use an existing matching
scoped decision or clarify with the user/configured project lead before
domain-specific delegation or writes; resolved configured facts need no new vote.
Independent neutral reads may continue. Domain selection does not waive required
branch inputs: read their actual originals and leave missing inputs Incomplete.
Never silently default to Game.

- **[Game]** keep the existing art bible workflow: visual identity, shape language, color, character direction, asset standards, and engine-aware constraints.
- **[Product]** use this same command as a product brand style guide workflow. Product outputs go to `design/brand/style-guide.md`; they do not use the game art bible path.

Never delete or replace the game art bible guidance below. Product guidance is an additional branch beside it.

If the selected domain is **Product**, run the Product Branch below, then skip the Game Branch.

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Game Concept, art bible if resuming, technical preferences, visual identity anchor, engine/platform constraints | Product Concept, optional existing style/design docs, interaction patterns, accessibility requirements, technical preferences, surface profile |
| Steps | Frame references, author visual identity, mood, shape, color, character/environment/UI/HUD/VFX/asset standards, sign-off | Classify product surface, author brand style guide, optionally author UI-heavy design system foundation, route interaction behavior to `/ux-design interaction-patterns` |
| Outputs | `design/art/art-bible.md` with game visual production constraints | `design/brand/style-guide.md`; optionally `design/design-system.md` only for UI-heavy products |
| Next steps | `/map-systems`, `/setup-engine`, `/design-system`, `/asset-spec`, `/consistency-check`, `/create-architecture` | `/ux-design interaction-patterns`, `/ux-design [workflow]`, `/create-architecture`, `/asset-spec` for docs/schema/package artifacts |

## Product Branch: Brand / Surface Style Guide

Use this branch for product projects: APIs, CLIs, SDKs, web apps, admin tools, data products, and documentation-heavy releases.

### Product Context Reads

Read:
- `design/cdd/product-concept.md` for core promise, JTBD, personas, MVP scope, anti-goals, and product principles.
- `standards/technical-preferences.md` if it exists for product type, target platform, framework, UI stack, docs toolchain, deployment target, and accessibility commitments.
- `design/accessibility-requirements.md` if it exists for accessibility tier and feature matrix.
- `design/ux/interaction-patterns.md` if it exists so visual standards do not contradict interaction behavior.
- `design/design-system.md` if it exists for UI-heavy products; update only missing sections unless the user explicitly asks for a revision.

Classify the product surface before authoring:

| Surface profile | Required design artifact behavior |
|-----------------|-----------------------------------|
| API-only | Do not require a UI design system. Brand style guide is optional; interaction patterns should cover API consumer behavior such as errors, pagination, auth prompts, examples, and docs handoff. |
| CLI-only | Do not require a UI design system. Brand style guide is optional; interaction patterns should cover command help, prompts, stdout/stderr, errors, destructive confirmations, and scripted usage. |
| SDK / library | Do not require a UI design system. Brand style guide is optional; interaction patterns should cover examples, typed errors, docs snippets, and integration workflows. |
| Web UI / desktop / mobile / admin console | UI-heavy. `design/design-system.md` is required before implementation; `design/brand/style-guide.md` is recommended when brand or docs visuals matter. |
| Multi-surface product | Apply the strictest relevant rule: UI-heavy surfaces need `design/design-system.md`; API/CLI/SDK surfaces need `design/ux/interaction-patterns.md`. |

### Product Outputs

Product `/art-bible` never writes `design/art/art-bible.md`.

Write or update:
- `design/brand/style-guide.md` when the product needs brand, documentation imagery, visual tone, illustration/screenshot rules, colors, typography, logo usage, or public-facing release materials.
- `design/design-system.md` only when the product is UI-heavy and the user chooses to create or update component-level UI rules in this session.

Route interaction behavior to `/ux-design interaction-patterns`, which writes `design/ux/interaction-patterns.md`. Do not duplicate API/CLI/web interaction rules inside `design/brand/style-guide.md` except as visual/copy tone constraints.

### Product Authoring Steps

1. Confirm the surface profile and scope with `AskUserQuestion`.
   - Options: `Brand style guide only` / `UI-heavy design system foundation` / `Resume existing product style docs`
   - Ask whether public docs, screenshots, diagrams, or release materials need visual standards.
2. If writing `design/brand/style-guide.md`, cover:
   - Brand promise and visual thesis tied to the Product Concept.
   - Voice and visual tone for product UI, docs, examples, screenshots, and release materials.
   - Color and typography rules, including accessibility minimums.
   - Iconography, diagrams, screenshots, and documentation imagery rules.
   - Explicit style prohibitions: what the product should not look or sound like.
3. If writing `design/design-system.md` for a UI-heavy product, cover:
   - Component pattern inventory and ownership boundaries.
   - Layout density, spacing, responsive behavior, and state design.
   - Form, table, navigation, modal, toast, loading, empty, error, and permission states.
   - Accessibility integration and localization/text expansion constraints.
   - Handoff rules to implementation and `/ux-review`.
4. If the product has any API, CLI, SDK, or UI consumer surface and `design/ux/interaction-patterns.md` does not exist, close with `/ux-design interaction-patterns` as the recommended next step.

### Product Close

Offer next steps based on the detected surface:
- `/ux-design interaction-patterns` — required for API, CLI, SDK, web UI, and multi-surface products with user or integrator interactions.
- `/ux-design [workflow-name]` — write a key workflow, API consumer journey, CLI flow, or screen spec.
- `/create-architecture` — continue Technical Setup once concept and CDD coverage are ready.
- `Stop here`.

---

## Game Branch: Art Bible

## Phase 0: Parse Arguments and Context Check

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `standards/director-gates.md` for the full check pattern.

Read `design/cdd/game-concept.md`. If it does not exist, fail with:
> "No game concept found. Run `/brainstorm` first — the art bible is authored after the game concept is approved."

Extract from concept.md:
- Game title (working title)
- Core fantasy and elevator pitch
- Game pillars (all of them)
- **Visual Identity Anchor** section if present (from brainstorm Phase 4 art-director output)
- Target platform (if noted)

**Retrofit mode detection**: Glob `design/art/art-bible.md`. If the file exists:
- Read it in full
- For each of the 9 sections, check whether the body contains real content (more than a `[To be designed]` placeholder or similar) vs. is empty/placeholder
- Build a section status table:

```
Section | Status
--------|--------
1. Visual Identity Statement | [Complete / Empty / Placeholder]
2. Color Palette | ...
3. Lighting & Atmosphere | ...
4. Character Art Direction | ...
5. Environment & Level Art | ...
6. UI Visual Language | ...
7. VFX & Particle Style | ...
8. Asset Standards | ...
9. Style Prohibitions | ...
```

- Present this table to the user:
  > "Found existing art bible at `design/art/art-bible.md`. [N] sections are complete, [M] need content. I'll work on the incomplete sections only — existing content will not be touched."
- Only work on sections with Status: Empty or Placeholder. Do not re-author sections that are already complete.

If the file does not exist, this is a fresh authoring session — proceed normally.

Read `standards/technical-preferences.md` if it exists — extract performance budgets and engine for asset standard constraints.

---

## Phase 1: Framing

Present the session context and ask two questions before authoring anything:

Use `AskUserQuestion` with two tabs:
- Tab **"Scope"** — "Which sections need to be authored today?"
  Options: `Full bible — all 9 sections` / `Visual identity core (sections 1–4 only)` / `Asset standards only (section 8)` / `Resume — fill in missing sections`
- Tab **"References"** — "Do you have reference games, films, or art that define the visual direction?"
  (Free text — let the user type specific titles. Do NOT preset options here.)

If the concept.md has a Visual Identity Anchor section, note it:
> "Found a visual identity anchor from brainstorm: '[anchor name] — [one-line rule]'. I'll use this as the foundation for the art bible."

---

## Phase 2: Visual Identity Foundation (Sections 1–4)

These four sections define the core visual language. **All other sections flow from them.** Author and write each to file before moving to the next.

### Section 1: Visual Identity Statement

**Goal**: A one-line visual rule plus 2–3 supporting principles that resolve visual ambiguity.

If a visual anchor exists from concept.md: present it and ask:
- "Build directly from this anchor?"
- "Revise it before expanding?"
- "Start fresh with new options?"

**Agent delegation (MANDATORY)**: Spawn `art-director` via Task:
- Provide: game concept (elevator pitch, core fantasy), full pillar set, platform target, any reference games/art from Phase 1 framing, the visual anchor if it exists
- Ask: "Draft a Visual Identity Statement for this game. Provide: (1) a one-line visual rule that could resolve any visual decision ambiguity, (2) 2–3 supporting visual principles, each with a one-sentence design test ('when X is ambiguous, this principle says choose Y'). Anchor all principles directly in the stated pillars — each principle must serve a specific pillar."

Present the art-director's draft to the user. Use `AskUserQuestion`:
- Options: `[A] Lock this in` / `[B] Revise the one-liner` / `[C] Revise a supporting principle` / `[D] Describe my own direction`

Write the approved section to file immediately.

### Section 2: Mood & Atmosphere

**Goal**: Emotional targets by game state — specific enough for a lighting artist to work from.

For each major game state (e.g., exploration, combat, victory, defeat, menus — adapt to this game's states), define:
- Primary emotion/mood target
- Lighting character (time of day, color temperature, contrast level)
- Atmospheric descriptors (3–5 adjectives)
- Energy level (frenetic / measured / contemplative / etc.)

**Agent delegation**: Spawn `art-director` via Task with the Visual Identity Statement and pillar set. Ask: "Define mood and atmosphere targets for each major game state in this game. Be specific — 'dark and foreboding' is not enough. Name the exact emotional target, the lighting character (warm/cool, high/low contrast, time of day direction), and at least one visual element that carries the mood. Each game state must feel visually distinct from the others."

Write the approved section to file immediately.

### Section 3: Shape Language

**Goal**: The geometric vocabulary that makes this game's world visually coherent and distinguishable.

Cover:
- Character silhouette philosophy (how readable at thumbnail size? Distinguishing trait per archetype?)
- Environment geometry (angular/curved/organic/geometric — which dominates and why?)
- UI shape grammar (does UI echo the world aesthetic, or is it a distinct HUD language?)
- Hero shapes vs. supporting shapes (what draws the eye, what recedes?)

**Agent delegation**: Spawn `art-director` via Task with Visual Identity Statement and mood targets. Ask: "Define the shape language for this game. Connect each shape principle back to the visual identity statement and a specific game pillar. Explain what these shape choices communicate to the player emotionally."

Write the approved section to file immediately.

### Section 4: Color System

**Goal**: A complete, producible palette system that serves both aesthetic and communication needs.

Cover:
- Primary palette (5–7 colors with roles — not just hex codes, but what each color means in this world)
- Semantic color usage (what does red communicate? Gold? Blue? White? Establish the color vocabulary)
- Per-biome or per-area color temperature rules (if the game has distinct areas)
- UI palette (may differ from world palette — define the divergence explicitly)
- Colorblind safety: which semantic colors need shape/icon/sound backup

**Agent delegation**: Spawn `art-director` via Task with Visual Identity Statement and mood targets. Ask: "Design the color system for this game. Every semantic color assignment must be explained — why does this color mean danger/safety/reward in this world? Identify which color pairs might fail colorblind players and specify what backup cues are needed."

Write the approved section to file immediately.

---

## Phase 3: Production Guides (Sections 5–8)

These sections translate the visual identity into concrete production rules. They should be specific enough that an outsourcing team can follow them without additional briefing.

### Section 5: Character Design Direction

**Agent delegation**: Spawn `art-director` via Task with sections 1–4. Ask: "Define character design direction for this game. Cover: visual archetype for the player character (if any), distinguishing feature rules per character type (how do players tell enemies/NPCs/allies apart at a glance?), expression/pose style targets (stiff/expressive/realistic/exaggerated), and LOD philosophy (how much detail is preserved at game camera distance?)."

Write the approved section to file.

### Section 6: Environment Design Language

**Agent delegation**: Spawn `art-director` via Task with sections 1–4. Ask: "Define the environment design language for this game. Cover: architectural style and its relationship to the world's culture/history, texture philosophy (painted vs. PBR vs. stylized — why this choice for this game?), prop density rules (sparse/dense — what drives the choice per area type?), and environmental storytelling guidelines (what visual details should tell the story without text?)."

Write the approved section to file.

### Section 7: UI/HUD Visual Direction

**Agent delegation**: Spawn in parallel:
- **`art-director`**: Visual style for UI — diegetic vs. screen-space HUD, typography direction (font personality, weight, size hierarchy), iconography style (flat/outlined/illustrated/photorealistic), animation feel for UI elements
- **`ux-designer`**: UX alignment check — does the visual direction support the interaction patterns this game requires? Flag any conflicts between art direction and readability/accessibility needs.

Collect both. If they conflict (e.g., art-director wants elaborate diegetic UI but ux-designer flags it would reduce combat readability), surface the conflict explicitly with both positions. Do NOT silently resolve — use `AskUserQuestion` to let the user decide.

Write the approved section to file.

### Section 8: Asset Standards

**Agent delegation**: Spawn in parallel:
- **`art-director`**: File format preferences, naming convention direction, texture resolution tiers, LOD level expectations, export settings philosophy
- **`technical-artist`**: Engine-specific hard constraints — poly count budgets per asset category, texture memory limits, material slot counts, importer constraints, anything from the performance budgets in `standards/technical-preferences.md`

If any art preference conflicts with a technical constraint (e.g., art-director wants 4K textures but performance budget requires 2K for mobile), resolve the conflict explicitly — note both the ideal and the constrained standard, and explain the tradeoff. Ambiguity in asset standards is where production costs are born.

Write the approved section to file.

---

## Phase 4: Reference Direction (Section 9)

**Goal**: A curated reference set that is specific about what to take and what to avoid from each source.

**Agent delegation**: Spawn `art-director` via Task with the completed sections 1–8. Ask: "Compile a reference direction for this game. Provide 3–5 reference sources (games, films, art styles, or specific artists). For each: name it, specify exactly what visual element to draw from it (not 'the general aesthetic' — a specific technique, color choice, or compositional rule), and specify what to explicitly avoid or diverge from (to prevent the 'trying to copy X' reading). References should be additive — no two references should be pointing in exactly the same direction."

Write the approved section to file.

---

## Phase 5: Art Director Sign-Off

**Review mode check** — apply before spawning AD-ART-BIBLE:
- `solo` → skip. Note: "AD-ART-BIBLE skipped — Solo mode." Proceed to Phase 6.
- `lean` → skip (not a PHASE-GATE). Note: "AD-ART-BIBLE skipped — Lean mode." Proceed to Phase 6.
- `full` → spawn as normal.

After all sections are complete (or the scoped set from Phase 1 is complete), spawn `creative-director` via Task using gate **AD-ART-BIBLE** (`standards/director-gates.md`).

Pass: art bible file path, game pillars, visual identity anchor.

Handle verdict per standard rules in `director-gates.md`. Record the verdict in the art bible's status header:
`> **Art Director Sign-Off (AD-ART-BIBLE)**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date]`

---

## Phase 6: Close

Before presenting next steps, check project state:
- Does `design/cdd/module-index.md` exist? → map-systems is done, skip that option
- Does `standards/technical-preferences.md` contain a configured engine (not `[TO BE CONFIGURED]`)? → setup-engine is done, skip that option
- Does `design/cdd/` contain any `*.md` files? → design-system has been run, skip that option
- Locate any saved `design/cdd/cross-review-*.md` records, then read their substantive verdict, reviewed scope and current input identities, required review coverage, and unresolved blockers. File existence only locates evidence. Treat /review-all-gdds as complete only when that evidence establishes an applicable completed review; otherwise keep the review pending and offer it below.
- Do CDDs exist (check above)? → include /consistency-check option

Use `AskUserQuestion` for next steps. Only include options that are genuinely next based on the state check above:

**Option pool — include only if not already done:**
- `[_] Run /map-systems — decompose the concept into systems before writing CDDs` (skip if module-index.md exists)
- `[_] Run /setup-engine — configure the engine (asset standards may need revisiting after engine is set)` (skip if engine configured)
- `[_] Run /design-system — start the first CDD` (skip if any CDDs exist)
- `[_] Run /review-all-gdds — cross-CDD consistency check (required before Technical Setup gate)` (skip only after the saved substantive review, required coverage, current input identities, and resolved blockers establish an applicable completed review; file existence alone is insufficient)
- `[_] Run /asset-spec — generate per-asset visual specs and AI generation prompts from approved CDDs` (include if CDDs exist)
- `[_] Run /consistency-check — scan existing CDDs against the art bible for visual direction conflicts` (include if CDDs exist)
- `[_] Run /create-architecture — author the master architecture document (next Technical Setup step)`
- `[_] Stop here`

Assign letters A, B, C… only to the options actually included. Mark the most logical pipeline-advancing option as `(recommended)`.

> **Always include** `/create-architecture` and Stop here as options — these are always valid next steps once the art bible is complete.

---

## Collaborative Protocol

Every section follows: **Question → Options → Decision → Draft (from art-director agent) → Approval → Write to file**

- Never draft a section without first spawning the relevant agent(s)
- Write each section to file immediately after approval — do not batch
- Surface all agent disagreements to the user — never silently resolve conflicts between art-director and technical-artist
- The art bible is a constraint document: it restricts future decisions in exchange for visual coherence. Every section should feel like it narrows the solution space productively.

---

## Recommended Next Steps

After the art bible is approved:
- Run `/map-systems` to decompose the concept into game systems before authoring CDDs
- Run `/setup-engine` if the engine is not yet configured (asset standards may need revisiting after engine selection)
- Run `/design-system [first-system]` to start authoring per-system CDDs
- Run `/consistency-check` once CDDs exist to validate them against the art bible's visual rules
- Run `/create-architecture` to produce the master architecture document
