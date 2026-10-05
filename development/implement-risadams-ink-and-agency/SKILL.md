---
name: implement
category: codebase-build
description: Build a piece of work (ticket, spec, or free-form request) through a tunable pipeline — test-first, verify, review, and track — where every phase can be skipped or tuned. Use when the user wants to actually build something, from a throwaway prototype to a CCB-gated feature.
codex-short-description: "Build through a tunable pipeline (every phase skippable)"
disable-model-invocation: true
compatibility: claude-code codex opencode
---

# Implement

Build the work — but first agree **how much process** it deserves. A throwaway prototype and a production feature run the same skill; they differ only in which **phases** are on. The run plan is proposed once, tuned by the user, then executed predictably.

The Jira project / Confluence space keys come from memory when tracking is on; read them, don't ask (`reference_jira_default_project.md`, `reference_confluence_default_space.md`).

## The pipeline

Five phases. Each can be **on**, **off**, or **tuned**:

1. **Source** — where the work is defined: a Jira ticket, a `/plan-to-spec` page, or free-form from the conversation.
2. **Test-first** — drive `/tdd` (red → green) at pre-agreed seams. *Off* = build directly, no tests.
3. **Verify** — typecheck + run tests (single files during, full suite at end). *Off* = no test/type setup to run.
4. **Review** — `/code-review` (Standards + Spec axes) of the working diff. *Off* = skip review.
5. **Track** — commit; open an MR; move the ticket. Tunable down to *commit only*, or *nothing* (prototype).

## Step 1 — Propose the run plan

Before building anything, **detect a preset** from the context and present the run plan as an editable list. The user edits any line or names a preset; you don't build until they approve.

**Presets:**

| Preset | Test-first | Verify | Review | Track |
| :--- | :--- | :--- | :--- | :--- |
| `prototype` | off | off | off | nothing (or commit only) |
| `standard` | at key seams | typecheck + tests | code-review | commit + MR |
| `full` | TDD throughout | typecheck + full suite | code-review | commit + MR + move ticket |

**Auto-detect** the starting preset:

- No test tooling in the repo, a `spike`/`scratch`/`prototype` path or explicit "quick/throwaway" → **`prototype`**.
- A Jira key or spec as the source, in a repo with tests + CI → **`full`**.
- Otherwise → **`standard`**.

Present it like this, and invite edits:

```text
Run plan (auto-detected: standard — edit any line, or say a preset):
- Source:     PRJ-1490 (Jira ticket)
- Test-first: TDD at the ExportService seam
- Verify:     typecheck + test suite
- Review:     code-review (Standards + Spec)
- Track:      commit + MR   (not moving the ticket)
```

Confirm seams here if Test-first is on (that's `/tdd`'s pre-agreement, pulled forward). Once approved, the plan is fixed for the run — state it back in one line and proceed.

## Step 2 — Execute the enabled phases

Run only the **on** phases, in order, honouring each tuning:

- **Test-first on** → work in **vertical slices** via `/tdd`: one seam, one failing test, minimal code to pass, repeat. Off → build the slice directly.
- **Verify on** → typecheck and run single test files as you go; run the full suite once at the end. Off → skip (and don't invent a test command that doesn't exist).
- **Review on** → **commit first, then** run `/code-review` against the branch point once the build is green. `code-review` diffs `<fixed-point>...HEAD`, which excludes staged and working-tree changes — reviewing before any commit exists hands both axes an empty diff and produces a clean report of nothing. Where Track is `nothing`, make an interim commit for the review and say so, or skip Review; don't run it against uncommitted work.
- **Track** → per the tuning: `commit only` stops at a commit on the current branch; `MR` also drafts one (delegate to `/mr-draft` if installed); `move ticket` transitions the Jira issue. `nothing` leaves the work uncommitted for the user to inspect.

Refactoring belongs to the **Review** phase, not the build loop (per `/tdd`).

## Step 3 — Close out

Report what ran and what was skipped, explicitly — a skipped phase is a stated outcome, not a silent omission:

```text
Done — ran: TDD (3 slices), verify (suite green), code-review.
Skipped: MR (track = commit only, per run plan).
Committed a1b2c3d on feature/csv-export-v2.
```

If Review surfaced findings, list them before the close-out so the user decides what to address now vs. later.

## Rules

- **Agree the plan before building.** The run plan is the one mandatory checkpoint; never start Phase 2 before the user approves Phase 1.
- **A skipped phase is reported, never hidden.** The close-out names every off phase so "no tests" is a visible decision, not an accident.
- **Don't fabricate a phase's tooling.** Verify off means there's nothing to run; don't invent a test command. Track = nothing means don't commit.
- **One preset is a starting point, not a cage.** The user can tune any single line without leaving the preset.
- **Reuse, don't reimplement.** Test-first is `/tdd`; review is `/code-review`; MR drafting is `/mr-draft`. This skill orchestrates them.
- **Confirm the work item back before building.** A bare `#2` or `PRJ-2` resolves against whatever numbered list is in view — a todo file, a checklist, the wrong project — and it resolves confidently, so the mistake only surfaces once work has started. Echo the resolved key *and its title* in the run plan.
- **One work item per run, one run per checkout.** Parallel `/implement` sessions in the same working directory share one index, one HEAD, and one stash: commits land on the wrong branch and stashes disappear. Use separate worktrees for parallelism, and clear context between tickets rather than batching them.
- **Committing is not completing.** The run ends at the commit (plus whatever Track is tuned to). It does not tick acceptance criteria, and it does not act on `code-review` findings — those are reported for the user to decide on. When Track doesn't include `move ticket`, say plainly that the ticket is still open.

> **Host portability:** tool names follow Claude Code conventions; on other hosts map by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/implement.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
