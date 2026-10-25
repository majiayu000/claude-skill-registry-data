---
name: saas-map-features
description: "Decompose a concept into individual systems, map dependencies, prioritize design order, create the systems index."
argument-hint: "[next | system-name] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, TaskCreate, TaskGet, TaskList, TaskUpdate, Agent, Bash(bash "*/.claude/skills/saas-map-features/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,review_mode,automation,workflow,docs.density,project.stage`

Resolved above — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.claude/docs/config-resolution.md`.

# Map Systems

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.


When this skill is invoked:

## Parse Arguments

Two modes:

- **No argument**: `/saas-map-features` — Run the full decomposition workflow (Phases 1-5)
  to create or update the systems index.
- **`next`**: `/saas-map-features next` — Pick the highest-priority undesigned system
  from the index and hand off to `/saas-design-system` (Phase 6).


See `.claude/docs/director-gates.md` for the full check pattern. Individual gate definitions live in `.claude/docs/director-gates/[gate-id].md` — the spawned agent reads its own gate file; do not read it in the parent session.


Every `AskUserQuestion` call follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt). In collaborative mode the
system list, dependency, priority and write approvals are separate questions:
each waits for its answer before the next step runs.

**`docs.density`** — it controls per-section *depth*, where `workflow`
controls which sections exist. `modes.rigor` sets both together; set
`docs.density` explicitly to vary depth alone: `terse` (the default, via `rigor: minimal`) = one-line system descriptions;
`balanced` = a brief paragraph per system + dependency notes (`rigor: standard`);
`thorough` = full system-by-system rationale + relationship analysis. Apply it to
every section you author.

> **Where the per-system prose goes.** `templates/features-modules-index.md`'s Systems
> Enumeration is a fixed-column table with no description column, so at
> `balanced` and `thorough` the prose belongs in `## Overview` — one short
> paragraph per system at `balanced`, plus relationship analysis at `thorough` —
> and in the `## Dependency Map` layer notes. **Do not add a column to the
> enumeration table** — it is a fixed contract in
> `.claude/docs/templates/features-modules-index.md`, and its consumers
> (`/saas-design-system` §6 and §7, `/saas-create-epics`) are written against the columns it
> defines. Widening it is a schema change, not a formatting choice.
>
> **How the consumers actually read it.** Nothing parses this table
> positionally. The two scripts that mention `features-modules-index.md`
> (`prd-structure-check.sh:51`, `review-scope.sh:40`) match it **by filename** in a
> `case` statement and parse no columns at all; the two skills key on the
> **`Category` column by name** (`design-system:229`, `:780`). So `Category` is
> the column that must never be renamed or dropped, and the table stays a fixed
> contract because every consumer is written against the set of columns the
> template defines.
> At `terse`, the table plus a one-paragraph `## Overview` is the whole output.

**`workflow`** (see `.claude/docs/workflow-modes.md`):
- `full` / `standard` — required before `/saas-design-system` (systems must be mapped
  before per-system PRDs are authored).
- `minimal` — not required (the product brief replaces the features index). Can
  still be run voluntarily.

---

## Phase 1: Read Concept (Required Context)

Read the product concept and any existing design work. This provides the raw material
for systems decomposition. Read each doc by section: check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise check if `.basinfy/` exists: if present, use the Basinfy Protocol (`basinfy_search` then `basinfy_read`); otherwise find the headings you need with the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Basinfy Protocol (`basinfy_search` / `basinfy_read` if `.basinfy/` exists) or the Grep tool (pattern `^#`, content mode) and Read those ranges with offset and limit.

**Required:**
- Read `design/prd/product-concept.md` (at `minimal`, read `design/product-brief.md`
  instead) — **fail with a clear message if neither is found**:
  > "No product concept found. Run `/saas-brainstorm` first to create one, then come back
  > to decompose it into systems."

