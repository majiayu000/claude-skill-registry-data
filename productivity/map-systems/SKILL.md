---
name: map-systems
description: "Use this skill when an approved concept must be decomposed into owned modules, dependencies, priorities, and a design/cdd/module-index.md design order."
argument-hint: "[next | module-name] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, TodoWrite, Task
---

## User Guide

- When to use: Decompose a concept into individual modules, map dependencies, prioritize design order, and create the module index. Supports both game and general product domains.
- Inputs: Command arguments: `/map-systems [next | module-name] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

When this skill is invoked:

## Parse Arguments

Two modes:

- **No argument**: `/map-systems` — Run the full decomposition workflow (Phases 1-5)
  to create or update the module index.
- **`next`**: `/map-systems next` — Pick the highest-priority undesigned module
  from the index and hand off to `/design-system` (Phase 6).

Also resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `standards/director-gates.md` for the full check pattern.

**Domain detection.** The concept document reveals the domain:
- **游戏专用**: concept doc at `design/cdd/game-concept.md` containing game-specific sections (Core Loop, MDA analysis, player types)
- **通用产品**: concept doc at `design/cdd/product-concept.md` containing product-specific sections (User Journey, JTBD, user personas)

Sections below are marked **[通用场景]** (both domains), **[游戏专用]** (game-domain), or **[通用产品]** (product-domain).

---

No argument runs the Phases 1-5 decomposition workflow and requires the actual
concept input below. Direct `next` or a named-module invocation enters Phase 6
without the Phase 1 decomposition read. When decomposition is followed by a
handoff, its required concept input must already have been read. Resolve an
unknown invocation before choosing a phase; missing inputs do not establish a
skip. Handoff, approval and index-completion requirements still apply.

## Phase 1: Read Concept (Required Context)

Read the concept document and any existing design work. This provides the raw material
for module decomposition.

**[通用场景]** Required:
- Read the concept document — **fail with a clear message if missing**:
  > "No concept document found. Run `/brainstorm` first
  > to create one, then come back to decompose it into modules."
  - **游戏专用**: Read `design/cdd/game-concept.md`
  - **通用产品**: Read `design/cdd/product-concept.md`

**[通用场景]** Optional (read if they exist):
- Read `design/cdd/principles.md` — principles constrain priority and scope
- Read `design/cdd/module-index.md` — if exists, **resume** from where it left off
  (update, don't recreate from scratch)
- Glob `design/cdd/*.md` — check which module CDDs already exist

**[通用场景]** If the module index already exists:
- Read it and present current status to the user
- Use `AskUserQuestion` to ask:
  "The module index already exists with [N] modules ([M] designed, [K] not started).
  What would you like to do?"
  - Options: "Update the index with new modules", "Design the next undesigned module",
    "Review and revise priorities"

---

## Phase 2: Module Enumeration (Collaborative)

Extract and identify all modules the project needs. This is the creative core of the
skill — it requires human judgment because concept docs rarely enumerate every
module explicitly.

**[通用场景]** Step 2a: Extract Explicit Modules

Scan the concept document for directly mentioned modules and components.

**[游戏专用]** Game concept sections to scan:
- Core Mechanics section (most explicit)
- Core Loop section (implies what modules drive each loop tier)
- Technical Considerations section (networking, procedural generation, etc.)
- MVP Definition section (required features = required modules)

**[通用产品]** Product concept sections to scan:
- Core Interaction section (most explicit)
- User Journey section (implies what modules support each journey stage)
- Technical Considerations section (integrations, data flow, etc.)
- MVP Definition section (required features = required modules)

**[通用场景]** Step 2b: Identify Implicit Modules

For each explicit module, identify the **hidden modules** it implies. Projects always
need more modules than the concept doc mentions.

**[游戏专用]** Game inference patterns:

- "Inventory" implies: item database, equipment slots, weight/capacity rules,
  inventory UI, item serialization for save/load
- "Combat" implies: damage calculation, health module, hit detection, status effects,
  enemy AI, combat UI (health bars, damage numbers), death/respawn
- "Open world" implies: streaming/chunking, LOD module, fast travel, map/minimap,
  point of interest tracking, world state persistence
- "Multiplayer" implies: networking layer, lobby/matchmaking, state synchronization,
  anti-cheat, network UI (ping, player list)
- "Crafting" implies: recipe database, ingredient gathering, crafting UI,
  success/failure mechanics, recipe discovery/learning
- "Dialogue" implies: dialogue tree module, dialogue UI, choice tracking, NPC
  state management, localization hooks
- "Progression" implies: XP module, level-up mechanics, skill tree, unlock
  tracking, progression UI, progression save data

**[通用产品]** Product inference patterns:

- "REST API" implies: authentication/authorization, rate limiting, request validation,
  error handling middleware, API documentation (OpenAPI), logging/monitoring
- "Web app" implies: routing, state management, component library, data fetching layer,
  client-side caching, form validation, error boundaries, responsive layout
- "Database" implies: schema/migration module, connection pooling, query builder/ORM,
  backup/restore, data validation, indexing strategy
- "Authentication" implies: session management, OAuth integration, role/permission
  module, password reset flow, MFA support, audit logging
- "Data pipeline" implies: ETL orchestration, data validation/sanitization,
  error handling/dead-letter queue, scheduling, monitoring/alerting
- "CLI tool" implies: argument parsing, config file handling, output formatting,
  error codes, progress indicators, shell completion
- "Real-time features" implies: WebSocket connection management, event broadcasting,
  presence tracking, message queuing, reconnection logic

Explain in conversation text why each implicit module is needed (with examples).

**[通用场景]** Step 2c: User Review

Present the enumeration organized by category. For each module, show:
- Name
- Category
- Brief description (1 sentence)
- Whether it was explicit (from concept) or implicit (inferred)

Then use `AskUserQuestion` to capture feedback:
- "Are there modules missing from this list?"
- "Should any of these be combined or split?"
- "Are there modules listed that this project does NOT need?"

Iterate until the user approves the enumeration.

---

## Phase 3: Dependency Mapping (Collaborative)

For each module, determine what it depends on. A module "depends on" another if
it cannot function without that other module existing first.

**[通用场景]** Step 3a: Map Dependencies

For each module, list its dependencies. Use these dependency heuristics:
- **Input/output dependencies**: Module A produces data Module B needs
- **Structural dependencies**: Module A provides the framework Module B plugs into
- **Interface dependencies**: Every core module has a corresponding interface module that
  depends on it (but the interface is designed after the core module)

**[通用场景]** Step 3b: Sort by Dependency Order

Arrange modules into layers:

**[游戏专用]** Game layers:
1. **Foundation**: Modules with zero dependencies (designed and built first)
2. **Core**: Modules depending only on Foundation modules
3. **Feature**: Modules depending on Core modules
4. **Presentation**: UI and feedback modules that wrap gameplay modules
5. **Polish**: Meta-modules, tutorials, analytics, accessibility

**[通用产品]** Product layers:
1. **Foundation**: Modules with zero dependencies — data store, config, logging, error handling (designed and built first)
2. **Core**: Modules depending only on Foundation — auth, API framework, data access layer
3. **Feature**: Modules depending on Core — business logic, integrations, user-facing features
4. **Integration**: Modules connecting features to external modules — webhooks, third-party APIs, export/import
5. **Polish**: Meta-modules, onboarding, analytics, accessibility, performance optimization

**[通用场景]** Step 3c: Detect Circular Dependencies

Check for cycles in the dependency graph. If found:
- Highlight them to the user
- Propose resolutions (interface abstraction, simultaneous design, breaking the
  cycle by defining a contract between the two modules)

**[通用场景]** Step 3d: Present to User

Show the dependency map as a layered list. Highlight:
- Any circular dependencies
- Any "bottleneck" modules (many others depend on them — these are high-risk)
- Any modules with no dependents (leaf nodes — lower risk, can be designed late)

Use `AskUserQuestion` to ask: "Does this dependency ordering look right? Any
dependencies I'm missing or that should be removed?"

**Review mode check** — apply before spawning TD-SYSTEM-BOUNDARY:
- `solo` → skip. Note: "TD-SYSTEM-BOUNDARY skipped — Solo mode." Proceed to priority assignment.
- `lean` → skip (not a PHASE-GATE). Note: "TD-SYSTEM-BOUNDARY skipped — Lean mode." Proceed to priority assignment.
- `full` → spawn as normal.

**After dependency mapping is approved, spawn `technical-director` via Task using gate TD-SYSTEM-BOUNDARY (`standards/director-gates.md`) before proceeding to priority assignment.**

Pass: the dependency map summary, layer assignments, bottleneck modules list, any circular dependency resolutions.

Present the assessment. If REJECT, revise the module boundaries with the user before moving to priority assignment. If CONCERNS, note them inline in the module index and continue.

---

## Phase 4: Priority Assignment (Collaborative)

Assign each module to a priority tier based on what milestone it's needed for.

### Step 4a: Auto-Assign Based on Concept

**[游戏专用]** Game priority tiers:
- **MVP**: Systems mentioned in the concept's "Required for MVP" section, plus their
  Foundation-layer dependencies
- **Vertical Slice**: Systems needed for a complete experience in one area
- **Alpha**: All remaining gameplay modules
- **Full Vision**: Polish, meta, and nice-to-have modules

**[通用产品]** Product priority tiers:
- **MVP Workflow**: Modules needed for the core user workflow to function end-to-end, plus their Foundation-layer dependencies
- **Integration Milestone**: Modules needed for external system integration (auth, APIs, webhooks, data pipelines)
- **Operational Readiness**: Remaining feature modules plus ops, monitoring, deployment
- **Full Vision**: Polish, analytics, accessibility, performance optimization

### Step 4b: User Review

Present the priority assignments in a table. For each tier, explain why modules
were placed there.

Use `AskUserQuestion` to ask: "Do these priority assignments match your vision?
Which modules should be higher or lower priority?"

Explain reasoning in conversation. **[游戏专用]** "I placed [module] in MVP because the core loop requires it — without [module], the 30-second loop can't function." **[通用产品]** "I placed [module] in MVP Workflow because the core user journey requires it — without [module], the primary workflow can't complete end-to-end."

**"Why" column guidance**: When explaining why each module was placed in a priority tier, connect to the user experience, not just technical necessity. "X depends on Y" alone is insufficient.

**[游戏专用]** Game examples:
- "Required for the core loop — without it, placement decisions have no consequence (Pillar 2: Placement is the Puzzle)"
- "Foundation for all economy decisions — players must understand upgrade costs to make meaningful placement choices"

**[通用产品]** Product examples:
- "Required for the core workflow — without it, invoice approval can't reach the user's inbox (Principle: Data Integrity)"
- "Foundation for all API consumers — third-party integrations must receive consistent error contracts"

**Review mode check** — apply before spawning PR-SCOPE:
- `solo` → skip. Note: "PR-SCOPE skipped — Solo mode." Proceed to writing the modules index.
- `lean` → skip (not a PHASE-GATE). Note: "PR-SCOPE skipped — Lean mode." Proceed to writing the modules index.
- `full` → spawn as normal.

**After priorities are approved, spawn `producer` via Task using gate PR-SCOPE (`standards/director-gates.md`) before writing the index.**

Pass: total module count per milestone tier, estimated implementation volume per tier (module count × average complexity), team size, stated project timeline.

Present the assessment. If UNREALISTIC, offer to revise priority tier assignments before writing the index. If CONCERNS, note them and continue.

### Step 4c: Determine Design Order

Combine dependency sort + priority tier to produce the final design order for the
detected domain.

**[游戏专用]** Game design order:
1. MVP Foundation modules first
2. MVP Core modules second
3. MVP Feature modules third
4. Vertical Slice Foundation/Core modules
5. Alpha modules needed for full gameplay coverage
6. Full Vision polish, meta, and nice-to-have modules

**[通用产品]** Product design order:
1. MVP Workflow Foundation modules first
2. MVP Workflow Core modules second
3. MVP Workflow Feature/UI/API modules third
4. Integration Milestone Foundation/Core modules
5. Operational Readiness modules (monitoring, deployment, migrations, support)
6. Full Vision polish, analytics, accessibility, and performance optimization

This is the order the team should write CDDs in.

---

## Phase 5: Create Module Index (Write)

### Step 5a: Draft the Document

Using the template at `templates/module-index.md`, populate the
modules index with all data from Phases 2-4:
- Fill the enumeration table
- Fill the dependency map
- Fill the recommended design order
- Fill the high-risk modules
- Fill progress tracker (all modules "Not Started" initially, unless CDDs already exist)

### Step 5b: Approval

Present a summary of the document:
- Total modules count by category
- MVP module count
- First 3 modules in the design order
- Any high-risk items

Ask: "May I write the modules index to `design/cdd/module-index.md`?"

Wait for approval. Write the file only after "yes."

**Review mode check** — apply before spawning CD-SYSTEMS:
- `solo` → skip. Note: "CD-SYSTEMS skipped — Solo mode." Proceed to Phase 7 next steps.
- `lean` → skip (not a PHASE-GATE). Note: "CD-SYSTEMS skipped — Lean mode." Proceed to Phase 7 next steps.
- `full` → spawn as normal.

**After the modules index is written, spawn `creative-director` via Task using gate CD-SYSTEMS (`standards/director-gates.md`).**

Pass: modules index path, game pillars/principles and core fantasy/promise (from the concept document), MVP priority tier module list.

Present the assessment. If REJECT, revise the module set with the user before CDD authoring begins. If CONCERNS, record them in the modules index as a `> **Creative Director Note**` at the top of the relevant tier section.

### Step 5c: Update Session State

Only when the exact create/update effect at `production/session-state/active.md`
is covered by scoped authority, write the applicable progress below. Otherwise
show progress in conversation; saving the module index alone does not authorize
session state. Present a concrete draft only if this new effect is requested:
- Task: Systems decomposition
- Status: Module index created
- File: design/cdd/module-index.md
- Next: Design individual module CDDs

**Verdict: COMPLETE** — modules index written to `design/cdd/module-index.md`.
If the user declined: **Verdict: BLOCKED** — user did not approve the write.

---

## Phase 6: Design Individual Systems (Handoff to /design-system)

This phase is entered when:
- The user says "yes" to designing modules after creating the index
- The user invokes `/map-systems [module-name]`
- The user invokes `/map-systems next`

### Step 6a: Select the System

- If a module name was provided, find it in the modules index
- If `next` was used, pick the highest-priority undesigned module (by design order)
- If the user just finished the index, ask:
  "Would you like to start designing individual modules now? The first module in
  the design order is [name]. Or would you prefer to stop here and come back later?"

Use `AskUserQuestion` for: "Start designing [module-name] now, pick a different
module, or stop here?"

### Step 6b: Hand Off to /design-system

Once a module is selected, invoke the `/design-system [module-name]` skill.

The `/design-system` skill handles the full CDD authoring process:
- Gathers context from game concept, modules index, and dependency CDDs
- Creates a file skeleton immediately
- Walks through all 8 required sections one at a time (collaborative, incremental)
- Cross-references existing docs to prevent contradictions
- Routes to specialist agents for domain expertise
- Writes each section to file as soon as it's approved
- Runs `/design-review` when complete
- Updates the modules index

**Do not duplicate the /design-system workflow here.** This skill owns the modules
*index*; `/design-system` owns individual module *CDDs*.

### Step 6c: Loop or Stop

After `/design-system` completes, use `AskUserQuestion`:
- "Continue to the next module ([next module name])?"
- "Pick a different module?"
- "Stop here for this session?"

If continuing, return to Step 6a.

---

## Phase 7: Suggest Next Steps

After the modules index is created (or after designing some modules), present next actions using `AskUserQuestion`:

- "Module index is written. What would you like to do next?"
  - [A] Start designing CDDs — run `/design-system [first-module-in-order]`
  - [B] Ask a director to review the index first — ask `creative-director` or `technical-director` to validate the module set before committing to 10+ CDD sessions
  - [C] Stop here for this session

**The director review option ([B]) is worth highlighting**: having a Creative Director or Technical Director review the completed modules index before starting CDD authoring catches scope issues, missing modules, and boundary problems before they're locked in across many documents. It is optional but recommended for new projects.

After any individual CDD is completed:
- "Run `/design-review design/cdd/[module].md` in a fresh session to validate quality"
- "Run `/review-all-gdds`, then `/gate-check systems-design` when all MVP CDDs are complete and reviewed"

---

## Collaborative Protocol

This skill follows the collaborative design principle at every phase:

1. **Question -> Options -> Decision -> Draft -> Approval** at every step
2. **AskUserQuestion** at every decision point (Explain -> Capture pattern):
   - Phase 2: "Missing modules? Combine or split?"
   - Phase 3: "Dependency ordering correct?"
   - Phase 4: "Priority assignments match your vision?"
   - Phase 5: "May I write the modules index?"
   - Phase 6: "Start designing, pick different, or stop?" then hand off to `/design-system`
3. **Scoped writes**: reuse existing authority for named paths/effects; present a
   concrete draft and obtain approval only for uncovered effects
4. **Incremental writing**: Update the modules index after each module is designed
5. **Handoff**: Individual CDD authoring is owned by `/design-system`, which handles
   incremental section writing, cross-referencing, design review, and index updates
6. **Session state updates**: after a milestone (index created, module designed,
   priorities changed), update `production/session-state/active.md` only within
   explicit create/update authority; otherwise retain the progress in conversation

**Never** auto-generate the full modules list and write it without review.
**Never** start designing a module without user confirmation.
**Always** show the enumeration, dependencies, and priorities for user validation.

## Context Window Awareness

If context reaches or exceeds 70% at any point, report the actual persistence state:

- Only after an authorized module index write and successful Read-back, name the
  saved `design/cdd/module-index.md` and suggest a fresh session to continue the
  established scope, using `/map-systems next` where applicable.
- Before saving, or after a failed write/read-back, keep the draft and unresolved
  decisions in conversation and provide a compact recovery summary for the next
  session. Do not claim the index is saved or create/update files merely because
  context is low. Recover the existing scope and approvals before dependent work.

---

## Recommended Next Steps

- Run `/design-system [first-module-in-order]` to author the first CDD (use design order from the index)
- Run `/map-systems next` to always pick the highest-priority undesigned module automatically
- Run `/design-review design/cdd/[module].md` in a fresh session after each CDD is authored
- Run `/review-all-gdds`, then `/gate-check systems-design` when all MVP CDDs are authored and reviewed
