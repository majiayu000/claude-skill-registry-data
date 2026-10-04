---
name: map
description: >-
  Codebase orientation for an unfamiliar or large repo — "map this before I
  work in it." Fans out read-only Explore sub-agents that navigate the code
  (keyless — grep/glob/read, no embeddings to go stale) along the order that
  matters: entry points, build/test/lint commands, architecture and key
  abstractions, conventions and gotchas, test layout. Distills the findings
  into a lean AGENTS.md at the repo root — the cross-tool standard file many
  agents auto-load — where every claim points to a real file and nothing
  survives that isn't load-bearing. Human-in-the-loop: it drafts, you approve,
  and it never writes or commits into your repo without an explicit yes. Stamps
  the map with date + commit so /map refresh regenerates only what went stale.
  Use before working in a repo you or the agent don't know — e.g. "/map",
  "/map the auth subsystem", "generate an AGENTS.md", "/map refresh". Run it
  upstream of feature or bugfix; for the end-of-session shipping gate use done.
---

# map — orient the agent to an unfamiliar codebase

`/map` — map the whole repo into a lean AGENTS.md at its root
`/map <subsystem>` — deep-map one area, into a scoped section
`/map refresh` — re-check an existing map and update only what went stale

Answer one question: **what would a competent engineer need to know before
touching this repo — and nothing more?** The strongest lever in agentic coding
isn't a smarter model, it's better orientation: an agent that knows the entry
points, the build commands, and the load-bearing conventions makes the right
change; one that guesses edits the wrong layer.

## Step 0 — Scope, and respect what exists

First, look before generating:

- **Existing agent files?** Check for `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`,
  `.github/copilot-instructions.md`. If one exists, this is a **REFRESH**, not a
  fresh write — read it, and update in place rather than duplicating. If a
  `CLAUDE.md` already carries the knowledge, offer to have `AGENTS.md` `@import`
  it instead of restating it. If the existing map carries a stamp and HEAD has
  moved past it, state the drift in one line when naming the mode — "map is N
  commits behind (touched: X, Y)" via `git rev-list --count` +
  `git diff --stat` over `<stamped-commit>..HEAD` — and offer the refresh
  unless this run already is one. A stamp that no longer resolves (rebase,
  shallow clone) is itself the staleness signal: report it and offer a fresh
  map. Staleness surfaces at every touch, never only when someone remembers
  `/map refresh`.
- **Size the repo** (`git ls-files | wc -l`, top-level layout) to scale the
  fan-out: a small repo maps in one pass inline; a large or polyglot one gets
  the full parallel sweep below.
- **A subsystem argument** (`/map the payment flow`) narrows every step to that
  area and produces a scoped section, not a whole-repo rewrite.

State which mode you picked (NEW / REFRESH / FOCUS) and why.

## Step 1 — Fan out along the read-first order

Dispatch read-only **Explore** sub-agents — one per lens — navigating by
`grep`/`glob`/`read` and following imports (no embeddings, no pre-index; always
fresh). This is the order practitioners converge on; run the lenses concurrently:

1. **Entry points & structure** — how does execution start (`main`, routes, CLI,
   handlers)? Top-level module/package layout and what each directory is *for*.
2. **Build / test / lint commands** — the knowledge no amount of code-reading
   reveals cheaply: the exact commands, from `package.json` scripts, `Makefile`,
   `pyproject.toml`, CI config. This is the single highest-value section.
3. **Architecture & key abstractions** — the main entities/types, the layers and
   their boundaries, how data flows through, the 3–5 files that matter most.
4. **Conventions & gotchas** — patterns the repo follows that deviate from the
   language default; footguns; "don't touch X"; implicit invariants a newcomer
   would break.
5. **Tests & fixtures** — how tests are organized, where fixtures/factories live,
   the command that runs a single test.

**Lossless hand-off:** each sub-agent writes its full findings to
`out/map/.work/<lens>.md` and returns a compact summary; you synthesize from
the files, not the relay. **Every finding names a file path** — a landmark
without a locator is a guess, and a guess in a map is worse than a blank.

## Step 2 — Distill to a LEAN AGENTS.md

Now cut. A bloated agent file gets *ignored* — the failure this skill must not
cause. For every candidate line apply the litmus test: **would removing it make
the agent make a mistake?** If not, cut it. Keep:

- What can't be guessed from reading code (commands, non-obvious conventions,
  gotchas, the "why" behind a structure).

Drop:

- Anything a `read` of the code trivially reveals, generic best-practices,
  restated language docs, and prose where a file path would do.

Prefer signatures and paths over paragraphs. Target well under ~200 lines —
shorter is stronger. Structure:

```markdown
# AGENTS.md
<!-- mapped 2026-07-09 @ <commit sha> · regenerate with /map refresh -->

## What this is
<one paragraph: what the project does, its shape>

## Build, test, run
<the exact commands — the part no one can guess>

## Architecture
<layers, key abstractions, data flow — each with a file path>

## Conventions & gotchas
<the load-bearing, non-default rules; the footguns>

## Landmarks
<entry points, core files, where tests/fixtures live — as paths>
```

## Step 3 — Approve, then write (never unprompted)

This file lands in **the user's repo**, so nothing is written without a yes:

1. Show the full drafted `AGENTS.md` in chat and invite edits — cuts as much as
   additions.
2. On approval, write it to the repo root (or update the existing file),
   stamped with today's `date +%F` and the current commit sha.
3. **Offer, don't perform, the commit** — draft a message per the repo's
   convention, but committing and pushing wait for an explicit yes, same as
   every other skill here.
4. Note that `feature` and `bugfix` will now read this file at the start of
   their runs — the map pays off downstream.

**Auto mode (under autopilot):** the draft→approve gate becomes
write-and-log — the map is written and stamped, the run's `log.md` records
what was generated and why, and committing still follows the run's charter.

On **REFRESH**: diff the map's claims against the current tree — flag sections
whose cited files moved, changed shape, or vanished; regenerate only those;
re-stamp. Don't rewrite what's still true. Command-shaped claims are re-proven
by running them, not by checking that the paths they mention still exist — a
command that no longer runs as claimed is stale even when every cited file is
in place; update the claim to what actually happened. Read-only commands
(test, lint, validate) run directly; state-changing ones (install, deploy,
migrate) only via an explicit dry-run flag — no dry-run mode means the claim
is marked unverified, never executed.

## Guardrails

- **A wrong map is worse than none.** A confident-but-stale line actively
  degrades the agent's reasoning. Every claim cites a file that exists; when
  unsure, leave it out and say so.
- **Lean or it's ignored.** The litmus test is non-negotiable — cut
  ruthlessly.
- **Never write or commit unprompted.** The output modifies the user's repo;
  draft → approve → write, and commit only on an explicit yes. (In auto
  mode, the autopilot charter is the prompt — the write is logged, not asked.)
- **Navigate, don't index.** Keyless by design — grep/glob/read/LSP, no
  embeddings to leak or go stale. Re-derived-but-fresh beats cached-but-wrong.
- **Evidence is a path.** No landmark, convention, or command without a locator
  or the command itself. The map is a set of verifiable pointers, not prose.
- **Respect what's there.** An existing AGENTS.md/CLAUDE.md is updated, not
  bulldozed; manual edits by the user are preserved.
