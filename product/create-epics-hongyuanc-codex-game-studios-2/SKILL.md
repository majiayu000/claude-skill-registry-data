---
name: create-epics
description: "Use when approved GDDs and architecture need translation into bounded, traceable implementation epics."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Do not add unlisted files or behavior; pause and request a new approval if scope expands.

# Create Epics

An epic is a named, bounded body of work that maps to one architectural module.
It defines **what** needs to be built and **who owns it architecturally**. It
does not prescribe implementation steps — that is the job of stories.

**Run this skill once per layer** as you approach that layer in development.
Do not create Feature layer epics until Core is nearly complete — the design
will have changed.

**Output:** `production/epics/[epic-slug]/EPIC.md` + `production/epics/index.md`

**Next step after each epic:** `$codex-game-studios:create-stories [epic-slug]`

**When to run:** After `$codex-game-studios:create-control-manifest` and `$codex-game-studios:architecture-review` pass.

---

## 1. Parse Arguments

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `.codex/studio.toml` and use its `review_mode` value
3. Map `review_mode = "phase-gated"` to lean optional-review depth; mandatory director gates still run. If config is unavailable, report it and use phase-gated behavior without writing configuration

See `../../../.codex/docs/director-gates.md` for the full check pattern.

**Modes:**
- `$codex-game-studios:create-epics all` — process all systems in layer order
- `$codex-game-studios:create-epics layer: foundation` — Foundation layer only
- `$codex-game-studios:create-epics layer: core` — Core layer only
- `$codex-game-studios:create-epics layer: feature` — Feature layer only
- `$codex-game-studios:create-epics layer: presentation` — Presentation layer only
- `$codex-game-studios:create-epics [system-name]` — one specific system
- No argument — ask: "Which layer or system would you like to create epics for?"

---

## 2. Load Inputs

### Step 2a — Summary scan (fast)

Search all GDDs for their `## Summary` sections before reading anything fully:

```bash
rg -n -A 5 '^## Summary' design/gdd/*.md
```

For `layer:` or `[system-name]` modes: filter to only in-scope GDDs based on
the Summary quick-reference. Skip full-reading anything out of scope.

### Step 2b — Full document load (in-scope systems only)

Using the Step 2a grep results, identify which systems are in scope. Read full documents **only for in-scope systems** — do not read GDDs or ADRs for out-of-scope systems or layers.

Read for in-scope systems:

- `design/gdd/systems-index.md` — authoritative system list, layers, priority
- In-scope GDDs only (Approved or Designed status, filtered by Step 2a results)
- `docs/architecture/architecture.md` — module ownership and API boundaries
- Accepted ADRs **whose domains cover in-scope systems only** — read the "GDD Requirements Addressed", "Decision", and "Engine Compatibility" sections; skip ADRs for unrelated domains
- `docs/architecture/control-manifest.md` — manifest version date from header
- `docs/architecture/tr-registry.yaml` — for tracing requirements to ADR coverage
- `../../../docs/engine-reference/[engine]/VERSION.md` — engine name, version, risk levels

Report: "Loaded [N] GDDs, [M] ADRs, engine: [name + version]."

---

## 3. Processing Order

Process in dependency-safe layer order:
1. **Foundation** (no dependencies)
2. **Core** (depends on Foundation)
3. **Feature** (depends on Core)
4. **Presentation** (depends on Feature + Core)

Within each layer, use the order from `systems-index.md`.

---

## 4. Define Each Epic

For each system, map it to an architectural module from `architecture.md`.

Check ADR coverage against the TR registry:
- **Traced requirements**: TR-IDs that have an Accepted ADR covering them
- **Untraced requirements**: TR-IDs with no ADR — warn before proceeding

Present to user before writing anything:

```
## Epic: [System Name]

**Layer**: [Foundation / Core / Feature / Presentation]
**GDD**: design/gdd/[filename].md
**Architecture Module**: [module name from architecture.md]
**Governing ADRs**: [ADR-NNNN, ADR-MMMM]
**Control Manifest Version**: [version/date]
**Engine Risk**: [LOW / MEDIUM / HIGH — highest risk among governing ADRs]
**GDD Requirements Covered by ADRs**: [N / total]
**Untraced Requirements**: [list TR-IDs with no ADR, or "None"]
**Acceptance Contract**: [GDD acceptance criteria represented by these TR-IDs]
**Test Evidence Contract**: [required automated/manual evidence by story type]
```

If there are untraced requirements:
> "⚠️ [N] requirements in [system] have no ADR. The epic can be created, but
> stories for these requirements will be marked Blocked until ADRs exist.
> Run `$codex-game-studios:architecture-decision` first, or proceed with placeholders."