**Optional (read if they exist):**
- Read `design/prd/product-pillars.md` — pillars constrain priority and scope
- Read `design/prd/features-modules-index.md` — if exists, **resume** from where it left off
  (update, don't recreate from scratch)
- Glob `design/prd/*.md` — check which system PRDs already exist

**If the systems index already exists:**
- Read it and present current status to the user
- Use `AskUserQuestion` to ask:
  "The systems index already exists with [N] systems ([M] designed, [K] not started).
  What would you like to do?"
  - Options: "Update the index with new systems", "Design the next undesigned system",
    "Review and revise priorities"

---

## Phase 2: Systems Enumeration (Collaborative)

Extract and identify all modules the SaaS application needs. This is the creative core of the
skill — it requires human judgment because concept docs rarely enumerate every
system explicitly.

### Step 2a: Extract Explicit Systems

Scan the product concept for directly mentioned systems and core workflows:
- Core Workflows section (most explicit)
- Core Loop section (implies what systems drive each loop tier)
- Technical Considerations section (networking, procedural generation, etc.)
- MVP Definition section (required features = required systems)

### Step 2b: Identify Implicit Systems

For each explicit system, identify the **hidden systems** it implies. SaaS applications always
need more systems than the concept doc mentions. Use this inference pattern:

- "Billing" implies: Stripe Checkout, webhook event listeners, subscription state machine,
  invoice PDF download, customer portal, plan limit enforcement
- "Multi-tenancy" implies: organization switcher, member invite tokens, RBAC roles (Owner/Admin/Member),
  database row-level security (RLS), tenant-scoped cache
- "Analytics & Reporting" implies: aggregation query pipeline, CSV/PDF export workers,
  interactive chart components, date-range filters, caching layer
- "Real-time Collaboration" implies: WebSocket / SSE connection manager, optimistic client updates,
  presence indicators, conflict resolution
- "AI Workflows" implies: streaming completion endpoints, prompt templates, vector embeddings,
  chunking pipeline, rate limiting per token quota, model fallback routing
- "Email Notifications" implies: template renderer, worker queue, bounce webhook handler,
  delivery event logging, notification preferences
- "Customer Onboarding & Activation" implies: onboarding checklist, product walkthroughs,
  activation milestones, trial expiration banners, upgrade triggers

Explain in conversation text why each implicit system is needed (with examples).

### Step 2c: User Review

Present the enumeration organized by category. For each system, show:
- Name
- Category
- Brief description (1 sentence)
- Whether it was explicit (from concept) or implicit (inferred)

Then use `AskUserQuestion` to capture feedback:
- "Are there systems missing from this list?"
- "Should any of these be combined or split?"
- "Are there systems listed that this SaaS product does NOT need?"

**At `collaborative`** — iterate until the user approves the enumeration.
**At `guided`** — ask once, apply the answer, and proceed; do not loop.
**At `autonomous`** — do not ask. Record the enumeration and its inferred systems
via `log_decision` and proceed.

---

## Phase 3: Dependency Mapping (Collaborative)

For each system, determine what it depends on. A system "depends on" another if
it cannot function without that other system existing first.

### Step 3a: Map Dependencies

For each system, list its dependencies. Use these dependency heuristics:
- **Input/output dependencies**: System A produces data System B needs
- **Structural dependencies**: System A provides the framework System B plugs into
- **UI dependencies**: Every core business workflow system has a corresponding UI system that
  depends on it (but UI is designed after the core business workflow system)

### Step 3b: Sort by Dependency Order

Arrange systems into layers:
1. **Foundation**: Systems with zero dependencies (designed and built first)
2. **Core**: Systems depending only on Foundation systems
3. **Feature**: Systems depending on Core systems
4. **Presentation**: UI and feedback systems that wrap core business workflow systems
5. **Polish**: Meta-systems, tutorials, analytics, accessibility

### Step 3c: Detect Circular Dependencies

Check for cycles in the dependency graph. If found:
- Highlight them to the user
- Propose resolutions (interface abstraction, simultaneous design, breaking the
  cycle by defining a contract between the two systems)

### Step 3d: Present to User

Show the dependency map as a layered list. Highlight:
- Any circular dependencies
- Any "bottleneck" systems (many others depend on them — these are high-risk)
- Any systems with no dependents (leaf nodes — lower risk, can be designed late)

Use `AskUserQuestion` to ask: "Does this dependency ordering look right? Any
dependencies I'm missing or that should be removed?"

**Review mode check** — apply before spawning TD-SYSTEM-BOUNDARY:
- `solo` → skip. Note: "TD-SYSTEM-BOUNDARY skipped — Solo mode." Proceed to priority assignment.
- `lean` → skip (not a PHASE-GATE). Note: "TD-SYSTEM-BOUNDARY skipped — Lean mode." Proceed to priority assignment.
- `full` → spawn as normal.

**After dependency mapping is approved, spawn `technical-director` via `Agent` using gate TD-SYSTEM-BOUNDARY (`.claude/docs/director-gates/td-api-boundary.md`) before proceeding to priority assignment.**

Pass: the dependency graph (each system → what it depends on), layer assignments, bottleneck systems, and any circular dependencies with their proposed resolutions.

Present the assessment. If REJECT, revise the system boundaries with the user, show the revised dependency map, and only then move to priority assignment. If CONCERNS, note them inline in the systems index and continue. If NOT ASSESSED [missing input], it is not an APPROVE: name what was missing, then supply it and re-run the gate, or continue with `TD-SYSTEM-BOUNDARY: NOT ASSESSED — [input]` noted in the index draft.

---

## Phase 4: Priority Assignment (Collaborative)

Assign each system to a priority tier based on what milestone it's needed for.

### Step 4a: Auto-Assign Based on Concept

Use these heuristics for initial assignment:
- **MVP**: Systems mentioned in the concept's "Required for MVP" section, plus their
  Foundation-layer dependencies
- **Vertical Slice**: Systems needed for a complete experience in one area
- **Alpha**: All remaining core business workflow systems
- **Full Vision**: Polish, meta, and nice-to-have systems

### Step 4b: User Review

Present the priority assignments in a table. For each tier, explain why systems
were placed there.

Use `AskUserQuestion` to ask: "Do these priority assignments match your vision?
Which systems should be higher or lower priority?"

Explain reasoning in conversation: "I placed [system] in MVP because the core loop
requires it — without [system], the 30-second loop can't function."

**How to phrase the reasoning** — this governs what you *say*, not a column you
write. Neither table has a `Why` column: Systems Enumeration is
`# / Name / Category / Priority / Status / Design Doc / Depends On`, and
Recommended Design Order is `Order / System / Priority / Layer / Agent(s) /
Est. Effort`. The rationale lives in the conversation above and, for anything
the user should still see after the session, in the index's `## Overview`
paragraph. Do not invent a column for it.

Mix technical necessity with user-experience reasoning. A purely technical
justification — "the billing system needs prorated math" — is insufficient on its
own when the system directly shapes what the user feels. Good reasoning names
both, and cites the pillar it serves:
- "Required for the core loop — without it the user's main choice has no
  consequence (Pillar [N]: [pillar name])"
- "This is where [system]'s identity is established — the workflow rules here
  are what make it feel different from [the sibling system]"
- "Foundation for every later economy decision — the user must understand
  costs before any of the choices built on top of it mean anything"

> **Fill the brackets from *this* project.** The bracketed slots are not
> decoration. Reasoning copied from another product's worked example carries that
> product's vocabulary instead of this one's.

**Review mode check** — apply before spawning PR-SCOPE:
- `solo` → skip. Note: "PR-SCOPE skipped — Solo mode." Proceed to Step 4c.
- `lean` → skip (not a PHASE-GATE). Note: "PR-SCOPE skipped — Lean mode." Proceed to Step 4c.
- `full` → spawn as normal.

**After priorities are approved, spawn `delivery-producer` via `Agent` using gate PR-SCOPE (`.claude/docs/director-gates/dp-scope-assessment.md`) before writing the index.**

Pass the gate's fields from the index: the full vision scope (every system in the index), the MVP definition (the MVP tier's systems), the scope tiers (system count per milestone tier, with estimated implementation volume — system count × average complexity), the stated project timeline as the timeline estimate, and team size.

