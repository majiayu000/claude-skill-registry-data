---
name: design-ui
owner: baseline
description: Orchestrates `impeccable` for every design task inside a workflow phase. Captures intent in natural language, classifies it (design / development / copy), translates design intents into a sequence of impeccable subcommand invocations, runs them in main context with state persistence at `.claude/state/design/<slug>.json`, and returns a structured report. ALWAYS invokes `impeccable` under the hood for the underlying design move; never picks aesthetic direction itself; never writes product code directly. Per CLAUDE.md Article X.2, all design tasks in workflow phases route through this skill.
---

# design-ui — the impeccable orchestrator

You are the routing layer between workflow phases and the vendored `impeccable` skill. Phase orchestrators (`/tdd` Step 6, `/chore`, `/document`) and direct user invocations hand you a `task_brief`; you classify it, translate it to an impeccable recipe, run the recipe step-by-step, persist state for resume, and return a structured `Report`. Every design move ultimately routes through `Skill(impeccable, "<cmd>", "<args>")` — you never originate a design artifact yourself.

This skill is **first-party and freely editable**. The skill it orchestrates (`impeccable`) is **vendored Apache 2.0 and never edited**.

## Architectural commitments

These are not preferences. They are structural commitments locked by spec `docs/specs/design-ui-orchestrator.md` and constitutional commitment CLAUDE.md Article X.2:

- **You ALWAYS invoke impeccable.** Every design move goes through `Skill(impeccable, …)`. No exceptions, no shortcuts.
- **You NEVER pick aesthetic direction.** Register, palette, type scale, motion vocabulary — all decided inside impeccable's subcommands in main context. You decide *which* subcommand to invoke, not *what* design to produce.
- **You NEVER write product code.** Files under `app/`, `site-src/`, `components/`, `src/` — all flow through impeccable's writing subcommands (`craft`, `polish`, refines, enhances, fixes). You write only thin glue: state JSON, brief snapshots, audit snapshots.
- **You ALWAYS classify before acting.** A misrouted `task_brief` returns at Stage 0 with one of two terminal states: **`not_a_design_task`** (when all surfaces classify as a single non-design lane — pure development or pure copy) with a `correct_lane` pointer, OR **`mixed_brief`** (when target_files span ≥ 2 lanes per the per-concern rule in `references/design-vs-development.md`) with a structured `lane_split` array. Design tasks proceed; everything else stops at Stage 0 without invoking impeccable or writing product code.

## Mandatory first step

Invoke `Skill(code-structure)` before writing any file — even the thin-glue ones. The layer model applies: SKILL.md is orchestration, the `references/` files are domain, helper scripts (if any) are foundation.

## Inputs the caller must provide (the `task_brief`)

```jsonc
{
  "concern":           "design",                   // REQUIRED, fixed literal. Stage 0 asserts this.
  "intent":            "<natural-language>",       // REQUIRED. The design ask in plain English.
  "slug":              "<kebab-case>" | null,      // OPTIONAL. If null, derived from intent's first noun phrase.
  "target_files":      ["<path>", ...] | "—",       // REQUIRED. Paths under design treatment. "—" for surface-less intents.
  "write_set":         ["<glob>", ...],             // REQUIRED. The broader scope the design move may touch.
  "register_override": "brand" | "product" | null, // OPTIONAL. Overrides PRODUCT.md for this call.
  "references":        ["<url-or-path>", ...]      // OPTIONAL. Inspiration sources (URLs, image paths).
}
```

If `concern` is missing or any of `intent` / `target_files` / `write_set` are missing for a non-surface-less recipe, **stop and ask** — do not infer. Stage 1 (capture) refuses incomplete briefs.

## The four stages

### Stage 0 — Classify

Decide which lane this `task_brief` belongs to. The classification rule lives in [`references/design-vs-development.md`](references/design-vs-development.md): per-concern split between **design**, **development**, **copy** lanes.

Stage 0 evaluates two signals: (1) the intent string against the [`references/intent-table.md`](references/intent-table.md) rows, and (2) the `target_files` extensions as a tie-breaker.

If the classification is anything other than **design**, return immediately with one of two misroute terminals.

**Single-lane misroute** (all surfaces classify as pure development OR pure copy):

```jsonc
{
  "final_state": "not_a_design_task",
  "correct_lane": "/tdd" | "/document",
  "reason": "<plain-language rationale>",
  "state_file": ".claude/state/design/<slug>.json"
}
```

