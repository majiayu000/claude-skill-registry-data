---
name: create-epics
description: "Translate approved CDDs + architecture into epics — one epic per architectural module. Defines scope, governing ADRs, technology risk, and untraced requirements. Does NOT break into stories — run /create-stories [epic-slug] after each epic is created."
argument-hint: "[system-name | layer: foundation|core|feature|presentation | all] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: technical-director
---

## Scope, decisions and exact evidence

Read `standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` from the
project root. Reuse original authorization only for its exact named paths, effects
and limits across roles/retries. Content agreement, writes, independent review,
ADR acceptance and Story/phase completion remain separate. Show a concrete draft
before asking about unresolved material choices or new effects; covered writes
need no repeated per-file or per-role permission.

Read/review-only never invokes a write entrypoint, including in memory. Report-only
may write its assigned new report, not inputs, indexes, session state, logs or T3
pointers. Each other effect needs existing scope or separate changeset authority.
No Memory Bank means the existing Story/review/conversation fallback, not activation.

Bind claims to original paths, full SHA-256 (64 hex), byte sizes, collection time
with timezone, source commit plus exact uncommitted/ignored/external identities.
Read actual bodies and minimum required direct/indirect evidence closure; retain
recoverable originals and disclose missing inputs. Resolve CDD DocKind/required
owner set and module semantic eight through `design/INSTRUCTIONS.md`, preserving
substantive aliases; headings, counts or existence cannot establish PASS.

Classify each meaningful choice as `covered`, `cdd-layer`, `no-adr`,
`documentation-update`, `adr-required` or `conflict`, with named requirement/owner,
existing TR-ID if assigned, exact Accepted ADR revision/section/scope or justified
no-ADR reason, affected paths/dependencies, evidence and action/owner/due phase.
Trust boundaries, public contracts, durable formats, state ownership and governing
architectural constraints require an Accepted decision or valid scoped exception
under existing governance before affected implementation starts/continues. Continue
independent work. Proposed, implemented, green tests, write approval and director
recommendations do not establish acceptance; historical approval needs exact input
and authority/scope match. Justified `cdd-layer`/`no-adr` waives no other readiness,
manifest or evidence prerequisite. The existing global Technical Setup minimum of
three Foundation ADRs in `workflow/workflow-catalog.yaml` remains a separate gate:
do not bypass it or manufacture ADRs to meet a count.

Absent, conflicting or ambiguous concept/domain evidence means Unknown. Continue
domain-independent checks; resolve the domain before applying its Game/Product
rules. Do not silently default to Game.

## User Guide

- When to use: Translate approved CDDs + architecture into epics — one epic per architectural module. Defines scope, governing ADRs, technology risk, and untraced requirements. Does NOT break into stories — run /create-stories [epic-slug] after each epic is created.
- Inputs: Command arguments: `/create-epics [system-name | layer: foundation|core|feature|presentation | all] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Create Epics

An epic is a named, bounded body of work that maps to one architectural module.
It defines **what** needs to be built and **who owns it architecturally**. It
does not prescribe implementation steps — that is the job of stories.

**Run this skill once per layer** as you approach that layer in development.
Do not create Feature layer epics until Core is nearly complete — the design
will have changed.

**Output:** `production/epics/[epic-slug]/EPIC.md` + `production/epics/index.md`

**Next step after each epic:** `/create-stories [epic-slug]`

**When to run:** After `/create-control-manifest` and `/architecture-review` pass.

**Domain detection.** Before loading CDDs, determine the project domain from
`design/cdd/`:
- **[游戏专用]** `game-concept.md` exists -> use player/system language,
  Engine Compatibility, engine risk, playtest/feel/UI evidence expectations.
- **[通用产品]** `product-concept.md` exists -> use user/module language,
  Technology or Stack Compatibility, stack risk, API/CLI/data/workflow evidence
  expectations.
- If both exist or neither exists, ask which domain this epic run should target.
  Do not mix game and product examples inside one epic file unless the project is
  explicitly hybrid.

---

## 1. Parse Arguments

Resolve the review mode once and store it for all gate spawns this run:
1. If `--review` was passed, require an explicit value of `full`, `lean` or `solo`.
2. Else read the actual `production/review-mode.txt` if present and require its
   value to be `full`, `lean` or `solo`.
3. Only when neither override nor global file is present, default to `lean`.

A missing/invalid explicit value or invalid selected global value requires correction
before gate dispatch. Report the actual source/value error; never silently fall back,
claim a skipped/completed gate, or infer approval from invalid mode input.
A valid explicit override takes precedence over the global file. Resolve only once.
See `standards/director-gates.md` for the full check pattern.

**Modes:**
- `/create-epics all` — process all systems in layer order
- `/create-epics layer: foundation` — Foundation layer only
- `/create-epics layer: core` — Core layer only
- `/create-epics layer: feature` — Feature layer only
- `/create-epics layer: presentation` — Presentation layer only
- `/create-epics [system-name]` — one specific system
- No argument — ask: "Which layer or system would you like to create epics for?"

---

## 2. Load Inputs

### Step 2a — Summary scan (fast)

Grep all CDDs for their `## Summary` sections before reading anything fully:

```
Grep pattern="## Summary" glob="design/cdd/*.md" output_mode="content" -A 5
```

For `layer:` or `[system-name]` modes: filter to only in-scope CDDs based on
the Summary quick-reference. Skip full-reading anything out of scope.

### Step 2b — Full document load (in-scope systems only)

Using the Step 2a grep results, identify which systems are in scope. Read full documents **only for in-scope systems** — do not read CDDs or ADRs for out-of-scope systems or layers.

Read for in-scope systems:

- `design/cdd/module-index.md` — authoritative system list, layers, priority
- In-scope CDDs only (Approved or Designed status, filtered by Step 2a results)
- `docs/architecture/architecture.md` — module ownership and API boundaries
- Accepted ADRs **whose domains cover in-scope systems only** — read the "CDD Requirements Addressed", "Decision", and "Engine Compatibility" (game) or "Technology Compatibility" / "Stack Compatibility" (product) sections; skip ADRs for unrelated domains
- `docs/architecture/control-manifest.md` — complete saved raw-byte SHA-256, byte size/path; retain readable date separately
- `docs/architecture/tr-registry.yaml` — for tracing requirements to ADR coverage
- `docs/engine-reference/[engine]/VERSION.md` (game) or `docs/reference/[stack]/VERSION.md` (product) — technology name, version, risk levels

Report: "Loaded [N] CDDs, [M] ADRs, technology: [engine or stack name + version]."

While reading each CDD, extract the domain-specific epic inputs:

- **[游戏专用]** Player Fantasy, Core Rules, Formulas, Tuning Knobs,
  Visual/Audio Requirements, and any playtest-sensitive acceptance criteria.
  Example: `combat-damage.md` may create an epic whose risk centers on damage
  formulas, hit reactions, animation timing, and engine physics callbacks.
- **[通用产品]** User Promise, primary workflow, Data Model, API/CLI contracts,
  permissions, integrations, configuration, and any latency-sensitive acceptance
  criteria. Example: `invoice-approval.md` may create an epic whose risk centers
  on approval state transitions, permission boundaries, API response contracts,
  audit logging, and migration safety.

---

## 3. Processing Order

Process in dependency-safe layer order:
1. **Foundation** (no dependencies)
2. **Core** (depends on Foundation)
3. **Feature** (depends on Core)
4. **Presentation** (depends on Feature + Core)

Within each layer, use the order from `module-index.md`.

---

## 4. Define Each Epic

For each system, map it to an architectural module from `architecture.md`.

Read current CDD/TR bodies and classify meaningful choices under all six dispositions.
Exact Accepted scope supports covered; named CDD/local reasons support cdd-layer/
no-adr. Missing links alone are not gaps. Required inputs, unassigned TRs, Proposed
required decisions, adr-required/conflict block affected implementation. With explicit
planning authority, create affected epics as Draft/Blocked with action/owner/
dependencies. Planning does not accept decisions or establish Story readiness;
independent epics continue.

Present to user before writing anything:

```
## Epic: [System Name]

**Layer**: [Foundation / Core / Feature / Presentation]
**CDD**: design/cdd/[filename].md
**Architecture Module**: [module name from architecture.md]
**Governing ADRs**: [ADR-NNNN, ADR-MMMM]
**Technology Risk**: [LOW / MEDIUM / HIGH — highest risk among governing ADRs]
**Requirement Dispositions**: [counts for all six; exact Accepted scope or named CDD/local reason]
**Unresolved Requirements**: [required missing input, adr-required/conflict or "None"]
**Planning Status**: [Ready for planning / Draft / Blocked with actual findings]
```

Add a short domain-specific scope note after the summary:

- **[游戏专用]** `Player-facing scope`: what the player can do, feel, see, or
  hear when the epic is complete. Include concrete examples such as "player
  attack resolves damage, hitstun, VFX, and HUD feedback in one frame-safe
  sequence."
- **[通用产品]** `User-facing scope`: what user workflow, API/CLI surface, data
  contract, or operational behavior is complete. Include concrete examples such
  as "user submits an invoice for approval, receives a stable response, and the
  audit log records the state transition."

For each unresolved required decision/input show disposition, missing evidence and
affected scope. Authorized Draft/Blocked planning may be saved but grants no
implementation readiness. Do not fabricate ADRs, active TR-IDs or manifest identity;
recommend owning repair/acceptance.

Ask: "Shall I create Epic: [name]?"
Options: "Yes, create it", "Skip", "Pause — I need to write ADRs first"

---

## 4b. Producer Epic Structure Gate

**Review mode check** — apply before spawning PR-EPIC:
- `solo` → skip. Note: "PR-EPIC skipped — Solo mode." Proceed to Step 5 (write epic files).
- `lean` → skip (not a PHASE-GATE). Note: "PR-EPIC skipped — Lean mode." Proceed to Step 5 (write epic files).
- `full` → spawn as normal.

