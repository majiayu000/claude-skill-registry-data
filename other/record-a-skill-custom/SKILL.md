---
name: record-a-skill-custom
description: Use when someone asks to record a demonstrated workflow, turn a screen recording or walkthrough into a skill, capture a process as a reusable skill, or check an existing skill before recording a new one.
argument-hint: [workflow-name-or-evidence-path]
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash(cp *), Bash(git status), Bash(git diff), Skill
---

## What This Skill Does

Turns evidence of a user performing a workflow — or a live guided walkthrough — into a
confirmed, reusable **workflow specification**: stable rules separated from runtime
data, decisions/dependencies/approvals/exceptions/validation requirements identified,
every material item tagged with provenance and confidence. Screens all evidence for
sensitive content before anything is written. Checks for overlap with existing skills
before proposing to build anything new. Hands the confirmed, approved specification to
`skill-builder`, which owns actual file construction, configuration, validation, and
testing.

This is a conceptual recreation of the "record a workflow from a demonstration" idea —
not a reproduction of any specific product's proprietary implementation.

**Responsibility boundary:**
- `record-a-skill-custom` owns: evidence intake, sensitivity screening, workflow reconstruction,
  provenance/confidence analysis, requirements extraction, the confirmed specification.
- `existing-asset-finder` owns: overlap discovery and the REUSE/EXTEND/MERGE/CREATE/STOP
  disposition. `record-a-skill-custom` never reimplements this search.
- `skill-builder` owns: final skill design, file construction, frontmatter/config,
  implementation, the full test suite, and the fidelity check against the specification.

Only an explicit `/record-a-skill-custom` invocation starts this workflow. Claude does not and
cannot auto-discover or auto-invoke it from natural language — `disable-model-invocation`
is set. If someone asks in conversation to "turn this into a skill" or "record what I
just did," Claude may point out that `/record-a-skill-custom` exists, but must not begin any
step of this workflow until the user types it explicitly.

For detailed screening-layer rules, the provenance/confidence taxonomy, the exact
handoff-package schema, and the full test/fidelity requirements, see
[reference.md](reference.md).

## Step-by-Step Workflow

### 1. Recommend an intake mode, then confirm it

Inspect `$ARGUMENTS` (a workflow name and/or an evidence path, if given) only to form a
recommendation — never to silently decide:

- **Mode A (pre-processed evidence)** — transcripts, written/narrated descriptions,
  screenshots (single or ordered/timestamped sequences), event logs (Markdown/text/
  CSV/JSON), example input files, example output files, SOPs/checklists/policies/
  templates, or an existing Claude Code skill (when proposing an update to it).
- **Mode B (live guided walkthrough)** — the user teaches the workflow interactively,
  one stage at a time, typing or pasting what they're doing as they do it.
- **Hybrid** — both modes together.

Raw `.mp4`/`.mov`/audio files and other unprocessed media are **not** valid direct
inputs. Never claim to have inspected such a file — ask the user to convert it into a
supported artifact (transcript, screenshots, description) first.

Show the recommended mode and why, then confirm via `AskUserQuestion`: options
**Mode A (pre-processed evidence)**, **Mode B (live guided walkthrough)**, and
**Hybrid (both)** — mark whichever step 1 determined as `(Recommended)`. Do not inspect
any evidence before this confirms. If the user later wants to add the other mode
mid-session, treat that as another confirmed scope change, not a silent expansion.

### 2. Authorize and inspect evidence

Only inspect sources the user has explicitly authorized. Never modify, move, rename, or
delete an original evidence file — read-only inspection of originals at all times.

### 3. Screen for sensitive content before any persistent write

Run the three-layer screening defined in [reference.md](reference.md) (pattern rules →
Claude semantic review → user confirmation for ambiguous findings) over every piece of
evidence before it is copied, quoted, or referenced in any file that will be written to
disk. Never reproduce a detected secret or sensitive value anywhere — chat, files, or
logs. Report only its category and a safe location reference.

### 4. Produce safe working copies

Once screening clears (or the user has approved specific redactions), copy — never
move — evidence into the task workspace. See Output Format below for the exact folder
layout. Every copy operation must show source and destination before running; see
Notes for the `Bash(cp *)` restrictions.

