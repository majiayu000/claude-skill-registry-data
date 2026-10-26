---
name: spec
description: Scaffold a spec-driven plan pack under docs/todo/<domain>/<feature>/ for a bigger piece of work — setup interview, 010-stepped task files, a README hub, and companion docs (PROGRESS/QUESTIONS/SUMMARY/REVIEW) — and tear it down again when the work ships. Use when the user says `/spec`, `/spec done`, "set up a spec for this", or wants a docs/todo planning directory for a larger feature. NOT for a change that fits in one spec file — that is `/new-spec`. NOT for a one-line fix.
user-invocable: true
---

# /spec

Turn a bigger piece of work into a **plan pack**: a temporary feature directory under
`docs/todo/<domain>/<feature>/` holding a `README.md` hub, 010-stepped task files, and a small set of
companion docs. `/spec` sets the pack up (with a short structural interview); `/spec done` retires it
when the work has shipped.

This skill scaffolds and stops. It does not design the feature in depth and it never starts
implementation.

## `/spec` vs `/new-spec`

| | Use |
|---|---|
| `/new-spec` | One change, one spec file — `docs/todo/NNN-short-name.md`. Half a page. The default for anything bigger than a one-line fix. |
| `/spec` | Work that needs **more than one commit and more than one session**: several tasks, an ordering between them, decisions still open, possibly more than one agent. |

They compose. A plan pack normally **anchors on a `SPEC.md` inside the pack** —
`docs/todo/<domain>/<feature>/SPEC.md`, structured per the pack-structure reference; that file holds the
Problem / Goal / Non-goals / *What must NOT change* / Test plan; the rest of the pack holds the
breakdown, the status log and the open decisions. If no spec exists yet, write `SPEC.md` first (same
discipline as `/new-spec`, different location) and link it from the pack README. A standalone `docs/todo/NNN-*.md`
remains the home of **standalone** specs (a `/new-spec` change with no pack); a pack's spec never
goes there. A pack without an anchor spec is allowed but say so explicitly.

## Pack shape (summary)

- **Flat pack** (default): `README.md` hub + `PROGRESS.md` + `010-`, `020-`… task files.
- **Phased pack** (work spans releases/phases): `README.md` + `PROGRESS.md` at the root, then
  `phase1-<slug>/`, `phase2-<slug>/` dirs, each with its own README index and restarted `010-`
  numbering.
- **Companion docs** beside the hub — a fixed, allowed set: `SPEC.md` (the anchor spec),
  `PROGRESS.md` (live status), `QUESTIONS.md` (decisions), `SUMMARY.md` (owner-facing plain-English
  digest), `REVIEW.md` (evidence).
  Nothing else —
  `START/INFO/OVERVIEW/PLAN.md` are banned.

Full detail — directory trees, numbering, companion-doc roles, phase naming, the docs phase — is in
**[references/pack-structure.md](references/pack-structure.md)**. Read it before scaffolding.

## `/spec` — set up a pack

### Step 1 — Gather context (read first, don't ask what you can read)

- Read **[../../../CLAUDE.md](../../../CLAUDE.md)** and
  **[docs/system/rules/10-golden-rules.md](../../../docs/system/rules/10-golden-rules.md)** if they aren't already in
  context. This app places real orders with real money; that shapes every pack.
- Read the pack's `SPEC.md` if the pack already exists, or any related standalone spec in
  `docs/todo/`. If there is no anchor spec and the work warrants one, plan to write `SPEC.md`
  (per the pack-structure reference) as part of scaffolding — proceed without it only if the user says so.
- Scan `docs/todo/` for an existing domain dir that fits and for related prior packs. If a related
  pack exists, propose **extending** it instead of forking a new dir.
- Skim the code the work touches — enough to name concrete building blocks for the reuse table and
  to know which layer each task lands on (`frontend/` → `controllers/` → `services/` → `db/`).
- **Decide the money question up front.** Does anything in this pack touch order placement, closing,
  partial closes, position sizing, the risk governor, or the MT5/EA bridge? If yes, the pack is
  money-touching: `/safe-change` governs those tasks, and they need owner sign-off plus a demo
  session before they can be called done. Record it in the README header and per task.