After all epics for the current layer are defined (Step 4 completed for all in-scope systems), and before writing any files, spawn `producer` via Task using gate **PR-EPIC** (`standards/director-gates.md`).

Pass: the full epic structure summary (all epics, their scope summaries, governing ADR counts), the layer being processed, milestone timeline and team capacity.

Present the producer's assessment. If UNREALISTIC, offer to revise epic boundaries (split overscoped or merge underscoped epics) before writing. If CONCERNS, surface them and let the user decide. Do not write epic files until the producer gate resolves.

---

## 5. Write Epic Files

Show the epic and intended index effects as one named changeset. Reuse covered
authority; otherwise ask: "May I write the epic to
`production/epics/[epic-slug]/EPIC.md` and its described index row?"

After user confirms, write:

### `production/epics/[epic-slug]/EPIC.md`

```markdown
# Epic: [System Name]

> **Layer**: [Foundation / Core / Feature / Presentation]
> **CDD**: design/cdd/[filename].md
> **Architecture Module**: [module name]
> **Status**: [Ready for planning / Draft / Blocked — actual prerequisites/findings]
> **Stories**: Not yet created — run `/create-stories [epic-slug]`

## Overview

[1 paragraph describing what this epic implements, derived from the CDD Overview
and the architecture module's stated responsibilities]

## Domain Scope

**Domain**: [Game / Product]

Include only the row matching the detected domain:

- **[游戏专用] Player-facing result**: [what player action, feedback loop,
  balancing surface, or playtestable moment becomes available]
- **[通用产品] User-facing result**: [what workflow, API/CLI capability, data
  contract, integration, or operational path becomes available]
- **Technology risk focus**: [engine/stack APIs, runtime constraints, migration
  risks, or performance budgets that stories must respect]

## Governing ADRs

| ADR | Decision Summary | Technology Risk |
|-----|-----------------|-------------|
| ADR-NNNN: [title] | [1-line summary] | LOW/MEDIUM/HIGH |

## CDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-[system]-001 | [requirement text from registry] | ADR-NNNN ✅ |
| TR-[system]-002 | [requirement text] | [cdd-layer/no-adr reason OR adr-required/conflict] |

## Definition of Done

This epic is complete when:
- All stories are implemented, reviewed, and closed via `/story-done`
- All acceptance criteria from `design/cdd/[filename].md` are verified
- All blocking test evidence required by each story type passes
- Advisory manual, smoke, or walkthrough evidence is captured in the matching subdirectory under `production/qa/evidence/` or in `production/qa/smoke-*.md`

Add only the relevant domain-specific completion row:

- **[游戏专用]** Gameplay, feel, UI, and tuning outcomes have matching test,
  smoke, playtest, or sign-off evidence as required by their story types.
- **[通用产品]** API, CLI, data/migration, auth, workflow, integration, and
  deployment outcomes have contract, integration, command, migration, permission,
  or smoke evidence as required by their story types.

## Next Step

Run `/create-stories [epic-slug]` to break this epic into implementable stories.
```

### Update `production/epics/index.md`

Create/update the master index only if its path/effect is in scope; otherwise
report the pending action. Preserve actual Draft/Blocked status:

```markdown
# Epics Index

Last Updated: [date]
Technology: [name + version]
Domain: [Game / Product]

| Epic | Layer | System | CDD | Stories | Status |
|------|-------|--------|-----|---------|--------|
| [name] | Foundation | [system] | [file] | Not yet created | [actual planning Ready/Draft/Blocked] |
```

---

## 6. Gate-Check Reminder

After writing all epics for the requested scope:

- **Foundation + Core complete**:
  - **[游戏专用]** required for the Pre-Production → Production gate. Run
    `/gate-check production` to check readiness.
  - **[通用产品]** required for the Architecture / Pre-Implementation →
    Implementation gate. Run `/gate-check implementation` or the configured
    product-stage target to check readiness.
- **Reminder**: Epics define scope. Stories define implementation steps. Run
  `/create-stories [epic-slug]` for each epic before developers can pick up work.

---

## Collaborative Protocol

1. **One epic at a time** — present each epic definition before asking to create it
2. **Warn on gaps** — flag untraced requirements before proceeding
3. **Scope before writing** — reuse named approved epic/index changesets; ask only for new effects
4. **No invention** — all content comes from CDDs, ADRs, and architecture docs
5. **Never create stories** — this skill stops at the epic level

After all requested epics are processed:

- **Write operation: COMPLETE** — [N] epic(s) written; report [D] Draft / [B] Blocked /
  [R] Ready for planning and actual unresolved actions. Writing does not qualify
  affected implementation. Run `/create-stories [epic-slug]` within planning scope.
- **Verdict: BLOCKED** — user declined all epics, or no eligible systems found.

## Exact-byte check availability

Use available read-only tools to collect complete raw-file SHA-256/byte size without
normalizing line endings. If exact bytes/digest or a required dependency cannot be
read, report the affected check incomplete; do not substitute a date, text rendering,
short hash or file existence. Analysis invokes no write entrypoint.