### 5. Reconstruct the workflow

Separate stable rules from runtime/example-specific data. Identify decisions,
dependencies, approvals, exceptions, and validation requirements. Abstract low-level
interface actions into reusable operational instructions — e.g. "click Status dropdown
→ select Pending → click Apply" becomes "filter records using the approved status
rule" — while retaining interface-specifics that are genuinely essential to completing
the workflow.

For every material rule, decision, stage, dependency, exception, validation
requirement, or boundary, record: **Statement, Provenance, Confidence, Evidence
reference, Confirmation status, Assumptions/conflicts/limitations**. See
[reference.md](reference.md) for the full provenance and confidence taxonomies — they
are two separate axes, not derived from each other.

If evidence conflicts, show the conflict and ask via `AskUserQuestion` which source is
authoritative — one option per conflicting source (mark the more likely one
`(Recommended)` only if the evidence itself suggests one; otherwise mark none). Never
silently pick one.

### 6. Evidence-sufficiency gate

The workflow may proceed only once the evidence establishes: goal, preconditions,
inputs, major stages, stable rules, runtime variables, decisions/branches,
dependencies, outputs, exceptions, approval boundaries, validation criteria, and
failure behavior. If gaps remain, run a focused follow-up interview (Mode A and/or
Mode B) targeting only what's missing — not a full re-interview of everything already
established.

### 7. Present the specification for confirmation

Show the reconstructed workflow specification and confirm via `AskUserQuestion`:
**Confirm this specification (Recommended)** / **I need to correct something**. If
corrections are needed, gather them as free text, update the specification, and ask
again. Do not proceed past this point on an unconfirmed specification.

### 8. Explicit scope selection — no default

Ask via `AskUserQuestion`, options:
- **Project** — `.claude/skills/<name>/`, this repository only.
- **Personal** — `~/.claude/skills/<name>/`, available across all the user's projects.

`record-a-skill-custom` may mark one `(Recommended)` with a stated reason (project: depends on
this repo's files/structure/business rules/one team; personal: useful across unrelated
projects, represents a general working method), but **no scope is inferred or
defaulted** — the user must actively pick. Before every CREATE, EXTEND, or MERGE
handoff, the user must explicitly choose project or personal scope and confirm the
exact target path. Never silently create or modify a personal-scope skill.

If a same-name skill exists in both scopes, detect it, explain which one takes
precedence, and ask via `AskUserQuestion`: **Reuse the existing one** / **Extend it** /
**Merge them** / **Stop here** — for a rename instead, use the question's free-text
option. Never silently create a shadowed or shadowing version.

### 9. Delegate the overlap check

Prepare a candidate asset profile (proposed name, purpose, triggers, inputs, major
operations, outputs, dependencies, boundaries) from the confirmed specification. Invoke
`existing-asset-finder` (via the Skill tool) with that profile — it is the sole
authority on overlap discovery across skills, docs, and database-backed assets. Consume
its returned disposition and evidence; never reproduce or override its search logic,
and do not call `skill-finder` by default (only if `existing-asset-finder` explicitly
flags a skill-specific uncertainty it can't resolve itself).

If `existing-asset-finder` is unavailable, fails, or returns an incomplete report,
report the failure and ask via `AskUserQuestion`: **Retry (Recommended)** /
**Use a limited fallback check** / **Stop here** — never silently fall back to a hidden
reimplementation.

### 10. Handle the disposition

- **REUSE** — stop; point the user to the existing asset.
- **EXTEND** — identify the capability gap against the confirmed specification; prepare
  an evidence-backed semantic diff (current behavior / required behavior / proposed
  changes / evidence+provenance / compatibility impact / affected files+tests /
  unresolved limitations); present it and ask via `AskUserQuestion`: **Approve these
  changes (Recommended)** / **I need changes to the proposal**. After approval, invoke
  `skill-builder` in **Mode 2** (audit) with the handoff package from
  [reference.md](reference.md). `record-a-skill-custom` never edits the existing skill
  directly.
- **MERGE** — present the merge target, overlap, compatibility impact, and affected
  files, then ask via `AskUserQuestion`: **Approve this merge (Recommended)** /
  **I need changes to the proposal** — before any handoff.
- **CREATE** — invoke `skill-builder` in **Mode 1** (build new) with the handoff
  package, including the confirmed scope and target path from step 8.
- **STOP** — halt the handoff and report the blocking reason clearly.

### 11. Prepare the skill-builder handoff package

Include the full test-requirements spec skill-builder's Step 6 must execute (the
10-category suite plus the fidelity gate) — see [reference.md](reference.md) for the
exact schema. `record-a-skill-custom` specifies these requirements; it never runs its own
separate test pass.