- **Behaviour / performance / "what is it actually doing" packs: gather evidence.** Read-only-query
  the local SQLite trade DB and read `latest_logs/` for the numbers that justify the change — real
  trades, real frequencies, current values. Capture it in a `REVIEW.md`. A behaviour spec without
  evidence is a guess. Read-only means `SELECT` only; never write to the DB from a spec session.

### Step 2 — Setup interview (structural only, a few questions max)

Use `AskUserQuestion`, recommendation-first (`(Recommended)` suffix), one round or two. Ask only what
you can't infer:

1. **Domain dir** — propose the existing match; a new domain dir only if nothing fits.
2. **Feature dir name** — propose a slug from the spec/description.
3. **Shape** — flat vs phased dirs. Recommend flat unless the work clearly spans releases/phases.
4. **Scope boundary** — what is explicitly out of scope.
5. **Anchor spec** — confirm the pack gets a `SPEC.md` (the default), or that there deliberately
   isn't one; note any related standalone `docs/todo/NNN-*.md` it builds on.
6. **User-facing?** — if it changes anything the user reads in the app's About / Setup Instructions /
   Glossary pages, or anything that belongs in `CHANGELOG.md` or `docs/system/rules/`, plan a **docs phase** as
   the last phase (see references). Ask now so it isn't forgotten.
7. **Who reviews it?** — if the requester isn't the implementer, or the change is broad, plan a
   **`SUMMARY.md`** (plain-English digest).

Do not interrogate design decisions here — open decisions go in `QUESTIONS.md` for the user to answer
inline. Don't ask what the anchor spec or the code already answers.

### Step 3 — Draft the breakdown before writing files

Outline the pack as a list — each planned `0N0-<slug>.md` with a one-line summary, in dependency
order, plus which companion docs apply and which tasks are money-touching — and show it to the user
to confirm **before** scaffolding.

### Step 4 — Scaffold

Create the dir and fill the templates with **real content from the spec, interview, evidence and code
reading** — never lorem placeholders:

- `SPEC.md` per the pack-structure reference — the anchor: Problem / Goal / Non-goals / What must NOT
  change / Design / Test plan / Rollout / Verification. Written first; everything else references it.
- `README.md` from [templates/README.md.tpl](templates/README.md.tpl) — the onboarding block, what/why
  prose, doc index (every task + companion doc), decisions-locked table (with a Source column),
  building-blocks reuse table, out-of-scope, open questions. The header carries **Touches money**.
- `PROGRESS.md` from [templates/PROGRESS.md.tpl](templates/PROGRESS.md.tpl) — the shared status log,
  one row per task. Add it whenever more than one agent/session will touch the pack (default yes for
  anything non-trivial).
- Task files from [templates/task.md.tpl](templates/task.md.tpl) — Problem/scope from the draft;
  `Tests first (TDD)` / `What to do` / `Where` / `Acceptance` filled as far as honestly known. **Every
  task with a code surface names its tests before its steps**, per
  [docs/system/rules/40-testing.md](../../../docs/system/rules/40-testing.md) — including the negative control for each
  green assertion. A task whose tests can't be named isn't specced; flag it open.
- **Companion docs as applicable:** `QUESTIONS.md`
  ([template](templates/QUESTIONS.md.tpl)) when there are open decisions; `SUMMARY.md`
  ([template](templates/SUMMARY.md.tpl)) for an owner-facing digest; `REVIEW.md` for the Step-1
  evidence.
- For a pack that builds UI, put the user-facing strings the user must confirm (labels, copy) in
  `QUESTIONS.md` so they are the user's words, not the builder's — do not invent them silently.
- If phased: **all** numbered files live inside phase dirs, starting `phase1-<slug>/`. Each phase dir
  gets its own index from [templates/phase-README.md.tpl](templates/phase-README.md.tpl) with its
  gating condition; the feature-root `README.md` stays the single hub. If user-facing, the last phase
  is the **docs phase** (documents what shipped: CHANGELOG, in-app help, `docs/system/rules/`).

### Step 5 — Hand off

Print the pack tree, then:

- If there's a `QUESTIONS.md`, say plainly that the user answers it inline before implementation
  starts.
- If any task is money-touching, name those tasks and say they route through `/safe-change` and need
  a demo session.
- Commit and push the pack to the notes repo (`git private add todo/<domain>/<feature>`,
  `git private commit -F <msgfile>`, `git private push`). See the rule below.

