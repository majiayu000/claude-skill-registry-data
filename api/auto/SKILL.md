---
name: auto
description: Non-interactive pipeline driver — chains /sdd:start → /sdd:spec → /sdd:plan → /sdd:implement → /sdd:commit → /sdd:mr without pausing, then stops once the MR is open (before /sdd:close). Never runs /sdd:close or /sdd:mr-address.
argument-hint: "<ticket-or-text>"
allowed-tools: Read, Bash(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py:*), Bash(git rev-parse:*), Bash(ls .specwork:*), Bash(cat .specwork/_spec/*), Bash(cat .specwork/_state/*)
---

# Auto Pilot

Drive the SDD pipeline end-to-end for a single ticket or free-text description,
without asking the developer to fire each step by hand. For trivial/focused work
the pipeline is deterministic; `/sdd:auto` runs it and only pauses at the Open
Questions gate, which genuinely needs a human.

This skill does **not** reimplement the pipeline. It invokes the existing skills
in order and enforces the gates between them.

---

## Core Rule

**Auto mode runs straight through to the MR.** It chains `/sdd:implement` → `/sdd:commit` → `/sdd:mr` with no pause, then ends once the MR is open. It must **never** run:

- `/sdd:close` — deletes the branch; that is a post-merge, human decision.
- `/sdd:mr-address` — needs human review comments that do not exist yet.

---

## Use Cases

```bash
/sdd:auto PROJ-15535                         # a Jira ticket
/sdd:auto "add a /health endpoint to the API" # a free-text description
```

---

## What It Does

| Step | Action | Gate |
|------|--------|------|
| 1 | Pipeline entry (`/sdd:start` only when needed) | **Pipeline exists + same work (matching ticket / no arg): continue, skip `/sdd:start`. Pipeline exists + different work: hard stop (pause/close first).** No pipeline + no ticket/description: hard stop. No pipeline + input present: run `/sdd:start` and ask branch A/B/C |
| 2 | `/sdd:spec` — draft the spec from source | — |
| 3 | **Open Questions gate** | **hard stop** if unresolved |
| 4 | `/sdd:plan` — discover targets, draft plan | — |
| 5 | `/sdd:implement` — repeat until every plan target is done | — |
| 6 | `/sdd:commit` — coverage gate + semantic commit (auto-continues to MR) | — |
| 7 | `/sdd:mr` — push and open/update the MR, then **STOP** | — |

---

## Step 1 — Start

Enable non-interactive mode for this run:

```bash
export SDD_NON_INTERACTIVE=1
```

Then detect whether a pipeline already exists:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py precheck
```

- If precheck **fails** (no active pipeline):
  - **Required-input guard (HARD STOP):** if `$ARGUMENTS` is empty (after
    trimming whitespace), there is nothing to start from — **do not run
    `/sdd:start`, do not create a branch, do not initialize `.specwork/`**. Stop
    immediately and tell the user:

    ```text
    ✗ Nothing to start. /sdd:auto needs a ticket key or a description.

      /sdd:auto PROJ-123
      /sdd:auto "add a /health endpoint to the API"
    ```

  - Otherwise, run `/sdd:start` with the full argument (`$ARGUMENTS`) and force
    branch confirmation (A/B/C).
- If precheck **passes** (pipeline already active), do **not** silently continue
  it. First decide whether `$ARGUMENTS` refers to the *same* work or to
  *different* work (the **active-pipeline guard** below). Only continue when it
  is the same work; otherwise stop.

Do not reinitialize `.specwork/` when a pipeline is already active.

### Active-pipeline guard (HARD STOP on different work)

When a pipeline is already active, resolve what it is:

```bash
ACTIVE_SLUG="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py resolve-slug)"
ACTIVE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
```

Then classify `$ARGUMENTS` and decide. A **ticket key** is the leading token of
`$ARGUMENTS` matching `^[A-Z][A-Z0-9]+-[0-9]+$`; anything else is free text:

| `$ARGUMENTS` | Meaning | Action |
|--------------|---------|--------|
| empty | continue the active pipeline | **continue** → skip `/sdd:start`, go to `/sdd:spec` |
| a ticket key that equals `$ACTIVE_SLUG` (case-insensitive) | same work | **continue** → skip `/sdd:start`, go to `/sdd:spec` |
| a ticket key that differs from `$ACTIVE_SLUG` | different work | **HARD STOP** |
| free text (not a ticket key) | cannot match → treat as different work | **HARD STOP** |

"Continue" means the same as before: skip `/sdd:start`, keep the current
branch/artifacts, and go straight to `/sdd:spec`.

On **HARD STOP**, write nothing and tell the user (fill in the real slug/branch):

```text
✗ There is an active pipeline for <ACTIVE_SLUG> (branch <ACTIVE_BRANCH>).
  You asked to start different work: "<$ARGUMENTS>".

  Before starting something new:
    • /sdd:pause   — stash <ACTIVE_SLUG> to resume it later
    • /sdd:close   — close it if it is merged or abandoned

  Want to keep going on <ACTIVE_SLUG>? Re-run with no argument.
```

Never guess past this — do not run `/sdd:spec` or anything downstream on a HARD STOP.

Then resolve the slug for the gates below:

```bash
SLUG="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py resolve-slug)"
```

---

## Step 2 — Spec

Run `/sdd:spec` (draft mode — no arguments). It writes the spec from `source.md`
using the stack-aware template and runs triage.

---

## Step 3 — Open Questions Gate (HARD STOP)

The only hard stop in auto mode. Drafting commonly leaves unresolved Open
Questions; auto mode must not guess past them.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py check-oqs "$SLUG"
```

If the exit code is non-zero (unresolved OQs exist), **stop** and tell the user:

```
BLOCKING — unresolved Open Questions in the spec.

Resolve them in `<abs>/.specwork/_spec/<slug>-spec.md`, then re-run /sdd:auto
(or continue manually with /sdd:plan).
```

Do **not** run `/sdd:plan` or anything downstream while OQs are open.

---

## Step 4 — Plan

Run `/sdd:plan`. It discovers target files and drafts the plan. (If the project is
small/obvious and `/sdd:plan` produces no plan, `/sdd:implement` falls back to inline
discovery — that is fine.)

---

## Step 5 — Implement

Run `/sdd:implement` repeatedly, once per focused step, until **every** target in
the plan is implemented. Each run validates its own inline tests. Do not commit
between steps — changes accumulate in the working tree.

---

## Step 6 — Commit

Run `/sdd:commit` directly after `/sdd:implement` — **no pause**. It stages the
accumulated changes, runs the test-coverage gate, and writes a semantic commit.
In non-interactive mode `/sdd:commit` continues automatically to `/sdd:mr`.

---

## Step 7 — MR, then STOP

Run `/sdd:mr`. It runs pre-push validation, pushes the branch, and opens or updates
the MR. **This is where auto mode ends.** Hand control back to the user for
review, merge, and close.

Print a short closing summary (branch, slug, MR link or manual URL) and stop.
Do **not** run `/sdd:close` or `/sdd:mr-address`.

---

## Rules

- Stop at the open MR — never `/sdd:close` or `/sdd:mr-address`.
- With no active pipeline and no ticket/description argument, hard stop at step 1 — never create a branch or `.specwork/` from empty input.
- With an active pipeline, only continue it when the argument is the same work (matching ticket key or no argument). If the argument is a different ticket or free text, hard stop and require `/sdd:pause` or `/sdd:close` — never silently spec over someone's in-progress pipeline.
- In non-interactive mode, continue automatically step-to-step without asking for confirmation.
- Only two pauses are allowed: (1) branch choice in `/sdd:start`, (2) unresolved Open Questions.
- If `.specwork/` is already initialized, `/sdd:auto` must skip `/sdd:start` entirely (no branch-choice pause in that case).
- The Open Questions gate (step 3) is the only hard stop.
- If any step fails, stop and surface the error — do not push past a failure.
- Do not skip a gate, and do not reorder steps.

---

## Requirements

- A ticket key or free-text description as the single argument.
- `python3` on PATH (the gates run through it).
- The same prerequisites as the underlying skills (`glab` for automatic MR
  creation is optional — `/sdd:mr` falls back to a manual URL).

---

## Related Skills

- `start`, `spec`, `plan`, `implement`, `commit`, `mr` — the steps this skill chains
- `test-design` / `test-impl` — optional; run by hand before `/sdd:auto` when a high-risk change warrants dedicated tests
- `handoff` — for delegating execution to another agent instead of driving it here