### 12. Report

Tell the user what was produced and where — mirroring `evidence-pack-builder`'s
end-of-run style: destination folder, files written, and a one-line status per
component (Available / Not provided / Not applicable), plus the final disposition and
handoff outcome.

## Output Format

```
output/record-a-skill-custom/<task-slug>/
  raw/                        # authorized copies of original evidence; no analysis (git-ignored)
  analysis/                   # redacted extracts, classifications, provenance+confidence
                               # records, conflicts, reconstruction notes
  workflow-specification.md   # the confirmed reusable workflow only
  _staging/                   # temporary extraction/reconstruction/redaction material (git-ignored)
```

After redaction, review, and explicit approval, `analysis/` and
`workflow-specification.md` may be written as persistent project artifacts.
`record-a-skill-custom` never runs `git add`, `git commit`, `git push`, or any publishing
operation. The user handles any later Git commit separately.

## Notes

- **Tool restrictions in practice:**
  - `Bash(cp *)` may only copy explicitly approved evidence into the confirmed task
    directory. Always resolve and display the source and destination before copying.
    Never use recursive copying against a broad, unresolved, home, repository-root, or
    filesystem-root path. Never overwrite an existing copy without showing the
    conflict and obtaining confirmation.
  - `Write` and `Edit` may operate only within the confirmed
    `output/record-a-skill-custom/<task-slug>/` workspace, or — after the separate scope,
    path, diff, and write approvals in step 10 — a `skill-builder`-controlled target.
    `record-a-skill-custom` itself must never edit the final generated/extended skill
    directly; that is always `skill-builder`'s action.
  - `Bash(git status)` and `Bash(git diff)` are inspection-only.
  - Known limitation: `allowed-tools`' `Bash(cp *)` pattern matches on command text, not
    semantics — it cannot technically prevent a recursive or broad-path `cp` invocation
    the way the rule above describes. That restriction is enforced by this instruction,
    not by the tool scoping itself.
  - Known limitation: the bare `Skill` entry in `allowed-tools` grants access to invoke
    any skill, not just `existing-asset-finder` and `skill-builder` as the workflow
    describes — `allowed-tools` currently has no confirmed syntax for scoping which
    named skill can be invoked. This boundary is enforced by the instructions in steps
    9-10, not by tool scoping.
- Never claim to have inspected unsupported media (raw video/audio) — ask for
  conversion first.
- Never reproduce a detected secret or PII value anywhere — category and safe location
  only.
- Require explicit confirmation before every persistent write.
- Copy evidence only — never move, rename, modify, or delete original source material.
- On conflicting evidence, surface the conflict and ask which source is authoritative
  — never silently pick one.
- Never override or reinterpret `existing-asset-finder`'s disposition.
- Never call `skill-finder` by default.
- Never promote a Low- or unresolved-confidence material item into a stable workflow
  rule without user confirmation; Medium/Low material items must be resolved or
  explicitly accepted as a limitation before handoff.
- Raw evidence and `_staging/` artifacts must never become runtime dependencies of the
  generated skill.
- This is a long, multi-gate, conversational skill by design — not meant to be fast or
  lightweight. Don't shortcut the confirmation gates to save turns.
- Clickable-question convention: every gate with a finite set of good answers uses
  `AskUserQuestion` (intake-mode confirm, conflicting-evidence source pick,
  specification confirm, scope choice, same-name collision handling, overlap-check
  retry decision, EXTEND/MERGE approval; see also `reference.md`'s Layer 3
  redact/exclude/retain confirmation). The workflow-name/evidence-path intake, any
  correction text, and the live Mode B walkthrough content itself stay free text —
  genuine content, not a finite menu.