**Stop.** The user holds the next move.

## `/spec done` — retire a pack

1. **Verify.** Read every task's `**Status:**` line (and `PROGRESS.md`). List anything not `Done` or
   deferred, and stop — the user can override, defer stragglers, or finish them first.
2. **Prove it green.** `python -m tools.checks all` must pass — the suite, all four gates, the
   coverage ratchet and the boot smoke. Paste the real output. If a money-touching task shipped,
   confirm the demo session happened and no real or demo order was touched by the tests.
3. **Harvest keepers.** Before deletion, move content that must outlive the pack to a real home:
   anything permanent from `SPEC.md` (the filled Verification checklist, design/seam notes →
   `CHANGELOG.md`, `docs/system/`), in-app help text, `docs/system/rules/` rules that changed,
   reusable queries or scripts (`tools/`). `SPEC.md` is deleted with the pack — git history is the
   archive.
3b. **Refresh stale skills.** Any `.claude/skills/` file that quotes a fact this pack changed —
   a contract count, a LOC number, "X is empty", a path — gets updated in the same change.
   (Found live 2026-08-11: frontend-conventions still claimed `components/` was empty and quoted
   a contract count three revisions old. Skills should state rules and point at gates; only gates
   own numbers.)
4. **Delete** `docs/todo/<domain>/<feature>/` (companion docs included) — never the domain dir
   itself. Confirm with the user first. Git history preserves everything.

Never touch `docs/todo/refactor/stage0/` at any point — it is an audit trail.

## Rules

- **Scaffold and stop.** Implementation starts only after the user reviews.
- **One hub.** `README.md` carries the onboarding, doc index, and decisions; keep its doc index in
  sync as files are added/removed. Only the allowed companion docs may sit beside it.
- **PROGRESS.md is the live truth.** Any agent picking up a task claims its row and updates its
  status — that's how parallel agents avoid collisions and see where the work is.
- **Later work extends, it doesn't fork.** A follow-up on an existing feature appends to the pack; no
  parallel dir for the same feature.
- **Always 010-stepped numbering.** Insert with `015-`; renumber only if the pack becomes unreadable.
- **Specs are TDD-driven.** Each task's `Tests first (TDD)` section is the contract: write those
  tests first, watch them fail, code to green. Pure-docs tasks mark it N/A.
- **Money-touching is declared, not discovered.** The README header and every affected task say so.
  A pack that quietly reshapes the close path is the exact failure this repo's rules exist to stop.
- **Answered questions are annotated, not deleted** (in `QUESTIONS.md` and the README short list).
- **Every change to the pack is pushed to the notes repo in the same session.** `docs/todo/` is
  the private repo `MooreSi/forex-gold-notes`: scaffolding, PROGRESS rows, QUESTIONS answers,
  status changes and `/spec done` deletions all go out with `git private add` /
  `commit -F` / `push`, whether or not a code commit follows. Stage only your own files.
- **User-facing copy is the user's, not yours.** Never invent the strings a UI shows and treat them
  as settled — put them in `QUESTIONS.md` for the user to confirm.

## Pairs with

- `/new-spec` — the same spec discipline for standalone changes (`docs/todo/NNN-*.md`); a pack's
  anchor spec uses its structure but lives at `docs/todo/<domain>/<feature>/SPEC.md`.
- `/safe-change` — the protocol for every money-touching task in the pack.
- `/add-tunable` — when a task introduces a number the user should be able to change.
- `/split-file` — when a task's target file is already over 800 lines.
- `/coverage-gap` — when a task lands on code with no tests at all.
- `/verify` — `python -m tools.checks all`; the gate every task ends on and `/spec done` requires.
- [docs/system/rules/40-testing.md](../../../docs/system/rules/40-testing.md) — the authoring rules for the tests each
  task names.
- [docs/system/rules/30-architecture.md](../../../docs/system/rules/30-architecture.md) — which layer a task belongs on.

## What this skill is NOT

- Not for small fixes — a single-commit change needs no plan pack; a single-file change needs
  `/new-spec`, not this.
- Not a design interrogation — structural setup questions only; open decisions go to `QUESTIONS.md`.
- Not an implementation kickoff — it never edits code.
- Not an archive system — retired packs are deleted, not moved; git history is the record.