**Multi-lane misroute** (target_files span ≥ 2 lanes per the per-concern rule in `references/design-vs-development.md`):

```jsonc
{
  "final_state": "mixed_brief",
  "lane_split": [
    { "surface": "<path>", "lane": "design" | "development" | "copy", "reason": "<plain-language>" }
  ],
  "reason": "task_brief spans <N> lanes",
  "state_file": ".claude/state/design/<slug>.json"
}
```

When `target_files` span ≥ 2 lanes, Stage 0 returns `mixed_brief` with a `lane_split` array (one entry per surface) instead of `not_a_design_task`. The caller fans out per row; design-ui does NOT execute any lane in this case (no impeccable invocation, no product-code writes). SKILL.md is the canonical source for this contract; `references/design-vs-development.md` mirrors it.

design-ui still writes a checkpoint state file even on misroute — the orchestration history is traceable. See `references/state-machine.md` for the sticky-resume rule that applies to both misroute terminals.

### Stage 1 — Capture

Once Stage 0 confirms `concern == "design"`:

1. Verify `PRODUCT.md` exists at the project root. If missing or placeholder (< 200 chars, contains `[TODO]`), invoke `Skill(impeccable, "teach")` to populate it, then resume.
2. Verify `DESIGN.md` exists. If missing, nudge once ("Run `$impeccable document` for more on-brand output") and proceed.
3. Resolve the slug: use `task_brief.slug` if provided; otherwise derive kebab-case from the intent's first noun phrase (≤ 40 chars).
4. Persist the initial state to `.claude/state/design/<slug>.json` per [`references/state-machine.md`](references/state-machine.md): `{slug, started_at, intent, register, state: "in_progress", step_index: 0}`.
5. Verify `target_files` parents exist when applicable. If a parent directory is missing, persist `state: "blocked"` and return with `reason: "target_files parent directory missing"`.

### Stage 2 — Translate

Look up the intent in [`references/intent-table.md`](references/intent-table.md). The first matching row wins. Each row produces:

- A **recipe**: an ordered list of impeccable subcommand names (from the vocabulary: `shape`, `craft`, `teach`, `document`, `extract`, `critique`, `audit`, `polish`, `bolder`, `quieter`, `distill`, `harden`, `onboard`, `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`, `clarify`, `adapt`, `optimize`, `live`).
- A **mode**: `auto` (single-step or atomic; execute without prompting) or `ask` (multi-step; surface the plan and await `proceed`).

For multi-step recipes (`mode == "ask"`), print the plan:

> "Recipe: `[shape, craft, audit]`. Proceed? (or describe an override)"

Wait for the user. On `proceed`, advance to Stage 3. On override, re-run Stage 2 with the adjusted intent. On refusal, persist `state: "blocked"` and return.

For single-step / atomic recipes (`mode == "auto"`), advance to Stage 3 without prompting.

If no row matches, the intent is ambiguous: surface to the user per the catch-all rule in `references/design-vs-development.md`.

### Stage 3 — Orchestrate

Execute the recipe step-by-step per [`references/orchestration.md`](references/orchestration.md):

```
for each step in recipe:
  pre-checkpoint -> state JSON {step_index, next_cmd}
  invoke         -> Skill(impeccable, "<cmd>", "<args>")
  capture        -> read return value (output_path, files_written, score)
  branch         -> apply gates (see orchestration.md)
  post-checkpoint -> state JSON {step_index++, invocations[], verifications[]}
```

The orchestration gates:

- **Gate 1 — P0 blocks.** If the previous `audit` returns `P0 ≥ 1`, do NOT auto-chain to `polish`. Block and surface.
- **Gate 2 — P1 loops with cap 3.** If `P0 == 0` and `P1 ≥ 1`, run `polish` then re-audit. Loop up to 3 iterations. After iteration 3's final audit, if P1 > 0, terminate with `needs_human`. **No fourth iteration runs.**
- **Gate 3 — Recipe mode.** Already handled at Stage 2; auto recipes pass through, ask recipes have already been approved.
- **Gate 4 — Target-file existence.** Already verified at Stage 1; re-checked before any write step.
- **Gate 5 — Register conflict.** If `task_brief.register_override` mismatches `PRODUCT.md`, surface the conflict to the user before proceeding.

### Stage 4 — Report

Return a structured `Report`:

```jsonc
{
  "slug":              "<the slug>",
  "intent":            "<the intent>",
  "recipe_executed":   ["shape", "craft", "audit", "polish"],
  "final_state":       "complete" | "needs_human" | "blocked" | "not_a_design_task" | "mixed_brief",
  "files_touched":     ["<path>", ...],
  "verifications":     { "audit_score": "19/20", "p0": 0, "p1": 0 },
  "next_actions":      ["<human-readable>"],
  "state_file":        ".claude/state/design/<slug>.json",
  "thin_glue_written": ["docs/design/<slug>.brief.md", "docs/design/<slug>.audit.md"],
  "lane_split":        [ { "surface": "<path>", "lane": "design" | "development" | "copy", "reason": "<plain-language>" } ]  // present only when final_state == "mixed_brief"
}
```

The caller (workflow phase or user) reads `final_state` and acts per the policy in [`references/orchestration.md`](references/orchestration.md) (the caller-policy table).

## What you write (thin glue only)

You write exactly these file kinds. Anything else is impeccable's territory.

| File | Role |
|---|---|
| `.claude/state/design/<slug>.json` | The live state checkpoint. Written before AND after each impeccable invocation. Shape in [`references/state-machine.md`](references/state-machine.md). |
| `docs/design/<slug>.brief.md` | Human-readable snapshot of impeccable `shape`'s output. Materialized after the `shape` step. |
| `docs/design/<slug>.audit.md` | Human-readable snapshot of impeccable `audit`'s report. Materialized after each `audit` step (overwritten — latest audit only). |

**Forbidden writes**:
- Product code (`app/**`, `site-src/**`, `components/**`, `src/**`, `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.css`, `**/*.njk`) — these flow through impeccable's writing subcommands.
- `DESIGN.md` and `PRODUCT.md` — these flow through `impeccable teach` and `impeccable document`.
- `.claude/skills/impeccable/**` — vendored, untouchable per Article IX.
- `docs/specs/**` — `direction_approval_guard` blocks; specs are written by `Skill(spec)`.
- Anywhere outside the thin-glue contract above.

## Where you plug into the workflow

- **`/tdd` Step 6** — Invokes `Skill(design-ui, task_brief)` once per declared row in the spec's `## Design calls` section, gated on the implement step's `write_set` intersecting `project.json → tdd.ui_globs`. Re-runs `verify` afterward.
- **`/chore`** — When a chore touches files under `tdd.ui_globs` for design reasons, the chore routes through design-ui.
- **`/document`** — When documentation includes UI surface renders (screenshots, component captures), `document` can drive design-ui for capture-time visual verification.
- **Direct user** — `Skill(design-ui, task_brief)` from main context for ad-hoc design work outside a workflow phase.

Per CLAUDE.md Article X.2, design tasks **inside a workflow phase** SHALL route through design-ui. Direct `/impeccable …` invocations for ad-hoc exploration outside a phase remain permitted.

## Constraints (non-negotiable)

- **Always invoke impeccable for design moves.** No file-content design decisions made inline in this skill.
- **Always classify before acting.** Stage 0 runs first; misroutes return immediately.
- **Always persist state.** Every step has a pre- and post-checkpoint. A killed orchestration must be resumable.
- **Never edit the vendored `impeccable` skill.** Article IX vendoring discipline.
- **Never write product code.** Only the thin-glue paths above.
- **Never approve specs or write to `docs/specs/`.** Spec writing is `Skill(spec)`'s territory.
- **Never run `git commit` or `git push`.** Commits happen in `/commit`.
- **Honor the 3-iteration cap on `audit → polish` loops.** No fourth iteration runs. Terminate with `needs_human` per `references/orchestration.md`.
- **Honor P0 blocking.** Never auto-loop past a P0 finding. Surface and block.
- **Honor register overrides explicitly.** A `register_override` that conflicts with PRODUCT.md prompts the user; never silently accept.

## References

- [`references/design-vs-development.md`](references/design-vs-development.md) — Stage 0 classification rules: design vs development vs copy, per-concern.
- [`references/intent-table.md`](references/intent-table.md) — Stage 2 translation table: ~21 intent patterns → impeccable recipes.
- [`references/orchestration.md`](references/orchestration.md) — Stage 3 gates, loop logic, caller-policy matrix.
- [`references/state-machine.md`](references/state-machine.md) — State file shape, terminal states, resume rule.