Use `request_user_input` for one decision at a time:
- Prompt: "Shall I include Epic: [name] in the proposed changeset?"
- Options:
  - `[A] Yes, create it`
  - `[B] Skip this epic`
  - `[C] Pause — I need to write ADRs first`

---

## 4b. Producer Epic Structure Gate

**Review mode check** — apply before spawning PR-EPIC:
- `solo` → skip. Note: "PR-EPIC skipped — Solo mode." Proceed to Step 5 (write epic files).
- `lean` → skip (not a PHASE-GATE). Note: "PR-EPIC skipped — Lean mode." Proceed to Step 5 (write epic files).
- `full` → spawn as normal.

After all epics for the current layer are defined (Step 4 completed for all in-scope systems), and before writing any files, spawn `producer` through Codex custom-agent delegation using gate **PR-EPIC** (`../../../.codex/docs/director-gates.md`).

Pass: the full epic structure summary (all epics, their scope summaries, governing ADR counts), the layer being processed, milestone timeline and team capacity.

Present the producer's assessment.

If UNREALISTIC: offer to revise epic boundaries (split overscoped or merge underscoped epics). Revise and re-run the gate before writing.

If CONCERNS, use `request_user_input`:
- Prompt: "Producer raised concerns about the epic structure. How do you want to proceed?"
- Options:
  - `[A] Proceed as planned — I accept the producer's concerns`
  - `[B] Revise epic boundaries — split or merge as recommended`
  - `[C] Stop — I want to reconsider the scope`

If [A]: proceed to Step 5.
If [B]: revise epic definitions from Step 4 and re-run the producer gate.
If [C]: stop. Verdict: **BLOCKED** — user wants to reconsider epic scope.

Do not write epic files until the producer gate resolves.

---

## 5. Complete Proposed Changeset and Write

After every epic has been reviewed and the producer gate resolves, show one complete proposed changeset containing every `production/epics/[epic-slug]/EPIC.md` path and `production/epics/index.md`. Ask once for approval of that whole list. After approval, write only those files without per-file prompts. If a new path or material scope change becomes necessary, pause and request a revised changeset.

### `production/epics/[epic-slug]/EPIC.md`

```markdown
# Epic: [System Name]

> **Layer**: [Foundation / Core / Feature / Presentation]
> **GDD**: design/gdd/[filename].md
> **Architecture Module**: [module name]
> **Status**: Ready
> **Control Manifest Version**: [version/date]
> **Stories**: Not yet created — run `$codex-game-studios:create-stories [epic-slug]`

## Overview

[1 paragraph describing what this epic implements, derived from the GDD Overview
and the architecture module's stated responsibilities]

## Governing ADRs

| ADR | Decision Summary | Engine Risk |
|-----|-----------------|-------------|
| ADR-NNNN: [title] | [1-line summary] | LOW/MEDIUM/HIGH |

## GDD Requirements

| TR-ID | Requirement | ADR Coverage |
|-------|-------------|--------------|
| TR-[system]-001 | [requirement text from registry] | ADR-NNNN ✅ |
| TR-[system]-002 | [requirement text] | ❌ No ADR |

## Definition of Done

This epic is complete when:
- All stories are implemented, reviewed, and closed via `$codex-game-studios:story-done`
- All acceptance criteria from `design/gdd/[filename].md` are verified
- All Logic and Integration stories have passing test files in `tests/`
- All Visual/Feel and UI stories have evidence docs with sign-off in `production/qa/evidence/`

## Next Step

Run `$codex-game-studios:create-stories [epic-slug]` to break this epic into implementable stories.
```

### Update `production/epics/index.md`

Create or update the master index:

```markdown
# Epics Index

Last Updated: [date]
Engine: [name + version]

| Epic | Layer | System | GDD | Stories | Status |
|------|-------|--------|-----|---------|--------|
| [name] | Foundation | [system] | [file] | Not yet created | Ready |
```

---

## 6. Gate-Check Reminder

After writing all epics for the requested scope:

- **Foundation + Core complete**: These are required for the Pre-Production →
  Production gate. Run `$codex-game-studios:gate-check production` to check readiness.
- **Reminder**: Epics define scope. Stories define implementation steps. Run
  `$codex-game-studios:create-stories [epic-slug]` for each epic before developers can pick up work.

---

## Collaborative Protocol

1. **One epic decision at a time** — review inclusion one epic at a time, then approve the complete file list once
2. **Warn on gaps** — flag untraced requirements before proceeding
3. **Ask before writing** — one approval covers every path in the complete proposed changeset
4. **No invention** — all content comes from GDDs, ADRs, and architecture docs
5. **Never create stories** — this skill stops at the epic level

After all requested epics are processed:

- **Verdict: COMPLETE** — [N] epic(s) written. Run `$codex-game-studios:create-stories [epic-slug]` per epic.
- **Verdict: BLOCKED** — user declined all epics, or no eligible systems found.