Present the assessment. PR-SCOPE answers REALISTIC / OPTIMISTIC / UNREALISTIC.
If UNREALISTIC, offer to revise priority tier assignments before writing the
index. If OPTIMISTIC, show the delivery-producer's suggested adjustments and ask whether to
apply them to the tiers before writing; if the user declines, note them and
continue. If NOT ASSESSED [missing input] — often the team size or timeline — it
is not a REALISTIC: name what was missing, then supply it and re-run the gate, or
continue with `PR-SCOPE: NOT ASSESSED — [input]` noted in the index draft.

### Step 4c: Determine Design Order

Combine dependency sort + priority tier to produce the final design order:
1. MVP Foundation systems first
2. MVP Core systems second
3. MVP Feature systems third
4. Vertical Slice Foundation/Core systems
5. ...and so on

This is the order the team should write PRDs in.

---

## Phase 5: Create Systems Index (Write)

### Step 5a: Draft the Document

Using the template at `.claude/docs/templates/features-modules-index.md`, populate the
systems index with all data from Phases 2-4:
- Fill the enumeration table
- Fill the dependency map
- Fill the recommended design order
- Fill the high-risk systems
- Fill progress tracker (all systems "Not Started" initially, unless PRDs already exist)

### Step 5b: Approval

Present a summary of the document:
- Total systems count by category
- MVP system count
- First 3 systems in the design order
- Any high-risk items

