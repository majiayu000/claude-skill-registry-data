---
name: govern
description: 'Runs a substantial design decision through review and sign-off into an ADR, RFD or design doc. Use when the user wants a choice made and recorded ("should I X or Y", "ADR for X", "decide between A and B"). Not for auditing records (use gov-review).'
argument-hint: <decision to govern> [artifact:adr|rfd|design|auto] [rich]
allowed-tools: Agent(gov-router), Agent(gov-provenance-recorder), Agent(gov-critic-alternatives), Agent(gov-critic-reversibility), Agent(gov-critic-blast-radius), Agent(gov-critic-assumptions), Agent(gov-critic-quick), Agent(gov-discussion-synthesizer), Agent(gov-artifact-writer), AskUserQuestion, Read, Write, Edit, Bash(git rev-parse *), Bash(mkdir *), Bash(date *), Bash(printf *), Bash(mv *), Bash(gh pr view *), Bash(gh auth status *), Glob, Grep
---

# Govern — Decision Lifecycle Orchestrator

## Overview

Takes a development decision and runs it through a five-phase lifecycle — route the right artifact (or none), discuss it through an adversarial critic panel scaled to the decision's weight, gate it behind an explicit human sign-off, write the durable record to `docs/`, then link it to the commit/PR and recommend the next step. Every governed decision lands with AI-provenance attached and a human's name on it. An agent proposes; a human approves.

## When to Use

A substantial, ambiguous design or architecture choice — behavior, public API, data schema, a dependency swap, a module boundary, security posture, or anything hard to reverse with more than one defensible approach.

### When NOT to use

- Behavior-preserving refactors, objective improvements (warning removal, a speedup), dev-invisible tweaks — exempt; just build.
- Trivial one-line fixes or throwaway prototype/spike code — the artifact overhead loses.
- Auditing artifacts that already exist — use `gov-review`. Installing the policy block — use `gov-init`.

## Input

- `$ARGUMENTS` — the decision to govern (free text). If empty, ask the user what decision to govern; never guess.
- `artifact:adr|rfd|design|auto` — optional explicit artifact override. `auto` or absent lets the router choose.
- `rich` — optional flag requesting the richer ADR (MADR) variant.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **MAX_DISCUSS_ITERATIONS**: 3 | **MAX_PANEL_AGENTS**: 4 | **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **DECISIONS_DIR**: `docs/decisions/` | **RFCS_DIR**: `docs/rfcs/` | **DESIGN_DIR**: `docs/design/`
- **Default statuses**: ADR `proposed` | RFD `prediscussion` | design `draft`
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| Phase | Goal                                   | Details             | Loop?              |
| ----- | -------------------------------------- | ------------------- | ------------------ |
| 0     | Setup                                  | inline below        | —                  |
| 1     | Propose — route the artifact (or none) | `phases/propose.md` | —                  |
| 2     | Discuss — weight-scaled critic panel   | `phases/discuss.md` | max 3 (heavy only) |
| 3     | Decide — human sign-off gate           | `phases/decide.md`  | feedback loop      |
| 4     | Record — write durable artifact        | `phases/record.md`  | —                  |
| 5     | Enforce — link commit/PR, recommend    | `phases/enforce.md` | —                  |

### Phase 0: Setup (inline)

1. Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
1. Parse `$ARGUMENTS`: the decision text, an optional `artifact:` override (`adr`/`rfd`/`design`/`auto`), and the optional `rich` flag. Empty decision → AskUserQuestion; never guess.
1. Derive `task_name` = `<YYYY_MM_DD>_govern_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is a snake_case summary of the decision (max 20 chars). On same-day collision append `_v2`, `_v3`.
1. **Resume check** (before creating the directory) — read `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` if it exists:
   - **No file** → fresh task; proceed.
   - **Status `complete`, `completed` or `aborted_by_user`** → auto-suffix `_v2`/`_v3`, log the bump to chat, proceed fresh.
   - **Status `pending`, `running`, `blocked` or `failed`** → present a Resume gate via AskUserQuestion (`Resume` re-enters at the recorded `Phase`; `Restart` archives the dir to `<task_name>_archived_<YYYY_MM_DD_HHMMSS>/` and starts fresh; `New` suffixes `_v2`). The human sign-off in Phase 3 never auto-resumes — re-present it.
   - **An unfinished status, but the run is unattended or nobody can answer** → report the path, `Status` and `what_remains`, then stop. Leave the file untouched, because it still describes the earlier run.
1. Create `<PROJECT_ROOT>/.mz/task/<task_name>/`. Write `state.md` per the inline v2 contract (State Management below): first line `schema_version: 2`, then `Status: running`, `Phase: 0`, `PhaseName: setup`, `Started: <ISO>`, `Iteration: 0`, `FilesWritten: []`, `phase_complete: false`, `what_remains: []`, plus `Decision: <text>`, `ArtifactOverride: <value|auto>`, `Rich: <bool>`.
1. Dispatch `gov-provenance-recorder` to write `<PROJECT_ROOT>/.mz/task/<task_name>/provenance.md` for *this* run — pass the task dir, the authoring agent (`gov-artifact-writer`, the agent that will write the durable record), the exact model id, the current ISO timestamp, and the trigger origin (`user-prompt` for a direct `/govern`, `automation` when the governance policy directed this invocation). It initializes `human_signoff: pending`. Append `provenance.md` to `FilesWritten`.
1. Emit a setup block: task_name, decision summary, override, rich flag, provenance path + derived trigger.

Read `phases/propose.md` and proceed to Phase 1.

### Phase 1: Propose

Dispatch `gov-router` to run the two-gate selection and write `routing.md`. If `ARTIFACT: none` → record a one-line exemption note, keep provenance, update state, and **stop at Phase 1** (report to the user — no discussion, no gate). Otherwise draft the populated artifact into `<PROJECT_ROOT>/.mz/task/<task_name>/draft.md` and carry `WEIGHT` forward. See `phases/propose.md`.

### Phase 2: Discuss

Weight-scaled. `heavy` → four opus critics in one parallel message (manifest first), then `gov-discussion-synthesizer`; loop the draft against the synthesis up to `MAX_DISCUSS_ITERATIONS`, escalating at the cap. `light` → one `gov-critic-quick` pass whose output is the verdict. `ARTIFACT: none` never reaches here. See `phases/discuss.md`.

### Phase 3: Decide

The human sign-off gate — the whole point of the pipeline. This orchestrator (not a subagent) emits the verbatim `draft.md` plus the verdict and the AI-provenance block as a plan-style chat message, then a short Approve/Reject AskUserQuestion selector beneath it. Approve → stamp `human_signoff`, advance status, go to Phase 4. Reject → write nothing to `docs/`. Any other reply is feedback → revise and re-present. **No auto-approve bypass exists on this gate.** See `phases/decide.md`.

### Phase 4: Record

Dispatch `gov-artifact-writer` (only after sign-off is stamped) to write the durable `docs/<dir>/NNNN-slug.md` with sequential numbering, the embedded provenance fence, and an initial status from the configured vocabulary. Append the path to `FilesWritten`. See `phases/record.md`.

### Phase 5: Enforce

Detect git context (commit, branch, optional open PR — read-only), append a `## Provenance / Links` section to the artifact, advance status where appropriate, and recommend the next skill (never auto-invoke). Mark state `complete`, `what_remains: []`. See `phases/enforce.md`.

## Red Flags

- You drafted to `docs/` before the human sign-off gate passed, or while `provenance.md` still read `human_signoff: pending`.
- You routed from memory instead of dispatching `gov-router`, or skipped the discuss panel on a `heavy` decision.
- You auto-approved the Phase 3 gate, or treated critic consensus as the human's approval. There is no auto-approve here.
- You auto-invoked the recommended next skill in Phase 5 instead of recommending it.

## Verification

Each phase emits a visible block; the final enforce block lists the artifact path, status, sign-off signature, git links, and the recommended next step, with `state.md` marked `complete` and `what_remains: []`.

## References

- `${CLAUDE_SKILL_DIR}/references/artifact-router.md`: Gate A (is an artifact needed) and Gate B (which one) selection logic, the weight label and the routing output contract. `gov-router` reads it in full at Phase 1.
- `${CLAUDE_SKILL_DIR}/references/adr-nygard-template.md`: minimal four-section ADR template with a filled example. Read it in full at Phase 1 when the router picks `adr-nygard`; `gov-artifact-writer` reads it again at Phase 4.
- `${CLAUDE_SKILL_DIR}/references/adr-madr-template.md`: rich MADR template for decisions with three or more options, with a filled example. Read it in full at Phase 1 when the router picks `adr-madr`; `gov-artifact-writer` reads it again at Phase 4.
- `${CLAUDE_SKILL_DIR}/references/rfd-template.md`: RFD template with the fixed six-state lifecycle and practice notes. Read it in full at Phase 1 when the router picks `rfd`; `gov-artifact-writer` reads it again at Phase 4.
- `${CLAUDE_SKILL_DIR}/references/design-doc-template.md`: informal design doc template with a filled skeleton. Read it in full at Phase 1 when the router picks `design`; `gov-artifact-writer` reads it again at Phase 4.
- `${CLAUDE_SKILL_DIR}/references/status-vocabularies.md`: status sets per artifact type and why they are configurable. Grep it for the artifact type's set; `gov-artifact-writer` reads it at Phase 4 to initialize the status, and `gov-review` reads it for status validity.
- `${CLAUDE_SKILL_DIR}/references/agdr-provenance-block.md`: canonical provenance fence with its fields, delimiters and `trigger` values. Only the `gov-provenance-recorder` agent reads it, in full, when it writes `provenance.md` in Phase 0; no phase file opens it.

## Error Handling

Detect → escalate via AskUserQuestion → never guess. Empty decision, an unreadable reference/template, an agent returning `BLOCKED` (retry once, then escalate), and `MAX_DISCUSS_ITERATIONS` hit without convergence (offer accept-with-unresolved / guidance / abort) all escalate. Always save state before dispatching agents.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.

Append every produced artifact to `FilesWritten` (routing.md, provenance.md, draft.md, discuss/discussion files, the `docs/` artifact). Record `human_signoff` only after the Phase 3 gate. Never rely on conversation memory for cross-phase state — context compaction destroys specific paths and decisions.