**At `automation: collaborative`** — ask: "May I write the systems index to
`design/prd/features-modules-index.md`?" Wait for approval. Write the file only after
"yes."

**At `automation: guided`** — a **new** index gets the same "May I write …?"
question, because `.claude/docs/automation-modes.md` has `guided` ask "May I
write?" for new files. When the index already exists, present the summary above,
name the destination (`design/prd/features-modules-index.md`), and write the update without
waiting for an explicit "yes". Say what you wrote afterwards.

**Review mode check** — apply before spawning CD-SYSTEMS:
- `solo` → skip. Note: "CD-SYSTEMS skipped — Solo mode." Proceed to Step 5c.
- `lean` → skip (not a PHASE-GATE). Note: "CD-SYSTEMS skipped — Lean mode." Proceed to Step 5c.
- `full` → spawn as normal.

**After the systems index is written, spawn `product-director` via `Agent` using gate CD-SYSTEMS (`.claude/docs/director-gates/pd-feature-coherence.md`).**

Pass: systems index path; product pillars and core value proposition — from `design/prd/product-concept.md`, or at `minimal` the pitch and "what they feel" line of `design/product-brief.md`, which has no pillars; the priority tier assignments for every tier (MVP / Vertical Slice / Alpha / Full Vision); and the high-risk and bottleneck systems from the dependency map.

Present the assessment. If REJECT, revise the system set with the user before PRD authoring begins. If CONCERNS, show them and use `AskUserQuestion`: `Revise the system set` / `Accept — record them in the index` / `Discuss further`. On *Revise*, rework the affected systems with the user and ask again before re-writing the index. On *Accept* — the option names the edit, so choosing it is the ask — record them in the systems index as a `> **Creative Director Note**`
placed **directly beneath the `## Priority Tiers` table**, naming the tier each
concern applies to — e.g. `> **Creative Director Note** (MVP): …`.
`templates/features-modules-index.md` has a Priority Tiers *definition table*, not a
section per tier, so there is no "top of the tier section" to write to — do not
direct the technical-writer to one. If NOT ASSESSED [missing input], it is not an APPROVE
(`.claude/docs/director-gates.md`): name what was missing, then supply it and
re-run the gate, or ask before recording `> **Creative Director Note**:
CD-SYSTEMS NOT ASSESSED — [input]` in the same place.

### Step 5c: Update Session State

After writing, create `production/session-state/active.md` if it does not exist, then update it with:
- Task: Systems decomposition
- Status: Systems index created
- File: design/prd/features-modules-index.md
- Next: Design individual system PRDs

**Verdict: COMPLETE** — systems index written to `design/prd/features-modules-index.md`.
If the user declined: **Verdict: BLOCKED** — user did not approve the write.

---

## Phase 6: Design Individual Systems (Handoff to /saas-design-system)

This phase is entered when:
- The user says "yes" to designing systems after creating the index
- The user invokes `/saas-map-features [system-name]`
- The user invokes `/saas-map-features next`

### Step 6a: Select the System

- If a system name was provided, find it in the systems index
- If `next` was used, pick the highest-priority undesigned system (by design order)
- If the user just finished the index, ask:
  "Would you like to start designing individual systems now? The first system in
  the design order is [name]. Or would you prefer to stop here and come back later?"

Use `AskUserQuestion` for: "Start designing [system-name] now, pick a different
system, or stop here?"

### Step 6b: Hand Off to /saas-design-system

Once a system is selected, invoke the `/saas-design-system [system-name]` skill.

The `/saas-design-system` skill handles the full PRD authoring process:
- Gathers context from product concept, systems index, and dependency PRDs
- Creates a file skeleton immediately
- Walks through all 8 required sections one at a time (collaborative, incremental)
- Cross-references existing docs to prevent contradictions
- Routes to specialist agents for domain expertise
- Writes each section to file as soon as it's approved
- Runs `/saas-design-review` when complete
- Updates the systems index

**Do not duplicate the /saas-design-system workflow here.** This skill owns the systems
*index*; `/saas-design-system` owns individual system *PRDs*.

### Step 6c: Loop or Stop

After `/saas-design-system` completes, use `AskUserQuestion`:
- "Continue to the next system ([next system name])?"
- "Pick a different system?"
- "Stop here for this session?"

If continuing, return to Step 6a.

---

## Phase 7: Suggest Next Steps

After the systems index is created (or after designing some systems), present next actions using `AskUserQuestion`:

- "Systems index is written. What would you like to do next?"
  - [A] Start designing PRDs — run `/saas-design-system [first-system-in-order]`
  - [B] Run `/saas-gate-check systems-design` — the Concept → Systems Design gate; offer this only while `project.stage` is still Concept
  - [C] Run `/saas-gate-check technical-setup` — the Systems Design → Technical Setup gate, once the MVP systems have PRDs
  - [D] Stop here for this session

**The gate-check option ([C]) is worth knowing about**: `/saas-gate-check technical-setup` checks that the Systems Design phase's required artifacts exist and runs the phase-gate directors before you commit to architecture. CD-SYSTEMS and TD-SYSTEM-BOUNDARY are this skill's own gates — they run here, in `full` review mode, not in `/saas-gate-check`.

After any individual PRD is completed:
- "Run `/saas-design-review design/prd/[system].md` in a fresh session to validate quality"
- "Run `/saas-gate-check technical-setup` when all MVP PRDs are complete"

---

## Collaborative Protocol

**Applies in `collaborative` mode (the default).** For `guided` and
`autonomous` modes, see `.claude/docs/automation-modes.md` — the rules below
describe what collaborative mode requires, not universal behavior.

This skill follows the collaborative design principle at every phase:

1. **Question -> Options -> Decision -> Draft -> Approval** at every step
2. **AskUserQuestion** at every decision point (Explain -> Capture pattern):
   - Phase 2: "Missing systems? Combine or split?"
   - Phase 3: "Dependency ordering correct?"
   - Phase 4: "Priority assignments match your vision?"
   - Phase 5: "May I write the systems index?"
   - Phase 6: "Start designing, pick different, or stop?" then hand off to `/saas-design-system`
3. **"May I write to [filepath]?"** before every file write
4. **Incremental writing**: Update the systems index after each system is designed
5. **Handoff**: Individual PRD authoring is owned by `/saas-design-system`, which handles
   incremental section writing, cross-referencing, design review, and index updates
6. **Session state updates**: Write to `production/session-state/active.md` after
   each milestone (index created, system designed, priorities changed)

**Never** auto-generate the full systems list and write it without review.
**Never** start designing a system without user confirmation.
**Always** show the enumeration, dependencies, and priorities for user validation.

## Context Window Awareness

If context reaches or exceeds 70% at any point, append this notice:

> **Context is approaching the limit (≥70%).** The systems index is saved to
> `design/prd/features-modules-index.md`. Open a fresh Claude Code session to continue
> designing individual PRDs — run `/saas-map-features next` to pick up where you left off.

---

## Recommended Next Steps

- Run `/saas-design-system [first-system-in-order]` to author the first PRD (use design order from the index)
- Run `/saas-map-features next` to always pick the highest-priority undesigned system automatically
- Run `/saas-design-review design/prd/[system].md` in a fresh session after each PRD is authored
- Run `/saas-gate-check technical-setup` when all MVP PRDs are authored and reviewed
